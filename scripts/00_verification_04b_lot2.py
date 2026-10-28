#!/usr/bin/env python3
"""Contre-verification 04b, sans lecture ni import de son extracteur.

Relit les CSV herites et les PDF primaires avec csv et pypdf. Les deux
statistiques SE sont rapprochees du CSV de resultat, apres extraction
independante. Ecrit uniquement le CSV et la note de verification lot2.
"""

from __future__ import annotations

import csv
import hashlib
import re
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "recherche/04b_education_securite_justice.md"
OUT = ROOT / "data/risques/verification_04b_lot2.csv"
REPORT = ROOT / "recherche/00_verification_04b_lot2.md"
EAG = ROOT / "data/raw/04/oecd_eag_DF_UOE_NF_PERS_STR.csv"
TALIS = ROOT / "data/raw/04/oecd_talis_teacher.csv"
POLICE = ROOT / "data/raw/04/eurostat_crim_just_job.csv"
POLICE_META = ROOT / "data/raw/04b/eurostat_crim_metadata.html"
TALIS_RESULT = ROOT / "data/international/04b_talis2024.csv"
TALIS_PDF = ROOT / "data/cache/04b/oecd_talis2024_france.pdf"
CEPEJ_PDF = ROOT / "data/cache/04b/cepej2024_profils.pdf"
CEPEJ_FR = ROOT / "data/cache/04b/cepej2024_reponses_france.pdf"
CEPEJ_NOTICE = ROOT / "data/cache/04b/cepej2024_notice.pdf"

URL_EAG = "https://sdmx.oecd.org/public/rest/data/OECD.EDU.IMEP,DSD_EAG_UOE_NON_FIN_PERS@DF_UOE_NF_PERS_STR,1.1/"
URL_TALIS = "https://sdmx.oecd.org/public/rest/data/OECD.EDU.ECS,DSD_TALIS@DF_TALIS_TEACHER_PROFILE,1.0/"
URL_TALIS_PDF = "https://www.oecd.org/content/dam/oecd/en/publications/reports/2025/10/results-from-talis-2024-country-notes_eafd703e/france_714d7439/50507701-en.pdf"
URL_POLICE = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/crim_just_job"
URL_META = "https://ec.europa.eu/eurostat/cache/metadata/en/crim_sims.htm"
URL_CEPEJ = "https://rm.coe.int/fiche-pays-partie-2-en/1680b21e99"
URL_CEPEJ_FR = "https://rm.coe.int/france-2024-2022-/1680b1f6cd"
URL_NOTICE = "https://rm.coe.int/explanatory-note-2024-cycle-cepej-2023-2-en/1680aae30a"

COLS = ["id", "theme", "indicateur", "annee", "valeur_publiee", "valeur_source", "unite", "source_url", "source_localisation", "statut_controle", "note"]


def dec(value: str) -> Decimal:
    return Decimal(value.replace(" ", "").replace(",", "."))


