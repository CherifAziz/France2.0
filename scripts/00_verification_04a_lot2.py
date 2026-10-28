#!/usr/bin/env python3
"""Contre-vérification indépendante de quinze nombres et d'un arrondi du lot 04a.

Aucun import, appel ou lecture du script extracteur 04a. Les cibles sont ses
CSV publiés ; les preuves sont relues dans les CSV/XML bruts et PDF primaires.
Usage : python -I scripts/00_verification_04a_lot2.py
"""
from __future__ import annotations

import csv
import gzip
import json
import logging
import math
import re
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
COLS = ["id", "theme", "indicateur", "annee", "valeur_publiee", "valeur_source", "unite", "source_url", "source_localisation", "statut_controle", "note"]
logging.getLogger("pypdf").setLevel(logging.ERROR)


def read_csv(relative, compressed=False):
    path = ROOT / relative
    opener = gzip.open if compressed else open
    with opener(path, "rt", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def only(rows, **criteria):
    matches = [r for r in rows if all(r[k] == str(v) for k, v in criteria.items())]
    assert len(matches) == 1, (criteria, len(matches))
    return matches[0]


def metadata(relative):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class VisibleText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.hidden = 0

    def handle_starttag(self, tag, attrs):
        if tag in ["script", "style"]:
            self.hidden += 1

    def handle_endtag(self, tag):
        if tag in ["script", "style"]:
            self.hidden -= 1

    def handle_data(self, text):
        if not self.hidden:
            self.parts.append(text)


def main():
    raw_path = "data/raw/04a/isora_selection_2022_2024.csv.gz"
    raw = read_csv(raw_path, compressed=True)
    imf_url = metadata(raw_path+".meta.json")["source_url"]
    lmp_path = "data/raw/04a/lmp_selection_2023_2024.csv.gz"
    lmp_raw = read_csv(lmp_path, compressed=True)
    lmp_url = metadata(lmp_path+".meta.json")["source_url"]
    comparison = only(read_csv("data/international/04a_isora_comparaison.csv"), pays_iso3="FRA", annee=2023)
    published_functions = read_csv("data/international/04a_isora_fonctions.csv")
    lmp_published = read_csv("data/international/04a_lmp_observations.csv")

    # Vocabulaire primaire : lu depuis XML SDMX, pas repris de l'extracteur.
    code_path = ROOT / "data/raw/04a/isora_codelist_6_0_6.xml.gz"
    tree = ET.fromstring(gzip.decompress(code_path.read_bytes()))
    codes = {n.attrib["id"]: n for n in tree.iter() if n.tag.rsplit("}", 1)[-1] == "Code"}
    names = {k: next((c.text for c in list(n) if c.tag.rsplit("}", 1)[-1] == "Name"), "") for k, n in codes.items()}
    assert names["337_180"] == "Total FTEs"
    assert "No. at end of FY" in names["83835_28"]
    assert "in thousands" in names["80040_3"]

    # Définition ETP annuel, monnaie en milliers, dépenses salariales avec
    # contributions retraite, fonctions du siège recouvrant les sept fonctions.
    questionnaire_path = ROOT / "data/cache/04a/isora_questionnaire_2025.pdf"
    questionnaire = PdfReader(questionnaire_path)
    form_c = " ".join(questionnaire.pages[i].extract_text() for i in [4, 5, 6])
    form_d = questionnaire.pages[9].extract_text()
    assert "thousands of local currency" in form_c
    assert "including contributions to pension plans" in form_c
    assert "available full time for the entire year" in form_c
    assert "both at headquarters and operating offices" in form_c
    assert "all staff, including contractual staff" in form_d
    assert "total number of staff at the end of the year" in form_d
    tax_report = PdfReader(ROOT / "data/cache/04a/tax_administration_2025.pdf")
    annex = tax_report.pages[152].extract_text()
    assert re.search(r"France\s+Direction Générale", annex)
    assert "www.impots.gouv.fr EUR" in re.sub(r"\s+", " ", annex)

    rows = []
    def imf(code):
        row = only(raw, JURISDICTION="FRA", INDICATOR=code, TIME_PERIOD=2023, FREQUENCY="A")
        return row, raw.index(row)+2

    def add(id_, theme, indicator, published, source, unit, url, loc, note, status="CONFORME"):
        agrees = math.isclose(float(published), float(source), rel_tol=1e-9, abs_tol=1e-8)
        rows.append(dict(id=id_, theme=theme, indicateur=indicator, annee=2023, valeur_publiee=published, valeur_source=source, unite=unit, source_url=url, source_localisation=loc, statut_controle=status if agrees else "ERREUR_VALEUR", note=note))

    fte, n_fte = imf("337_180")
    staff, n_staff = imf("83835_28")
    add("04aV01", "fiscalite", "Ressources fiscales déclarées, Form C", comparison["etp_fiscaux"], fte["OBS_VALUE"], "ETP_annuels", imf_url, f"{raw_path} / ligne {n_fte}, 337_180 ; questionnaire PDF 5-6 Q1", "ETP annuel, éventuellement estimé ; pas nombre de personnes en stock ni emplois administratifs supprimables.")
    add("04aV02", "fiscalite", "DGFiP, agents de fin d'exercice Form D", comparison["agents_fin_exercice"], staff["OBS_VALUE"], "personnes_fin_exercice", imf_url, f"{raw_path} / ligne {n_staff}, 83835_28 ; questionnaire PDF 10 Q1 ; Tax Administration 2025 PDF 153, annexe B", "La table internationale identifie la DGFiP comme répondant français. Form D porte sur les personnels, contractuels inclus, en stock. L'écart avec 38 406 ne se réduit pas à une conversion PP/ETP ; il manque une réconciliation nationale complète des missions.", "CONFORME_CHAMP_DISTINCT")

    operating, n_op = imf("337_176")
    revenue, n_rev = imf("80040_3")
    cost, n_cost = imf("337_012")
    add("04aV03", "fiscalite", "Dépenses de fonctionnement fiscales", comparison["depenses_fonct_k_monnaie_locale"], operating["OBS_VALUE"], "milliers_EUR", imf_url, f"{raw_path} / ligne {n_op}, 337_176 ; questionnaire PDF 6 Q1b ; nomenclature Subtitle1 A.16", "La réponse en milliers est conforme au questionnaire ; 4 276 335 k€ = 4,276335 Md€. Pas de coût d'entrée marginal.")
    add("04aV04", "fiscalite", "Recettes nettes, valeur du CSV IMF", comparison["recettes_export_monnaie_locale"], revenue["OBS_VALUE"], "EUR_interpretation_validee_identite", imf_url, f"{raw_path} / ligne {n_rev}, 80040_3, SCALE={revenue['SCALE']} ; XML code 80040_3 ; questionnaire PDF 3", "Le libellé XML dit « in thousands » mais la valeur de cet export est 636 876 942 000. L'identité du ratio publié est cohérente en unités pour cette valeur ; aucune multiplication générale par 10^SCALE n'est validée. Ne pas présenter cette identité comme résolution complète du contrat de métadonnées.", "CONFORME_VALEUR_RESERVE_UNITE")
    recomputed_cost = 100*float(operating["OBS_VALUE"])*1000/float(revenue["OBS_VALUE"])
    assert math.isclose(recomputed_cost, float(cost["OBS_VALUE"]), rel_tol=1e-9, abs_tol=1e-9)
    add("04aV05", "fiscalite", "Coût de collecte recalculé", comparison["cout_collecte_pct"], recomputed_cost, "pourcent_recettes_nettes", imf_url, f"{raw_path} / lignes {n_op}, {n_rev}, {n_cost} ; XML 337_012, Legend", "100 × 4 276 335 × 1 000 / 636 876 942 000 = 0,67145388979 %. Le ratio brut 337_012 vaut 0,6714538898 %. Dépenses salariales avec cotisations retraite selon questionnaire ; ratio moyen non assimilable à une économie.")

    # Sept fonctions : identifiants sélectionnés dans le dictionnaire primaire.
    functions = [
        ("95230_206", "usagers_declarations_paiements", "Registration"),
        ("94020_206", "audit_enquetes_verifications", "Audit"),
        ("94030_206", "recouvrement_force", "Enforced debt"),
        ("96970_206", "contentieux", "Dispute"),
        ("96980_206", "rh", "Human resource"),
        ("98810_206", "informatique", "ICT"),
        ("95240_206", "autres_fonctions", "Other functions"),
    ]
    total = 0
    for i, (identifier, label, expected_name) in enumerate(functions, 6):
        assert expected_name in names[identifier], (identifier, names[identifier])
        source, line = imf(identifier)
        target = only(published_functions, pays_iso3="FRA", annee=2023, fonction=label)
        total += float(source["OBS_VALUE"])
        share = 100*float(source["OBS_VALUE"])/float(fte["OBS_VALUE"])
        assert math.isclose(share, float(target["part_pct_recalculee"]), rel_tol=1e-9, abs_tol=1e-8)
        add(f"04aV{i:02d}", "fiscalite_fonctions", label, target["etp"], source["OBS_VALUE"], "ETP_annuels", imf_url, f"{raw_path} / ligne {line}, {identifier} ; XML Name ; questionnaire PDF 7 Q3", f"Part recalculée {share:.9f} %. Fonctions de siège et bureaux opérationnels incluses ; ne pas ajouter la part du siège (4 %) comme huitième fonction.")
    assert total == float(fte["OBS_VALUE"]), (total, fte["OBS_VALUE"])

    # SPE : dépenses, pas salariés ; million de monnaie nationale explicite.
    for i, (programme, indicator) in enumerate([("LMP_11", "placement_et_services_lies"), ("LMP_13", "autres_couts_ou_non_identifies"), ("LMP_10", "SPE_et_administration_total")], 13):
        matches = [r for r in lmp_raw if r["REF_AREA: Reference area"] == "FRA: France" and r["MEASURE: Measure"] == "EXP: Public expenditure" and r["PROGRAMME: Programme"].split(":")[0] == programme and r["UNIT_MEASURE: Unit of measure"] == "XDC: National currency" and r["TIME_PERIOD: Time period"] == "2023"]
        assert len(matches) == 1
        source = matches[0]
        assert source["UNIT_MULT: Unit multiplier"] == "6: Millions"
        target = only(lmp_published, pays_iso3="FRA", annee=2023, mesure="EXP", programme=programme, unite="XDC")
        assert int(target["multiplicateur"]) == 6
        published_millions = float(target["valeur_unites"])/1_000_000
        add(f"04aV{i:02d}", "emploi_SPE", indicator, published_millions, source["OBS_VALUE"], "millions_EUR", lmp_url, f"{lmp_path} / ligne {lmp_raw.index(source)+2}, {programme}, XDC, UNIT_MULT=6 ; métadonnées LMP §3.2/3.4", "Catégorie 1 : activités des SPE et autres services aux chercheurs d'emploi financés publiquement. Ce n'est ni le budget du seul France Travail, ni les seules fonctions de soutien. LMP_13 n'est pas un nombre d'agents administratifs ; LMP_12 manquant en France ne vaut pas zéro.")
    assert len(rows) == 15
    scope_parser = VisibleText()
    scope_parser.feed((ROOT/"data/raw/04a/lmp_metadonnees.html").read_text(encoding="utf-8"))
    scope = re.sub(r"\s+", " ", " ".join(scope_parser.parts))
    assert "other publicly funded services for jobseekers" in scope
    assert "Public Employment Services" in scope
    assert "intervention" in scope
    lmp_comparison = only(read_csv("data/international/04a_lmp_comparaison.csv"), pays_iso3="FRA", annee=2023)
    ratio = 100*5187/6899
    assert math.isclose(ratio, float(lmp_comparison["part_autres_non_ventiles_pct"]), abs_tol=1e-8)
    assert lmp_comparison["administration_prestations_pct_pib"] == ""
    rows[-1]["note"] += f" Identité : 1 712 + 5 187 = 6 899 ; part LMP_13 = {ratio:.9f} %, conforme à 04a. Le champ inclut des services externes financés et ne permet pas une comparaison de productivité des seuls organismes."

    # Contrôle supplémentaire demandé après la livraison de la note : arrondi UK
    # dans le point 6 de la synthèse. La valeur exacte reste dans valeur_source.
    uk_fte = only(raw, JURISDICTION="GBR", INDICATOR="337_180", TIME_PERIOD=2023, FREQUENCY="A")
    uk_pop = only(raw, JURISDICTION="GBR", INDICATOR="398_003", TIME_PERIOD=2023, FREQUENCY="A")
    uk_ratio = only(raw, JURISDICTION="GBR", INDICATOR="337_010", TIME_PERIOD=2023, FREQUENCY="A")
    exact_uk = 1000*float(uk_fte["OBS_VALUE"])/float(uk_pop["OBS_VALUE"])
    assert math.isclose(exact_uk, 1000/float(uk_ratio["OBS_VALUE"]), rel_tol=1e-9)
    note = (ROOT/"recherche/04a_fiscalite_emploi.md").read_text(encoding="utf-8")
    target = re.search(r"\*\*(0,[0-9]+) au Royaume-Uni\*\*", note)
    assert target, "Valeur UK de la synthèse à localiser si sa formulation change"
    published_uk = float(target.group(1).replace(",", "."))
    rows.append(dict(id="04aV16", theme="fiscalite_arrondi_UK", indicateur="UK ETP fiscaux pour 1000 habitants, synthèse point 6", annee=2023, valeur_publiee=published_uk, valeur_source=exact_uk, unite="ETP_pour_1000_habitants", source_url=imf_url, source_localisation=f"{raw_path} / GBR 337_180 ligne {raw.index(uk_fte)+2}, 398_003 ligne {raw.index(uk_pop)+2}, 337_010 ligne {raw.index(uk_ratio)+2} ; note 04a synthèse point 6", statut_controle="CONFIRME_APRES_CORRECTION" if published_uk == round(exact_uk, 3) else "ERREUR_ARRONDI", note=f"58 587 × 1000 / 68 350 000 = {exact_uk:.12f} ; arrondi à trois décimales attendu : {exact_uk:.3f}. Trace : première lecture de la synthèse à 0,858 le 28/10/2026 ; correction par l'auteur à 0,857, puis contrôle rejoué. Le tableau et le CSV étaient corrects ; aucun calcul CSV n'a changé."))

    destination = ROOT / "data/risques/verification_04a_lot2.csv"
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLS)
        writer.writeheader()
        writer.writerows(rows)
    errors = [r["id"] for r in rows if r["statut_controle"].startswith("ERREUR")]
    print(json.dumps(dict(controles=len(rows), erreurs=errors, somme_sept_fonctions=total, cout_collecte=recomputed_cost, part_LMP13=ratio, definitions_PDF_et_HTML="vérifiées directement"), ensure_ascii=False))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
