#!/usr/bin/env python3
"""Modèle national de réduction des effectifs administratifs — moteur de calcul reproductible.

Principes (cf. rapport, chapitre 13) :
  * Euros constants 2026, horizon 2027-2036.
  * Registre des viviers d'effectifs (data/reformes/registre_viviers.csv) : chaque ETP public visé appartient
    à un seul vivier. Les réformes d'un même vivier s'appliquent SUCCESSIVEMENT au reliquat (ordre de priorité),
    ce qui interdit de compter deux fois le même poste (ex. suppression d'agence puis IA sur le même service).
  * Le non-remplacement est plafonné chaque année par les départs définitifs du vivier
    (taux_departs × effectif résiduel). Un excédent est reporté sur les années suivantes et signalé.
  * Économie d'un poste non remplacé = coût de l'agent NON RECRUTÉ (coût d'entrée), croissant avec
    l'ancienneté qu'il aurait acquise (GVT individuel), plafonné au coût moyen. Pensions exclues :
    la contribution employeur aux régimes de retraite des fonctionnaires finance les pensions déjà
    liquidées et ne disparaît pas avec le poste (lecture « hors CAS Pensions » de la Direction du Budget).
  * Deux lectures : (1) économie budgétaire employeur hors pensions ; (2) économie consolidée APU en statique
    (retrait des cotisations, CSG et impôts qui reviennent aux APU si l'emploi n'est pas recréé ailleurs).
  * Économies nettes = brutes − coûts récurrents − investissements − indemnités − coûts des transferts
    de charges (recrutements nécessaires ailleurs, prestataires).

Usage : python3 modele/modele.py [--hyp modele/hypotheses.json] [--out modele/resultats]
"""
import argparse
import csv
import json
import os
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCENARIOS = ["prudent", "intermediaire", "ambitieux", "radical"]


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def fnum(x, default=0.0):
    if x is None:
        return default
    x = str(x).strip().replace(" ", "").replace(",", ".")
    if x in ("", "NA", "nd", "n.d.", "-"):
        return default
    return float(x)


def load(hyp_path):
    hyp = json.load(open(hyp_path, encoding="utf-8"))
    viviers = {r["vivier_id"]: r for r in read_csv(os.path.join(ROOT, hyp["fichiers"]["viviers"]))}
    reformes = read_csv(os.path.join(ROOT, hyp["fichiers"]["reformes"]))
    return hyp, viviers, reformes


def cout_annuel(hyp, versant, annees_depuis_non_recrutement):
    """Coût évité (k€ 2026) d'un poste non pourvu, n années après la date où il aurait été pourvu."""
    c = hyp["couts_k_eur"][versant]
    entree, moyen = c["cout_entree_hors_pension"], c["cout_moyen_hors_pension"]
    g = hyp["gvt_individuel_reel"]
    return min(moyen, entree * (1 + g) ** annees_depuis_non_recrutement)