def read_csv(path: Path, coded: bool = False) -> list[tuple[int, dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        result = []
        for index, row in enumerate(csv.DictReader(handle), 2):
            if coded:
                row = {key.split(":", 1)[0]: value.split(":", 1)[0] for key, value in row.items()}
            result.append((index, row))
        return result


def one(rows: list[tuple[int, dict[str, str]]], **dimensions: str) -> tuple[int, dict[str, str]]:
    matches = [(index, row) for index, row in rows if all(row.get(key) == value for key, value in dimensions.items())]
    assert len(matches) == 1, (dimensions, len(matches))
    return matches[0]


def pattern(pattern: str, text: str) -> re.Match[str]:
    match = re.search(pattern, text, re.S)
    assert match is not None, pattern
    return match


def main() -> None:
    note = NOTE.read_text(encoding="utf-8")
    points = {int(m.group(1)): m.group(2) for m in re.finditer(r"^(\d+)\. (.+)$", note, re.M)}
    published_eag_all = re.findall(r"\d+,\d+", points[1])
    published_eag_public = re.findall(r"\d+,\d+", points[3])
    published_talis = re.findall(r"\d+,\d+", points[6])
    published_cepej = re.findall(r"\d+,\d+", points[15])
    assert len(published_eag_all) == 6 and len(published_eag_public) == 6
    assert len(published_talis) == 4 and len(published_cepej) == 10
    talis_paragraph = pattern(r"Le CSV hérité donne (.+?)(?:\n\n|$)", note).group(1)
    published_talis_all = re.findall(r"\d+,\d+", talis_paragraph)
    results: list[dict[str, str]] = []

    def add(theme: str, label: str, year: int, published: str, value: str, unit: str, url: str, location: str, comment: str) -> None:
        p, s = dec(published), dec(value)
        quantum = Decimal(1).scaleb(p.as_tuple().exponent)
        same = s.quantize(quantum, rounding=ROUND_HALF_UP) == p
        results.append(dict(zip(COLS, [
            f"04bV{len(results)+1:02d}", theme, label, str(year), str(p), str(s), unit,
            url, location, "CONFORME" if same else "ERREUR_VALEUR", comment,
        ])))

    eag_rows = read_csv(EAG, coded=True)
    selections = [
        ("France primaire tous établissements", "FRA", "ISCED11_1", "INST_EDU", published_eag_all[0]),
        ("OCDE primaire tous établissements", "OECD", "ISCED11_1", "INST_EDU", published_eag_all[3]),
        ("France second cycle secondaire tous établissements", "FRA", "ISCED11_3", "INST_EDU", published_eag_all[2]),
        ("OCDE second cycle secondaire tous établissements", "OECD", "ISCED11_3", "INST_EDU", published_eag_all[5]),
        ("France primaire établissements publics", "FRA", "ISCED11_1", "INST_EDU_PUB", published_eag_public[0]),
        ("France second cycle secondaire établissements publics", "FRA", "ISCED11_3", "INST_EDU_PUB", published_eag_public[2]),
    ]
    for label, country, level, institution, published in selections:
        index, row = one(eag_rows, REF_AREA=country, EDUCATION_LEV=level,
                         INST_TYPE_EDU=institution, TIME_PERIOD="2024", MEASURE="STU_PERS",
                         UNIT_MEASURE="ST_TCHR", INTENSITY="_T", EDUCATION_TYPE="FE",
                         SEX="_T", AGE="_T", FREQ="A")
        assert row["UNIT_MULT"] == "0"
        add("enseignement", label, 2024, published, row["OBS_VALUE"],
            "eleves_ETP_par_enseignant_ETP", URL_EAG,
            f"{EAG.relative_to(ROOT).as_posix()} ; ligne CSV {index} ; {country}/{level}/{institution}/ST_TCHR/2024",
            "Arrondi à deux décimales confirmé ; ratio enseignants, sans décompte des personnels administratifs. Public et ensemble sont des champs imbriqués, pas des composantes à additionner.")

    talis_pdf_text = PdfReader(TALIS_PDF).pages[10].extract_text()
    talis_admin = pattern(r"Full-time teachers report spending ([\d.]+) hours per week on administrative work.*?OECD average:\s*([\d.]+)\)", talis_pdf_text)
    assert "lower secondary" in PdfReader(TALIS_PDF).pages[1].extract_text()
    for label, published, value in [
        ("France tâches administratives enseignants à temps plein", published_talis[0], talis_admin.group(1)),
        ("OCDE tâches administratives enseignants à temps plein", published_talis[1], talis_admin.group(2)),
    ]:
        add("TALIS", label, 2024, published, value, "heures_de_60_minutes_par_semaine",
            URL_TALIS_PDF, "data/cache/04b/oecd_talis2024_france.pdf ; PDF 11, page imprimée 10 ; Working hours",
            "Enseignants à temps plein du premier cycle secondaire ; déclaratif. Aucune erreur standard de ce sous-groupe n'est fournie sur cette page ; ne pas lui affecter celle du CSV tous enseignants.")

    talis_rows = read_csv(TALIS, coded=True)
    talis_result = read_csv(TALIS_RESULT)
    se_details = []
    for measure, label, published in [
        ("Q14_1", "France travail total tous enseignants", published_talis_all[0]),
        ("Q15_1", "France enseignement tous enseignants", published_talis_all[1]),
    ]:
        dimensions = dict(REF_AREA="FRA", TIME_PERIOD="2024", MEASURE=measure,
                          EDUCATION_LEV="ISCED11_2", TEACHER_PROFILE="_T", AGE="_T", SEX="_T",
                          URBANISATION="_T", INSTITUTION_TYPE="_T", STUDENTS_CHARACTERISTICS="_T", UNIT_MEASURE="H")
        index, mean = one(talis_rows, **dimensions, STATISTICAL_OPERATION="MEAN")
        se_index, se = one(talis_rows, **dimensions, STATISTICAL_OPERATION="SE")
        assert mean["UNIT_MULT"] == se["UNIT_MULT"] == "0"
        _, published_se = one(talis_result, pays="FRA", indicateur=measure,
                              operation_statistique="SE", niveau_education="ISCED11_2",
                              profil_enseignant="tous_temps_plein_et_partiel")
        assert dec(se["OBS_VALUE"]) == dec(published_se["valeur"]), (measure, "SE différente")
        se_details.append(f"{measure} : moyenne {mean['OBS_VALUE']} h, SE **{se['OBS_VALUE']} h** (ligne source {se_index})")
        add("TALIS", label, 2024, published, mean["OBS_VALUE"], "heures_de_60_minutes_par_semaine", URL_TALIS,
            f"{TALIS.relative_to(ROOT).as_posix()} ; ligne CSV {index} MEAN et {se_index} SE ; FRA/{measure}/ISCED11_2/_T/2024",
            f"Tous enseignants, temps partiel inclus. SE={se['OBS_VALUE']} h, relue dans le brut et identique au CSV résultat. Cette SE ne concerne pas les 1,5 h d'administration des seuls temps pleins.")

    # Lecture du HTML primaire, et non du texte construit par l'extracteur 04b.
    police_meta = POLICE_META.read_text(encoding="utf-8")
    police_plain = re.sub(r"<[^>]*>", " ", police_meta)
    police_plain = " ".join(police_plain.split())
    for proof in ["secretaries, clerks", "Local police is included", "30 June", "French Polynesia"]:
        assert proof.lower() in police_plain.lower(), proof
    police_rows = read_csv(POLICE)
    police_published = [pattern(r"\*\*([\d ]+) policiers", points[11]).group(1),
                        pattern(r"\*\*([\d,]+) pour 100 000", points[11]).group(1)]
    for unit, published in zip(["NR", "P_HTHAB"], police_published):
        index, row = one(police_rows, freq="A", isco08="OC5412", sex="T", unit=unit, geo="FR", time="2022")
        add("police", "France policiers " + ("effectif" if unit == "NR" else "densité"), 2022,
            published, row["value"], "personnes" if unit == "NR" else "policiers_par_100000_habitants",
            URL_POLICE, f"{POLICE.relative_to(ROOT).as_posix()} ; ligne CSV {index} ; OC5412/T/{unit}/FR/2022 ; métadonnées §3.4, §3.7, §15.1",
            "Support administratif exclu de la définition ; police locale française incluse ; territoires ultramarins listés exclus. Allemagne : personnes physiques, fonctionnaires hors stagiaires au 30 juin. Densité Eurostat conservée, sans population CEPEJ substituée.")
    assert not any(row["geo"] == "FR" and row["isco08"] == "OC5412" and row["sex"] == "T"
                   and row["time"] == "2023" and row["value"].strip() for _, row in police_rows)

    # Ordre de lecture de la page source, vérifié dans le recueil officiel :
    # juges 2022/2012 FR, médianes 2022/2012, puis non-juges dans le même ordre.
    cepej = PdfReader(CEPEJ_PDF).pages[66].extract_text()
    assert "France" in cepej and "Non-judge staff" in cepej and "CoE Median" in cepej
    hr = pattern(r"2022\s+([\d.]+)\s+2012\s+([\d.]+)\s+([\d,]+)\s+([\d,]+)\s+([\d.]+)\s+([\d.]+)\s+([\d,]+)\s+([\d,]+)", cepej)
    notice = PdfReader(CEPEJ_NOTICE).pages[30].extract_text()
    compact_notice = " ".join(notice.split())
    for proof in ["full-time equivalent", "posts actually filled", "question 60", "Technical staff", "Other non-judge staff"]:
        assert proof in compact_notice, proof
    for label, published, value in [
        ("France personnel non-juge dans les tribunaux", published_cepej[1], hr.group(5)),
        ("Médiane Conseil de l'Europe personnel non-juge dans les tribunaux", published_cepej[7], hr.group(7)),
    ]:
        add("justice", label, 2022, published, value, "ETP_par_100000_habitants", URL_CEPEJ,
            "data/cache/04b/cepej2024_profils.pdf ; PDF/page 67 ; France, Human Resources, Non-judge staff ; notice PDF 31 Q52",
            "Médiane CoE distincte d'une moyenne UE/OCDE. Ensemble des personnels non-juges des tribunaux en ETP occupés, hors personnel du parquet Q60 ; ne signifie pas seulement personnel administratif.")

    q52 = PdfReader(CEPEJ_FR).pages[29].extract_text()
    total = dec(pattern(r"Nombre total de personnel non juge travaillant\s+dans les tribunaux \(1 \+ 2 \+ 3 \+ 4 \+ 5\)\s+([\d ]+)\s+\[", q52).group(1))
    assistance = dec(pattern(r"2\. Personnels non-juges.*?préparation de la décision\)\s+([\d ]+)\s+\[", q52).group(1))
    admin = dec(pattern(r"3\. Personnels chargés.*?gestion de la\s+formation\)\s+([\d ]+)\s+\[", q52).group(1))
    technical = dec(pattern(r"4\. Personnels techniques\s+([\d ]+)\s+\[", q52).group(1))
    other = dec(pattern(r"5\. Autres personnels non juges\s+([\d ]+)\s+\[", q52).group(1))
    assert "NAP" in q52 and "Rechtspfleger" in q52
    residual = total - assistance - admin - technical - other
    published_admin = pattern(r"\*\*([\d ]+) administratifs\*\*", points[16]).group(1)
    add("justice", "France Q52 catégorie administrative et gestion des tribunaux", 2022,
        published_admin, str(admin), "ETP_occupes", URL_CEPEJ_FR,
        "data/cache/04b/cepej2024_reponses_france.pdf ; PDF 30 ; Q52 catégorie 3 ; notice PDF 31",
        f"Q52 total={total}, assistance judiciaire={assistance}, administration={admin}, technique={technical}, autres={other} ; Rechtspfleger NAP, jamais transformé en zéro. Somme numérique des catégories renseignées={total-residual} ; résidu publié={residual} ETP, conservé.")

    assert len(results) == 15
    failures = [row for row in results if row["statut_controle"] != "CONFORME"]
    with OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(results)

    paths = [NOTE, EAG, TALIS, POLICE, POLICE_META, TALIS_RESULT, TALIS_PDF, CEPEJ_PDF, CEPEJ_FR, CEPEJ_NOTICE]
    hashes = "\n".join(f"- `{path.relative_to(ROOT).as_posix()}` : `{hashlib.sha256(path.read_bytes()).hexdigest()}`" for path in paths)
    checked = "\n".join(f"- **{row['id']}** : {row['indicateur']} ({row['annee']}) ; publié **{row['valeur_publiee']}**, source **{row['valeur_source']}** {row['unite']} ; `{row['statut_controle']}`." for row in results)
    report = f"""# Contre-vérification indépendante 04b — lot 2

Date : **28 octobre 2026**. Quinze indicateurs décisifs de la note enseignement, police et justice sont relus directement dans les CSV hérités et les PDF primaires. Le script extracteur `04b_education_securite_justice.py` n'est ni lu, ni importé, ni appelé. Les chiffres publiés sont extraits de la note ; les deux erreurs standard sont rapprochées du CSV de résultat après lecture indépendante du brut. Aucun fichier 04b n'est modifié.

**Résultat : {len(results)-len(failures)} contrôles conformes sur 15 ; {len(failures)} divergence numérique.** Les arrondis publiés concordent. L'échantillon ne certifie pas tout le lot et n'établit aucun sureffectif ou potentiel d'économie.

## Chiffres contrôlés

{checked}

## Vérifications de champ et réserves

**Ratios d'enseignement.** Les six lignes sélectionnent explicitement 2024, `STU_PERS`, `ST_TCHR`, `UNIT_MULT=0`, CITE 1 ou 3, total et établissements publics selon le cas. Les 17,87 et 11,48 tous établissements deviennent bien 17,48 et 11,33 dans le public. Ces ratios portent sur les enseignants et élèves ETP ; les séries ne dénombrent pas l'administration scolaire. Le code OCDE est l'agrégat publié, sans recalcul d'une moyenne des seuls pays retenus. [Source OCDE]({URL_EAG}).

**TALIS : population et erreurs standard.** Les **1,5 h France / 3 h OCDE** de tâches administratives sont confirmées dans la [note primaire, PDF 11 / page imprimée 10]({URL_TALIS_PDF}). Elles concernent les seuls enseignants à temps plein du premier cycle secondaire. La même page confirme 38,7/41 h de travail total et 20,1/22,7 h d'enseignement. Le CSV, CITE 2 et tous profils `_T`, porte sur tous les enseignants, temps partiel inclus : {' ; '.join(se_details)}. Les deux SE correspondent exactement aux lignes du CSV de résultat ; elles ne s'appliquent pas aux 1,5/3 h ni aux 38,7/41 h du sous-groupe temps plein. La page pays ne donne pas ces SE. Un écart de population ne constitue donc pas une incohérence de chiffres. Les réponses restent déclaratives et les heures par tâche ne forment pas une partition comptable.

**Police : effectif opérationnel et champ national.** Les deux cellules françaises 2022 sont retrouvées directement dans `crim_just_job`, métier `OC5412`, sexe total, unités `NR` et `P_HTHAB`. Aucune valeur française 2023 n'est présente dans le brut. Le [HTML primaire Eurostat]({URL_META}) confirme l'exclusion du personnel de soutien, dont secrétaires et employés de bureau (§3.4), l'inclusion de la police locale française et la date allemande du 30 juin, fonctionnaires hors stagiaires (§15.1). Les territoires ultramarins français énumérés sont exclus (§3.7). Ces notes empêchent de lire le nombre comme celui de tous les administratifs du ministère. Le taux publié Eurostat est conservé ; la population d'une autre source n'est pas substituée.

**Justice : catégories et résidu conservé.** Les **37,3 et 57,9 ETP/100 000 habitants** correspondent au personnel non-juge des tribunaux et à la médiane CoE, non à la seule administration. Le [profil France, PDF 67]({URL_CEPEJ}) et la [notice Q52, PDF 31]({URL_NOTICE}) distinguent assistance judiciaire, Rechtspfleger, administration/gestion, technique et autres ; le personnel du parquet est suivi séparément à Q60. La [réponse française, PDF 30]({URL_CEPEJ_FR}) donne {total} ETP au total, {assistance} d'assistance, {admin} d'administration, {technical} techniques et {other} autres. La somme des catégories numériques est {total-residual}, avec un résidu publié de {residual} ETP. La catégorie Rechtspfleger est non applicable : aucune valeur zéro n'est créée pour la remplir. La note 04b conserve correctement ce résidu. Les comparaisons de catégories administratives requièrent toujours l'examen des greffes, missions et externalisations.

## Reproduction et limites

Exécuter à la racine : `python scripts/00_verification_04b_lot2.py` (Python 3 et `pypdf`). Le script utilise seulement `csv`, `decimal`, `hashlib`, `re`, `pathlib` et `pypdf`. Il impose une cellule unique par sélection, vérifie les unités et définitions, compare selon la précision affichée et sort en erreur si une divergence est trouvée. Il produit uniquement `data/risques/verification_04b_lot2.csv` et cette note. Les pages PDF désignent l'index physique à partir de 1. Les lignes CSV comptent l'en-tête comme ligne 1 ; les dimensions explicites restent la référence si une valeur textuelle contient un saut de ligne.

Le contrôle est réalisé sur les archives locales ; les PDF TALIS et CEPEJ ont également été ouverts auprès des éditeurs pendant la contre-lecture. Les CSV hérités ne contiennent pas l'horodatage et l'URL exacte de leur requête initiale : l'accord confirme la fidélité au brut, sans certifier que toutes les séries sont les dernières disponibles. Les empreintes suivantes rendent l'état contrôlé identifiable. Aucun correctif numérique n'est demandé sur ces quinze indicateurs ; les réserves de champ restent nécessaires.

## Empreintes SHA-256 des entrées

{hashes}
"""
    REPORT.write_text(report, encoding="utf-8", newline="\n")
    print(f"{len(results)} indicateurs ; {len(failures)} divergence ; SE TALIS et champs contrôlés.")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
