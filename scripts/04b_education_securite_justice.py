#!/usr/bin/env python3
"""Comparaisons documentées EAG/TALIS, police et justice. Aucun modèle de sureffectif.

python -I scripts/04b_education_securite_justice.py [--download]
--download restaure les documents primaires absents via fetch.py ; les cinq CSV
hérités 04 et le fichier 02 restent des entrées préalablement contrôlées.
Les PDF sont des données, jamais exécutés. Les nombres de pages sont en base 1.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import logging
import re
import subprocess
import sys
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/international"
DATE = "2026-10-28"
COE_ANALYSES = "https://rm.coe.int/cepej-evaluation-report-part-1-en-/1680b272ac"
COE_PROFILS = "https://rm.coe.int/fiche-pays-partie-2-en/1680b21e99"
COE_FR = "https://rm.coe.int/france-2024-2022-/1680b1f6cd"
TALIS_FR = "https://www.oecd.org/content/dam/oecd/en/publications/reports/2025/10/results-from-talis-2024-country-notes_eafd703e/france_714d7439/50507701-en.pdf"
EAG_FR = "https://www.oecd.org/content/dam/oecd/en/publications/reports/2026/09/education-at-a-glance-2026-country-notes_4b77712b/france_3915c659/c75b2cc7-en.pdf"
EURO_METADATA = "https://ec.europa.eu/eurostat/cache/metadata/en/crim_sims.htm"
FLOW = {
    "ratios": "https://sdmx.oecd.org/public/rest/data/OECD.EDU.IMEP,DSD_EAG_UOE_NON_FIN_PERS@DF_UOE_NF_PERS_STR,1.1/",
    "remunerations": "https://sdmx.oecd.org/public/rest/data/OECD.EDU.IMEP,DSD_EAG_UOE_FIN@DF_UOE_FIN_NATURE_STAFF,3.2/",
    "depenses": "https://sdmx.oecd.org/public/rest/data/OECD.EDU.IMEP,DSD_EAG_UOE_FIN@DF_UOE_INDIC_FIN_PERSTUD,3.2/",
    "talis": "https://sdmx.oecd.org/public/rest/data/OECD.EDU.ECS,DSD_TALIS@DF_TALIS_TEACHER_PROFILE,1.0/",
    "police": "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/crim_just_job",
}
FILES = {
    "ratios": "oecd_eag_DF_UOE_NF_PERS_STR.csv",
    "remunerations": "oecd_eag_staffcomp_subset.csv",
    "depenses": "oecd_eag_perstud_subset.csv",
    "talis": "oecd_talis_teacher.csv",
    "police": "eurostat_crim_just_job.csv",
}
DOCS = [
    (COE_ANALYSES, "cepej2024_analyses", "data/cache/04b", ".pdf"),
    (COE_PROFILS, "cepej2024_profils", "data/cache/04b", ".pdf"),
    (COE_FR, "cepej2024_reponses_france", "data/cache/04b", ".pdf"),
    ("https://rm.coe.int/explanatory-note-2024-cycle-cepej-2023-2-en/1680aae30a", "cepej2024_notice", "data/cache/04b", ".pdf"),
    (TALIS_FR, "oecd_talis2024_france", "data/cache/04b", ".pdf"),
    (EAG_FR, "oecd_eag2026_france", "data/cache/04b", ".pdf"),
    ("https://ec.europa.eu/eurostat/documents/d/education-and-training/uoe-manual-2026-final", "uoe_manuel2026", "data/cache/04b", ".pdf"),
    (EURO_METADATA, "eurostat_crim_metadata", "data/raw/04b", ".html"),
    ("https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/crim_off_cat?format=JSON&lang=en&freq=A&iccs=ICCS0101&unit=P_HTHAB&sinceTimePeriod=2022&untilTimePeriod=2022", "eurostat_homicide2022_iccs", "data/raw/04b", ".json"),
]
# Pages du recueil CEPEJ, pas rang dans un classement. Les trois entités du
# Royaume-Uni restent séparées. Canada et agrégats UE/OCDE ne sont pas couverts.
PROFILES = [
    ("AUT", "Austria", 22), ("BEL", "Belgium", 30),
    ("DNK", "Denmark", 54), ("EST", "Estonia", 58),
    ("FIN", "Finland", 62), ("FRA", "France", 66),
    ("DEU", "Germany", 74), ("IRL", "Ireland", 90),
    ("ITA", "Italy", 94), ("NLD", "Netherlands", 126),
    ("NOR", "Norway", 134), ("POL", "Poland", 138),
    ("PRT", "Portugal", 142), ("ESP", "Spain", 162),
    ("SWE", "Sweden", 166), ("CHE", "Switzerland", 170),
    ("UK:ENG&WAL", "UK - England and Wales", 182),
    ("UK:NIR", "UK - Northern Ireland", 186),
    ("UK:SCO", "UK - Scotland", 190),
]
COLS = ["id", "fonction", "pays", "pays_libelle", "indicateur", "valeur", "unite", "annee", "niveau_education", "type_etablissement", "operation_statistique", "profil_enseignant", "champ", "statut", "obs_status", "source_url", "source_localisation", "note"]
logging.getLogger("pypdf").setLevel(logging.ERROR)


def read_csv(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def write_csv(name, rows, cols=None):
    path = OUT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    if cols is None:
        cols = COLS
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=cols)
        writer.writeheader()
        writer.writerows(rows)


def code(value):
    return value.split(": ", 1)[0]


def norm(row):
    return {key.split(":", 1)[0]: value for key, value in row.items()}


def number(value):
    if value in (None, "", "NA", "NAP", "M", "O"):
        return None
    return float(str(value).replace(" ", "").replace(",", "."))


def fact(id_, function, geo, name, indicator, value, unit, year, scope, url, loc, **extra):
    entry = dict(dict.fromkeys(COLS, ""), id=id_, fonction=function, pays=geo, pays_libelle=name,
                 indicateur=indicator, valeur="" if value is None else value, unite=unit,
                 annee=year, champ=scope, statut="FAIT", source_url=url, source_localisation=loc)
    entry.update(extra)
    return entry


def source_row(row, kind, n, indicator, unit=None, **extra):
    return fact(f"{kind}_{n}", "enseignement", code(row["REF_AREA"]), row["REF_AREA"].split(": ", 1)[-1],
                indicator, number(row["OBS_VALUE"]), unit or code(row["UNIT_MEASURE"]),
                int(row["TIME_PERIOD"]), "", FLOW[kind], f"data/raw/04/{FILES[kind]} / ligne CSV {n}",
                obs_status=" | ".join(row[k] for k in ["OBS_STATUS", "OBS_STATUS_2", "OBS_STATUS_3"] if row.get(k)),
                niveau_education=code(row["EDUCATION_LEV"]), **extra)


def education(inputs):
    ratios = []
    for n, row in inputs["ratios"]:
        if code(row["EDUCATION_LEV"]) not in ["ISCED11_1", "ISCED11_2", "ISCED11_3", "ISCED11_34", "ISCED11_35"]:
            continue
        # Toutes les dimensions restantes ont été lues ; une évolution du fichier
        # vers d'autres dimensions doit interrompre le calcul, pas être agrégée.
        for key, expected in {"MEASURE": "STU_PERS", "UNIT_MEASURE": "ST_TCHR", "SEX": "_T", "AGE": "_T", "INTENSITY": "_T", "EDUCATION_TYPE": "FE", "UNIT_MULT": "0"}.items():
            assert code(row[key]) == expected, (key, row[key])
        entry = source_row(row, "ratios", n, "eleves_par_enseignant", "eleves_ETP_par_enseignant_ETP", type_etablissement=code(row["INST_TYPE_EDU"]))
        entry["champ"] = "Élèves et enseignants ETP de même CITE et type d'établissement ; éducation formelle ; CITE 3 contient 34 et 35"
        entry["note"] = "Ratio de ressources enseignantes, pas taille de classe ni nombre d'administratifs. Public/privé/total sont imbriqués ; aucune somme."
        ratios.append(entry)
    write_csv("04b_education_ratios.csv", ratios)

    remuneration, spending = [], []
    for kind, output in [("remunerations", remuneration), ("depenses", spending)]:
        for n, row in inputs[kind]:
            if row["TIME_PERIOD"] != "2023" or code(row["EDUCATION_LEV"]) not in ["ISCED11_1", "ISCED11_2", "ISCED11_3"]:
                continue
            for k, expected in {"EXP_SOURCE": "_T", "EXP_DESTINATION": "INST_EDU"}.items():
                assert code(row[k]) == expected
            entry = source_row(row, kind, n, code(row["EXPENDITURE_TYPE"]), type_etablissement="INST_EDU")
            entry["champ"] = "Tous établissements, toutes sources de financement ; même niveau CITE ; dépenses de l'année 2023"
            if kind == "remunerations":
                assert code(row["UNIT_MULT"]) == "6" and code(row["PRICE_BASE"]) == "V"
                entry["unite"] = "millions_monnaie_nationale_courante"
                entry["note"] = "Enseignants CUR_COMPT ; non-enseignants CUR_COMPO ; total CUR_COMP. Non-enseignants inclut soutiens et services. Pas de comparaison des montants entre monnaies."
            else:
                assert code(row["UNIT_MULT"]) == "0"
                entry["note"] = "USD_PPP_ST = dollars PPA par élève ETP ; PT_B1GQ_POP = % du PIB/habitant. Aucun mélange de ces unités."
            output.append(entry)
    groups = {}
    for entry in remuneration:
        groups.setdefault((entry["pays"], entry["niveau_education"]), {})[entry["indicateur"]] = entry
    residuals = []
    for (geo, level), group in groups.items():
        if not all(k in group and group[k]["valeur"] != "" for k in ["CUR_COMP", "CUR_COMPO", "CUR_COMPT"]):
            continue
        total, non, teach = [group[k] for k in ["CUR_COMP", "CUR_COMPO", "CUR_COMPT"]]
        # Les montants sont déjà publiés arrondis, et certains pays incluent une
        # composante dans une autre. Pas d'imputation d'un composant manquant.
        residuals.append(dict(pays=geo, niveau=level, residu=total["valeur"]-non["valeur"]-teach["valeur"]))
        entry = dict(total, id=f"remun_share_{geo}_{level}", indicateur="part_remuneration_non_enseignante", valeur=100*non["valeur"]/total["valeur"], unite="pourcent_remuneration", statut="ESTIMATION")
        entry["source_localisation"] = non["source_localisation"] + " ; " + total["source_localisation"]
        entry["note"] = "100 × CUR_COMPO / CUR_COMP ; part de masse de rémunération, pas part de postes administratifs."
        if abs(total["valeur"]-non["valeur"]-teach["valeur"]) > 1:
            entry["note"] += " Attention : les composants ne reconstituent pas le total publié à 1 million près ; différence de périmètre ou de déclaration non résolue."
        remuneration.append(entry)
    write_csv("04b_education_remunerations.csv", remuneration)
    write_csv("04b_education_depense_eleve.csv", spending)

    depp = []
    for row in read_csv(ROOT / "data/france/02_metiers.csv"):
        if not row["id"].startswith("DEPP_") or row["id"].startswith(("DEPP_MISSION", "DEPP_AESH_CONTROLE")):
            continue
        entry = fact(row["id"], "enseignement", "FRA", "France", row["metier_ou_groupe"], number(row["valeur"]), row["unite"], int(row["annee"]), row["couverture"], row["source_url"], row["source_localisation"], note=row["note"] + " | Reprise 02 : les parents et les enfants se recouvrent ; ne pas sommer les lignes.")
        depp.append(entry)
    depp_lookup = {r["id"]: r for r in depp}
    total = depp_lookup["DEPP_NE48_PP"]
    for parent_id, indicator in [("DEPP_NE24_PP", "part_vie_scolaire_dans_non_enseignants"), ("DEPP_NE27_PP", "part_administratifs_dans_non_enseignants")]:
        part = depp_lookup[parent_id]
        depp.append(dict(part, id="depp_share_"+parent_id, indicateur=indicator, valeur=100*part["valeur"]/total["valeur"], unite="pourcent_PP", statut="ESTIMATION", source_localisation=part["source_localisation"]+" ; "+total["source_localisation"], note="100 × sous-ensemble / total des non-enseignants ; le numérateur est déjà inclus dans le dénominateur."))
    write_csv("04b_personnels_education_fr.csv", depp)
    return ratios, remuneration, spending, depp, residuals


def talis(inputs):
    output = []
    for n, row in inputs["talis"]:
        if not (code(row["EDUCATION_LEV"]) == "ISCED11_2" and code(row["TEACHER_PROFILE"]) == "_T" and code(row["MEASURE"]) in ["Q14_1", "Q15_1"] and code(row["STATISTICAL_OPERATION"]) in ["MEAN", "SE"]):
            continue
        for k in ["AGE", "SEX", "URBANISATION", "INSTITUTION_TYPE", "STUDENTS_CHARACTERISTICS"]:
            assert code(row[k]) == "_T", (k, row[k])
        entry = source_row(row, "talis", n, code(row["MEASURE"]), "heures_par_semaine", operation_statistique=code(row["STATISTICAL_OPERATION"]), profil_enseignant="tous_temps_plein_et_partiel", type_etablissement="_T")
        entry["champ"] = "TALIS 2024, premier cycle secondaire, tous enseignants ; statistiques d'enquête déclaratives"
        entry["note"] = "Q14_1 = travail total ; Q15_1 = enseignement. SE conservée à part. La différence ne mesure pas les tâches administratives."
        output.append(entry)
    reader = PdfReader(ROOT / "data/cache/04b/oecd_talis2024_france.pdf")
    work = reader.pages[10].extract_text()
    assert "38.7" in work and "1.5 hours" in work and "average: 3" in work
    # Transcription contrôlée de la note pays, valeurs arrondies publiées.
    tasks = [("travail_total", 38.7, 41.0), ("enseignement", 20.1, 22.7),
             ("preparation", 7.2, 7.4), ("correction", 5.3, 4.6), ("administration", 1.5, 3.0)]
    for indicator, fr, oecd in tasks:
        for geo, name, value in [("FRA", "France", fr), ("OECD", "OCDE", oecd)]:
            output.append(fact(f"talis_ft_{geo}_{indicator}", "enseignement", geo, name, indicator, value, "heures_par_semaine", 2024, "TALIS, premier cycle secondaire, enseignants à temps plein, établissements publics et privés du champ de l'enquête", TALIS_FR, "data/cache/04b/oecd_talis2024_france.pdf / p. imprimée 10 (PDF 11), Working hours ; tables 3.8 et 3.10", operation_statistique="MEAN_arrondie", profil_enseignant="temps_plein", note="Moyenne déclarée, semaine de référence ; les tâches ne constituent pas une décomposition additive exacte du total ; SE du temps plein non disponible dans ce fichier."))
    contexts = [("stress_administratif", 58, None, 11), ("stress_changements_prescriptions", 62, None, 11),
                ("classe_avec_plusieurs_formes_diversite", 91, 77, 12), ("part_temps_classe_maintien_ordre", 18, 15, 12),
                ("changements_sans_ressources", 49, 31, 12)]
    for indicator, fr, oecd, page in contexts:
        for geo, name, value in [("FRA", "France", fr), ("OECD", "OCDE", oecd)]:
            if value is None:
                continue
            output.append(fact(f"talis_ctx_{geo}_{indicator}", "enseignement", geo, name, indicator, value, "pourcent", 2024, "TALIS, premier cycle secondaire ; tous enseignants, pas seulement temps plein", TALIS_FR, f"data/cache/04b/oecd_talis2024_france.pdf / PDF {page} (imprimée {page-1})", profil_enseignant="tous", note="Déclarations d'enquête ; diversité = plus d'une catégorie parmi comportement, langue, besoins spécifiques. Le maintien de l'ordre est une part du temps en classe."))
    write_csv("04b_talis2024.csv", output)
    return output


def police(inputs):
    output = []
    notes = {
        "FR": "Police locale incluse ; territoires ultramarins listés au §3.7 exclus. Aucun soutien administratif dans la définition commune. Pas de donnée 2023 française dans le brut.",
        "DE": "Personnes physiques de fonctionnaires hors stagiaires au 30 juin, domaine fonctionnel Police : date différente du 31 décembre commun.",
        "BE": "Personnel opérationnel fédéral + local ; personnel civil exclu.",
        "EE": "2019-2022 : 1er janvier de l'année suivante ; personnel administratif exclu.",
        "IE": "Forensic Science Ireland inclus.",
        "CH": "Depuis janvier 2022 : seuls les personnels autorisés à exercer la coercition policière ; rupture de méthode.",
    }
    for n, row in inputs["police"]:
        if row["isco08"] != "OC5412" or row["time"] != "2022":
            continue
        assert row["sex"] == "T" and row["freq"] == "A"
        output.append(fact(f"police_{n}", "police", row["geo"], row["geo_label"], "policiers", number(row["value"]), "personnes" if row["unit"] == "NR" else "personnes_pour_100000_habitants", 2022, "Policiers, définition Eurostat-UNODC ; hors secrétaires et employés de soutien ; référence commune 31 décembre, exceptions nationales", FLOW["police"], f"data/raw/04/{FILES['police']} / ligne {n} ; métadonnées §3.4, 3.7, 4, 15.1 Police Officers", obs_status=row["flag"], note=notes.get(row["geo"], "Note nationale spécifique non indiquée dans la rubrique Police Officers ; définition commune à vérifier auprès du correspondant national.") + " Le taux emploie la population résidente de référence Eurostat ; ce n'est pas un taux d'administration des forces."))
    write_csv("04b_police2022.csv", output)
    # Indicateur de contexte distinct : infractions enregistrées, et non victimes
    # ou affaires élucidées. Pas de division mécanique des emplois par ce taux.
    raw = ROOT / "data/raw/04b/eurostat_homicide2022_iccs.json"
    data = json.loads(raw.read_text(encoding="utf-8"))
    assert data.get("value"), "Réponse homicide vide : filtre ICCS0101 à contrôler"
    dims = [sorted(data["dimension"][d]["category"]["index"], key=data["dimension"][d]["category"]["index"].get) for d in data["id"]]
    context = []
    meta = json.loads(raw.with_suffix(".meta.json").read_text(encoding="utf-8"))
    for i, combination in enumerate(itertools.product(*dims)):
        item = dict(zip(data["id"], combination))
        value = data["value"].get(str(i)) if isinstance(data["value"], dict) else data["value"][i]
        if value is None:
            continue
        geo = item["geo"]
        context.append(fact(f"homicide_{geo}", "police", geo, data["dimension"]["geo"]["category"]["label"][geo], "infractions_homicide_volontaire_enregistrees", value, "infractions_pour_100000_habitants", 2022, "Infractions d'homicide volontaire enregistrées par la police ; exclut tentatives ; ce n'est pas le nombre de victimes", meta["source_url"], f"data/raw/04b/eurostat_homicide2022_iccs.json / geo={geo}, ICCS0101, P_HTHAB, 2022", obs_status=data.get("status", {}).get(str(i), ""), note="Besoin/service : un contexte parmi d'autres, pas charge exhaustive ni effet causal de l'effectif. Voir différences de plainte, définition et enregistrement, Eurostat crim §3.4/15.1."))
    write_csv("04b_police_contexte2022.csv", context)
    return output


def justice():
    output = []
    reader = PdfReader(ROOT / "data/cache/04b/cepej2024_profils.pdf")
    general = PdfReader(ROOT / "data/cache/04b/cepej2024_analyses.pdf")
    human_ids = ["juges_professionnels", "non_juges", "procureurs", "non_procureurs"]
    medians = {"juges_professionnels": 17.6, "non_juges": 57.9, "procureurs": 11.2, "non_procureurs": 14.7}
    for geo, name, first in PROFILES:
        texts = [reader.pages[i].extract_text() for i in range(first-1, first+3)]
        assert name in texts[0][:180] and "2022" in texts[0][:80]
        block = texts[1].split("Lawyers", 1)[1].split("Gender Balance", 1)[0]
        values = re.findall(r"\b(?:\d+[.,]\d+|NAP|NA)\b", block)
        assert len(values) == 20, (geo, values)
        for j, indicator in enumerate(human_ids):
            assert number(values[j*4+2]) == medians[indicator]
            note = "FTE demandé par CEPEJ ; postes effectivement occupés. Pas un effectif de fonctionnaires du ministère entier."
            if indicator == "non_procureurs" and geo == "FRA":
                note += " Q60 France : juristes assistants et assistants spécialisés ; délégués du procureur exclus. Comparabilité des greffes siège/parquet à expertiser : pas de correction inventée."
            output.append(fact(f"cepej_{geo}_{indicator}", "justice", geo, name, indicator, number(values[j*4]), "ETP_pour_100000_habitants", 2022, "Système judiciaire CEPEJ ; tribunaux et parquet séparés ; non-juges = cinq catégories dont assistance judiciaire, administration, technique", COE_PROFILS, f"data/cache/04b/cepej2024_profils.pdf / PDF {first+1}, fiche pays 2/4 ; Q46/Q52/Q55/Q60", obs_status=values[j*4] if number(values[j*4]) is None else "", note=note))
        # Tableau central, trois types d'affaires au premier degré. NA et NAP restent vides.
        dt = re.search(r"Administrative\s+(\S+)\s+Criminal\s+(\S+)\s+Civil\s+(\S+)", texts[0])
        assert dt, geo
        for indicator, token in zip(["DT_administratif_1", "DT_penal_1", "DT_civil_contentieux_1"], dt.groups()):
            output.append(fact(f"cepej_{geo}_{indicator}", "justice", geo, name, indicator, number(token), "jours_theoriques", 2022, "Première instance ; DT = affaires pendantes fin d'année / résolues dans l'année × 365", COE_PROFILS, f"data/cache/04b/cepej2024_profils.pdf / PDF {first}, fiche pays 1/4 ; détail PDF {first+2}", obs_status=token if number(token) is None else "", note="Ratio de stock/flux, pas durée moyenne des dossiers terminés ni jugement causal de productivité. Contentieux non homogènes entre droits nationaux."))
        incoming = texts[2].split("Incoming Cases", 1)[1].split("Total number of 1st instance", 1)[0]
        tail = re.split(r"2022\s+2020\s+2018\s+2016\s+2014\s+2012", incoming)[1]
        values_in = re.findall(r"\b(?:\d+\.\d+|NAP|NA)\b", tail)
        if geo == "UK:NIR":
            # La mise en page ne livre que 15 valeurs pour 18 cellules. Ne pas
            # décaler arbitrairement les colonnes : cette série n'est pas extraite.
            values_in = ["NA"] * 18
        else:
            assert len(values_in) == 18, (geo, values_in)
        for j, field in enumerate(["civil_contentieux", "penal", "administratif"]):
            token = values_in[j*6]
            output.append(fact(f"cepej_{geo}_entrantes_{field}_1", "justice", geo, name, f"entrantes_{field}_1", number(token), "affaires_pour_100_habitants", 2022, "Première instance ; catégories CEPEJ et périmètre national, non pondérées par complexité", COE_PROFILS, f"data/cache/04b/cepej2024_profils.pdf / PDF {first+2}, fiche 3/4 Incoming Cases", statut="NON TROUVÉ" if geo == "UK:NIR" else "FAIT", obs_status="non_extrait_graphique_incomplet" if geo == "UK:NIR" else token if number(token) is None else "", note="Irlande du Nord : extraction graphique incomplète, pas de valeur imputée." if geo == "UK:NIR" else "Nombre d'affaires, pas heures nécessaires ; certains pays comptent par événement et d'autres par auteur pour le parquet."))
    for indicator, value in medians.items():
        output.append(fact(f"cepej_median_{indicator}", "justice", "COE_MEDIAN", "Médiane Conseil de l'Europe", indicator, value, "ETP_pour_100000_habitants", 2022, "Médiane de pays/entités disponibles CEPEJ ; ce n'est ni moyenne UE ni norme d'effectif", COE_PROFILS, "data/cache/04b/cepej2024_profils.pdf / PDF 67, fiche France 2/4", note="Composition variable selon données disponibles ; ne pas assimiler à un groupe de pays riches comparables."))
    # La figure 3.12 est un vrai tableau textuel, plus contrôlable qu'un graphique.
    table = general.pages[50].extract_text(extraction_mode="layout")
    indicators = ["non_juges_par_juge", "categories123_par_juge", "rechtspfleger_par_juge", "assistants_justice_par_juge", "administration_par_juge", "techniques_par_juge", "autres_par_juge"]
    for geo, name, first in PROFILES + [("Median", "Médiane Conseil de l'Europe", 0)]:
        match = re.search(r"^\s*" + re.escape(geo) + r"\s+(.+)$", table, flags=re.M)
        assert match, geo
        tokens = match.group(1).split()
        assert len(tokens) == 7, (geo, tokens)
        for indicator, token in zip(indicators, tokens):
            output.append(fact(f"cepej_split_{geo}_{indicator}", "justice", "COE_MEDIAN" if geo == "Median" else geo, name, indicator, number(token), "ETP_non_juges_par_ETP_juge", 2022, "Q52 rapporté aux juges Q46 ; catégories 1+2+3 sont un sous-total ; total et composants non additifs", COE_ANALYSES, "data/cache/04b/cepej2024_analyses.pdf / PDF 51 (imprimée 51), figure 3.12", obs_status=token if number(token) is None else "", note="Catégories nationales ; Espagne : presque tout en autres ; Finlande/Pays-Bas/Norvège : détail non disponible. NAP n'est pas zéro."))
    # Quelques chiffres saisis depuis les textes et graphiques des fiches lus.
    budgets = [("FRA", "France", 77.2, .20, 66), ("DEU", "Germany", 136.1, .30, 74), ("ITA", "Italy", 100.6, .31, 94), ("ESP", "Spain", 96.8, .34, 162), ("NLD", "Netherlands", 138.8, .26, 126), ("SWE", "Sweden", 121.3, .24, 166), ("COE_MEDIAN", "Médiane Conseil de l'Europe", 74.8, .28, 66)]
    for geo, name, euro, pct, first in budgets:
        for indicator, value, unit in [("budget_systeme_judiciaire_hab", euro, "euros_courants_par_habitant"), ("budget_systeme_judiciaire_pib", pct, "pourcent_PIB")]:
            output.append(fact(f"cepej_{geo}_{indicator}", "justice", geo, name, indicator, value, unit, 2022, "Budget exécuté du système judiciaire = tribunaux + parquet + aide judiciaire ; hors prisons, PJJ, administration ministérielle ; pas PPA", COE_PROFILS, f"data/cache/04b/cepej2024_profils.pdf / PDF {first}, fiche 1/4", note="Montants transcrits du profil officiel. Les différences de prix, revenus, frais de justice et externalisation restent à expliquer."))
    for geo, name, value, first in [("FRA", "France", 1.15, 67), ("DEU", "Germany", 1.27, 75), ("COE_MEDIAN", "Médiane Conseil de l'Europe", 1.58, 67)]:
        output.append(fact(f"cepej_{geo}_sites", "justice", geo, name, "sites_judiciaires", value, "sites_pour_100000_habitants", 2022, "Tous tribunaux, sites géographiques ; distinct des entités juridiques de première instance", COE_PROFILS, f"data/cache/04b/cepej2024_profils.pdf / PDF {first}, fiche 2/4 All courts (geographic locations)", note="Pas une mesure du temps de trajet, de l'accessibilité numérique ni du besoin rural."))
    for indicator, value in [("DT_civil_contentieux_1", 239), ("DT_administratif_1", 292)]:
        output.append(fact(f"cepej_median_{indicator}", "justice", "COE_MEDIAN", "Médiane Conseil de l'Europe", indicator, value, "jours_theoriques", 2022, "Première instance ; médiane de pays/entités disponibles pour le type d'affaire", COE_PROFILS, "data/cache/04b/cepej2024_profils.pdf / PDF 68, fiche France 3/4"))
    fr_reader = PdfReader(ROOT / "data/cache/04b/cepej2024_reponses_france.pdf")
    fr_page = fr_reader.pages[29].extract_text()
    for indicator, value in [("Q52_non_juges", 25388), ("Q52_assistants_justice", 20190), ("Q52_administration", 3424), ("Q52_techniques", 898), ("Q52_autres", 874)]:
        assert f"{value:,}".replace(",", " ") in fr_page or str(value) in fr_page
        output.append(fact(f"cepej_FR_{indicator}", "justice", "FRA", "France", indicator, value, "ETP", 2022, "Q52 : non-juges dans les tribunaux ; pas tout le ministère ; total source conservé", COE_FR, "data/cache/04b/cepej2024_reponses_france.pdf / PDF 30, Q52", note="Les composants publiés valent 25 386 ETP contre un total de 25 388 : résidu de 2 ETP conservé, cause non expliquée par le document."))
    for indicator, numerator in [("part_assistance_Q52", 20190), ("part_administration_Q52", 3424)]:
        output.append(fact(f"cepej_FR_{indicator}", "justice", "FRA", "France", indicator, 100*numerator/25388, "pourcent_ETP", 2022, "Q52 ; dénominateur total publié 25 388, malgré résidu de 2 ETP des composants", COE_FR, "data/cache/04b/cepej2024_reponses_france.pdf / PDF 30, Q52", statut="ESTIMATION", note=f"100 × {numerator} / 25388 ; aucune assimilation des fonctions d'assistance aux fonctions administratives."))
    write_csv("04b_justice2022.csv", output)
    return output


def comparisons(groups):
    result = []
    for dataset, rows in groups.items():
        # Chaque groupe conserve année, unité, niveau, établissement et profil.
        by_key = {}
        for row in rows:
            if row["valeur"] == "" or row["operation_statistique"] == "SE":
                continue
            if row["unite"] == "millions_monnaie_nationale_courante":
                continue
            key = tuple(row[k] for k in ["indicateur", "annee", "unite", "niveau_education", "type_etablissement", "profil_enseignant", "operation_statistique"])
            by_key.setdefault(key, {})[row["pays"]] = row
        for key, values in by_key.items():
            fr = values.get("FR") if dataset == "police" else values.get("FRA")
            if fr is None:
                continue
            for geo, comp in values.items():
                if geo in ["FR", "FRA"] or not comp["valeur"]:
                    continue
                result.append(dict(dataset=dataset, indicateur=key[0], annee=key[1], unite=key[2], niveau_education=key[3], type_etablissement=key[4], profil_enseignant=key[5], comparateur=geo, valeur_france=fr["valeur"], valeur_comparateur=comp["valeur"], ecart=fr["valeur"]-comp["valeur"], ecart_relatif_pct=100*(fr["valeur"]/comp["valeur"]-1), statut="ESTIMATION", source_url=fr["source_url"], source_localisation=fr["source_localisation"]+" ; "+comp["source_localisation"], limite="Écart descriptif France/comparateur à dimensions identiques ; métadonnées nationales, besoins et qualité non neutralisés. Aucun potentiel d'emplois ou euros déduit."))
    cols = ["dataset", "indicateur", "annee", "unite", "niveau_education", "type_etablissement", "profil_enseignant", "comparateur", "valeur_france", "valeur_comparateur", "ecart", "ecart_relatif_pct", "statut", "source_url", "source_localisation", "limite"]
    write_csv("04b_ecarts.csv", result, cols)
    return result


def four_levels(ratios, cops, courts):
    """Les corrections non identifiées ont une cellule vide, jamais zéro."""
    rows = []
    def select(items, **criteria):
        values = [r for r in items if all(str(r[k]) == str(v) for k, v in criteria.items())]
        assert len(values) == 1, criteria
        return values[0]
    def add(function, level, label, left=None, right=None, note="", source="", loc=""):
        if left and right:
            assert left["unite"] == right["unite"] and left["annee"] == right["annee"]
        rows.append(dict(fonction=function, niveau=level, indicateur=label, france=left["valeur"] if left else "", comparateur=right["pays"] if right else "", valeur_comparateur=right["valeur"] if right else "", ecart=left["valeur"]-right["valeur"] if left and right else "", ecart_relatif_pct=100*(left["valeur"]/right["valeur"]-1) if left and right and right["valeur"] else "", unite=left["unite"] if left else "non_identifiee", annee=left["annee"] if left else "non_identifiee", statut="ESTIMATION" if left and right else "NON TROUVÉ", source_url=left["source_url"] if left else source, source_localisation=(left["source_localisation"]+" ; "+right["source_localisation"]) if left and right else loc, note=note))
    base = dict(indicateur="eleves_par_enseignant", annee=2024, niveau_education="ISCED11_1")
    for level, institution in [("1_brut", "INST_EDU"), ("2_perimetre", "INST_EDU_PUB")]:
        fr = select(ratios, **base, pays="FRA", type_etablissement=institution)
        de = select(ratios, **base, pays="DEU", type_etablissement=institution)
        add("enseignement", level, "Ratio élèves/enseignant primaire France-Allemagne", fr, de, "Même année/CITE/unité ; total établissements au brut, public au niveau 2. Cette restriction ne corrige ni besoins sociaux ni organisation scolaire. Plus d'élèves/enseignant signifie moins de ressources enseignantes par élève.")
    add("enseignement", "3_besoins_service", "Effectifs ajustés à besoins et qualité constants", note="Non identifié : ventilation comparable des soutiens, besoins éducatifs, horaires élèves, options, dispersion géographique et résultats à intégrer. TALIS documente la diversité des classes mais n'identifie pas une correction d'effectifs.", source=TALIS_FR, loc="PDF 11-12, temps de travail et diversité ; EAG D2, méthode")
    add("enseignement", "4_potentiel", "Réduction d'ETP compatible avec qualité", note="Non identifié ; une part de rémunération non enseignante ou 1,5 h d'administration enseignante ne donne pas des postes supprimables. Pilotes nécessaires.", source=TALIS_FR, loc="PDF 11 ; data/france/02_metiers.csv, DEPP")
    fr = select(cops, pays="FR", unite="personnes_pour_100000_habitants")
    de = select(cops, pays="DE", unite="personnes_pour_100000_habitants")
    add("police", "1_brut", "Policiers pour 100 000 habitants France-Allemagne", fr, de, "Même année 2022 et unité ; dates nationales différentes et hors soutien dans la définition commune.")
    add("police", "2_perimetre", "Policiers et soutien à périmètre/date identiques", note="Non identifié : police locale incluse en France ; Allemagne au 30 juin et hors stagiaires ; soutien exclu. Aucun facteur de correction établi.", source=EURO_METADATA, loc="§3.4, §3.7, §15.1 Police Officers")
    add("police", "3_besoins_service", "Effectifs par charge/mission et qualité", note="Non identifié : homicides enregistrés 2022 disponibles, mais ne couvrent ni missions, ni temps de procédure, ni présence territoriale. Plaintes/élucidation/victimations/temps d'intervention manquent au rapprochement.", source=EURO_METADATA, loc="§3.4/15.1 ; data/raw/04b/eurostat_homicide2022_iccs.json")
    add("police", "4_potentiel", "ETP administratifs évitables", note="Non identifié : le brut porte sur policiers opérationnels ; aucun dénominateur comparable des personnels administratifs, aucun pilote de temps net validé.", source=EURO_METADATA, loc="§3.4 Criminal Justice Personnel")
    fr = select(courts, pays="FRA", indicateur="non_juges", unite="ETP_pour_100000_habitants")
    de = select(courts, pays="DEU", indicateur="non_juges", unite="ETP_pour_100000_habitants")
    add("justice", "1_brut", "Non-juges pour 100 000 habitants France-Allemagne", fr, de, "Les cinq fonctions incluent assistance judiciaire et technique. Pas un ratio d'administratifs.")
    fr = select(courts, pays="FRA", indicateur="administration_par_juge")
    de = select(courts, pays="DEU", indicateur="administration_par_juge")
    add("justice", "2_perimetre", "Restriction aux fonctions administratives déclarées, par juge", fr, de, "Restriction fonctionnelle Q52, pas correction complète. Le dénominateur juges diffère fortement ; 0,45/0,33 ne prouve pas un excès par habitant. Rechtspfleger, greffes et externalisation diffèrent.")
    add("justice", "3_besoins_service", "Ressources ajustées aux affaires, délais et accès", note="Non identifié : affaires entrantes et DT documentés en 2022, mais pas de pondération de complexité, de règles procédurales ou d'accessibilité. Q60 France restreint ; aucune correction inventée.", source=COE_PROFILS, loc="Fiches 3/4 ; France PDF 68, Allemagne PDF 76")
    add("justice", "4_potentiel", "ETP ou budget économisables à qualité constante", note="Non identifié : un retard plus long n'est pas un gisement d'emplois. Expérimenter les tâches de dossier et mesurer le temps net réaffectable, les erreurs, droits des parties et délais.", source=COE_ANALYSES, loc="p. 50-52 et chapitre Efficacité/qualité")
    write_csv("04b_quatre_niveaux.csv", rows, ["fonction", "niveau", "indicateur", "france", "comparateur", "valeur_comparateur", "ecart", "ecart_relatif_pct", "unite", "annee", "statut", "source_url", "source_localisation", "note"])


def register():
    rows = []
    for kind, filename in FILES.items():
        path = ROOT / "data/raw/04" / filename
        rows.append(dict(id=f"04b_heritage_{kind}", titre=filename, institution="Eurostat" if kind == "police" else "OCDE", date_publication="non documentée dans le téléchargement hérité", url=FLOW[kind], date_consultation=DATE, acces="integral", sha256_16=hashlib.sha256(path.read_bytes()).hexdigest()[:16], notes="Lecture intégrale du CSV local contrôlé ; URL canonique reconstruite. L'URL et l'horodatage exacts de la requête initiale manquent ; pas de certification de fraîcheur de l'API."))
    for old in read_csv(ROOT / "sources/registre_02.csv"):
        if "chapitre-2-les-enseignants" in old["url"] or "chapitre-3-les-personnels-non-enseignants" in old["url"]:
            rows.append(dict(old, id="04b_reprise_"+old["id"], notes=old["notes"]+" | Source réutilisée du chantier 02 ; pas une vérification indépendante.") )
    rows.append(dict(id="04b_eag_D2_lecture_web", titre="EAG 2026 D2, méthode des ratios et classes", institution="OCDE", date_publication="2026-09-29", url="https://www.oecd.org/en/publications/education-at-a-glance-2026_b4968bbc-en/full-report/how-do-student-teacher-ratios-and-class-sizes-vary-across-education-levels_30c0e06c.html", date_consultation=DATE, acces="partiel", sha256_16="", notes="Texte méthode lu avec l'outil web ; téléchargement terminal 403 conservé séparément. Pas de prétendue empreinte du texte web intégral."))
    for directory in ["data/raw/04b", "data/cache/04b"]:
        for meta_path in sorted((ROOT / directory).glob("*.meta.json")):
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            url = meta["source_url"]
            institution = "Conseil de l'Europe / CEPEJ" if "coe.int" in url else "Eurostat" if "europa.eu" in url else "OCDE"
            publication = "2024-10-16" if "cepej2024" in meta_path.name else "2025-10" if "talis2024" in meta_path.name else "2026-09-29" if "eag2026" in meta_path.name else "2026" if "2026" in meta_path.name else "mise à jour métadonnées 2026-04-29" if "crim_metadata" in meta_path.name else "voir manifeste"
            rows.append(dict(id="04b_"+meta_path.name.removesuffix(".meta.json"), titre=meta_path.name.removesuffix(".meta.json"), institution=institution, date_publication=publication, url=url, date_consultation=meta["date_consultation"], acces=meta["acces"], sha256_16=meta["sha256"][:16], notes=f"Brut : {meta['raw_path']}. HTTP {meta['http_status']}. Conversion : {meta.get('conversion','')}. Les pages bloquées/JSON sans valeur ne sont pas utilisés comme statistiques."))
    cols = ["id", "titre", "institution", "date_publication", "url", "date_consultation", "acces", "sha256_16", "notes"]
    path = ROOT / "sources/registre_04b.csv"
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=cols)
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--download", action="store_true")
    args = parser.parse_args()
    for url, stem, directory, ext in DOCS:
        path = ROOT / directory / (stem+ext)
        if not path.exists() and args.download:
            subprocess.run([sys.executable, "-I", str(ROOT / "scripts/fetch.py"), url, stem, "--out-dir", str(ROOT/directory), "--timeout", "45"], check=True)
        if not path.exists():
            raise FileNotFoundError(f"{path} absent. Restauration : python -I scripts/04b_education_securite_justice.py --download")
        if ext == ".pdf":
            assert path.read_bytes().startswith(b"%PDF-"), path
    inputs = {kind: [(i, norm(row)) for i, row in enumerate(read_csv(ROOT / "data/raw/04" / filename), 2)] for kind, filename in FILES.items()}
    # Eurostat n'a pas de colonnes 'code: libellé', norm ne change rien ici.
    ratios, remuneration, spending, depp, residuals = education(inputs)
    time = talis(inputs)
    cops = police(inputs)
    courts = justice()
    gaps = comparisons(dict(ratios=ratios, remunerations=remuneration, depenses=spending, talis=time, police=cops, justice=courts))
    four_levels(ratios, cops, courts)
    collections = dict(ratios=ratios, remunerations=remuneration, depenses=spending, personnels_fr=depp, talis=time, police=cops, justice=courts)
    for name, rows in collections.items():
        ids = [r["id"] for r in rows]
        assert len(set(ids)) == len(ids), name
        assert all(r["source_url"] and r["source_localisation"] and r["annee"] and r["statut"] for r in rows)
    assert next(r for r in cops if r["pays"] == "FR" and r["unite"] == "personnes")["valeur"] == 245983
    assert next(r for r in courts if r["id"] == "cepej_FRA_non_juges")["valeur"] == 37.3
    control = dict(date=DATE, lignes={k: len(v) for k, v in collections.items()}, ecarts=len(gaps), controle_ids="sans doublons", residus_remuneration=residuals, residu_Q52_France=25388-(20190+3424+898+874), faits_cles=dict(police_fr2022=245983, nonjuges_fr_pour100000=37.3, enseignants_publics_pp=747404, administration_talis_fr_heures=1.5), avertissements=["Ratio élèves/enseignant ≠ taille de classe", "Non-enseignants et non-juges ≠ administratifs", "NA/NAP/valeur vide jamais convertis en zéro", "Frais de justice en euros courants, pas PPA", "TALIS tous enseignants et temps plein sont deux populations", "Pas de correction chiffrée des besoins ; potentiel non identifié", "Police France 2023 absente du brut ; millésime commun retenu 2022", "Q60 France auxiliaires du parquet seulement : comparaison internationale prudente", "Q52 composantes : écart 2 ETP non imputé"])
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/"04b_controles.json").write_text(json.dumps(control, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    (OUT/"04b_parametres.json").write_text(json.dumps(dict(date=DATE, fichiers=FILES, source_urls=FLOW, profils_cepej=PROFILES, annee_police=2022, annee_ratios=2024, annee_finances=2023, annee_talis=2024, annee_cepej=2022, note="Les CSV de ratios incluent 2020-2024 pour contrôles temporels. Les écarts ont toujours la même année et unité ; aucun lissage ou conversion en postes supprimables."), ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    register()
    print(json.dumps(dict(lignes=control["lignes"], ecarts=len(gaps), residu_Q52=control["residu_Q52_France"]), ensure_ascii=False))


if __name__ == "__main__":
    main()
