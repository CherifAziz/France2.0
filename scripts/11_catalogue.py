#!/usr/bin/env python3
"""Construit le catalogue des réformes, le registre des viviers et les fiches A–M.

Entrées : contenu rédigé dans scripts/11_fiches_*.py, hypothèses modele/hypotheses.json.
Sorties : data/reformes/registre_viviers.csv, data/reformes/catalogue_reformes.csv,
recherche/fiches/RNN_*.md, recherche/11_catalogue_reformes.md et modele/resultats/.

Les investissements sont dérivés des cibles calculées par le moteur (premier passage
sans investissement), puis le moteur est relancé : les rubriques G des fiches
reprennent exactement ses résultats. Aucun téléchargement ; aucun extracteur auteur.
"""
import csv
import importlib.util
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SC = ["prudent", "intermediaire", "ambitieux", "radical"]
SC_LABEL = {"prudent": "Prudent", "intermediaire": "Intermédiaire", "ambitieux": "Ambitieux", "radical": "Radical"}


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


modele = load_module(ROOT / "modele/modele.py", "modele")
FICHES = load_module(ROOT / "scripts/11_fiches_etat.py", "fiches_etat").FICHES \
    + load_module(ROOT / "scripts/11_fiches_local_social.py", "fiches_local").FICHES

DEP_FPE = 39146 / 1501736   # pensions civiles FPE 2025 / fonctionnaires FPE fin 2024
DEP_FPT = 46897 / 1417086
DEP_FPH = 22753 / 827014
# plafonds communs : bornés par les contractions observées (Irlande −9,6 %, Portugal −12 %, Royaume-Uni −20,2 %) ;
# le radical dépasse tout précédent et n'est pas démontré.
PLAFONDS = (0.05, 0.12, 0.20, 0.35)
VIVIERS = [
    dict(vivier_id="V_DGFIP", description="DGFiP, titulaires et contractuels en fonction 2025",
         versant="FPE_DGFIP", etp_base=round(94569 * 2579100 / 2581870, 1), taux_departs_annuel=DEP_FPE,
         sources="DGFiP cahier statistique 2025 PDF p.46-47 (88 659 + 5 910 PP) ; conversion EQTP/PP FPE 2024 (IP2094 / DGAFP) ; départs : pensions civiles FPE 2025 / fonctionnaires FPE",
         chevauchement="Inclus dans les corps administratifs et techniques FPE ; retiré de V_FPE_AUTRES. Millésime 2025 contre 2024."),
    dict(vivier_id="V_FPE_AUTRES", description="Autres corps administratifs et techniques de la FPE (ministères et EPA, dont opérateurs)",
         versant="FPE", etp_base=round((378909 - 94569 - 52432) * 2579100 / 2581870, 1), taux_departs_annuel=DEP_FPE,
         sources="DGAFP RA 2026 postes FPE figure 2 B11+B26+B37 (79 668 + 157 099 + 142 142) moins DGFiP et filière administrative scolaire",
         chevauchement="Fonctionnaires seulement (total de la figure = 1 501 736 fonctionnaires FPE, contrôle V5-04) : contractuels administratifs absents. Mêle personnels administratifs et techniques. La DGFiP et le scolaire soustraits incluent des contractuels : base légèrement sous-estimée."),
    dict(vivier_id="V_MEN_ADM", description="Filière administrative de l'Éducation nationale",
         versant="FPE", etp_base=50849, taux_departs_annuel=DEP_FPE,
         sources="DEPP, personnels non enseignants, tableau 3.1 L27 (ETP au 30/11/2025)",
         chevauchement="Retirée de V_FPE_AUTRES (52 432 PP)."),
    dict(vivier_id="V_FPT_ADM", description="Filière administrative de la fonction publique territoriale",
         versant="FPT", etp_base=round(453224 * 1980400 / 2017830, 1), taux_departs_annuel=DEP_FPT,
         sources="DGAFP RA 2026 postes FPT figure 1 filière S28 ; conversion EQTP/PP FPT 2024 ; départs : pensions CNRACL FPT 2025 / fonctionnaires FPT",
         chevauchement="Filière statutaire, pas mesure des tâches ; disjointe des autres viviers."),
    dict(vivier_id="V_FPH_ADM", description="Filière administrative de la fonction publique hospitalière",
         versant="FPH", etp_base=round(121829 * 1222300 / 1248591, 1), taux_departs_annuel=DEP_FPH,
         sources="DGAFP RA 2026 postes FPH figure 1 filière T25 ; conversion EQTP/PP FPH 2024 ; départs : pensions CNRACL FPH 2025 / fonctionnaires FPH",
         chevauchement="Ne pas superposer aux postes SAE (110 089)."),
    dict(vivier_id="V_OPS", description="Organismes de protection sociale (droit privé, financement public prédominant)",
         versant="HORS_FP", etp_base=162623, taux_departs_annuel=DEP_FPE,
         sources="DGAFP RA 2026 effectifs, figure 3 (162 623 PP fin 2024), utilisées comme majorant des ETP ; taux de départ FPE faute de donnée propre",
         chevauchement="Hors fonction publique ; tous métiers des caisses, pas seulement les fonctions support."),
    dict(vivier_id="V_FT", description="France Travail",
         versant="HORS_FP", etp_base=48232, taux_departs_annuel=DEP_FPE,
         sources="Jaune Opérateurs PLF 2027, plafond d'emplois 2027 (48 232 ETPT) ; taux de départ FPE faute de donnée propre",
         chevauchement="Agents de droit privé : absents des corps de fonctionnaires de V_FPE_AUTRES (contrôle V5-04), donc disjoints."),
    dict(vivier_id="V_FONCT", description="Dépenses de fonctionnement sans effectif (achats, immobilier, instances)",
         versant="FPE", etp_base=0, taux_departs_annuel=0,
         sources="Sans effectif : les fiches y portent des économies de fonctionnement en M€",
         chevauchement="Sans objet."),
]
VIV = {v["vivier_id"]: v for v in VIVIERS}
FIELDS = ["id", "intitule", "vivier_id", "ordre", *[f"taux_{s}" for s in SC],
          "part_non_remplacement", "part_suppression_indemnisee", "part_redeploiement", "part_transfert", "type_transfert",
          "annee_debut", "duree_ans", *[f"invest_meur_{s}" for s in SC], "invest_duree_ans",
          *[f"cout_recurrent_meur_{s}" for s in SC], "cout_recurrent_proportionnel", *[f"eco_fonct_meur_{s}" for s in SC], *[f"effet_recettes_meur_{s}" for s in SC],
          "confiance", "mode_investissement", "fiche", "sources"]


