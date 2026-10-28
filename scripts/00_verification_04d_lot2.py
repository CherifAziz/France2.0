"""Contre-vérification de 15 ensembles de chiffres de la note 04d.

Relit directement les XLSX, CSV SDMX et PDF primaires archivés ; n'importe ni
n'exécute scripts/04d_territoires_support.py, et ne lit pas ses CSV dérivés.
Les valeurs publiées sont celles de la note auditée ; les valeurs source sont
extraites ici. Une seconde lecture ne constitue pas une seconde observation statistique.
"""
from __future__ import annotations

import csv
import json
import re
import sys
from decimal import Decimal
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if (ROOT / ".cache/python_deps").is_dir():
    sys.path.append(str(ROOT / ".cache/python_deps"))
from openpyxl import load_workbook
from pypdf import PdfReader

CACHE = ROOT / "data/cache/04d"
RAW = ROOT / "data/raw/04d"
ROWS: list[dict] = []


def source_url(folder: Path, name: str) -> str:
    return json.loads((folder / (name + ".meta.json")).read_text(encoding="utf-8"))["source_url"]


def decimal(s: str | int | float) -> Decimal:
    return Decimal(re.sub(r"\s+", "", str(s)).replace(",", "."))


def compact(s: str) -> str:
    return " ".join(s.split())


def capture(pattern: str, text: str) -> Decimal:
    m = re.search(pattern, text, re.I)
    if m is None:
        raise ValueError(f"Expression non trouvée dans le primaire : {pattern}")
    return decimal(m.group(1))


def add(id_: str, theme: str, indicator: str, year: str, claim: str, found: str,
        unit: str, url: str, location: str, note: str, status: str = "CONFIRME") -> None:
    ROWS.append(dict(id=id_, theme=theme, indicateur=indicator, annee=year,
                     valeur_publiee=claim, valeur_source=found, unite=unit,
                     source_url=url, source_localisation=location,
                     statut_controle=status, note=note))


