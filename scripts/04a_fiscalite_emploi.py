#!/usr/bin/env python3
"""Audit fiscalité / services publics de l'emploi : observations et contrôles.

python -I scripts/04a_fiscalite_emploi.py --download
python -I scripts/04a_fiscalite_emploi.py             # reproduction hors réseau
Les CSV HTTP sont archivés gzip sans perte, mtime=0, avec deux empreintes.
SCALE (ISORA) n'est jamais appliqué automatiquement à OBS_VALUE.
"""
from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import io
import json
import math
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw/04a"
CACHE = ROOT / "data/cache/04a"
OUT = ROOT / "data/international"
DATE = "2026-10-28"
COUNTRIES = "FRA DEU ITA ESP PRT BEL NLD CHE AUT GBR IRL SWE DNK NOR FIN POL EST CAN USA AUS NZL JPN KOR".split()
YEARS = (2023, 2024)
CORE = "337_010 337_011 337_012 337_013 337_014 337_015 337_017 337_018 337_022 337_098 337_166 337_167 337_176 337_177 337_178 337_179 337_180 337_214 337_225 337_250 337_251 337_252 398_003 80040_3 80080_3 91320_3 80240_3 80250_3 95100_3 83835_28 95910 111_200 111_201 111_202 337_091".split()
FUNCTIONS = {
    "95230_206": ("usagers_declarations_paiements", "337_166"),
    "94020_206": ("audit_enquetes_verifications", "337_017"),
    "94030_206": ("recouvrement_force", "337_018"),
    "96970_206": ("contentieux", "337_250"),
    "96980_206": ("rh", "337_251"),
    "98810_206": ("informatique", "337_252"),
    "95240_206": ("autres_fonctions", "337_167"),
}
ROLES = "80240_0 86280 86290 86310 86320 86330 86340 91410 91420 93770".split()
EXTRA = "91710_206 91710_208 95930_206 95940_206 95950_206 95960_207 95780_206 95780_208 95880_206 95880_208".split()
INDICATORS = list(dict.fromkeys(CORE + list(FUNCTIONS) + ROLES + EXTRA))
PES_URL = "https://www.oecd.org/content/dam/oecd/en/publications/reports/2026/06/the-world-of-public-employment-services-2026_781934e6/4aebd080-en.pdf"
TAX_URL = "https://www.oecd.org/content/dam/oecd/en/publications/reports/2025/11/tax-administration-2025_6360fad8/cc015ce8-en.pdf"
QUESTIONNAIRE_URL = "https://www.oecd.org/content/dam/oecd/en/about/programmes/oecd-data-collection-programme/taxation/tax-administration-series-international-survey-on-revenue-administration-isora/ISORA-questionnaire.pdf"


def write_csv(name, rows):
    path = OUT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"Aucune ligne pour {name}")
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def number(value):
    try:
        result = float(value)
    except (ValueError, TypeError):
        return None
    return result if math.isfinite(result) else None


def empty(value):
    return "" if value is None else round(value, 9) if isinstance(value, float) else value


def code(value):
    return (value or "").split(":", 1)[0].strip()


