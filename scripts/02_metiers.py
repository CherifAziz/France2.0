#!/usr/bin/env python3
"""Nomenclature fonctionnelle et extractions métier, DGAFP/DEPP/DREES.

python -I scripts/02_metiers.py
python -I scripts/02_metiers.py --download  # récupère les XLSX et le PDF DGFiP manquants

Les classes A/B/C sont des affectations analytiques, distinctes des catégories
hiérarchiques. D est un drapeau de revue, jamais un reliquat de postes inutiles.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw/02"
DGAFP = ROOT / "data/raw/01/dgafp_ra2026"
OUT = ROOT / "data/france"
DATE = "2026-10-28"
URL_POSTES = "https://www.fonction-publique.gouv.fr/files/files/publications/vue-rapport-annuel/2026/ra_2026_postes.zip"
URL_EFFECTIFS = "https://www.fonction-publique.gouv.fr/files/files/publications/vue-rapport-annuel/2026/ra_2026_effectifs.zip"
EDU = "https://www.education.gouv.fr/sites/default/files/document/"
DREES = "https://www.drees.solidarites-sante.gouv.fr/sites/default/files/2026-07/"
DGFIP_URL = "https://www.economie.gouv.fr/files/files/directions_services/dgfip/Rapport/2025/ra_2025_cahierstat.pdf"
DGFIP_PDF = ROOT / "data/cache/02/dgfip_cahier_stat2025.pdf"
DGFIP_RESTORE = "python -I scripts/fetch.py '" + DGFIP_URL + "' dgfip_cahier_stat2025 --out-dir data/cache/02"
DOWNLOADS = {
    "depp_ch1_2025_2026": EDU + "chapitre-1-les-personnels-de-l-enseignement-scolaire-520471.xlsx",
    "depp_ch2_2025_2026": EDU + "chapitre-2-les-enseignants-520474.xlsx",
    "depp_ch3_2025_2026": EDU + "chapitre-3-les-personnels-non-enseignants-520477.xlsx",
    "depp_ch4_2025_2026": EDU + "chapitre-4-les-missions-et-lieux-d-exercices-520480.xlsx",
    "depp_ch12_2025_2026": EDU + "chapitre-12-les-accompagnants-d-eleves-en-situation-de-handicap-520495.xlsx",
    "drees_es2026_f05": DREES + "ES%202026%20-%20Fiche%2005%20-%20Les%20postes%20de%20personnel%20m%C3%A9dical%20ou%20pharmaceutique.xlsx",
    "drees_es2026_f06": DREES + "ES%202026%20-%20Fiche%2006%20-%20Les%20postes%20de%20personnel%20non%20m%C3%A9dical%20salari%C3%A9.xlsx",
    "drees_es2026_f07": DREES + "ES%202026%20-%20Fiche%2007%20-%20Les%20%C3%A9volutions%20des%20effectifs%20salari%C3%A9s%20du%20secteur%20hospitalier.xlsx",
}
LOCAL = {
    "fpe": "ra2026_caracteristiques_postes_donnees_comp_FPE.xlsx",
    "fpt": "ra2026_caracteristiques_postes_donnees_comp_FPT.xlsx",
    "fph": "ra2026_caracteristiques_postes_donnees_comp_FPH.xlsx",
    "fp": "ra2026_caracteristiques_postes_donnees_comp_FP.xlsx",
    "ens": "RA_2026_effectifs_donnees_comp_FPE.xlsx",
}


def save_csv(name, rows, folder=OUT):
    folder.mkdir(parents=True, exist_ok=True)
    with (folder / name).open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--download", action="store_true")
    args = parser.parse_args()
    if args.download:
        for name, url in DOWNLOADS.items():
            if not (RAW / f"{name}.xlsx").exists():
                subprocess.run([sys.executable, "-I", str(ROOT / "scripts/fetch.py"), url, name,
                                "--out-dir", str(RAW), "--timeout", "45"], check=True)
        if not DGFIP_PDF.exists():
            subprocess.run([sys.executable, "-I", str(ROOT / "scripts/fetch.py"), DGFIP_URL, "dgfip_cahier_stat2025",
                            "--out-dir", str(DGFIP_PDF.parent), "--timeout", "45"], check=True)
    paths = {key: DGAFP / name for key, name in LOCAL.items()}
    paths.update({key: RAW / f"{key}.xlsx" for key in DOWNLOADS})
    books = {key: load_workbook(path, read_only=True, data_only=True) for key, path in paths.items()}
    records = []

    def add(rid, label, key, sheet, cells, cls, versant, group, scope, *, multiplier=1,
            unit="PP", date="2024-12-31", statut="FAIT", parent="", additive="oui",
            note="", dimension="metier_ou_filiere"):
        if isinstance(cells, str):
            cells = [cells]
        values = [books[key][sheet][cell].value for cell in cells]
        if not all(isinstance(value, (int, float)) for value in values):
            raise ValueError(f"Cellule non numérique : {key} {sheet} {cells} {values}")
        value = sum(values) * multiplier
        if multiplier == 1000 or unit == "PP" or unit == "postes_SAE":
            value = int(round(value))
        url = DOWNLOADS.get(key, URL_EFFECTIFS if key == "ens" else URL_POSTES)
        parents = {"DEPP_ENS_PUBLIC": "DEPP_ENS18", "DEPP_ENS_PRIVE": "DEPP_ENS33",
                   "DEPP_ENS_TOTAL": "DEPP_ENS42", "DEPP_NON_ENS": "DEPP_NE48", "DEPP_VIE_SCOLAIRE": "DEPP_NE24"}
        if parent in parents:
            parent = parents[parent] + "_" + unit
        records.append({"id": rid, "metier_ou_groupe": label, "valeur": value, "unite": unit,
                        "annee": int(date[:4]), "date_observation": date, "versant_ou_secteur": versant,
                        "classe_fonctionnelle_dominante": cls, "statut_classification": "HYPOTHÈSE" if cls != "non_attribuee" else "NON TROUVÉ",
                        "drapeau_D_revue": "non_evalue", "dimension_source": dimension,
                        "groupe_disjonction": group, "additif_dans_groupe": additive, "parent_id": parent,
                        "couverture": scope, "statut": statut, "source_url": url,
                        "source_localisation": f"{paths[key].relative_to(ROOT).as_posix()} / {sheet}!{','.join(cells)}",
                        "note": note})

    # Filières FPT : une partition statistique exhaustive de la FPT, pas des tâches.
    for row in range(28, 40):
        label = books["fpt"]["Figure 1 filiere"][f"B{row}"].value
        cls = {28: "C", 29: "A/B", 30: "A/B", 31: "A/B", 32: "A/B", 33: "A/B",
               34: "A/B", 35: "A/B", 36: "A/B", 37: "B/A", 38: "non_attribuee", 39: "A/B/C"}[row]
        add(f"FPT_F{row}", f"FPT — {label}", "fpt", "Figure 1 filiere", f"S{row}", cls, "FPT",
            "SIASP_FPT_filieres_2024", "Emploi principal au 31/12/2024, tous statuts, France hors Mayotte, hors contrats aidés",
            multiplier=1000, additive="non" if row == 39 else "oui", parent="FPT_F39" if row < 39 else "",
            note="Filière du cadre d'emploi, pas mesure des tâches. La filière technique contient aussi des métiers directement rendus aux habitants.")

    # Filières FPH non médicales ; total médical construit par différence explicite.
    for row in range(25, 32):
        label = books["fph"]["Figure 1 filiere"][f"B{row}"].value
        cls = {25: "C", 26: "A/B", 27: "A/B", 28: "A/B", 29: "B", 30: "non_attribuee", 31: "A/B/C"}[row]
        add(f"FPH_F{row}", f"FPH non médical — {label}", "fph", "Figure 1 filiere", f"T{row}", cls, "FPH",
            "SIASP_FPH_nonmedical_filieres_2024", "Personnels hors médecins et internes, emploi principal au 31/12/2024, France hors Mayotte, hors contrats aidés",
            multiplier=1000, additive="non" if row == 31 else "oui", parent="FPH_F31" if row < 31 else "",
            note="Filière statutaire : un professionnel peut avoir des missions de gestion. Ne pas superposer aux postes SAE.")
    add("FPH_TOTAL", "Total FPH", "fp", "Figure 4 catégorie", "Q41", "A/B/C", "FPH", "SIASP_FPH_2024",
        "Tous statuts, emploi principal au 31/12/2024, France hors Mayotte, hors contrats aidés", multiplier=1000, additive="non")
    total_fph = next(rec["valeur"] for rec in records if rec["id"] == "FPH_TOTAL")
    non_med = next(rec["valeur"] for rec in records if rec["id"] == "FPH_F31")
    med_record = dict(next(rec for rec in records if rec["id"] == "FPH_TOTAL"))
    med_record.update({"id": "FPH_MEDICAUX", "metier_ou_groupe": "FPH médecins et internes (par différence)",
                       "valeur": total_fph - non_med, "classe_fonctionnelle_dominante": "A/B", "statut": "ESTIMATION",
                       "additif_dans_groupe": "oui", "parent_id": "FPH_TOTAL",
                       "source_localisation": "ra2026_caracteristiques_postes_donnees_comp_FP.xlsx / Figure 4 catégorie!Q41 − ra2026_caracteristiques_postes_donnees_comp_FPH.xlsx / Figure 1 filiere!T31",
                       "note": "1248591 − 1103987 ; ce sont des PP Siasp, pas les postes médicaux SAE, qui incluent notamment les sages-femmes selon une autre nomenclature."})
    records.append(med_record)

    # Groupes FPE identifiables : conserver les sous-ensembles plutôt que sommer tous les cadres.
    named = [
        (7, "Encadrement et direction A+", "C", "A+"),
        (8, "Inspection, contrôle et expertise A+", "C/A", "A+"),
        (9, "Enseignement supérieur, recherche et assimilés A+", "A/B/C", "A+"),
        (11, "Attachés et inspecteurs", "C/A", "A"), (12, "Ingénieurs de l'État (hors militaires)", "B/A/C", "A"),
        (13, "Professeurs certifiés et agrégés", "A/B", "A"), (14, "Police : commandants", "A/B/C", "A"),
        (19, "Professeurs des écoles", "A/B", "A"), (20, "Professeurs de lycée professionnel", "A/B", "A"),
        (21, "Police : capitaines et lieutenants", "A/B/C", "A"), (22, "Encadrement pénitentiaire catégorie A", "A/B/C", "A"),
        (25, "Greffiers", "A/C", "B"), (26, "Personnels administratifs et techniques", "B/C", "B"),
        (27, "Encadrement pénitentiaire catégorie B", "A/B/C", "B"), (32, "Police : brigadiers, chefs et majors", "A/B/C", "B"),
        (33, "Police : gardiens de la paix", "A/B/C", "B"), (34, "Surveillance pénitentiaire catégorie B", "A/B", "B"),
        (37, "Adjoints administratifs et techniques", "B/C", "C"), (38, "Surveillance pénitentiaire catégorie C", "A/B", "C"),
    ]
    for row, label, cls, statutory in named:
        add(f"FPE_PCS{row}", label, "fpe", "Figure 2 catégorie", f"B{row}", cls, "FPE",
            "SIASP_FPE_PCS_fonctionnaires_selection_2024", "Fonctionnaires des ministères et EPA, emplois principaux fin 2024, France hors Mayotte, hors contrats aidés",
            multiplier=1000, dimension="PCS_croisee_categorie_hierarchique",
            note=f"Catégorie hiérarchique source : {statutory}. Classification fonctionnelle distincte et mixte. Une ligne de corps ne mesure pas les tâches réelles.")
    add("FPE_MILITAIRES", "Militaires de la FPE, tous ministères et EPA", "fpe", "Figure 1 statut", "G17", "A/B/C", "FPE",
        "SIASP_FPE_statuts_2024", "Tous militaires et militaires volontaires, emploi principal fin 2024, France hors Mayotte, hors contrats aidés",
        multiplier=1000, note="Inclut notamment la gendarmerie. Ne pas ajouter une seconde fois un total de gendarmes.")
    for row in [6, 11]:
        add(f"FPE_MIL_MIN{row}", "Militaires — " + books["fpe"]["Figure 2 statut"][f"A{row}"].value,
            "fpe", "Figure 2 statut", f"D{row}", "A/B/C", "FPE", "SIASP_FPE_militaires_par_ministere_2024",
            "Militaires et volontaires, ministères et EPA de tutelle, emploi principal fin 2024, France hors Mayotte, hors contrats aidés",
            multiplier=1000, parent="FPE_MILITAIRES", note="Sous-ensemble du total militaire ; aucune assimilation de tout le ministère à un métier.")
    add("FPE_ENSEIGNANTS", "Enseignants de la FPE, tous ministères et EPA", "ens", "Figure 2", "P14", "A/B", "FPE",
        "SIASP_FPE_enseignants_2024", "Emplois principaux fin 2024, tous statuts, France hors Mayotte, hors contrats aidés",
        multiplier=1000, note="Inclut élèves enseignants et privé sous contrat ; exclut chercheurs, directeurs d'établissement, inspecteurs, orientation et surveillance. Comprend 19 militaires ; chevauche les enseignants PCS déjà listés.")
    add("FPE_JUSTICE_TOTAL", "Département ministériel Justice, ensemble des métiers", "fpe", "Figure 2 statut", "F12", "A/B/C", "FPE",
        "SIASP_FPE_departements_ministeriels_2024", "Ministère et EPA rattachés, emplois principaux fin 2024, France hors Mayotte, hors contrats aidés",
        multiplier=1000, additive="non", note="Agrégat institutionnel comprenant magistrats, pénitentiaire, greffes, éducatif, technique et administratif ; ne pas le classer intégralement en C ni l'ajouter aux métiers déjà sélectionnés.")

    # DEPP : PP et ETP de même date, mais champs distincts du stock Siasp 2024.
    for row, label, parent in [(6, "Enseignants publics du premier degré", "DEPP_ENS_PUBLIC"),
                               (9, "Enseignants publics du second degré", "DEPP_ENS_PUBLIC"),
                               (18, "Enseignants scolaires publics", "DEPP_ENS_TOTAL"),
                               (21, "Enseignants privés sous contrat du premier degré", "DEPP_ENS_PRIVE"),
                               (24, "Enseignants privés sous contrat du second degré", "DEPP_ENS_PRIVE"),
                               (33, "Enseignants scolaires privés sous contrat", "DEPP_ENS_TOTAL"),
                               (42, "Enseignants scolaires publics et privés sous contrat", "")]:
        for col, unit in [("D", "PP"), ("L", "ETP_au_30_novembre")]:
            add(f"DEPP_ENS{row}_{unit}", label, "depp_ch2_2025_2026", "2.1", f"{col}{row}", "A/B", "Enseignement scolaire",
                f"DEPP_enseignants_2025_{unit}", "Corps enseignants scolaires, rémunérés MEN, France (hors Mayotte pour privé), hors étudiants en préprofessionnalisation",
                unit=unit, date="2025-11-30", parent=parent, additive="oui" if row in [6, 9, 21, 24] else "non",
                note="Approche par corps, pas seulement mission d'enseignement effectif ; hors supérieur et enseignement agricole. Ne pas ajouter à la série Siasp 2024.")
    for row, label, cls, parent in [(6, "Direction d'établissement scolaire", "C/A", "DEPP_NON_ENS"),
                                   (9, "Inspection scolaire", "C", "DEPP_NON_ENS"),
                                   (12, "Encadrement supérieur scolaire", "C", "DEPP_NON_ENS"),
                                   (18, "Personnels d'éducation", "A", "DEPP_VIE_SCOLAIRE"),
                                   (21, "Assistance éducative (AED et AESH)", "A", "DEPP_VIE_SCOLAIRE"),
                                   (24, "Vie scolaire, ensemble", "A/B", "DEPP_NON_ENS"),
                                   (27, "ASS — filière administrative", "C", "DEPP_NON_ENS"),
                                   (30, "ASS — santé et sociale", "A", "DEPP_NON_ENS"),
                                   (33, "ASS — filière technique", "B", "DEPP_NON_ENS"),
                                   (39, "ITRF scolaires", "B/A/C", "DEPP_NON_ENS"),
                                   (48, "Non-enseignants scolaires, ensemble", "A/B/C", "")]:
        for col, unit in [("D", "PP"), ("L", "ETP_au_30_novembre")]:
            add(f"DEPP_NE{row}_{unit}", label, "depp_ch3_2025_2026", "3.1", f"{col}{row}", cls, "Enseignement scolaire public",
                f"DEPP_non_enseignants_2025_{unit}", "Personnels non enseignants rémunérés MEN, France, en activité, hors apprentis",
                unit=unit, date="2025-11-30", parent=parent, additive="non" if row in [24, 48] else "oui",
                note="Les personnels non enseignants comprennent la vie scolaire et la santé : ils ne sont pas tous administratifs.")
    for row, label in [(6, "Conseillers principaux d'éducation"), (9, "Psychologues EN et conseillers d'orientation"),
                       (12, "Personnels d'éducation contractuels"), (18, "AESH"), (21, "AED")]:
        for col, unit in [("D", "PP"), ("M", "ETP_au_30_novembre")]:
            add(f"DEPP_VIE{row}_{unit}", label, "depp_ch3_2025_2026", "3.10", f"{col}{row}", "A", "Enseignement scolaire public",
                f"DEPP_vie_scolaire_detail_2025_{unit}", "Corps de vie scolaire, rémunérés MEN, France, en activité, hors apprentis",
                unit=unit, date="2025-11-30", parent="DEPP_NE24_" + unit,
                note="Sous-ensemble de la vie scolaire ; ne pas ajouter à ses agrégats ni au total des non-enseignants.")
    for col, unit in [("C", "PP"), ("K", "ETP_au_30_novembre")]:
        add("DEPP_AESH_CONTROLE_" + unit, "AESH — contrôle chapitre 12", "depp_ch12_2025_2026", "12.1", f"{col}15", "A", "Enseignement scolaire public",
            f"DEPP_controle_AESH_2025_{unit}", "Corps AESH, rémunérés MEN, France, en activité", unit=unit, date="2025-11-30",
            additive="non", parent="DEPP_VIE18_" + unit, note="Même population que le chapitre 3 ; contrôle et non personnel supplémentaire.")

    # Répartition des missions : pourcentages, pas effectifs supplémentaires ni parts de temps.
    for sheet, col, leaf_rows in [("4.1", "D", [5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16]),
                                  ("4.7", "G", [5, 6, 7, 8, 9, 10])]:
        for row in leaf_rows:
            label = books["depp_ch4_2025_2026"][sheet][f"A{row}"].value
            add(f"DEPP_MISSION_{sheet}_{row}", label, "depp_ch4_2025_2026", sheet, f"{col}{row}", "non_attribuee",
                "Enseignement scolaire public", f"DEPP_missions_{sheet}_2025", "Corps enseignants publics du degré correspondant, au 30 novembre 2025",
                unit="pourcent_de_personnes", date="2025-11-30", dimension="mission_principale",
                note="Part d'agents selon la mission ; pas pourcentage du temps de travail. Direction et enseignement peuvent être exercés simultanément.")

    # DREES SAE : postes de travail non dédupliqués et géographie propre, séparés des PP.
    for col, sector in [("C", "Public"), ("D", "Prive_non_lucratif"), ("E", "Prive_lucratif"), ("F", "Ensemble")]:
        for row in range(5, 18):
            label = books["drees_es2026_f06"]["ES2026_Fiche 6_Tableau1"][f"B{row}"].value
            cls = "C" if row == 13 else "B" if row == 16 else "A/B" if row in range(5, 12) or row in [14, 15] else "A/B/C"
            add(f"SAE_NM_{sector}_{row}", label, "drees_es2026_f06", "ES2026_Fiche 6_Tableau1", f"{col}{row}", cls,
                "Hospitalier_" + sector, "SAE_nonmedical_2024_" + sector,
                "Postes des seuls services sanitaires, France avec Saint-Martin/Saint-Barthélemy et SSA ; hors médico-social, formation et prestataires",
                unit="postes_SAE", parent="" if row == 17 else f"SAE_NM_{sector}_5" if row in range(6, 12) else f"SAE_NM_{sector}_12" if row in range(13, 17) else f"SAE_NM_{sector}_17", additive="non" if row in [5, 12, 17] or sector == "Ensemble" else "oui",
                note="Postes, non personnes physiques dédupliquées ; profession/grade de recrutement, pas tâches effectivement réalisées. Agrégats soignants/non-soignants ne s'ajoutent pas à leurs sous-ensembles.")
        for row in [5, 6, 7, 8, 9, 13, 14, 15, 16]:
            label = books["drees_es2026_f05"]["ES2026_Fiche 5_Tableau1"][f"B{row}"].value
            add(f"SAE_MED_{sector}_{row}", label, "drees_es2026_f05", "ES2026_Fiche 5_Tableau1", f"{col}{row}", "A/B",
                "Hospitalier_" + sector, "SAE_medical_2024_" + sector,
                "Postes de médecins, odontologistes, pharmaciens, internes/juniors/FFI et sages-femmes ; France avec Saint-Martin/Saint-Barthélemy et SSA",
                unit="postes_SAE", parent="" if row == 16 else f"SAE_MED_{sector}_5" if row in [6, 7] else f"SAE_MED_{sector}_8" if row in [9, 13, 14] else f"SAE_MED_{sector}_16", additive="non" if row in [5, 8, 16] or sector == "Ensemble" else "oui",
                note="Sages-femmes classées médicales dans SAE ; ne pas les ajouter de nouveau à la filière soignante Siasp. Salariés/libéraux et étudiants distinguent ce champ du total FPH.")
    for row in range(5, 14):
        label = books["drees_es2026_f06"]["ES2026_Fiche 6_Tableau2"][f"B{row}"].value
        add(f"SAE_ETP_DISC{row}", label, "drees_es2026_f06", "ES2026_Fiche 6_Tableau2", f"C{row}", "non_attribuee", "Hospitalier_tous_secteurs",
            "SAE_disciplines_ETP_2024", "Personnels non médicaux, tous secteurs juridiques, France avec Saint-Martin/Saint-Barthélemy et SSA",
            unit="ETP_moyen_annuel_remunere", dimension="discipline_ou_section", additive="non" if row in [6, 12, 13] else "oui",
            note="Section Administration : imputation d'ETP par discipline, distincte de la profession personnel administratif. Pas une classe C directement mesurée.")
    for row in range(4, 16):
        label = books["drees_es2026_f07"]["ES205_F07_Tableau1"][f"B{row}"].value
        add(f"DREES_PP_PUBLIC{row}", label, "drees_es2026_f07", "ES205_F07_Tableau1", f"H{row}", "C" if row == 14 else "A/B/C",
            "Hospitalier_public", "DREES_hospitalier_public_PP_2024",
            "Salariés hospitaliers au 31/12, France hors Saint-Martin/Saint-Barthélemy avec SSA, y compris Mayotte/contrats aidés, hors stagiaires/externes/apprentis",
            additive="non" if row in [4, 5, 9, 13] else "oui",
            note="Séries Siasp/BTS complétées SAE ; champ sanitaire distinct de la FPH complète. Ne pas additionner aux postes SAE.")

    # Données documentaires de la DGFiP : extraction de deux totaux PDF avec contrôle des colonnes.
    dgfip_path = DGFIP_PDF
    if dgfip_path.exists():
        from pypdf import PdfReader
        reader = PdfReader(dgfip_path)
        for page_index, rid, label in [(45, "DGFIP_TITULAIRES2025", "DGFiP, effectifs hors non-titulaires, ouvriers du cadastre inclus"),
                                       (46, "DGFIP_CONTRACTUELS2025", "DGFiP, effectifs contractuels et assimilés du tableau")]:
            lines = reader.pages[page_index].extract_text(extraction_mode="layout").splitlines()
            line = next(line for line in lines if line.strip().startswith("TOTAL "))
            numbers = [int(x.replace("\u00a0", "").replace(" ", "")) for x in re.findall(r"\d{1,3}(?:[\u00a0 ]\d{3})*", line)]
            assert len(numbers) == 4 and sum(numbers[:3]) == numbers[3], "Structure du tableau DGFiP modifiée"
            rec = dict(records[0])
            rec.update({"id": rid, "metier_ou_groupe": label, "valeur": numbers[-1], "unite": "PP",
                        "annee": 2025, "date_observation": "2025-12-31", "versant_ou_secteur": "DGFiP",
                        "classe_fonctionnelle_dominante": "A/B/C", "dimension_source": "institution_et_statut",
                        "groupe_disjonction": "DGFiP_effectifs_en_fonction_2025", "parent_id": "", "additif_dans_groupe": "oui",
                        "couverture": "Effectifs en fonction à la DGFiP ; périmètre des notes du tableau",
                        "source_url": DGFIP_URL,
                        "source_localisation": f"Cahier statistiques 2025 DGFiP, page PDF {page_index + 1}, ligne TOTAL par catégorie A/B/C",
                        "note": "Rupture avec 2024 : agents en fonction au lieu de payés. Le tableau contractuels comprend notamment apprentis, volontaires du service civique et payés à la tâche ; pas un nouveau vivier à ajouter au total FPE. Recouvrement, contrôle, informatique et fonctions support ne sont pas tous des tâches C supprimables."})
            records.append(rec)

    # Panier homogène en date/unité/champ : pas une mesure de tâches de terrain.
    def value(rid):
        return next(rec["valeur"] for rec in records if rec["id"] == rid)
    ids = [rec["id"] for rec in records]
    assert len(ids) == len(set(ids)), "Identifiant métier dupliqué"
    assert all(not rec["parent_id"] or rec["parent_id"] in ids for rec in records), "Parent métier absent"
    assert all(rec["parent_id"] != rec["id"] for rec in records), "Un groupe ne peut pas être son propre parent"
    military_teachers = int(round((books["fpe"]["Figure 2 statut"]["D18"].value - books["fpe"]["Figure 2 statut"]["D19"].value) * 1000))
    basket = [
        ("Enseignants FPE", value("FPE_ENSEIGNANTS"), "FPE_ENSEIGNANTS", "Champ enseignant Siasp incluant le privé sous contrat et les élèves enseignants"),
        ("Militaires FPE", value("FPE_MILITAIRES"), "FPE_MILITAIRES", "Gendarmerie incluse, tous ministères et EPA"),
        ("Police : quatre groupes de corps identifiés", sum(value(f"FPE_PCS{x}") for x in [14, 21, 32, 33]), "FPE_PCS14;FPE_PCS21;FPE_PCS32;FPE_PCS33", "Sélection incomplète ; ne comprend pas tous les agents de la police nationale"),
        ("Filière soignante FPH non médicale", value("FPH_F28"), "FPH_F28", "Classement de filière, pas relevé de tâches"),
        ("Médecins et internes FPH", value("FPH_MEDICAUX"), "FPH_MEDICAUX", "Différence entre total FPH et personnels non médicaux"),
        ("Greffiers fonctionnaires FPE", value("FPE_PCS25"), "FPE_PCS25", "Hors greffiers privés de tribunaux de commerce"),
        ("Surveillance pénitentiaire B et C", value("FPE_PCS34") + value("FPE_PCS38"), "FPE_PCS34;FPE_PCS38", "Somme B/C pour neutraliser le reclassement"),
        ("Encadrement pénitentiaire A et B", value("FPE_PCS22") + value("FPE_PCS27"), "FPE_PCS22;FPE_PCS27", "Somme A/B pour neutraliser le reclassement"),
        ("Filière incendie-secours FPT", value("FPT_F31"), "FPT_F31", "Filière, distincte des pompiers militaires déjà militaires FPE ; pas volontaires"),
        ("Déduction enseignants militaires", -military_teachers, "FPE_ENSEIGNANTS;FPE_MILITAIRES", "Intersections statuts/enseignants : D18-D19, figure 2 statut FPE"),
    ]
    basket_rows = [{"composante": label, "valeur_pp": val, "annee": 2024, "date_observation": "2024-12-31",
                    "source_ids": ids, "statut": "ESTIMATION", "source_url": URL_POSTES + " ; " + URL_EFFECTIFS,
                    "source_localisation": "Références détaillées des identifiants dans 02_metiers.csv",
                    "note": note + " ; panier de groupes à dominante opérationnelle, pas effectif strict de tâches de terrain ni catégorie A intégrale."}
                   for label, val, ids, note in basket]
    save_csv("02_panier_siasp_2024.csv", basket_rows)
    save_csv("02_metiers.csv", records)
    coverage = [
        ("Enseignants", "FPE_ENSEIGNANTS;DEPP_ENS18_PP;DEPP_ENS33_PP", "FAIT", "Corps/profession et dates disponibles ; pas une mesure de tout le temps effectivement devant élèves."),
        ("AESH et AED", "DEPP_VIE18_PP;DEPP_VIE21_PP", "FAIT", "PP et ETP de novembre 2025 ; inclus dans vie scolaire, pas à ajouter à Siasp 2024."),
        ("Médecins et internes", "FPH_MEDICAUX;SAE_MED_Public_5;SAE_MED_Public_8", "ESTIMATION", "FPH par différence en PP ; SAE par postes, champs distincts."),
        ("Infirmiers et aides-soignants", "SAE_NM_Public_7;SAE_NM_Public_8;DREES_PP_PUBLIC10;DREES_PP_PUBLIC11", "FAIT", "Deux unités/sources conservées séparées : postes SAE et PP salariés hospitaliers."),
        ("Police", "FPE_PCS14;FPE_PCS21;FPE_PCS32;FPE_PCS33", "FAIT", "Quatre corps de fonctionnaires seulement ; pas tout le personnel ni une mesure des seuls policiers opérationnels."),
        ("Gendarmerie", "FPE_MILITAIRES;FPE_MIL_MIN11", "NON TROUVÉ", "Incluse dans militaires FPE ; militaires Intérieur est un proxy institutionnel, pas un décompte vérifié des seules tâches de gendarmerie."),
        ("Armées", "FPE_MIL_MIN6;FPE_MILITAIRES", "FAIT", "Militaires par ministère de tutelle, pas tous les agents du ministère ni uniquement les combattants."),
        ("Pompiers", "FPT_F31", "FAIT", "Filière incendie-secours FPT ; exclut les volontaires et ne doit pas doubler les militaires FPE."),
        ("Magistrats", "", "NON TROUVÉ", "Pas de décompte comparable isolé des magistrats fin 2024 dans les tables lues ; A+ est une liste de codes, pas un effectif."),
        ("Greffiers", "FPE_PCS25", "FAIT", "Fonctionnaires FPE ; greffes privés des tribunaux de commerce exclus."),
        ("Pénitentiaire", "FPE_PCS22;FPE_PCS27;FPE_PCS34;FPE_PCS38", "FAIT", "Encadrement et surveillance sélectionnés, pas totalité de l'administration pénitentiaire."),
        ("Travail social", "FPT_F35;FPT_F32;FPH_F27", "FAIT", "Filières et secteurs distincts ; catégories comportant des tâches mixtes, champ national exhaustif non reconstruit."),
        ("Technique territorial", "FPT_F37", "FAIT", "Filière technique de la FPT, sans ventilation métier/tâches interne."),
        ("DGFiP", "DGFIP_TITULAIRES2025;DGFIP_CONTRACTUELS2025", "FAIT" if dgfip_path.exists() else "NON TROUVÉ", "PP en fonction 2025 si PDF présent ; métiers internes et définition contractuels à conserver, pas un bloc de tâches supprimables."),
        ("Douane", "", "NON TROUVÉ", "Ventilation récente surveillance/opérations commerciales/soutiens non obtenue dans les documents lus."),
    ]
    coverage_rows = []
    for family, ids_, status, note in coverage:
        source_urls = sorted({rec["source_url"] for rec in records if rec["id"] in ids_.split(";")})
        if not source_urls:
            source_urls = ["https://www.justice.gouv.fr/documentation/etudes-statistiques" if family == "Magistrats"
                           else "https://www.economie.gouv.fr/dgfip/rapports/les-rapports-dactivite-de-la-dgfip" if family == "DGFiP"
                           else "https://www.douane.gouv.fr/"]
        coverage_rows.append({"famille": family, "reference_ids": ids_, "annee": "selon_reference", "statut": status,
                              "source_url": " ; ".join(source_urls), "source_localisation": "02_metiers.csv et recherche/02_metiers_classification.md, limites",
                              "couverture_et_limite": note})
    save_csv("02_couverture_metiers.csv", coverage_rows)

    # Les revendications rapportées restent dans un fichier séparé des statistiques.
    claims = [("Enseignants, tous niveaux selon la recension", 870000), ("Militaires selon la recension", 270000),
              ("Policiers et gendarmes selon la recension", 250000), ("Pompiers professionnels selon la recension", 42000),
              ("Magistrats selon la recension", 9000), ("Soignants hospitaliers selon la recension", 750000)]
    save_csv("02_positions_2_2m.csv", [{"groupe": label, "valeur_revendiquee": val, "unite_revendiquee": "agents_non_harmonises",
              "annee": "non_precisee", "statut": "HYPOTHÈSE", "nature": "Chiffre politique rapporté, non statistique validée",
              "source_url": "https://metainfos.com/2026/10/24/la-politique-de-rupture-de-sarah-knafo/",
              "source_localisation": "Rubrique Des fonctionnaires trop nombreux, recension attribuée à Johan Hardoy / Polémia",
              "note": "Article secondaire lu intégralement ; livre non lu, page originale non connue ; non utilisé pour calibrer un vivier."} for label, val in claims])

    # Contrôles de fond, y compris les chevauchements qui invalident des sommes naïves.
    assert sum(value(f"FPT_F{x}") for x in range(28, 39)) == value("FPT_F39")
    assert sum(value(f"FPH_F{x}") for x in range(25, 31)) == value("FPH_F31")
    assert value("DEPP_ENS18_PP") + value("DEPP_ENS33_PP") == value("DEPP_ENS42_PP")
    assert value("DEPP_ENS18_ETP_au_30_novembre") + value("DEPP_ENS33_ETP_au_30_novembre") == value("DEPP_ENS42_ETP_au_30_novembre")
    assert value("DEPP_VIE18_PP") == value("DEPP_AESH_CONTROLE_PP")
    assert value("DEPP_VIE18_ETP_au_30_novembre") == value("DEPP_AESH_CONTROLE_ETP_au_30_novembre")
    assert value("DEPP_VIE18_PP") + value("DEPP_VIE21_PP") == value("DEPP_NE21_PP")
    assert sum(value(f"DEPP_NE{x}_PP") for x in [6, 9, 12, 18, 21, 27, 30, 33, 39]) == value("DEPP_NE48_PP")
    assert sum(value(f"SAE_NM_Public_{x}") for x in range(6, 12)) == value("SAE_NM_Public_5")
    assert sum(value(f"SAE_NM_Public_{x}") for x in range(13, 17)) == value("SAE_NM_Public_12")
    assert value("SAE_NM_Public_5") + value("SAE_NM_Public_12") == value("SAE_NM_Public_17")
    controls = {"date": DATE, "nombre_lignes_metiers": len(records), "enseignants_siasp_2024_pp": value("FPE_ENSEIGNANTS"),
                "source_DGFiP": {"pdf_disponible": dgfip_path.exists(),
                                 "lignes_DGFiP_produites": sum(rec["id"].startswith("DGFIP_") for rec in records),
                                 "statut": "FAIT" if dgfip_path.exists() else "NON TROUVÉ",
                                 "commande_restaurer": DGFIP_RESTORE,
                                 "autre_commande": "python -I scripts/02_metiers.py --download",
                                 "note": "Le PDF est restauré automatiquement avec --download. Sans le PDF et sans cette option, deux lignes DGFiP sont omises et cette absence est explicitement signalée ici."},
                "militaires_enseignants_intersection_pp": military_teachers, "panier_professions_siasp_2024_pp": sum(v for _, v, _, _ in basket),
                "panier_terrain_strict_etabli": False, "part_admin_FPT": value("FPT_F28") / value("FPT_F39"),
                "part_admin_FPH_total": value("FPH_F25") / total_fph,
                "part_admin_FPH_nonmedical": value("FPH_F25") / non_med,
                "part_admin_SAE_public_nonmedical": value("SAE_NM_Public_13") / value("SAE_NM_Public_17"),
                "part_nonsoignants_SAE_public_nonmedical": value("SAE_NM_Public_12") / value("SAE_NM_Public_17"),
                "part_assistance_educative_dans_nonenseignants": value("DEPP_NE21_PP") / value("DEPP_NE48_PP"),
                "part_vie_scolaire_dans_nonenseignants": value("DEPP_NE24_PP") / value("DEPP_NE48_PP"),
                "part_administrative_dans_nonenseignants": value("DEPP_NE27_PP") / value("DEPP_NE48_PP"),
                "somme_chiffres_revendiques_recension": sum(v for _, v in claims),
                "conclusion_controles": "Partitions des filières, DEPP PP/ETP, doubles comptes AED/AESH et SAE soignant/non-soignant vérifiés. Aucune partition exhaustive des tâches A/B/C/D nationale n'est construite."}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "02_controles.json").write_text(json.dumps(controls, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    registry = []
    for key, path in paths.items():
        registry.append({"id": "02_" + key.upper(), "titre": path.name, "institution": "DEPP" if key.startswith("depp") else "DREES" if key.startswith("drees") else "DGAFP-SDessi / Insee-Siasp",
                         "date_publication": "2026" if key.startswith("depp") else "2026-07" if key.startswith("drees") else "2026-10-15",
                         "url": DOWNLOADS.get(key, URL_EFFECTIFS if key == "ens" else URL_POSTES),
                         "date_consultation": DATE, "acces": "integral", "sha256_16": hashlib.sha256(path.read_bytes()).hexdigest()[:16],
                         "notes": "Empreinte du XLSX. DEPP : fiche datée 15/04/2026, fichiers modifiés 15/09/2026, observations novembre 2025. DREES : panorama paru 20/05/2026, fiches complètes juillet 2026. Métadonnées HTTP conservées à côté des téléchargements."})
    for stem, pubdate, institution, comment in [
        ("dgfip_cahier_stat2025", "2026-05-06", "DGFiP", "PP en fonction, rupture de champ 2024/2025 ; PDF pp. 46-47."),
        ("drees_es2026_f06", "2026-07", "DREES", "PDF pp. 56-59 ; distinction postes, PP, ETP et classification profession/service."),
        ("knafo_sudradio_20260914", "2026-09-14", "Sud Radio", "Article éditorial sur le livre ; source secondaire, pas entretien intégral ni statistique primaire."),
        ("knafo_recension_20261024", "2026-10-24", "Metainfos / recension Johan Hardoy, source Polémia", "Position rapportée ; aucune validation statistique indépendante du chiffrage politique."),
        ("police_feminisation_20260306", "2026-03-06", "Police nationale", "Page primaire lue avec outil web ; récupération requests HTTP403. Année d'observation du total non précisée, non utilisée dans le panier."),
        ("depp_enc2026", "2026-08-25", "DEPP", "Page primaire lue avec outil web ; récupération requests HTTP403. Approche par mission distincte des corps, non utilisée dans le panier."),
    ]:
        meta_path = ROOT / "data/cache/02" / f"{stem}.meta.json"
        if meta_path.exists():
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            registry.append({"id": "02_" + stem.upper(), "titre": stem, "institution": institution,
                             "date_publication": pubdate, "url": meta["source_url"], "date_consultation": DATE,
                             "acces": "partiel" if meta["acces"] == "inaccessible" else "integral",
                             "sha256_16": meta["sha256"][:16] if meta["acces"] != "inaccessible" else "",
                             "notes": comment + " Les réponses HTTP403 ne sont pas présentées comme le document primaire archivé."})
    for rid, title, institution, pubdate, url, note in [
        ("02_DREES_PROV2025", "Premiers résultats sur les établissements de santé en 2025, ER 1380", "DREES", "2026-07-28",
         "https://drees.solidarites-sante.gouv.fr/publications-communique-de-presse/etudes-et-resultats/260728-deficit-des-hopitaux-publics",
         "Page primaire lue par outil web ; première estimation 2025, sans ventilation métier finale utilisée ici. Pas d'empreinte locale de contenu revendiquée."),
        ("02_JUSTICE_CC2025", "Les chiffres clés de la Justice, édition 2025", "Ministère de la Justice / SSER", "2025-10-28",
         "https://www.justice.gouv.fr/sites/default/files/2025-12/Chiffres%20Cles%202025.pdf",
         "PDF primaire consulté par outil web, parties moyens/intervenants ; pages PDF 6-11. Date de publication de la fiche de collection 28/10/2025 ; fichier à cette URL version décembre 2025. Pas d'empreinte locale revendiquée ni chiffre PP magistrats imputé.")]:
        registry.append({"id": rid, "titre": title, "institution": institution, "date_publication": pubdate,
                         "url": url, "date_consultation": DATE, "acces": "partiel", "sha256_16": "", "notes": note})
    save_csv("registre_02.csv", registry, ROOT / "sources")
    for book in books.values():
        book.close()
    print(json.dumps(controls, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
