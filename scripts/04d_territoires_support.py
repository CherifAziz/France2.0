#!/usr/bin/env python3
"""Chantier 04d : structures territoriales et périmètres des fonctions support.

Extraction XLSX/SDMX et transcription explicitement manuelle des tableaux PDF.
Les assertions contrôlent les sommes et les ancres, pas la validité causale des
estimations citées. Aucun de ces montants ne calibre le modèle financier.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
import sys
from decimal import Decimal
from pathlib import Path

from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw/04d"
CACHE = ROOT / "data/cache/04d"
OUT = ROOT / "data/international"
DATE = "2026-10-28"
MANIFEST = RAW / "documents_support.json"


def write_csv(path, rows):
    if not rows:
        raise ValueError(f"Sortie vide : {path}")
    for row in rows:
        for original, conventional in [("source", "source_url"), ("localisation", "source_localisation"), ("statut_preuve", "statut")]:
            if original in row:
                row[conventional] = row.pop(original)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def restore():
    """Restaure les instantanés ; refuse les réponses modifiées ou inaccessibles."""
    import requests
    for item in json.loads(MANIFEST.read_text(encoding="utf-8")):
        if item.get("acces") != "integral":
            continue
        target = ROOT / item["raw_path"]
        if target.exists():
            if digest(target) != item["sha256"]:
                raise ValueError(f"Archive locale modifiée : {target}")
            continue
        if item.get("accept"):
            response = requests.get(item["source_url"], headers={"Accept": item["accept"]}, timeout=90)
            response.raise_for_status()
            if hashlib.sha256(response.content).hexdigest() != item["sha256"]:
                raise ValueError(f"Distribution modifiée : {target}; ne pas écraser le millésime")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(response.content)
        else:
            subprocess.run([sys.executable, str(ROOT / "scripts/fetch.py"), item["source_url"],
                            target.stem, "--out-dir", str(target.parent), "--timeout", "90"], check=True)
            if digest(target) != item["sha256"]:
                raise ValueError(f"Distribution modifiée : {target}")


def make_manifest():
    """Registre léger conservé avec les données ; le cache lourd reste ignoré."""
    consulted = {
        "ravignon_rapport2024": "PDF 8-9, 42-46, 96-100, 111; tableaux 9, 10, 25, 26 et 28",
        "senat_agences_rapport2025": "PDF 21-22, 217, 230-231; autres extraits ciblés sur définitions et montants",
        "dae_rapport2025": "PDF 46-47, 80, 86-87; tableaux achats et économies achats",
        "dae_reference2025": "PDF 3-5; définition et distinction économie achat / économie budgétaire",
        "dgcl_ch2_2026": "2.2 nb CL!B4:F29; 2.5a EPCI!B4:G19",
        "dgcl_ch1_2026": "Classeur téléchargé; non exploité dans les chiffres de cette note",
        "oecd_sng_struct_2020_2026": "90 observations; dimensions, unité, multiplicateur, année",
        "loi_fonciere2026": "Accès direct 403; contenu législatif non lu, état daté vérifié sur Sénat",
    }
    manifests = sorted(CACHE.glob("*.meta.json")) + sorted(RAW.glob("*.meta.json"))
    rows = []
    for path in manifests:
        item = json.loads(path.read_text(encoding="utf-8"))
        name = path.name.removesuffix(".meta.json")
        item["identifiant"] = "04D_" + name
        item["lecture"] = consulted.get(name, "Lecture ciblée de la page ou des métadonnées; pas de lecture exhaustive annoncée")
        item["raw_path"] = item.get("raw_path", "").replace("\\", "/")
        if name == "oecd_sng_struct_2020_2026":
            item["acces"] = "integral"
            item["raw_path"] = "data/raw/04d/oecd_sng_struct_2020_2026.csv"
        rows.append(item)
    MANIFEST.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    publications = {"ravignon_rapport2024": "2024-05-29", "ravignon_page": "2024-05-29", "ravignon_rapport_page": "2024-05-29",
                    "senat_agences_rapport2025": "2025-07-01", "senat_agences_notice": "2025-07-01",
                    "dae_rapport2025": "2026-06-18", "dae_reference2025": "2025; date éditoriale exacte NON TROUVÉ",
                    "dgcl_ch2_2026": "2026; page mise à jour septembre; date exacte du XLSX NON TROUVÉ",
                    "dgcl_ch1_2026": "2026; date éditoriale exacte NON TROUVÉ"}
    institutions = {"ravignon": "Mission Ravignon / ministère de l'Économie", "senat": "Sénat", "dae": "Direction des achats de l'État",
                    "die": "Direction de l'immobilier de l'État", "dgcl": "DGCL / Insee", "sng": "OCDE", "oecd": "OCDE", "loi": "Légifrance"}
    write_csv(ROOT / "sources/registre_04d.csv", [{
        "id": r["identifiant"], "titre": r["identifiant"].removeprefix("04D_").replace("_", " "),
        "institution": institutions.get(r["identifiant"].removeprefix("04D_").split("_")[0], "NON TROUVÉ"),
        "date_publication": publications.get(r["identifiant"].removeprefix("04D_"), "NON TROUVÉ; millésime et consultation distincts"),
        "url": r["source_url"], "date_consultation": r["date_consultation"],
        "acces": r.get("acces", "inaccessible"), "http": r.get("http_status", ""),
        "archive": r["raw_path"], "sha256": r.get("sha256", ""),
        "sha256_16": r.get("sha256", "")[:16], "pages_total": r.get("pages", ""), "notes": r["lecture"],
        "date_derniere_modification_http": r.get("last_modified", "") or "NON TROUVÉ",
    } for r in rows])


def meta(name):
    return next(r for r in json.loads(MANIFEST.read_text(encoding="utf-8")) if r["identifiant"] == "04D_" + name)


def territorial_data():
    path = RAW / "oecd_sng_struct_2020_2026.csv"
    if digest(path) != meta(path.stem)["sha256"]:
        raise ValueError("Empreinte WOFI différente")
    rows = list(csv.DictReader(path.open(encoding="utf-8-sig", newline="")))
    result, keys = [], set()
    for row in rows:
        code = lambda name: row[name].split(":", 1)[0]
        key = tuple(row[k] for k in list(row)[1:11])
        assert key not in keys, "Clé SDMX dupliquée"
        keys.add(key)
        exponent = int(code("UNIT_MULT: Unit multiplier"))
        value = Decimal(row["OBS_VALUE"]) * Decimal(10) ** exponent
        result.append({
            "pays": code("REF_AREA: Reference area"), "indicateur": code("MEASURE: Measure"),
            "annee": row["TIME_PERIOD: Time period"], "valeur": str(value),
            "unite": "habitants par municipalité" if code("MEASURE: Measure") == "MUN_SIZE" else "unités institutionnelles",
            "unite_sdmx": row["UNIT_MEASURE: Unit of measure"], "multiplicateur_sdmx": exponent,
            "precision_decimales": row["DECIMALS: Decimals"],
            "statut_source": row["OBS_STATUS: Observation status"], "statut_preuve": "FAIT",
            "source": meta(path.stem)["source_url"], "localisation": f"{code('REF_AREA: Reference area')}.{code('MEASURE: Measure')};{row['TIME_PERIOD: Time period']}",
            "sha256_source": digest(path), "date_consultation": DATE,
        })
    assert len(rows) == 90 and {r["annee"] for r in result} == {"2020"}
    write_csv(OUT / "04d_structures_territoriales_2020.csv", result)

    path = RAW / "dgcl_ch2_2026.xlsx"
    assert digest(path) == meta(path.stem)["sha256"]
    book = load_workbook(path, data_only=True, read_only=True)
    selected = [("2.2 nb CL", n, cell) for n, cell in [
        ("collectivites_locales_total", "F6"), ("collectivites_territoriales", "F7"),
        ("communes", "F8"), ("conseils_departementaux", "F12"), ("conseils_regionaux", "F16"),
        ("statut_particulier", "F20"), ("groupements", "F26"), ("epci_fiscalite_propre", "F27"), ("syndicats", "F28")]]
    selected += [("2.5a EPCI", n, cell) for n, cell in [
        ("metropoles_hors_Lyon", "F5"), ("communautes_urbaines", "F6"), ("communautes_agglomeration", "F7"),
        ("communautes_communes", "F8"), ("metropole_Lyon", "F10"),
        ("communes_regroupees_y_compris_Lyon", "F11"), ("communes_isolees", "F12")]]
    output = [{"indicateur": n, "valeur": book[s][cell].value, "unite": "unités institutionnelles",
               "date_reference": "2026-01-01", "annee": 2026, "champ": "France métropolitaine et DOM; définition propre à la DGCL",
               "source": meta(path.stem)["source_url"], "localisation": s + "!" + cell,
               "sha256_source": digest(path), "date_consultation": DATE, "statut_preuve": "FAIT"} for s,n,cell in selected]
    d = {r["indicateur"]: r["valeur"] for r in output}
    assert d["collectivites_locales_total"] == d["collectivites_territoriales"] + d["groupements"]
    assert d["collectivites_territoriales"] == d["communes"] + d["conseils_departementaux"] + d["conseils_regionaux"] + d["statut_particulier"]
    assert d["groupements"] == d["epci_fiscalite_propre"] + d["syndicats"]
    assert d["epci_fiscalite_propre"] == sum(d[x] for x in ["metropoles_hors_Lyon", "communautes_urbaines", "communautes_agglomeration", "communautes_communes"])
    assert d["communes"] == d["communes_regroupees_y_compris_Lyon"] + d["communes_isolees"]
    write_csv(OUT / "04d_dgcl_organisation2026.csv", output)
    book.close()


def pdf_transcriptions():
    rows = []

    def add(name, page, indicator, value, unit, year, status, scope, use, anchor):
        source = meta(name)
        raw = ROOT / source["raw_path"]
        if not raw.exists():
            raise FileNotFoundError(f"Cache absent : {raw}; relancer avec --download")
        assert digest(raw) == source["sha256"], str(raw)
        text = raw.with_suffix(".txt").read_text(encoding="utf-8")
        body = re.search(r"\[PAGE " + str(page) + r"\](.*?)(?=\[PAGE |\Z)", text, re.S).group(1)
        compact = lambda s: re.sub(r"\s+", "", s)
        assert compact(anchor) in compact(body), (name, page, anchor)
        rows.append({"indicateur": indicator, "valeur": value, "unite": unit, "annee": year,
                     "statut_preuve": status, "champ": scope, "usage_autorise": use,
                     "source": source["source_url"], "localisation": f"PDF p.{page}",
                     "methode_extraction": "transcription manuelle; ancre et empreinte vérifiées",
                     "sha256_source": source["sha256"], "date_consultation": DATE})

    rav = "ravignon_rapport2024"
    add(rav,43,"enquete_collectivites_exploitees",178,"réponses exploitables",2024,"FAIT","155 communes, 11 groupements, 9 départements, 3 régions","Apprécier la méthode; pas un échantillon aléatoire démontré","178")
    add(rav,43,"enquete_services_Etat_exploites",54,"réponses exploitables",2024,"FAIT","Préfectures et directions déconcentrées; hors certains réseaux et opérateurs","Apprécier le champ de l'extrapolation","54")
    add(rav,46,"enchevetrement_total_table10",7443997405,"EUR/an valorisés",2024,"ESTIMATION","Temps déclaré extrapolé et autres estimations; somme incluant de la coordination nécessaire","Ne pas convertir en économies budgétaires ni en postes supprimables","7 443 997 405")
    add(rav,45,"enchevetrement_patrimoine_RH_finances",1856810109,"EUR/an valorisés",2024,"ESTIMATION","Tableau10; comprend relations DGFiP, CDG/CNFPT et financements patrimoine","Sous-ensemble du total; pas additionnel","1 856 810 109")
    add(rav,45,"enchevetrement_relations_DGFiP",1356245301,"EUR/an valorisés",2024,"ESTIMATION","Relations financières État/collectivités; 1,28Md€ de coût État dans la ligne","Chevauchement avec fiscalité/comptabilité publique; pas une économie intégrale","1 356 245 301")
    add(rav,96,"RH_collectivites_agents",31040,"agents; ETP non établi",2021,"ESTIMATION","Métiers RH identifiés par CNFPT, hors 13600 agents CNFPT/CDG ajoutés dans le texte","Pas un vivier complet ni intégralement administratif supprimable","31 040")
    add(rav,96,"RH_avec_CNFPT_CDG_agents",44640,"agents; ETP non établi",2021,"ESTIMATION","31040 + 13600 agents CNFPT/CDG selon mission; formation et prévention incluses","Ne pas ajouter aux emplois FPT déjà comptés","44 640")
    for name,value,anchor in [("RH_cout_catA",376.7,"376,7"),("RH_cout_catB",463.5,"463,5"),("RH_cout_catC",592.5,"592,5")]:
        add(rav,98,name,value,"M EUR/an estimés",2021,"ESTIMATION","Tableau25; métiers RH dans les collectivités; titre tronqué dans le PDF","Composante de masse salariale, pas une économie",anchor)
    add(rav,97,"RH_cout_ensemble",2047.3,"M EUR/an estimés",2021,"ESTIMATION","Base chiffrée dans le texte; raccordement au tableau25 non reconstitué, inclusion exacte CNFPT/CDG non explicitée","Différent de la somme du tableau25; ne pas les additionner","2 047,3")
    add(rav,100,"RH_gain_simplification_5pct",102.4,"M EUR/an hypothétiques",2024,"HYPOTHÈSE","5% d'efficience appliqués à la base RH de la mission; absence de comptabilité analytique reconnue","Scénario externe non calibré; pas une économie observée","102,4")
    add(rav,100,"RH_gain_simplification_10pct",204.7,"M EUR/an hypothétiques",2024,"HYPOTHÈSE","10% d'efficience; même base que l'hypothèse5%","Alternative au scénario5%; ne pas additionner","204,7")
    sen = "senat_agences_rapport2025"
    add(sen,231,"operateurs_support_base",2700,"M EUR/an estimés",2024,"HYPOTHÈSE","10% des charges personnel et fonctionnement; hors interventions, universités et centres de recherche","Estimation de périmètre support; pas mesure analytique","2,7")
    add(sen,231,"operateurs_support_reduction20pct",540,"M EUR/an hypothétiques",2025,"HYPOTHÈSE","20% de réduction de la base support de2,7Md€; qualifié très volontariste","Potentiel conditionnel non net des coûts de transition; aucune conversion automatique en ETP","540")
    add(sen,217,"immobilier_surface_cible",25,"pourcentage de réduction ciblée",2032,"HYPOTHÈSE","Bureaux et locaux d'activités éligibles; 20Mm² sur96Mm² de patrimoine total","Objectif gouvernemental, pas réalisation constatée","25 %")
    add(sen,217,"immobilier_economie_annoncee",1000,"M EUR/an hypothétiques",2032,"HYPOTHÈSE","Loyers et entretien selon projet décrit en2025; pas tout le patrimoine, transition non déduite","Vérifier trajectoire actualisée, externalité des loyers et investissements; ne pas ajouter aux coûts achats","milliard")
    dae = "dae_rapport2025"
    departments = [("interministeriel",177.18,"177,18"),("agriculture",2.23,"2,23"),("armees",72.01,"72,01"),
                   ("culture",0.75,"0,75"),("economie",13.76,"13,76"),("education",5.52,"5,52"),
                   ("affaires_etrangeres",1.86,"1,86"),("interieur",72.92,"72,92"),("justice",25.71,"25,71"),
                   ("premier_ministre",3.66,"3,66"),("social",2.39,"2,39"),("ecologie",34.54,"34,54")]
    for name,value,anchor in departments + [("total",412.53,"412,53")]:
        add(dae,87,"achats_gains_" + name,value,"M EUR d'économies achats; TVA non explicitée au tableau",2025,"ESTIMATION",
            "État; gains de prix par la méthode DAE, volumes de référence hypothétiques",
            "Indicateur prix calculé; ni trésorerie budgétaire observée ni baisse d'effectifs",anchor)
    assert abs(sum(Decimal(str(v)) for _,v,_ in departments) - Decimal("412.53")) <= Decimal("0.01"), "Arrondis du tableau DAE"
    for name,value,anchor in [("Etat_hors_defense_securite",24364,"24 364"),("defense_securite",25881,"25 881"),("Etat_total",50245,"50 245")]:
        add(dae,46,"achats_depenses_" + name,value,"M EUR TTC",2025,"FAIT",
            "Cartographie ministérielle Chorus; champ distinct des EP et des gains achats HT",
            "Dépense d'achats exécutée; concept et période distincts des gains achats calculés à la notification",anchor)
    write_csv(OUT / "04d_support_indicateurs.csv", rows)
    return len(rows)


def four_levels():
    domains = [
        ("Organisation territoriale", "oecd_sng_struct_2020_2026", "FRA/DNK;2020;MUN_SIZE", 2020,
         ["France1927,95 habitants/municipalité, Danemark59504,12; différence institutionnelle brute",
          "SUB WOFI et total DGCL distincts; EPCI et syndicats non tous inclus dans WOFI; coopération déjà généralisée",
          "Dispersion, compétences, démographie, délégation et résultats de service non ajustés",
          "ETP et économie nette non identifiés; mesurer les processus réellement mutualisables"]),
        ("Coordination territoriale", "ravignon_rapport2024", "PDF43-46,tableau10", 2024,
         ["7,444Md€ de temps valorisé et autres estimations; pas un écart international",
          "Coordination nécessaire incluse; sous-échantillons et champs incomplets; relations DGFiP imbriquées",
          "Part incompressible et qualité de la coordination non mesurées",
          "Part évitable et conversion en dépenses marginales non identifiées; ne pas additionner aux mesures RH/DGFiP"]),
        ("RH et paie territoriales", "ravignon_rapport2024", "PDF96-100,tableaux25-26", 2021,
         ["31040 agents métiers RH, 44640 après ajout CNFPT/CDG; ETP non établi",
          "Formation et prévention comprises; externalisations et collectivités à consolider; coût du texte distinct du tableau25 sans raccordement complet",
          "Statuts, actes, effectifs gérés, erreurs et délais non ajustés",
          "Hypothèses externes5%-10% soit102,4-204,7M€; potentiel net et départs non identifiés"]),
        ("Support des opérateurs", "senat_agences_rapport2025", "PDF230-231", 2024,
         ["Base support2,7Md€ reconstituée par ratio10%; pas comptabilité analytique exhaustive",
          "Hors interventions, universités et recherche; périmètres agences/opérateurs superposés",
          "Volumes, missions, contraintes juridiques et externalisations non ajustés",
          "Hypothèse externe20% soit540M€ bruts; transition et gain additionnel non calibrés"]),
        ("Achats", "dae_rapport2025", "PDF46-47,80,86-87", 2025,
         ["412,53M€ de gains achats État calculés à la notification;24,364Md€ de dépenses hors D&S",
          "Prix de référence et volumes estimés distincts des dépenses budgétaires; État/EP et années2024/25 à séparer",
          "Quantités réelles, qualité, indexation et changements de méthode non neutralisés",
          "Gain budgétaire additionnel et coût des équipes achats non identifiés; recouvrements SI/immobilier"]),
        ("Immobilier et SI", "senat_agences_rapport2025", "PDF217; état juridique actualisé par Sénat2026", 2025,
         ["Projet immobilier25% de surfaces en moins et1Md€ annuel à terme; hypothèse gouvernementale",
          "Périmètre éligible20Mm² sur96Mm²; loyer public interne et cession ponctuelle distincts; loi août2026 déjà engagée",
          "Besoins d'accueil, accessibilité, entretien différé, migrations et cybersécurité non ajustés",
          "Potentiel net additionnel non identifié; investissements, loyers internes et doublons achats à traiter"]),
    ]
    rows=[]
    for domain, name, location, year, descriptions in domains:
        for level,description in enumerate(descriptions,1):
            rows.append({"domaine":domain,"niveau":level,"type_niveau":["écart ou constat brut","périmètre","besoins et service","potentiel réformable"][level-1],
                         "valeur_etp":"","valeur_economie_nette_M_EUR":"","description":description,"annee":year,
                         "statut":"NON TROUVÉ" if level>=3 else "ESTIMATION",
                         "source_url":meta(name)["source_url"],"source_localisation":location,
                         "date_consultation":DATE,"note":"Les montants hypothétiques externes cités dans le texte ne sont pas un potentiel net identifié; blanc n'est pas zéro"})
    write_csv(OUT/"04d_quatre_niveaux.csv",rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--download", action="store_true", help="Restaurer le cache à partir du manifeste versionné")
    parser.add_argument("--rebuild-manifest", action="store_true", help="Réassembler les métadonnées des sources déjà archivées")
    args = parser.parse_args()
    if args.download:
        restore()
    if args.rebuild_manifest or not MANIFEST.exists():
        make_manifest()
    territorial_data()
    count = pdf_transcriptions()
    four_levels()
    print(f"04d : 90 observations WOFI, 16 cellules DGCL, {count} transcriptions PDF; contrôles de sommes et d'ancres réussis")


if __name__ == "__main__":
    main()
