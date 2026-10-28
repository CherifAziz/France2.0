#!/usr/bin/env python3
"""Extrait les coûts PAP 2026 et contrôles de pensions depuis les sources archivées.

python -I scripts/01c_extrait_couts.py [--fetch]
--fetch récupère les instantanés absents avec scripts/fetch.py. Les documents
téléchargés ne sont jamais exécutés. Aucune calibration nationale n'est créée.
"""
import argparse
import csv
import importlib.util
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "data/cache/01c"
SOURCES = [
    ("pap2026_gestion", "PAP 2026 – mission Gestion des finances publiques (programmes 156 et 218)", "Direction du Budget", "2025-10", "https://www.assemblee-nationale.fr/dyn/contenu/visualisation/1087984/file/PAP2026_BG_Gestion_finances_publiques_GA.pdf", "pp. 45, 49-51 et 111-112 consultées ; coûts prévisionnels 2026 ; contrôles visuels pp. 50 et 111"),
    ("pap2026_218", "PAP 2026 – programme 218, version par programme", "Direction du Budget", "2025-10", "https://www.budget.gouv.fr/documentation/file-download/31060", "pp. imprimées 24-25, soit PDF 23-24 ; même tableau que mission p. 111, pas une source statistique indépendante"),
    ("jaune2027_pensions", "Rapport sur les pensions de retraite de la fonction publique – PLF 2027", "Direction du Budget", "2026-10", "https://www2.assemblee-nationale.fr/static/17/Annexes-DL/PLF_2027/12-Jaune-2027-Pensions-de-retraite-fonction-publique.pdf", "pp. 20-24, 44 et 55-57 consultées ; contrôle visuel p. 20 ; avertissement pypdf sur des pages tournées hors extraits utilisés"),
    ("cnracl_cotisations", "Calcul des cotisations CNRACL", "CNRACL / Caisse des dépôts", "", "https://www.cnracl.retraites.fr/employeur/cotisations-declarations/cotisations/calcul-des-cotisations", "tableau annuel 2026 et assiette des cotisations"),
    ("cnracl_hausse2026", "Augmentation des taux de cotisations au 1er janvier 2026", "CNRACL / Caisse des dépôts", "2025-12-19", "https://www.cnracl.retraites.fr/employeur/actualites/augmentation-des-taux-de-cotisations-au-1er-janvier-2026-contribution-et-surcotisation", "37,65 % en 2026 et trajectoire à 43,65 % en 2028 ; date de publication affichée"),
    ("sre_cotisations", "Les établissements publics nationaux ou organismes publics dotés de l'autonomie financière", "Service des retraites de l'État", "", "https://retraitesdeletat.gouv.fr/professionnels/le-versement-des-cotisations/les-etablissements-publics-nationaux-ou-organismes", "rubriques taux, assiette, retenues et contribution ATI"),
    ("jaune2027_conseil", "Recours aux conseils extérieurs – annexe au PLF 2027", "Direction du Budget", "2026-10", "https://www2.assemblee-nationale.fr/static/17/Annexes-DL/PLF_2027/27-Jaune-2027-Recours-aux-cabinets-de-conseil.pdf", "pp. 3-4 et 15-16 consultées ; 714 pages accessibles, aucune prétention à lecture intégrale des annexes contractuelles"),
    ("igas_cnracl2024", "Situation financière de la CNRACL : bilan et perspectives, fiche du rapport", "IGAS-IGF-IGA", "2024-09-27", "https://www.igas.gouv.fr/situation-financiere-de-la-caisse-nationale-de-retraite-des-agents-des-collectivites-locales-bilan-et-perspectives", "fiche intégrale consultée, mise à jour affichée 16/12/2025 ; PDF du rapport non utilisé comme preuve"),
    ("insee_s13", "Administrations publiques en 2025 : définitions des secteurs", "Insee", "2026-08-28", "https://www.insee.fr/fr/statistiques/8988833", "rubrique documentation S13 et S1314 ; comptes nationaux distincts des budgets d'employeurs"),
    ("an_plf2026", "Dossier législatif du PLF 2026", "Assemblée nationale", "", "https://www.assemblee-nationale.fr/dyn/17/dossiers/PLF_2026", "index ayant fourni le lien PAP mission Gestion des finances publiques"),
    ("an_plf2027", "Dossier législatif du PLF 2027", "Assemblée nationale", "2026-10-01", "https://www.assemblee-nationale.fr/dyn/17/dossiers/PLF_2027", "au 28/10/2026 la mission Gestion des finances publiques et lutte contre les fraudes est affichée sans hyperlien ; jaunes pensions et conseil liés"),
    ("exercice2026", "Index budgétaire exercice 2026", "Direction du Budget", "", "https://www.budget.gouv.fr/documentation/documents-budgetaires-lois/exercice-2026", "réponse HTTP 200 de 212 octets : défi Incapsula, aucun index lisible"),
    ("exercice2027", "Index budgétaire exercice 2027", "Direction du Budget", "", "https://www.budget.gouv.fr/documentation/documents-budgetaires-lois/exercice-2027", "réponse HTTP 200 de 212 octets : défi Incapsula, aucun index lisible"),
    ("decret_cnracl", "Décret n° 2025-86, article 1", "Légifrance", "2025-01-31", "https://www.legifrance.gouv.fr/jorf/article_jo/JORFARTI000051070363", "HTTP 403 ; aucun fait numérique de cette extraction ne repose sur l'extrait du moteur de recherche"),
    ("an_cas2026", "Rapport d'information n° 3066 sur le CAS Pensions et les opérateurs de recherche", "Assemblée nationale", "2026-07-15", "https://www.assemblee-nationale.fr/dyn/opendata/RINFANR5L17B3066.html", "parties I et II consultées ; distinguer les faits de financement et les positions du rapporteur ou auditionnés"),
    ("jaune2026_conseil", "Recours aux conseils extérieurs – annexe au PLF 2026", "Direction du Budget", "2025-10", "https://www.assemblee-nationale.fr/dyn/contenu/visualisation/1090037/file/27-Jaune2026_Recours_Conseils.pdf", "pp. 3-4 consultées pour contrôle du périmètre 2023-2024 ; chiffres retenus dans l'extraction issus du PLF 2027"),
]
FIELDS = ["indicateur", "programme", "categorie", "valeur", "unite", "annee", "champ",
          "nature", "convention_pensions", "source_url", "source_localisation",
          "date_publication", "statut", "formule", "note"]