def slug(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")[:48]


def rows_for(fiches, money):
    rows = []
    for f in fiches:
        r = {"id": f["id"], "intitule": f["titre"], "vivier_id": f["vivier"], "ordre": f["ordre"],
             "part_non_remplacement": f["parts"][0], "part_suppression_indemnisee": f["parts"][1],
             "part_redeploiement": f["parts"][2], "part_transfert": f["parts"][3], "type_transfert": "",
             "annee_debut": f["debut"], "duree_ans": f["duree"], "invest_duree_ans": 3 if f["invest"] == "ia" else 2,
             "confiance": f["confiance"], "mode_investissement": f["invest"],
             "cout_recurrent_proportionnel": int(f["recurrent"] == "retro"),
             "fiche": f"recherche/fiches/{f['id']}_{slug(f['titre'])}.md",
             "sources": " ; ".join(url for _, url in f["S"] if url.startswith("http"))}
        for i, s in enumerate(SC):
            r[f"taux_{s}"] = f["taux"][i]
            inv, rec = money.get((f["id"], s), (0.0, 0.0))
            r[f"invest_meur_{s}"] = round(inv, 3)
            r[f"cout_recurrent_meur_{s}"] = round(rec, 3)
            r[f"eco_fonct_meur_{s}"] = f.get("eco_fonct", (0, 0, 0, 0))[i]
            r[f"effet_recettes_meur_{s}"] = f.get("recettes", (0, 0, 0, 0))[i]
        rows.append(r)
    return rows


def write_csv(path, rows, fields):
    with open(path, "w", encoding="utf-8", newline="") as stream:
        w = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def money_from_targets(hyp, fiches):
    """Investissements et coûts récurrents dérivés des cibles du moteur (premier passage)."""
    viviers = {v["vivier_id"]: {**v, **{f"plafond_reduction_{s}": PLAFONDS[i] for i, s in enumerate(SC)}} for v in VIVIERS}
    rows = [{k: str(v) for k, v in r.items()} for r in rows_for(fiches, {})]
    money = {}
    for s in SC:
        _, plans, _ = modele.prepare(hyp, viviers, rows, s)
        targets = {p["row"]["id"]: p["target"] for lst in plans.values() for p in lst}
        for f in fiches:
            i = SC.index(s)
            entry = hyp["couts_k_eur"][VIV[f["vivier"]]["versant"]]["cout_entree_hors_pension"]
            gross = targets[f["id"]] * f["parts"][0] * entry / 1000  # M€/an en régime permanent, au coût d'entrée
            base = VIV[f["vivier"]]["etp_base"]
            active = f["taux"][i] > 0
            inv = rec = 0.0
            if f["invest"] == "payback":
                inv = 2 * gross
            elif f["invest"] == "payback3":
                inv = 3 * gross
            elif f["invest"] == "ia" and active:
                inv = 0.267 * base / 1000
            if f["recurrent"] == "ia" and active:
                rec = 0.0105 * base / 1000
            elif f["recurrent"] == "retro":
                rec = 0.5 * gross
            money[(f["id"], s)] = (inv, rec)
    return money


def fmt(x, d=0):
    if x is None:
        return "—"
    s = f"{x:,.{d}f}".replace(",", " ").replace(".", ",")
    return "0" if s in ("-0", "−0") else s.replace("-", "−")


def read_results():
    out = {}
    for s in SC:
        with open(ROOT / f"modele/resultats/reformes_{s}.csv", encoding="utf-8") as stream:
            for r in csv.DictReader(stream):
                out[(r["id"], s)] = {k: (float(v) if re.fullmatch(r"-?[\d.e+-]+", v or "") else v) for k, v in r.items()}
    with open(ROOT / "modele/resultats/synthese_scenarios.csv", encoding="utf-8") as stream:
        synth = {r["scenario"]: r for r in csv.DictReader(stream)}
    with open(ROOT / "modele/resultats/alertes.txt", encoding="utf-8") as stream:
        alerts = [a for a in stream.read().splitlines() if a]
    return out, synth, alerts


def section_g(f, res, catalogue):
    lines = ["| Indicateur | " + " | ".join(SC_LABEL[s] for s in SC) + " |", "|---|" + "---:|" * 4]
    row = lambda label, key, d=0: f"| {label} | " + " | ".join(fmt(res[(f['id'], s)][key], d) for s in SC) + " |"
    lines += [row("ETP visés (cible)", "etp_cible"), row("Postes en moins en 2036", "etp_postes_en_moins"),
              row("ETP redéployés", "etp_redeployes"), row("Cible non réalisée en 2036 (ETP)", "etp_cible_non_realisee"),
              row("Économie nette 2036 (M€)", "net_annee_finale_meur", 1),
              row("Cumul net 2027-2031 (M€)", "cumul_net_5ans", 1), row("Cumul net 2027-2036 (M€)", "cumul_net_10ans", 1),
              row("Cumul consolidé APU 2027-2036 (M€)", "cumul_consolide_10ans", 1)]
    inv = " | ".join(fmt(float(catalogue[f["id"]][f"invest_meur_{s}"]), 1) for s in SC)
    rec = " | ".join(fmt(float(catalogue[f["id"]][f"cout_recurrent_meur_{s}"]), 1) for s in SC)
    lines += [f"| Investissement total (M€) | {inv} |", f"| Coût récurrent à terme (M€/an) | {rec} |"]
    return "\n".join(lines)


def write_fiche(f, res, catalogue, path):
    v = VIV[f["vivier"]]
    src = "\n".join(f"- [{label}]({url})" for label, url in f["S"])
    text = f"""# Réforme {f['id']} — {f['titre']}

Vivier : **{f['vivier']}** ({v['description']}) · ordre d'application **{f['ordre']}** · début **{f['debut']}**, durée **{f['duree']} ans** · confiance **{f['confiance']}**.

**A. Problème identifié.** {f['A']}

**B. Organisation actuelle.** {f['B']}

**C. Comparaison internationale.** {f['C']}

**D. Réforme proposée.** {f['D']}

**E. Effectifs concernés.** {f['E']}

**F. Réduction envisageable.** {f['F']} Taux appliqués au reliquat du vivier : {' / '.join(fmt(t * 100, 2) + ' %' for t in f['taux'])} (prudent / intermédiaire / ambitieux / radical). Répartition : non-remplacement {fmt(f['parts'][0] * 100)} %, redéploiement {fmt(f['parts'][2] * 100)} %, suppression indemnisée {fmt(f['parts'][1] * 100)} %, transfert {fmt(f['parts'][3] * 100)} %.

**G. Économies.** Résultats du moteur financier (`modele/modele.py`), en M€ 2026 constants, par écart à une référence qui remplace tous les départs. Le non-remplacement est valorisé au coût d'entrée hors pension, croissant de 1 % par an jusqu'au coût moyen ; les postes ne disparaissent qu'au rythme des départs à la retraite du vivier.

{section_g(f, res, catalogue)}

**H. Investissements nécessaires.** {f['H']}

**I. Conséquences sur le service.** {f['I']}

**J. Contraintes.** {f['J']}

**K. Calendrier.** {f['K']}

**L. Niveau de confiance.** {f['L']}

**Indicateur de validation à 2-3 ans.** {f['V']}

**M. Sources et calculs.**

{src}

Calculs : {f['calc']} Paramètres nationaux : [hypotheses.json](../../modele/hypotheses.json) ; ligne `{f['id']}` de [catalogue_reformes.csv](../../data/reformes/catalogue_reformes.csv) ; vivier dans [registre_viviers.csv](../../data/reformes/registre_viviers.csv). Reproduction : `python -I scripts/11_catalogue.py`.
"""
    path.write_text(text, encoding="utf-8", newline="\n")


def alert_fr(alert):
    m = re.match(r"\[(\w+)\] (R\d+) : ([\d,.]+) ETP de non-remplacement demandés mais non réalisés en (\d+) \((\w+), \w+\)", alert)
    if not m:
        return alert
    sc, rid, etp, year, vid = m.groups()
    return f"en scénario {SC_LABEL[sc].lower()}, {fmt(float(etp.replace(',', '')))} ETP de {rid} restent non réalisés en {year} faute de départs dans {vid}"


def write_index(res, synth, alerts, rows, hyp):
    s = lambda sc, k: float(synth[sc][k])
    total_base = sum(v["etp_base"] for v in VIVIERS)
    max_cap = sum(v["etp_base"] * PLAFONDS[3] for v in VIVIERS)
    lines = ["# 11 — Catalogue des réformes chiffrées", "",
             "Catalogue arrêté au **30 octobre 2026**. Trente fiches de réforme suivent la structure A à M du cahier des charges, avec un indicateur de validation à deux ou trois ans. Chaque fait cité provient d'une note des lots 1 à 3 contre-vérifiée ; chaque taux de réduction est une **[HYPOTHÈSE]** rattachée à un précédent observé. Les économies sont calculées par le moteur financier sur la même base pour toutes les fiches. **Ces totaux sont préliminaires** : les analyses de sensibilité, le test formel des seuils et la contre-expertise relèvent des phases 4 et 5.", "",
             "## 1. Résultats préliminaires par scénario", "",
             "| Indicateur | " + " | ".join(SC_LABEL[x] for x in SC) + " |", "|---|" + "---:|" * 4]
    for label, key, d in [("Postes en moins en 2031", "postes_en_moins_5ans", 0), ("Postes en moins en 2036", "postes_en_moins_10ans", 0),
                          ("Économie nette en 2036 (M€)", "eco_nette_2036_meur", 0), ("Économie consolidée APU en 2036 (M€)", "eco_consolidee_2036_meur", 0),
                          ("Cumul net 2027-2031 (M€)", "cumul_net_5ans_meur", 0), ("Cumul net 2027-2036 (M€)", "cumul_net_10ans_meur", 0),
                          ("Investissements 2027-2036 (M€)", "invest_horizon_meur", 0)]:
        lines.append(f"| {label} | " + " | ".join(fmt(s(x, key), d) for x in SC) + " |")
    lines += ["",
              f"**Aucun scénario n'approche 500 000 postes.** Le scénario radical retire environ **{fmt(s('radical', 'postes_en_moins_10ans'))} postes en 2036**, pour **{fmt(s('radical', 'eco_nette_2036_meur') / 1000, 1)} Md€** d'économie nette annuelle. "
              f"Les sept viviers administratifs réunissent **{fmt(total_base)} ETP** ; même en retirant 35 % de chacun (plafond du scénario radical, au-delà de tout précédent observé), on obtiendrait **{fmt(max_cap)} postes**. "
              "Atteindre 500 000 ou 800 000 postes supposerait donc de réduire aussi des métiers non administratifs (enseignants, soignants, forces de sécurité), ce que ni le plan audité ni ce catalogue ne proposent.", "",
              "Les départs à la retraite limitent aussi le rythme : " + (" ; ".join(alert_fr(a) for a in alerts) if alerts else "aucune cible n'est bloquée par les départs") + ".", "",
              f"Le cumul net sur 2027-2031 est {'négatif' if s('radical', 'cumul_net_5ans_meur') < 0 else 'faible'} dans le scénario radical ({fmt(s('radical', 'cumul_net_5ans_meur'))} M€) : les investissements précèdent les économies, qui n'apparaissent qu'au rythme des départs.", "",
              "La masse des économies vient des mutualisations de fonctions support (communes, opérateurs, caisses, hôpitaux) et de la revue des opérateurs. L'IA pèse peu : aucune source ne montre de conversion du temps libéré en postes, et France Travail a réaffecté le sien.", "",
              "## 2. Méthode", "", "### 2.1 Viviers disjoints", "",
              "| Vivier | Description | ETP de base | Taux de départ annuel | Source | Recouvrements |", "|---|---|---:|---:|---|---|"]
    for v in VIVIERS:
        lines.append(f"| {v['vivier_id']} | {v['description']} | {fmt(v['etp_base'])} | {fmt(v['taux_departs_annuel'] * 100, 2)} % | {v['sources']} | {v['chevauchement']} |")
    lines += ["", "Plafonds de réduction par vivier : **5 / 12 / 20 / 35 %** (prudent / intermédiaire / ambitieux / radical). Les trois premiers encadrent les contractions observées à l'étranger (Irlande −9,6 %, Portugal −12 %, Royaume-Uni −20,2 %, toutes suivies d'un rebond) ; le radical les dépasse et n'est pas démontré.", "",
              "Le taux de départ retenu est celui des **départs à la retraite des fonctionnaires civils** (pensions 2025 / fonctionnaires fin 2024, par versant). C'est une borne prudente : les sorties de contractuels, plus nombreuses, sont souvent des fins de contrat remplacées et ne libèrent pas de postes.", "",
              "### 2.2 Hypothèses nationales", "",
              "| Paramètre | Valeur | Justification |", "|---|---|---|"]
    for versant, c in hyp["couts_k_eur"].items():
        lines.append(f"| Coût d'entrée / moyen hors pension, {versant} | {fmt(c['cout_entree_hors_pension'], 2)} / {fmt(c['cout_moyen_hors_pension'], 2)} k€ | {c['_source']} |")
    for key, src in [("gvt_individuel_reel", "_gvt_source"), ("taux_conservation_consolide", "_conservation_source"),
                     ("facteur_transfert_cout", "_transfert_source"), ("fraction_economie_premiere_annee", "_fraction_source")]:
        lines.append(f"| {key} | {fmt(hyp[key], 2)} | {hyp[src]} |")
    lines += ["", "### 2.3 Conventions", "",
              "- **Référence.** Les économies sont des écarts à une trajectoire qui remplace tous les départs. Les mouvements déjà votés ou engagés (schémas d'emplois du PLF 2027, foncière immobilière, investissements IA de France Travail) sont dans la référence et ne sont pas recomptés.",
              "- **Ordre et non-cumul.** Dans chaque vivier, les réformes s'appliquent au reliquat, dans l'ordre structures (10-19), simplification (20-29), mutualisation (30-39), IA (40-49), règle transversale (50). Un même poste ne peut être compté deux fois.",
              "- **Investissements.** Faute de coûts publiés, convention de **deux années d'économie brute** (sur le modèle du timbre électronique : 2,65 M€, retour en deux ans), **trois années** pour les projets à risque élevé (paie, suppression d'un échelon). Pour l'IA, analogie avec France Travail 2025 : 267 € par ETP d'investissement, 10,5 € par ETP et par an de fonctionnement.",
              "- **Pas de licenciement.** Les réductions passent par le non-remplacement des départs ou le redéploiement ; aucune fiche ne recourt à la suppression indemnisée de postes de fonctionnaires.",
              "- **Fiches à effet nul.** R03 (redéploiement), R23 (recettes seulement), R27 (externalisation non retenue) et R30 (non chiffrable) restent au catalogue pour documenter les choix.", "",
              "## 3. Les trente fiches", "",
              "| Fiche | Vivier | Confiance | Postes en moins 2036 (P / I / A / R) | Économie nette 2036, M€ (P / I / A / R) |", "|---|---|---|---|---|"]
    for r in rows:
        link = r["fiche"].replace("recherche/", "")
        postes = " / ".join(fmt(res[(r["id"], x)]["etp_postes_en_moins"]) for x in SC)
        net = " / ".join(fmt(res[(r["id"], x)]["net_annee_finale_meur"]) for x in SC)
        lines.append(f"| [{r['id']} — {r['intitule']}]({link}) | {r['vivier_id']} | {r['confiance']} | {postes} | {net} |")
    lines += ["", "## 4. Limites", "",
              "- Les taux de réduction sont des hypothèses : aucune fiche ne repose sur une mesure française de postes effectivement supprimés après réforme.",
              "- Les coûts territoriaux, hospitaliers et des organismes de droit privé sont des proxys du coût de l'État ; les investissements suivent une convention, pas des devis.",
              "- Les viviers sont des filières ou des corps statutaires, pas des mesures de tâches ; le vivier de l'État mêle personnels administratifs et techniques.",
              "- Les effets sur les pensions futures, la sous-traitance et les indicateurs de service sont qualitatifs dans les fiches ; ils seront quantifiés quand les données le permettront.",
              "- La phase 5 testera la sensibilité au coût par ETP, au taux de départ, au GVT, à la conversion du temps libéré par l'IA et au taux de conservation APU.", "",
              "## 5. Reproduction", "", "```powershell", "python -I scripts/11_catalogue.py", "```", "",
              "Le script écrit `data/reformes/registre_viviers.csv`, `data/reformes/catalogue_reformes.csv`, les fiches de `recherche/fiches/` et ce document, puis exécute `modele/modele.py` dont les résultats sont dans `modele/resultats/`. Le contenu rédigé des fiches est dans `scripts/11_fiches_etat.py` et `scripts/11_fiches_local_social.py`.", ""]
    (ROOT / "recherche/11_catalogue_reformes.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")


def main():
    hyp_path = ROOT / "modele/hypotheses.json"
    hyp = json.loads(hyp_path.read_text(encoding="utf-8"))
    viv_rows = [{**{k: v[k] for k in ("vivier_id", "description", "versant", "etp_base")},
                 "taux_departs_annuel": round(v["taux_departs_annuel"], 6),
                 **{f"plafond_reduction_{s}": PLAFONDS[i] for i, s in enumerate(SC)},
                 "sources": v["sources"], "chevauchement": v["chevauchement"]} for v in VIVIERS]
    write_csv(ROOT / "data/reformes/registre_viviers.csv", viv_rows, list(viv_rows[0]))
    money = money_from_targets(hyp, FICHES)
    rows = rows_for(FICHES, money)
    write_csv(ROOT / "data/reformes/catalogue_reformes.csv", rows, FIELDS)
    subprocess.run([sys.executable, "-I", str(ROOT / "modele/modele.py"), "--hyp", str(hyp_path),
                    "--out", str(ROOT / "modele/resultats")], check=True)
    res, synth, alerts = read_results()
    catalogue = {r["id"]: r for r in rows}
    out = ROOT / "recherche/fiches"
    out.mkdir(exist_ok=True)
    for f in FICHES:
        write_fiche(f, res, catalogue, ROOT / catalogue[f["id"]]["fiche"])
    write_index(res, synth, alerts, rows, hyp)
    json.dump({"fiches": len(FICHES), "viviers": len(VIVIERS), "alertes": len(alerts),
               "synthese": {s: {k: synth[s][k] for k in ("postes_en_moins_10ans", "eco_nette_2036_meur", "cumul_net_10ans_meur")} for s in SC}},
              sys.stdout, ensure_ascii=False, indent=1)
    print()


if __name__ == "__main__":
    main()