def main() -> None:
    audit_note = (ROOT / "recherche/04d_territoires_fonctions_support.md").read_text(encoding="utf-8")
    # Cellules originales DGCL, avec en-têtes et note de champ.
    w = load_workbook(RAW / "dgcl_ch2_2026.xlsx", data_only=True)
    url = source_url(RAW, "dgcl_ch2_2026")
    s = w["2.2 nb CL"]
    assert s["F5"].value == 2026 and s["A8"].value == "Communes"
    communes = int(s["F8"].value)
    assert communes == 34875
    add("V04d_01", "Stocks territoriaux", "Communes au 1er janvier2026", "2026-01-01", "34875", str(communes),
        "communes", url, "2.2 nb CL!F8 ; année F5 ; ventilation F9/F10",
        "34 746 communes métropolitaines+129 outre-mer=34 875 ; institutions, sans mesure des agents.")
    s = w["2.5a EPCI"]
    epci, lyon = int(s["F9"].value), int(s["F10"].value)
    assert epci == 1252 and lyon == 1
    assert sum(s[f"F{i}"].value for i in [5, 6, 7, 8]) == epci
    assert s["F11"].value + s["F12"].value == s["F13"].value == communes
    assert "Lyon" in s["A19"].value
    add("V04d_02", "Stocks territoriaux", "EPCI à fiscalité propre et champ Lyon", "2026-01-01", "1252", str(epci),
        "EPCI", url, "2.5a EPCI!F5:F13 ; note A19",
        "21 métropoles+14 CU+230 CA+987 CC=1 252 ; Lyon=1 est distinct. Communes regroupées34 871+isolées4=34 875, Lyon inclus dans les regroupées.")

    # Données SDMX primaires : dimensions et unités sont contrôlées avant sélection.
    with (RAW / "oecd_sng_struct_2020_2026.csv").open(encoding="utf-8-sig", newline="") as f:
        raw_sng = list(csv.DictReader(f))
    sng = [{k.split(":", 1)[0]: v.split(":", 1)[0] for k, v in r.items()} for r in raw_sng]
    periods = sorted({r["TIME_PERIOD"] for r in sng})
    assert len(sng) == 90 and periods == ["2020"]
    assert all(r["UNIT_MULT"] == "0" for r in sng)
    url = source_url(RAW, "oecd_sng_struct_2020_2026")
    add("V04d_03", "WOFI période", "Année statistique de l'extraction2020-2026", "2020", "2020 ;90 observations",
        ";".join(periods)+" ;"+str(len(sng))+" observations", "année statistique et lignes", url, "TIME_PERIOD sur les90 lignes primaires",
        "La requête va jusqu'à2026 mais ne fournit que2020. Le téléchargement2026 ne change pas l'année ; aucun effectif d'agents mesuré.")
    fra = {r["MEASURE"]: r for r in sng if r["REF_AREA"] == "FRA"}
    assert fra["MUN"]["UNIT_MEASURE"] == "SNGU" and int(fra["MUN"]["OBS_VALUE"]) == 34955
    add("V04d_04", "WOFI structure", "Municipalités françaises", "2020", "34955", fra["MUN"]["OBS_VALUE"],
        "unités municipales", url, "REF_AREA=FRA;MEASURE=MUN;TIME_PERIOD=2020;UNIT=SNGU;UNIT_MULT=0",
        "À distinguer du stock DGCL2026 ; SUB=35 074 et REG=18 sont d'autres niveaux, non un nombre d'agents.")
    size = decimal(fra["MUN_SIZE"]["OBS_VALUE"])
    assert round(size, 2) == Decimal("1927.95")
    assert fra["MUN_SIZE"]["STATISTICAL_OPERATION"] == "MEAN" and fra["MUN_SIZE"]["UNIT_MEASURE"] == "PS"
    add("V04d_05", "WOFI taille", "Taille moyenne d'une municipalité française", "2020", "1927.95", str(size),
        "habitants par municipalité, moyenne", url, "FRA;MUN_SIZE;STATISTICAL_OPERATION=MEAN;UNIT_MEASURE=PS;2020",
        "Valeur exacte1 927,952568 arrondie à1 927,95 ; ne corrige ni densité, ni compétences, ni coopération et ne mesure pas une productivité.")

    # Pages du PDF original Ravignon, indices de page distincts de la pagination imprimée.
    reader = PdfReader(CACHE / "ravignon_rapport2024.pdf")
    page = lambda n: compact(reader.pages[n-1].extract_text(extraction_mode="layout"))
    p43, p45, p46, p96, p97, p98, p100 = (page(n) for n in [43, 45, 46, 96, 97, 98, 100])
    url = source_url(CACHE, "ravignon_rapport2024")
    sample = capture(r"soit\s+([\d\s]+)\s+collectivités", p43)
    assert sample == 178 and "11 groupements de communes" in p43 and "54 préfectures" in p43
    assert "n’ont pas été sollicités" in p43 or "n'ont pas été sollicités" in p43
    add("V04d_06", "Ravignon méthode", "Échantillon exploité", "rapport2024", "178 collectivités;11 intercommunalités;54 services État",
        f"{sample} collectivités;11 groupements;54 préfectures/directions", "répondants exploités", url, "PDF p.43, imprimée36, suite tableau9 et méthode",
        "155 communes+11 groupements+9 départements+3 régions=178 ; extrapolation de temps déclarés et coûts hypothétiques ; opérateurs non interrogés.")
    total = capture(r"Total\s+[\d\s]+€\s+[\d\s]+€\s+[\d\s]+€\s+[\d\s]+€\s+[\d\s]+€\s+([\d\s]+)\s*€", p46)
    assert total == 7443997405
    assert "1 856 810 109" in p45 and "1 356 245 301" in p45
    add("V04d_07", "Ravignon coordination", "Coût valorisé de l'enchevêtrement", "rapport2024", "7443.997 M€;arrondi7.444 Md€",
        f"{total} EUR;{total/Decimal(1000000)} M€", "EUR/an valorisés, estimation externe", url, "PDF p.45-46, imprimées38-39, tableau10 Total",
        "Montant publié confirmé ; coûts patrimoine/RH/finances1,856810109 Md€ et DGFiP1,356245301 Md€ inclus. Coordination nécessaire comprise, pas des crédits supprimables. Tableau inspecté visuellement.")
    staff = capture(r"([\d\s]+)\s+agents\s+occuperaient", p96)
    extra = capture(r"S’y ajoutent les\s+([\d\s]+)\s+effectifs", p96)
    combined = capture(r"soit\s+([\d\s]+)\s+agents\s*\(cf", p96)
    assert (staff, extra, combined) == (31040, 13600, 44640) and staff+extra == combined
    add("V04d_08", "Ravignon métiers RH", "Agents RH et ajout CNFPT/CDG", "2021 selon rapport", "31040+13600=44640",
        f"{staff}+{extra}={combined}", "agents ; ETP non établi", url, "PDF p.96, imprimée89, paragraphe du ratio gérants/gérés ; tableau25 p.98",
        "Dix métiers dont formation, prévention, santé/sécurité ; estimation reprise du CNFPT. La source ne les identifie pas comme un vivier d'ETP supprimables.")
    text_cost = capture(r"estimé à\s+([\d\s]+,\d+)\s*M€", p97)
    m = re.search(r"Total\s+31\s+040\s+1\s+965\s+300\s+N\.A\.\s+N\.A\.\s+N\.A\.\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)", p98)
    assert m is not None
    columns = [decimal(x) for x in m.groups()]
    tab_cost = sum(columns)
    assert columns == [Decimal("376.7"), Decimal("463.5"), Decimal("592.5")] and tab_cost == Decimal("1432.7")
    assert text_cost == Decimal("2047.3")
    remains = "base élargie" in audit_note
    add("V04d_09", "Ravignon base RH", "Base de masse salariale du texte et somme tableau25", "2021 selon rapport", "2047.3 M€ texte;1432.7 M€ tableau25",
        f"{text_cost} texte;{tab_cost} tableau25;écart={text_cost-tab_cost}", "M€/an estimés", url, "PDF p.97-98, imprimées90-91, texte et total des3 coûts A/B/C du tableau25",
        "Montants confirmés. Formulation initiale de la synthèse : 'base élargie à2 047,3 M€'. Le texte ne précise pas explicitement que2 047,3 M€ inclut CNFPT/CDG ; ce périmètre n'est pas démontré. Raccordement de614,6 M€ non reconstitué. Titre tronqué confirmé visuellement."
        + (" Précision recommandée au parent, non modifiée par le vérificateur." if remains else " Correction coordonnée par le parent le28/10/2026 : coût publié dans le texte, raccordement au tableau25 non reconstitué et inclusion exacte CNFPT/CDG non explicitée. Rédaction finale relue."),
        "CORRECTION_PERIMETRE_A_FAIRE" if remains else "CONFIRME_APRES_CORRECTION")
    hi = capture(r"10\s*%\s+([\d,]+)", p100)
    lo = capture(r"5\s*%\s+([\d,]+)", p100)
    assert (hi, lo) == (Decimal("204.7"), Decimal("102.4"))
    assert round(text_cost*Decimal(".10"),1) == hi and round(text_cost*Decimal(".05"),1) == lo
    assert "En l’absence de comptabilité analytique" in p100
    add("V04d_10", "Ravignon hypothèses", "Gains RH supposés5 % et10 %", "rapport2024", "5%=102.4;10%=204.7",
        f"5%={lo};10%={hi}", "M€/an hypothétiques", url, "PDF p.100, imprimée93, tableau26 et paragraphe précédent",
        "Calculs arrondis confirmés sur la base textuelle2 047,3 M€ ; hypothèses d'efficience externes, sans comptabilité analytique précise, pas une réalisation.")

    senate = PdfReader(CACHE / "senat_agences_rapport2025.pdf")
    p217, p231 = (compact(senate.pages[n-1].extract_text(extraction_mode="layout")) for n in [217, 231])
    url = source_url(CACHE, "senat_agences_rapport2025")
    base = capture(r"évalué à\s+([\d,]+)\s*milliards", p231)
    rate = capture(r"Une réduction de\s+(\d+)\s*%", p231)
    gain = capture(r"ordre de\s+(\d+)\s*millions", p231)
    assert (base,rate,gain) == (Decimal("2.7"),20,540) and base*1000*rate/100 == gain
    assert "hors universités et centres de recherche" in p231 and "hors charges d’intervention" in p231
    assert "très volontariste" in p231
    add("V04d_11", "Support opérateurs", "Hypothèse de baisse20 % du support", "base opérateurs2024;rapport2025", "2700×20%=540",
        f"{base} Md€×{rate}%={gain} M€", "M€/an hypothétiques", url, "PDF p.231, paragraphe coût des fonctions support",
        "Base déjà estimée avec ratio10 % ; hors interventions, universités/recherche. Hypothèse externe explicitement très volontariste ; coûts de transition non retranchés.")
    surface = capture(r"soit environ\s+(\d+)\s*millions de mètres", p217)
    reduction = capture(r"réduction des surfaces de bureaux occupées de\s+(\d+)\s*%", p217)
    horizon = capture(r"d’ici\s+(\d{4})", p217)
    release = capture(r"soit\s+(\d+)\s*millions de mètres", p217)
    assert (surface,reduction,horizon,release) == (20,25,2032,5)
    assert "un milliard d’euros en dépenses annuelles d’entretien et de loyers" in p217
    add("V04d_15", "Immobilier", "Objectif de surfaces et gain de foncière", "cible2032;estimation rapport2025", "20M m²;−25%;5M m²;1000 M€/an",
        f"{surface}M m²;−{reduction}%;{release}M m²;2032;1 Md€/an", "surfaces et gain hypothétique annuel à terme", url, "PDF p.217 et notes1-2",
        "5 millions m²=25 % de20 ; moitié libération de baux, moitié cessions ; estimation gouvernementale historique. Distinguer gains annuels, ventes ponctuelles, investissements et réforme déjà engagée.")

    dae = PdfReader(CACHE / "dae_rapport2025.pdf")
    p46, p86, p87 = (compact(dae.pages[n-1].extract_text(extraction_mode="layout")) for n in [46,86,87])
    url = source_url(CACHE,"dae_rapport2025")
    savings = capture(r"Total\s+(\d+,\d+)", p87)
    source_values = [decimal(x) for x in re.findall(r"(?<![\d,])(\d+,\d{2})(?![\d,])",p87)]
    # Les12 contributions ministérielles, puis leur total : indépendamment du script auteur.
    assert len(source_values) == 13 and sum(source_values[:-1]) == source_values[-1] == savings == Decimal("412.53")
    assert "estimation du volume de commandes" in p86 and "distingué des économies budgétaires réelles" in p86
    add("V04d_12", "Achats performance", "Économies achats État et concept", "2025", "412.53", str(savings),
        "M€ d'économies achats calculées, non crédits constatés", url, "PDF p.86 définition et p.87 tableau total",
        "Somme indépendante des12 lignes=412,53 M€. Prix de référence et volumes estimés ; la DAE distingue explicitement les économies budgétaires, dépendant des quantités réelles.")
    assert "50 245" in p46 and "24 364" in p46 and "25 881" in p46
    assert 24364+25881 == 50245
    add("V04d_13", "Achats dépenses", "Dépenses d'achat de l'État et défense/sécurité", "2025", "50245=24364+25881",
        "50245=24364+25881", "M€ de dépenses", url, "PDF p.46, graphique et tableau hors D&S",
        "Dépenses totales50,245 Md€, hors D&S24,364 et D&S25,881 ; distinct du périmètre État+EP et du calcul d'économies. Les valeurs du graphique ont été relues dans la page PDF.")

    # Source primaire parlementaire : état de procédure, sans prétendre lire Légifrance403.
    html = (CACHE / "senat_fonciere2026.html").read_text(encoding="utf-8")
    text = compact(unescape(re.sub(r"<[^>]+>", " ", html)))
    assert "LOI n° 2026-795 du 18 août 2026" in text
    assert "Le Président de la République a promulgué cette loi le mardi 18 août 2026" in text
    url = source_url(CACHE,"senat_fonciere2026")
    add("V04d_14", "Actualisation juridique", "Promulgation du cadre de foncière", "2026-08-18", "loi2026-795 du18/08/2026",
        "loi2026-795 du18/08/2026", "numéro et date de promulgation", url, "Page Sénat, La loi en clair, titre et paragraphe chronologique",
        "État de procédure primaire confirmé ; ne valide pas une économie réalisée et ne constitue pas une lecture intégrale du texte Légifrance, dont le403 est signalé.")

    ROWS.sort(key=lambda r:r["id"])
    assert len(ROWS) == 15
    output = ROOT / "data/risques/verification_04d_lot2.csv"
    with output.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["id","theme","indicateur","annee","valeur_publiee","valeur_source","unite","source_url","source_localisation","statut_controle","note"])
        w.writeheader()
        w.writerows(ROWS)
    print(json.dumps({"controles":len(ROWS),"numeriques_confirmes":15,
                      "reserves_perimetre":sum(r["statut_controle"] == "CORRECTION_PERIMETRE_A_FAIRE" for r in ROWS),
                      "confirmes_apres_correction":sum(r["statut_controle"] == "CONFIRME_APRES_CORRECTION" for r in ROWS)},ensure_ascii=False))


if __name__ == "__main__":
    main()