def plain(alias):
    return (CACHE / f"{alias}.txt").read_text(encoding="utf-8").replace("\u00a0", " ")


def pages(alias):
    return {int(n): content for n, content in re.findall(
        r"\[PAGE (\d+)\]\n(.*?)(?=\[PAGE |\Z)", plain(alias), flags=re.S)}


def num(text):
    return float(text.replace(" ", "").replace("€", "").replace(",", ".").strip())


def cost_rows(text):
    selected = text.split("ENTREE-SORTIE")[-1] if "ENTREE-SORTIE" in text else text.split("ENTRÉE-SORTIE")[-1]
    found = {}
    for line in selected.splitlines():
        if re.match(r"^Catégorie (A\+|A|B|C)\s", line.strip()):
            parts = re.split(r"\s{2,}", line.strip())
            if len(parts) != 7:
                raise ValueError(f"Colonnes de coût ambiguës : {parts}")
            found[parts[0].removeprefix("Catégorie ")] = [num(v) for v in parts[1:]]
    if set(found) != {"A+", "A", "B", "C"}:
        raise ValueError(f"Catégories manquantes : {list(found)}")
    return found


def write_csv(path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader(); writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fetch", action="store_true")
    args = parser.parse_args()
    if args.fetch:
        spec = importlib.util.spec_from_file_location("fetch_sources", ROOT / "scripts/fetch.py")
        fetcher = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(fetcher)
        for alias, _, _, _, url, _ in SOURCES:
            if not (CACHE / f"{alias}.meta.json").exists():
                result = fetcher.fetch(url, alias, CACHE, timeout=35)
                print(alias, result.get("acces"), result.get("http_status"))
    source = {row[0]: row for row in SOURCES}
    rows = []

    def add(indicator, value, unit, year, alias, loc, *, program="", category="", nature="prévision PAP", pensions="HCAS ; autres retraites non ventilées", status="[FAIT]", formula="", note="", scope=""):
        info = source[alias]
        rows.append(dict(zip(FIELDS, [indicator, program, category, value, unit, year,
            scope or (f"Programme {program}, catégorie {category}" if category else f"Programme {program}"),
            nature, pensions, info[4], loc, info[3], status, formula, note])))

    mission = pages("pap2026_gestion")
    standalone = pages("pap2026_218")
    tables = {"156": cost_rows(mission[50]), "218": cost_rows(standalone[24])}
    if tables["218"] != cost_rows(mission[111]):
        raise ValueError("Le tableau 218 diffère entre versions mission et programme")
    metrics = ["cout_entree_hcas", "cout_global_hcas", "cout_sortie_hcas",
               "remuneration_activite_entree", "remuneration_activite_globale", "remuneration_activite_sortie"]
    for program, table in tables.items():
        alias = "pap2026_gestion" if program == "156" else "pap2026_218"
        loc = "p. 50 (PDF 50), Coûts entrée-sortie" if program == "156" else "p. imprimée 25 (PDF 24), Coûts entrée-sortie ; mission p. 111"
        for cat, values in table.items():
            for indicator, value in zip(metrics, values):
                add(indicator, value, "EUR_par_ETP_an", 2026, alias, loc, program=program, category=cat,
                    note="Moyenne prévisionnelle propre au programme et à ses flux ; ni coût national ni coût des moins de 30 ans")
            add("ecart_sortie_moins_entree_hcas", values[2] - values[0], "EUR_par_ETP_an", 2026, alias, loc,
                program=program, category=cat, status="[ESTIMATION]", formula="cout_sortie_hcas - cout_entree_hcas",
                note="Écart entre coûts moyens ; ne constitue ni un GVT agrégé ni l'économie marginale de non-remplacement")
    for program, content, alias, loc in (
        ("156", mission[49], "pap2026_gestion", "p. 49 (PDF 49), tableau Éléments salariaux ; commentaires p. 50"),
        ("218", standalone[23], "pap2026_218", "p. imprimée 24 (PDF 23), tableau Éléments salariaux"),
    ):
        gvt = {}
        for label in ("solde", "positif", "négatif"):
            match = re.search(r"^GVT\s+" + label + r"\s+(-?[\d ]+,\d+)", content, flags=re.M)
            if not match:
                raise ValueError(f"GVT {label} absent du programme {program}")
            gvt[label] = num(match.group(1))
            add("gvt_" + label, gvt[label], "MEUR", 2026, alias, loc, program=program,
                note="Variation agrégée de masse salariale HCAS ; pas un taux individuel réel de progression d'une cohorte")
        if abs(gvt["positif"] + gvt["négatif"] - gvt["solde"]) > 0.011:
            raise ValueError(f"GVT non réconcilié pour {program}")
    # Les taux ci-dessous sont des pourcentages de leur assiette légale, pas du salaire chargé total.
    match = re.search(r"^2026\s*\|\s*([\d,]+)\s*\|\s*([\d,]+)", plain("cnracl_cotisations"), flags=re.M)
    if not match:
        raise ValueError("Ligne 2026 du tableau CNRACL absente")
    for label, value in (("cnracl_retenue_salariale", num(match.group(1))), ("cnracl_contribution_employeur", num(match.group(2)))):
        add(label, value, "pourcent_assiette_CNRACL", 2026, "cnracl_cotisations", "Tableau des taux de cotisations, ligne 2026", nature="taux réglementaire publié", pensions="cotisation pension", scope="Fonctionnaires affiliés CNRACL", note="Assiette : TIB, NBI, CTI et sujétion aides-soignants selon règles applicables")
    if not re.search(r"43,65\s*%\s*en\s*2028", plain("cnracl_hausse2026")):
        raise ValueError("Trajectoire CNRACL 2028 absente")
    add("cnracl_contribution_employeur", 43.65, "pourcent_assiette_CNRACL", 2028, "cnracl_hausse2026", "Paragraphe trajectoire jusqu'en 2028", nature="taux futur prévu par la réglementation citée au 28/10/2026", pensions="cotisation pension", scope="Fonctionnaires affiliés CNRACL", note="Ne préjuge pas d'un maintien ultérieur du droit")
    sre = re.sub(r"[*_]", "", plain("sre_cotisations"))
    for label, pattern in (("cas_contribution_employeur_civils", r"contribution employeur est de ([\d,]+) %"), ("cas_retenue_salariale", r"retenue salariale est de ([\d,]+) %"), ("ati_contribution_employeur", r"contribution ATI est de ([\d,]+) %")):
        match = re.search(pattern, sre)
        if not match:
            raise ValueError(f"Taux SRE absent : {label}")
        add(label, num(match.group(1)), "pourcent_assiette_reglementaire", 2026, "sre_cotisations", "Rubrique Les taux de cotisation", nature="taux réglementaire publié", pensions="CAS pensions, sauf ATI : invalidité", scope="Fonctionnaires civils concernés, règles SRE", note="82,28 % hors ATI ; avec ATI 0,32 %, total 82,60 % sur l'assiette commune pertinente")
    advice = pages("jaune2027_conseil")[15]
    total_line = next(line for line in advice.splitlines() if line.strip().startswith("Total") and "271" in line)
    amounts = [num(v) for v in re.findall(r"(\d[\d ]*)\s*€", total_line)]
    if len(amounts) != 5:
        raise ValueError("Série des AE conseil ambiguë")
    for year, value in zip(range(2021, 2026), amounts):
        add("conseil_strategie_organisation_AE", value, "EUR_AE", year, "jaune2027_conseil", "p. 15 (PDF 15), Consommation des crédits", nature="réalisation déclarée des engagements nets", pensions="sans objet", scope="Budget général et comptes spéciaux dotés de crédits ; 8 groupes de marchandises", note="Périmètre étroit ; pas dépenses totales de prestataires, ni ETP, ni crédits de paiement ; annulations incluses")
    for base_year, base in ((2021, amounts[0]), (2024, amounts[3])):
        add(f"evolution_AE_conseil_2025_vs_{base_year}", (amounts[4] / base - 1) * 100, "pourcent", 2025,
            "jaune2027_conseil", "p. 15, série des consommations AE", nature="calcul sur réalisations", pensions="sans objet", status="[ESTIMATION]", formula=f"(AE_2025 / AE_{base_year} - 1) * 100", scope="Même périmètre de 8 GM", note="Variation des engagements, pas économie annuelle consolidée")
    for versant in ("FPE", "FPT", "FPH"):
        add("cout_entree_national_hors_toutes_pensions", "", "EUR_par_ETP_an", 2026, "pap2026_gestion", "Recherche PAP 156/218, RA DGAFP 2026 : aucun coût national des recrutements évités tous métiers/versants", program=versant, nature="paramètre non calibré", pensions="retraitement nécessaire", status="[NON TROUVÉ]", scope=versant, note="Laisser vide : HCAS par programme ne remplace pas une ventilation nationale ni les cotisations hors CAS")
    add("taux_conservation_consolide_national", "", "fraction", 2026, "jaune2027_pensions", "pp. 20-24 pour mécanismes, aucun coefficient national statique fourni", nature="paramètre non calibré", pensions="hors pensions à préciser", status="[NON TROUVÉ]", scope="APU", note="Nécessite cotisations, CSG, IR et hypothèse de retour à l'emploi ; aucune valeur forfaitaire imputée")
    add("gvt_individuel_reel_national", "", "fraction_par_an", 2026, "pap2026_gestion", "pp. 49-50 : GVT agrégés du programme 156, pas trajectoire individuelle nationale réelle", nature="paramètre non calibré", pensions="HCAS à rapprocher du hors pensions", status="[NON TROUVÉ]", scope="Cohortes des recrutements évités dans les trois versants", note="Les taux agrégés de GVT et les salaires moyens par âge ne calibrent pas ce paramètre")
    write_csv(ROOT / "data/france/01c_couts_documentes.csv", rows, FIELDS)
    registry = []
    for i, (alias, title, institution, date, url, notes) in enumerate(SOURCES, 1):
        metadata_path = CACHE / f"{alias}.meta.json"
        meta = json.loads(metadata_path.read_text(encoding="utf-8")) if metadata_path.exists() else {}
        access = meta.get("acces", "inaccessible")
        if alias in ("exercice2026", "exercice2027"):
            access = "inaccessible"
        registry.append(dict(zip(
            ["id", "titre", "institution", "date_publication", "url", "date_consultation", "acces", "sha256_16", "notes"],
            [f"01C_{i:02d}", title, institution, date, url, meta.get("date_consultation", ""), access, meta.get("sha256", "")[:16], notes])))
    write_csv(ROOT / "sources/registre_01c.csv", registry, list(registry[0]))
    print(f"{len(rows)} indicateurs ; {len(registry)} sources ; tableaux PAP et GVT réconciliés")


if __name__ == "__main__":
    main()