def run_scenario(hyp, viviers, reformes, sc):
    years = list(range(hyp["annee_debut"], hyp["annee_fin"] + 1))
    out_reform = []
    by_year = {y: defaultdict(float) for y in years}
    alerts = []

    # regroupement par vivier, ordre de priorité croissant
    per_vivier = defaultdict(list)
    for r in reformes:
        if fnum(r.get(f"taux_{sc}")) <= 0 and fnum(r.get(f"eco_fonct_meur_{sc}")) <= 0:
            continue
        per_vivier[r["vivier_id"]].append(r)
    for v in per_vivier:
        per_vivier[v].sort(key=lambda r: fnum(r.get("ordre"), 99))

    for vid, lst in per_vivier.items():
        if vid not in viviers:
            alerts.append(f"vivier inconnu {vid}")
            continue
        V = viviers[vid]
        base = fnum(V["etp_base"])
        versant = V["versant"]
        taux_dep = fnum(V["taux_departs_annuel"])
        plafond = fnum(V.get("plafond_reduction_" + sc), 1.0)
        residuel = base
        reduit_total = 0.0
        # stock de capacité de départs consommée par les réformes précédentes du même vivier, par année
        dep_consommes = {y: 0.0 for y in years}
        for r in lst:
            taux = fnum(r.get(f"taux_{sc}"))
            etp_cible = taux * residuel
            # respect du plafond de soutenabilité du vivier
            if reduit_total + etp_cible > plafond * base:
                etp_cible = max(0.0, plafond * base - reduit_total)
                alerts.append(f"{r['id']}: plafond du vivier {vid} atteint ({sc})")
            p_nr = fnum(r.get("part_non_remplacement"), 1.0)
            p_sup = fnum(r.get("part_suppression_indemnisee"), 0.0)
            p_red = fnum(r.get("part_redeploiement"), 0.0)
            p_tr = fnum(r.get("part_transfert"), 0.0)
            tot = p_nr + p_sup + p_red + p_tr
            if abs(tot - 1) > 1e-6:
                alerts.append(f"{r['id']}: parts de mode != 1 ({tot:.2f}), normalisées")
                p_nr, p_sup, p_red, p_tr = (p / tot for p in (p_nr, p_sup, p_red, p_tr))
            debut = int(fnum(r.get("annee_debut"), hyp["annee_debut"]))
            duree = max(1, int(fnum(r.get(f"duree_ans_{sc}"), fnum(r.get("duree_ans"), 5))))
            # trajectoire cible : linéaire sur la durée
            cible_annuelle = {y: (etp_cible / duree if debut <= y < debut + duree else 0.0) for y in years}
            # non-remplacement plafonné par les départs disponibles du vivier ; report des excédents
            report = 0.0
            cum_nr, cum_sup, cum_red, cum_tr = 0.0, 0.0, 0.0, 0.0
            flux_nr = {}
            res_y = residuel
            for y in years:
                demande_nr = cible_annuelle[y] * p_nr + report
                dispo = max(0.0, taux_dep * (base - reduit_total - cum_nr - cum_sup - cum_red - cum_tr) - dep_consommes[y])
                f = min(demande_nr, dispo)
                report = demande_nr - f
                dep_consommes[y] += f
                flux_nr[y] = f
                cum_nr += f
                cum_sup += cible_annuelle[y] * p_sup
                cum_red += cible_annuelle[y] * p_red
                cum_tr += cible_annuelle[y] * p_tr
            if report > 1:
                alerts.append(f"{r['id']}: {report:,.0f} ETP de non-remplacement non réalisables d'ici {years[-1]} "
                              f"(départs insuffisants dans {vid}, {sc})")
            # économies annuelles
            cfac = hyp["facteur_transfert_cout"]
            ind = hyp["indemnite_depart_k_eur"]
            inv_total = fnum(r.get(f"invest_meur_{sc}"))
            inv_duree = max(1, int(fnum(r.get("invest_duree_ans"), 3)))
            rec = fnum(r.get(f"cout_recurrent_meur_{sc}"))
            eco_f = fnum(r.get(f"eco_fonct_meur_{sc}"))
            recettes = fnum(r.get(f"effet_recettes_meur_{sc}"))
            cohortes = []  # (annee, etp) pour le calcul du coût évité croissant
            cum = {"nr": 0.0, "sup": 0.0, "red": 0.0, "tr": 0.0}
            res_r = {"id": r["id"], "intitule": r["intitule"], "vivier": vid, "scenario": sc,
                     "etp_cible": etp_cible}
            cumul_net = 0.0
            for y in years:
                cohortes.append((y, flux_nr[y] + cible_annuelle[y] * p_sup))
                cum["nr"] += flux_nr[y]
                cum["sup"] += cible_annuelle[y] * p_sup
                cum["red"] += cible_annuelle[y] * p_red
                cum["tr"] += cible_annuelle[y] * p_tr
                # économie brute masse salariale (k€ -> M€)
                eco_ms = sum(e * cout_annuel(hyp, versant, y - y0) for (y0, e) in cohortes) / 1000.0
                # transferts : l'activité est reprise ailleurs à un coût = facteur × coût moyen
                cout_tr = cum["tr"] * hyp["couts_k_eur"][versant]["cout_moyen_hors_pension"] * cfac / 1000.0
                eco_ms_nette_tr = eco_ms + cum["tr"] * hyp["couts_k_eur"][versant]["cout_moyen_hors_pension"] / 1000.0 - cout_tr
                montee = min(1.0, max(0.0, (y - debut + 1) / duree)) if y >= debut else 0.0
                eco_fonct = eco_f * montee
                invest = inv_total / inv_duree if debut - 1 <= y < debut - 1 + inv_duree else 0.0
                indem = cible_annuelle[y] * p_sup * ind / 1000.0
                cout_rec = rec * montee
                brut = eco_ms_nette_tr + eco_fonct
                net = brut - invest - indem - cout_rec + recettes * montee
                consolide = eco_ms * hyp["taux_conservation_consolide"] + eco_fonct - invest - indem - cout_rec + recettes * montee
                cumul_net += net
                b = by_year[y]
                b["etp_non_remplaces"] += flux_nr[y]
                b["etp_supprimes_indemnises"] += cible_annuelle[y] * p_sup
                b["etp_redeployes"] += cible_annuelle[y] * p_red
                b["etp_transferes"] += cible_annuelle[y] * p_tr
                b["eco_brute_meur"] += brut
                b["invest_meur"] += invest
                b["indemnites_meur"] += indem
                b["cout_recurrent_meur"] += cout_rec
                b["eco_nette_meur"] += net
                b["eco_consolidee_apu_meur"] += consolide
                res_r[f"net_{y}"] = net
            res_r.update({
                "etp_non_remplaces": cum["nr"], "etp_supprimes_indemnises": cum["sup"],
                "etp_redeployes": cum["red"], "etp_transferes": cum["tr"],
                "etp_postes_en_moins": cum["nr"] + cum["sup"] + cum["tr"],
                "cumul_net_5ans": sum(res_r[f"net_{y}"] for y in years[:5]),
                "cumul_net_10ans": cumul_net,
                "net_regime_" + str(years[-1]): res_r[f"net_{years[-1]}"],
                "confiance": r.get("confiance", ""),
            })
            out_reform.append(res_r)
            reduit_total += cum["nr"] + cum["sup"] + cum["red"] + cum["tr"]
            residuel = base - reduit_total
    return out_reform, by_year, alerts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hyp", default=os.path.join(ROOT, "modele", "hypotheses.json"))
    ap.add_argument("--out", default=os.path.join(ROOT, "modele", "resultats"))
    a = ap.parse_args()
    hyp, viviers, reformes = load(a.hyp)
    os.makedirs(a.out, exist_ok=True)
    synth = []
    all_alerts = []
    for sc in SCENARIOS:
        per_r, by_year, alerts = run_scenario(hyp, viviers, reformes, sc)
        all_alerts += [f"[{sc}] {x}" for x in alerts]
        years = sorted(by_year)
        with open(os.path.join(a.out, f"reformes_{sc}.csv"), "w", newline="", encoding="utf-8") as f:
            if per_r:
                keys = list(per_r[0].keys())
                w = csv.DictWriter(f, fieldnames=keys)
                w.writeheader()
                for row in per_r:
                    w.writerow({k: (round(v, 1) if isinstance(v, float) else v) for k, v in row.items()})
        with open(os.path.join(a.out, f"trajectoire_{sc}.csv"), "w", newline="", encoding="utf-8") as f:
            keys = ["annee"] + list(next(iter(by_year.values())).keys())
            w = csv.writer(f)
            w.writerow(keys)
            for y in years:
                w.writerow([y] + [round(by_year[y][k], 1) for k in keys[1:]])
        last = years[-1]
        cum_etp = sum(by_year[y]["etp_non_remplaces"] + by_year[y]["etp_supprimes_indemnises"] + by_year[y]["etp_transferes"] for y in years)
        cum_etp5 = sum(by_year[y]["etp_non_remplaces"] + by_year[y]["etp_supprimes_indemnises"] + by_year[y]["etp_transferes"] for y in years[:5])
        synth.append({
            "scenario": sc,
            "postes_en_moins_5ans": round(cum_etp5),
            "postes_en_moins_10ans": round(cum_etp),
            "etp_redeployes_10ans": round(sum(by_year[y]["etp_redeployes"] for y in years)),
            "eco_brute_annee5_meur": round(by_year[years[4]]["eco_brute_meur"]),
            "eco_nette_annee5_meur": round(by_year[years[4]]["eco_nette_meur"]),
            f"eco_nette_{last}_meur": round(by_year[last]["eco_nette_meur"]),
            f"eco_consolidee_{last}_meur": round(by_year[last]["eco_consolidee_apu_meur"]),
            "cumul_net_5ans_meur": round(sum(by_year[y]["eco_nette_meur"] for y in years[:5])),
            "cumul_net_10ans_meur": round(sum(by_year[y]["eco_nette_meur"] for y in years)),
            "invest_total_meur": round(sum(by_year[y]["invest_meur"] for y in years)),
        })
    with open(os.path.join(a.out, "synthese_scenarios.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(synth[0].keys()))
        w.writeheader()
        w.writerows(synth)
    with open(os.path.join(a.out, "alertes.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(all_alerts) + "\n")
    for s in synth:
        print(s)
    print(f"{len(all_alerts)} alertes -> {os.path.join(a.out, 'alertes.txt')}")


if __name__ == "__main__":
    main()