def archive(name, url, download, accept=None, compressed=False):
    path = RAW / name
    meta_path = path.with_suffix(path.suffix + ".meta.json")
    if not path.exists():
        if not download:
            raise FileNotFoundError(f"Instantané absent : {path}. Relancer avec --download")
        headers = {"User-Agent": "France20-independent-audit/1.0"}
        if accept:
            headers["Accept"] = accept
        response = requests.get(url, headers=headers, timeout=45)
        response.raise_for_status()
        body = response.content
        if b"<!doctype html" in body[:200].lower() or b"<html" in body[:200].lower():
            raise ValueError(f"Réponse HTML inattendue : {url}")
        if ".csv" in name and b"OBS_VALUE" not in body[:5000]:
            raise ValueError(f"Absence de colonne d'observation SDMX : {url}")
        stored = gzip.compress(body, mtime=0) if compressed else body
        RAW.mkdir(parents=True, exist_ok=True)
        path.write_bytes(stored)
        meta_path.write_text(json.dumps(dict(source_url=url, final_url=response.url, date_consultation=DATE,
                             http_status=response.status_code, content_type=response.headers.get("Content-Type", ""),
                             raw_path=str(path.relative_to(ROOT)).replace("\\", "/"), compression="gzip sans perte, mtime=0" if compressed else "aucune",
                             bytes=len(stored), original_bytes=len(body), sha256=hashlib.sha256(stored).hexdigest(),
                             sha256_http_body=hashlib.sha256(body).hexdigest(), acces="integral"), indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    stored = path.read_bytes()
    if hashlib.sha256(stored).hexdigest() != meta["sha256"]:
        raise ValueError(f"Empreinte d'archive différente : {path}")
    body = gzip.decompress(stored) if compressed else stored
    if hashlib.sha256(body).hexdigest() != meta["sha256_http_body"]:
        raise ValueError(f"Empreinte du corps HTTP différente : {path}")
    return body, meta


def load_isora(download):
    url = ("https://api.imf.org/external/sdmx/2.1/data/ISORA,ISORA_LATEST_DATA_PUB,5.0.0/"
           + "+".join(COUNTRIES)+"."+"+".join(INDICATORS)+".A?startPeriod=2022&endPeriod=2024")
    body, meta = archive("isora_selection_2022_2024.csv.gz", url, download,
                         "application/vnd.sdmx.data+csv;version=1.0.0", True)
    rows = list(csv.DictReader(io.StringIO(body.decode("utf-8-sig"))))
    keys = [(r["JURISDICTION"], r["INDICATOR"], r["TIME_PERIOD"]) for r in rows]
    if len(keys) != len(set(keys)):
        raise ValueError("Clé ISORA dupliquée")
    return rows, meta


def load_lmp(download):
    flow = "OECD.ELS.JAI,DSD_LMP@DF_LMP,1.0"
    structure_url = "https://sdmx.oecd.org/public/rest/v1/dataflow/OECD.ELS.JAI/DSD_LMP@DF_LMP/1.0?references=datastructure"
    body, smeta = archive("lmp_structure.xml", structure_url, download)
    root = ET.fromstring(body)
    dimensions = [x[1] for x in sorted((int(e.attrib["position"]), e.attrib["id"]) for e in root.iter()
                                      if e.tag.split("}")[-1] == "Dimension" and "position" in e.attrib)]
    filters = {"REF_AREA": "+".join(COUNTRIES), "MEASURE": "EXP+STO",
               "PROGRAMME": "LMP_10+LMP_11+LMP_12+LMP_13+LMP_20T70+LMP_80_90+_T",
               "UNIT_MEASURE": "PT_B1GQ+XDC+PS+PT_LF"}
    if set(filters) != set(dimensions):
        raise ValueError(f"Structure LMP modifiée : {dimensions}")
    key = ".".join(filters[d] for d in dimensions)
    url = f"https://sdmx.oecd.org/public/rest/v1/data/{flow}/{key}?startPeriod=2023&endPeriod=2024"
    body, meta = archive("lmp_selection_2023_2024.csv.gz", url, download,
                         "application/vnd.sdmx.data+csv; charset=utf-8; labels=both", True)
    rows = [{k.split(":",1)[0]:v for k,v in r.items()} for r in csv.DictReader(io.StringIO(body.decode("utf-8-sig")))]
    return rows, meta, smeta


def unique(rows, **filters):
    matches = [r for r in rows if all(code(r.get(k, "")) == str(v) for k,v in filters.items())]
    if len(matches)>1:
        raise ValueError(f"Clé insuffisante : {filters}")
    return matches[0] if matches else None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--download", action="store_true", help="Autoriser le téléchargement d'instantanés absents")
    args = parser.parse_args()
    with ThreadPoolExecutor(max_workers=3) as pool:
        tax_future = pool.submit(load_isora, args.download)
        lmp_future = pool.submit(load_lmp, args.download)
        unit_future = pool.submit(archive, "imf_unit_mult.xml", "https://api.imf.org/external/sdmx/2.1/codelist/IMF/CL_UNIT_MULT/1.0.2", args.download)
        tax, tax_meta = tax_future.result()
        lmp, lmp_meta, lmp_structure_meta = lmp_future.result()
        _, unit_meta = unit_future.result()
    codes_body, codes_meta = archive("isora_codelist_6_0_6.xml.gz", "https://api.imf.org/external/sdmx/2.1/codelist/ISORA/CL_ISORA_TAX/6.0.6", args.download, compressed=True)
    codes_root=ET.fromstring(codes_body)
    names={}
    indicator_dictionary=[]
    for element in codes_root.iter():
        if element.tag.split("}")[-1]!="Code":continue
        labels=[x.text or "" for x in element if x.tag.split("}")[-1]=="Name" and x.attrib.get("{http://www.w3.org/XML/1998/namespace}lang","en")=="en"]
        if labels:names[element.attrib["id"]]=labels[0]
        if element.attrib.get("id") in INDICATORS:
            annotations={}
            for annotation in element.iter():
                if annotation.tag.split("}")[-1]!="Annotation":continue
                parts={x.tag.split("}")[-1]:x.text or "" for x in annotation}
                annotations[parts.get("AnnotationTitle","")]=parts.get("AnnotationText","")
            indicator_dictionary.append(dict(indicateur=element.attrib["id"],libelle=labels[0] if labels else "",question=annotations.get("Question",""),
                                             table=annotations.get("Table Index",""),titre_table=annotations.get("Table Title",""),sous_titre_unite=annotations.get("Subtitle1",""),
                                             formule_originale=annotations.get("OriginalFormula",""),legende=annotations.get("Legend",""),echelle_diffusion=annotations.get("DissemScale",""),
                                             source_url=codes_meta["source_url"],source_localisation=codes_meta["raw_path"],annee="2026 nomenclature",statut="[FAIT]"))
    if any(c not in names for c in INDICATORS):
        raise ValueError("Nomenclature actuelle incomplète pour la sélection")
    write_csv("04a_dictionnaire_isora.csv",sorted(indicator_dictionary,key=lambda r:r["indicateur"]))
    index = {(r["JURISDICTION"],r["INDICATOR"],r["TIME_PERIOD"]):r for r in tax}
    def raw(country, indicator, year):
        return index.get((country, indicator, str(year)))
    def val(country, indicator, year):
        item=raw(country,indicator,year)
        return number(item["OBS_VALUE"]) if item else None
    obs=[]
    for item in tax:
        obs.append(dict(pays_iso3=item["JURISDICTION"], indicateur=item["INDICATOR"], libelle=names.get(item["INDICATOR"],""),
                        annee=item["TIME_PERIOD"], valeur_brute=item["OBS_VALUE"], valeur_numerique=empty(number(item["OBS_VALUE"])), echelle_source=item.get("SCALE",""),
                        note=item.get("FOOTNOTE",""), source_url=tax_meta["source_url"], source_localisation=tax_meta["raw_path"], statut="[FAIT]"))
    write_csv("04a_isora_observations.csv",obs)
    controls=[]
    comp=[]
    alloc=[]
    for country in COUNTRIES:
        for year in YEARS:
            fte, head, population, popfte = [val(country,c,year) for c in ("337_180","83835_28","398_003","337_010")]
            operating, salaries, revenue, reported = [val(country,c,year) for c in ("337_176","337_177","80040_3","337_012")]
            ratio = 100*operating*1000/revenue if operating is not None and revenue else None
            scale_ok = ratio is not None and reported is not None and math.isclose(ratio,reported,rel_tol=1e-6,abs_tol=1e-7)
            controls.append(dict(pays_iso3=country,annee=year,controle="cout_collecte_echelle",valeur_publiee=empty(reported),valeur_recalculee=empty(ratio),
                                 conforme=scale_ok,statut="[ESTIMATION]",formule="100 × 337_176 × 1000 / 80040_3 ; aucune multiplication générale par 10^SCALE",
                                 note="Valide le facteur d'unités de cette identité, pas un contrat général de l'API",source_url=tax_meta["source_url"],source_localisation=tax_meta["raw_path"]))
            population_identity = population/fte if population is not None and fte else None
            controls.append(dict(pays_iso3=country,annee=year,controle="population_par_etp",valeur_publiee=empty(popfte),valeur_recalculee=empty(population_identity),
                                 conforme=population_identity is not None and popfte is not None and math.isclose(population_identity,popfte,rel_tol=1e-6,abs_tol=1e-6),
                                 statut="[ESTIMATION]",formule="398_003 / 337_180",note="Champ administration fiscale déclarée ; pas l'emploi public total",source_url=tax_meta["source_url"],source_localisation=tax_meta["raw_path"]))
            role_values={c:(raw(country,c,2022) or {}).get("OBS_VALUE","") for c in ROLES}
            other_roles=" ; ".join(names.get(c,c)+"="+v for c,v in role_values.items() if v)
            functions=[val(country,c,year) for c in FUNCTIONS]
            if fte and all(v is not None for v in functions):
                controls.append(dict(pays_iso3=country,annee=year,controle="somme_sept_fonctions",valeur_publiee=fte,valeur_recalculee=sum(functions),
                                     conforme=math.isclose(fte,sum(functions),rel_tol=1e-6,abs_tol=1.1),statut="[ESTIMATION]",formule="somme des sept fonctions C.Q3 ; siège non ajouté",
                                     note="Parts siège et fonctions se recouvrent : ne jamais les additionner",source_url=tax_meta["source_url"],source_localisation=tax_meta["raw_path"]))
            for indicator,(function,pct_code) in FUNCTIONS.items():
                count,pct=val(country,indicator,year),val(country,pct_code,year)
                alloc.append(dict(pays_iso3=country,annee=year,fonction=function,etp=empty(count),part_pct_publiee=empty(pct),part_pct_recalculee=empty(100*count/fte if count is not None and fte else None),
                                  statut_part_recalculee="[ESTIMATION]" if count is not None and fte else "[NON TROUVÉ]",
                                  source_url=tax_meta["source_url"],source_localisation=tax_meta["raw_path"]+" ; "+indicator+" ; "+pct_code,statut="[FAIT]" if count is not None else "[NON TROUVÉ]"))
            op_base=operating*1000 if scale_ok else None
            comp.append(dict(pays_iso3=country,annee=year,etp_fiscaux=empty(fte),agents_fin_exercice=empty(head),population=empty(population),
                             etp_fiscaux_pour_1000_habitants=empty(1000/popfte if popfte else None),cout_collecte_pct=empty(reported),
                             statut_etp_fiscaux_pour_1000="[ESTIMATION]" if popfte else "[NON TROUVÉ]",
                             depenses_fonct_k_monnaie_locale=empty(operating),salaires_k_monnaie_locale=empty(salaries),recettes_export_monnaie_locale=empty(revenue),
                             echelle_monnaie_validee_par_ratio=scale_ok,cout_fonct_par_etp_monnaie_locale=empty(op_base/fte if op_base is not None and fte else None),
                             statut_cout_par_etp="[ESTIMATION]" if op_base is not None and fte else "[NON TROUVÉ]",
                             part_salaires_pct=empty(val(country,"337_013",year)),part_siege_pct=empty(val(country,"337_022",year)),
                             administration_jointe_douanes=(raw(country,"95910",year) or {}).get("OBS_VALUE",""),
                             missions_hors_fiscalite_annee=2022,missions_hors_fiscalite=other_roles,
                             peri_etp="Form C : ressources fiscales annuelles déclarées ou estimées ; agents Form D en stock, non interchangeables",
                             source_url=tax_meta["source_url"],source_localisation=tax_meta["raw_path"],statut="[FAIT]",note="Ratios calculés identifiés par les intitulés et contrôles ; coût par ETP moyen inclut pensions dans les salaires, pas coût d'entrée évitable"))
    write_csv("04a_isora_comparaison.csv",comp)
    write_csv("04a_isora_fonctions.csv",alloc)
    write_csv("04a_controles_isora.csv",controls)
    lmp_obs=[]
    for item in lmp:
        value=number(item["OBS_VALUE"])
        multiplier=number(code(item.get("UNIT_MULT")))
        lmp_obs.append(dict(pays_iso3=code(item["REF_AREA"]),annee=item["TIME_PERIOD"],mesure=code(item["MEASURE"]),programme=code(item["PROGRAMME"]),
                            unite=code(item["UNIT_MEASURE"]),valeur_brute=item["OBS_VALUE"],multiplicateur=code(item.get("UNIT_MULT")),
                            valeur_unites=empty(value*10**int(multiplier) if value is not None and multiplier is not None else None),flag=code(item.get("OBS_STATUS")),
                            source_url=lmp_meta["source_url"],source_localisation=lmp_meta["raw_path"],statut="[FAIT]"))
    write_csv("04a_lmp_observations.csv",lmp_obs)
    lmp_comp=[]
    for country in COUNTRIES:
        for year in YEARS:
            def lval(program,unit):
                item=unique(lmp,REF_AREA=country,TIME_PERIOD=year,MEASURE="EXP",PROGRAMME=program,UNIT_MEASURE=unit)
                return number(item["OBS_VALUE"]) if item else None
            values={p:lval(p,"PT_B1GQ") for p in ["LMP_10","LMP_11","LMP_12","LMP_13","LMP_20T70","LMP_80_90","_T"]}
            total,other=values["LMP_10"],values["LMP_13"]
            total_xdc,other_xdc=lval("LMP_10","XDC"),lval("LMP_13","XDC")
            parts=[values[p] for p in ["LMP_11","LMP_12","LMP_13"]]
            lmp_comp.append(dict(pays_iso3=country,annee=year,spe_total_pct_pib=empty(total),placement_pct_pib=empty(parts[0]),
                                 administration_prestations_pct_pib=empty(parts[1]),autres_non_ventiles_pct_pib=empty(other),
                                 part_autres_non_ventiles_pct=empty(other_xdc/total_xdc*100 if other_xdc is not None and total_xdc else None),
                                 statut_part_autres="[ESTIMATION]" if other_xdc is not None and total_xdc else "[NON TROUVÉ]",
                                 formule_part_autres="100 × LMP13/XDC / LMP10/XDC ; évite de diviser des %PIB déjà arrondis",
                                 ventilation_3_composantes_complete=all(x is not None for x in parts),
                                 ecart_somme_composantes_pct_pib=empty(sum(parts)-total if total is not None and all(x is not None for x in parts) else None),
                                 mesures_actives_2_7_pct_pib=empty(values["LMP_20T70"]),aides_passives_8_9_pct_pib=empty(values["LMP_80_90"]),toutes_politiques_pct_pib=empty(values["_T"]),
                                 spe_total_monnaie_locale_millions=empty(total_xdc),
                                 source_url=lmp_meta["source_url"],source_localisation=lmp_meta["raw_path"],statut="[FAIT]",
                                 note="Catégorie1 = services et administration, inclut prestations externes publiques financées ; catégories2-9 ne sont pas des frais de gestion ; parts calculées ESTIMATION"))
    write_csv("04a_lmp_comparaison.csv",lmp_comp)
    levels=[]
    for theme,table,metric,unit in [("fiscalite",comp,"etp_fiscaux_pour_1000_habitants","ETP fiscaux pour 1000 habitants"),("fiscalite",comp,"cout_collecte_pct","% recettes nettes collectées"),("emploi",lmp_comp,"spe_total_pct_pib","% PIB")]:
        for year in YEARS:
            french=next(r for r in table if r["pays_iso3"]=="FRA" and r["annee"]==year)
            for item in table:
                if item["annee"]!=year or item["pays_iso3"]=="FRA":continue
                fv,pv=number(french[metric]),number(item[metric])
                levels.append(dict(domaine=theme,pays_reference="FRA",pays_compare=item["pays_iso3"],annee=year,indicateur=metric,unite=unit,
                                   france=empty(fv),pays=empty(pv),niveau1_ecart_brut_france_moins_pays=empty(fv-pv if fv is not None and pv is not None else None),
                                   niveau2_ecart_apres_perimetre="",niveau2_statut="[NON TROUVÉ]",
                                   niveau2_documentation=item.get("administration_jointe_douanes","")+" ; missions déclarées en2022 : "+item.get("missions_hors_fiscalite","") if theme=="fiscalite" else "LMP10 inclut placement, gestion des prestations et autres coûts ; comparaison de sous-catégories impossible si ventilation absente",
                                   niveau3_ecart_apres_besoins="",niveau3_statut="[NON TROUVÉ]",
                                   niveau3_documentation="Assiettes, types d'impôts, conformité et prestations de contrôle non normalisés" if theme=="fiscalite" else "Portefeuilles, éloignement de l'emploi, prestations, intensité d'accompagnement et résultats non normalisés",
                                   niveau4_etp_supprimables="",niveau4_economies="",niveau4_statut="[NON TROUVÉ]",
                                   niveau4_documentation="Écart brut non convertible en sureffectif ; gains conditionnels à mesurer par réforme",
                                   source_url=item["source_url"],source_localisation=item["source_localisation"],statut="[ESTIMATION]" if fv is not None and pv is not None else "[NON TROUVÉ]"))
    write_csv("04a_quatre_niveaux.csv",levels)
    candidates=[
        ("04A_FISC_1","Automatiser les contrôles de forme et réduire les ressaisies fiscales","10356 ETP déclarés en2023 dans enregistrement, services, déclarations et paiements ; aucun taux de suppression retenu", "Chronométrer des flux homogènes, simplifier les pièces et données déjà connues, tester automatisation puis vérification humaine ; déployer seulement après validation",
         "Temps complet par dossier, taux de reprise, réclamations, accessibilité, erreurs et recettes ; expérimentation avec groupe témoin ou déploiement randomisé", "CoûtSI, reprise des données, licences, cybersécurité, formation et maintenance à chiffrer avant décision", "Aucune baisse d'effectifs avant charge nette vérifiée et stabilisation du service",TAX_URL+" ; "+QUESTIONNAIRE_URL,"Questionnaire Form C Q3 ; Tax Administration2025 chapitre9, p.141-143"),
        ("04A_FISC_2","Mutualiser les fonctions support sur des périmètres démontrés","1881 ETP RH et2536 ETP informatique en2023 dans le champ fiscal déclaré ; pas un vivier entièrement supprimable", "Cartographier fonctions communes, harmoniser les données agents et procédures, regrouper les opérations répétitives en conservant sécurité et expertise de proximité",
         "Coût par dossier RH, disponibilitéSI, délai d'assistance, incidents et temps métier ; comparer unités pilotes à unités non traitées", "MigrationSIRH, interopérabilité, formation, conduite du changement ; économies et coût de transition inconnus", "RH, informatique et siège se recouvrent : registre unique d'ETP ; ne pas additionner une suppression d'agence et la mutualisation du même poste",QUESTIONNAIRE_URL,"Form C Q2 etQ3"),
        ("04A_FISC_3","Réaffecter du temps simplifié au contrôle selon rendement net","10153 ETP audit,6302 recouvrement forcé,4933 contentieux en2023 ; leurs charges ne sont pas des coûts inutiles", "Tester l'assistance documentaire et la priorisation des dossiers, puis réallouer la capacité gagnée vers les segments où recettes et conformité justifient le coût",
         "Recettes effectivement encaissées nettes des annulations, effets de dissuasion évalués, délais et droits du contribuable ; échantillons aléatoires pour éviter sélection des seuls dossiers faciles", "Qualité des données, formation et supervision ; aucun rendement marginal national déduit du ratio coût/recettes", "Une baisse du coût fiscal doit retrancher toute perte de recettes et dégradation des contrôles ; pas de conversion automatique temps/postes",TAX_URL,"Chapitre9, encadré9.2, p.128-129 ; ISORA tablesA.18-A.21"),
        ("04A_PES_1","Ventiler et piloter les coûts de service de l'emploi","5187 M€ de coûts autres/non ventilés LMP13 en2023 ; ce total n'est pas une économie", "Créer une comptabilité par service rendu et bénéficiaire pour placement, indemnisation et support ; identifier ressources internes, prestations externes et coûts communs",
         "Rapprochement annuel dépenses/ETP/prestations sans résidu inexpliqué ; coût complet par parcours et non par seule inscription", "Comptabilité analytique et gouvernance des données à chiffrer ; pas de création d'un système déclaratif redondant", "Ne pas assimilerLMP13 à tâches inutiles ; administration des prestations absente comme sous-catégorie distincte enFrance",lmp_meta["source_url"],"LMP10,11,12,13 / France2023 ; métadonnéesDGEMPL §3 et6.2"),
        ("04A_PES_2","Expérimenter des contrats de placement fondés sur l'emploi durable","1712 M€ classés placement/services connexes LMP11 en2023 ; financement externe inclus dans une lecture complète", "Comparer des contrats comprenant paiement initial, étapes contrôlées et bonus d'emploi durable selon la difficulté des publics ; évaluer face à une offre publique comparable",
         "Emploi et revenus à6/12mois, maintien durable, coût total public+prestataire, qualité et non-sélection des publics difficiles ; affectation aléatoire quand possible", "Achat, contrôle des contrats, systèmes de suivi, audits et risques de défaillance à inclure", "Externaliser un poste ne le supprime pas économiquement ; résultats historiques ne garantissent pas ceux de contrats nouveaux", "https://doi.org/10.1257/app.6.4.142 ; https://doi.org/10.1787/c6392a59-en", "Behaghel etal.2014, p.142 et résultats ; OCDE2022 sections3-5"),
        ("04A_PES_3","Réduire les démarches redondantes du réseau sans alléger l'accompagnement utile","Profils internationaux non harmonisés ; pas de cible nationaleETP prouvée", "Cartographier l'entrée en parcours, réutiliser les données autorisées entre partenaires, supprimer les demandes répétées et transférer le temps gagné au conseil ciblé",
         "Temps administratif net par parcours, nombre de justificatifs redemandés, délai de premier accompagnement, emploi durable et satisfaction ; comparaison de territoires de composition semblable", "Interopérabilité, habilitations, protection des données et accueil hors ligne à prévoir", "Les gains support, les transformations informatiques et les gainsIA sur les mêmes agents ne se cumulent pas ; les heures de conseil récupérées ne sont pas des postes supprimés",PES_URL,"Chapitres2-3 et profils France/Allemagne/Pays-Bas ; sources et définitions annexeC"),
    ]
    write_csv("04a_reformes_candidates.csv",[dict(id=c[0],intitule=c[1],vivier_et_preuve=c[2],operation=c[3],validation_a_2_3_ans=c[4],investissements_et_couts=c[5],risques_et_non_double_compte=c[6],
              etp_supprimables="",economies_nettes_annuelles="",confiance_sur_existence_du_probleme="moyenne à élevée selon les sources",confiance_sur_gain_chiffre="faible, non quantifié",
              source_url=c[7],source_localisation=c[8],annee="2023-2026",statut="[HYPOTHÈSE]") for c in candidates])
    registry=[]
    for sid,title,institution,meta in [("04A_ISORA","ISORA latest v5 sélection 2022-2024","FMI / ISORA",tax_meta),("04A_LMP","Labour Market Programmes sélection 2023-2024","OCDE",lmp_meta),("04A_LMP_DSD","Structure SDMX LMP","OCDE",lmp_structure_meta),("04A_UNIT_MULT","Nomenclature UNIT_MULT, codes0 et3","FMI",unit_meta),("04A_ISORA_CODES","Nomenclature ISORA CL_ISORA_TAX v6.0.6","ISORA",codes_meta)]:
        registry.append(dict(id=sid,titre=title,institution=institution,date_publication="",url=meta["source_url"],date_consultation=meta["date_consultation"],acces="integral",sha256_16=meta["sha256"][:16],notes=meta["raw_path"]+" ; "+meta.get("compression","")))
    for folder in (RAW,CACHE):
        for path in sorted(folder.glob("*.meta.json")):
            meta=json.loads(path.read_text(encoding="utf-8"))
            if path.name.endswith(".gz.meta.json") or path.stem in ("lmp_structure.xml.meta","imf_unit_mult.xml.meta"):continue
            if not meta.get("source_url"):continue
            if any(r["url"]==meta["source_url"] for r in registry):continue
            institutions={"uwv":"UWV", "ba":"Bundesagentur für Arbeit", "france_travail":"France Travail", "world_public":"BID / OCDE / WAPES", "tax_administration":"OCDE", "isora_questionnaire":"ISORA / OCDE", "lmp_metadonnees":"Commission européenne, DG EMPL", "pes_experience":"Behaghel / Crépon / Gurgand, AEJ Applied Economics", "pes_contractualisation":"OCDE"}
            institution=next((v for k,v in institutions.items() if path.name.startswith(k)),"Institution indiquée dans le document primaire")
            registry.append(dict(id="04A_DOC_"+path.name.removesuffix(".meta.json"),titre=path.name.removesuffix(".meta.json"),institution="Voir document primaire",
                                 date_publication="",url=meta["source_url"],date_consultation=meta["date_consultation"],acces="partiel",sha256_16=meta["sha256"][:16],
                                 notes=meta["raw_path"]+" ; sections et pages effectivement lues dans recherche/04a_fiscalite_emploi.md ; téléchargement intégral ne signifie pas lecture intégrale"))
            registry[-1]["institution"]=institution
            if folder==CACHE:
                (RAW/path.name).write_text(json.dumps(meta,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    registry.sort(key=lambda r:r["id"])
    sources_path=ROOT/"sources/registre_04a.csv"
    sources_path.parent.mkdir(exist_ok=True)
    with sources_path.open("w",newline="",encoding="utf-8") as stream:
        writer=csv.DictWriter(stream,fieldnames=list(registry[0]));writer.writeheader();writer.writerows(registry)
    missing_checks=[r for r in controls if not r["conforme"] and r["valeur_publiee"]!="" and r["valeur_recalculee"]!=""]
    print(json.dumps(dict(observations_isora=len(obs),observations_lmp=len(lmp_obs),comparaisons_fiscales=len(comp),comparaisons_emploi=len(lmp_comp),
                         comparaisons_quatre_niveaux=len(levels),controles_non_conformes=missing_checks,sources=len(registry)),ensure_ascii=True,indent=2))


if __name__=="__main__":
    main()
