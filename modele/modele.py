#!/usr/bin/env python3
"""Moteur de scénarios en euros constants, sans calibration nationale intégrée.

Voir modele/README.md pour les conventions et le périmètre financier. Les cibles
successives portent sur des fractions distinctes du vivier initial. La simulation
des départs porte sur le stock réellement présent au début de chaque année.
Les ETP sont des espérances continues, pas des nombres de personnes individuelles.
"""
import argparse
import csv
import json
import math
import os
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCENARIOS = ["prudent", "intermediaire", "ambitieux", "radical"]
MODES = ("non_remplacement", "suppression_indemnisee", "redeploiement", "transfert")
MONEY = ("invest_meur", "cout_recurrent_meur", "eco_fonct_meur", "effet_recettes_meur")
YEAR_FIELDS = (
    "etp_non_remplaces", "etp_supprimes_indemnises", "etp_redeployes", "etp_transferes",
    "etp_recrutements_publics_destination", "etp_postes_apu_en_moins",
    "etp_postes_origine_en_moins_stock", "etp_postes_apu_en_moins_stock",
    "etp_departs_disponibles", "etp_departs_utilises",
    "eco_masse_salariale_origine_meur", "eco_fonctionnement_meur", "eco_brute_meur",
    "cout_transferts_meur", "cout_transferts_charge_source_meur", "invest_meur",
    "indemnites_meur", "cout_recurrent_meur", "effet_recettes_meur",
    "eco_nette_meur", "eco_consolidee_apu_meur",
)
EPS = 1e-8


def read_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def fnum(x, default=0.0):
    """Lecture des nombres CSV ; les champs obligatoires utilisent number()."""
    if x is None:
        return default
    x = str(x).strip().replace("\u00a0", "").replace(" ", "").replace(",", ".")
    if x.lower() in ("", "na", "nd", "n.d.", "-"):
        return default
    value = float(x)
    if not math.isfinite(value):
        raise ValueError(f"Nombre non fini : {x!r}")
    return value


def number(row, key, *, default=None, minimum=None, maximum=None, integer=False):
    value = fnum(row.get(key), default)
    if value is None:
        raise ValueError(f"Champ numérique obligatoire manquant : {key}")
    if integer and value != int(value):
        raise ValueError(f"{key} doit être un entier : {value}")
    if minimum is not None and value < minimum:
        raise ValueError(f"{key} < {minimum} : {value}")
    if maximum is not None and value > maximum:
        raise ValueError(f"{key} > {maximum} : {value}")
    return int(value) if integer else value


def load(hyp_path):
    with open(hyp_path, encoding="utf-8-sig") as f:
        hyp = json.load(f)
    rows = read_csv(os.path.join(ROOT, hyp["fichiers"]["viviers"]))
    viviers = {}
    for row in rows:
        vid = row.get("vivier_id")
        if not vid or vid in viviers:
            raise ValueError(f"Identifiant de vivier vide ou dupliqué : {vid!r}")
        viviers[vid] = row
    return hyp, viviers, read_csv(os.path.join(ROOT, hyp["fichiers"]["reformes"]))


def cout_annuel(hyp, versant, annees_depuis_non_recrutement):
    """Coût d'entrée non engagé, en k€, avec GVT réel plafonné au coût moyen."""
    c = hyp["couts_k_eur"][versant]
    entree = number(c, "cout_entree_hors_pension", minimum=0)
    moyen = number(c, "cout_moyen_hors_pension", minimum=0)
    g = number(hyp, "gvt_individuel_reel", minimum=0)
    return min(moyen, entree * (1 + g) ** annees_depuis_non_recrutement)


def prepare(hyp, viviers, reformes, sc):
    """Valide et affecte les cibles sans consommer les départs futurs."""
    if sc not in SCENARIOS:
        raise ValueError(f"Scénario inconnu : {sc}")
    first = number(hyp, "annee_debut", integer=True)
    last = number(hyp, "annee_fin", integer=True, minimum=first)
    number(hyp, "gvt_individuel_reel", minimum=0)
    number(hyp, "taux_conservation_consolide", minimum=0, maximum=1)
    number(hyp, "facteur_transfert_cout", minimum=0)
    number(hyp, "indemnite_depart_k_eur", minimum=0)
    number(hyp, "fraction_economie_premiere_annee", default=1, minimum=0, maximum=1)
    plans, alerts, seen = defaultdict(list), [], set()
    for r in reformes:
        rid, vid = r.get("id"), r.get("vivier_id")
        if not rid or rid in seen:
            raise ValueError(f"Identifiant de réforme vide ou dupliqué : {rid!r}")
        seen.add(rid)
        if vid not in viviers:
            raise ValueError(f"{rid} : vivier inconnu {vid!r}")
        if not r.get("intitule"):
            raise ValueError(f"{rid} : intitulé manquant")
        rate = number(r, f"taux_{sc}", minimum=0, maximum=1)
        parts = [number(r, "part_" + m, minimum=0, maximum=1) for m in MODES]
        if abs(sum(parts) - 1) > EPS:
            raise ValueError(f"{rid} : les parts doivent sommer à 1, reçu {sum(parts)}")
        start = number(r, "annee_debut", integer=True)
        if start < first:
            raise ValueError(f"{rid} : réforme antérieure à l'horizon ; un état initial explicite est nécessaire")
        duration = number(r, f"duree_ans_{sc}", default=fnum(r.get("duree_ans"), None), minimum=1, integer=True)
        money = {k: number(r, f"{k}_{sc}", minimum=None if k == "effet_recettes_meur" else 0) for k in MONEY}
        inv_duration = number(r, "invest_duree_ans", default=1, minimum=1, integer=True)
        inv_start = number(r, "annee_invest_debut", default=start, integer=True)
        if inv_start > start and money["invest_meur"] > 0:
            raise ValueError(f"{rid} : l'investissement initial commence après la mise en œuvre")
        transfer = r.get("type_transfert", "").strip()
        transfer_source_share, transfer_retention, recruitment_ratio = 0.0, 0.0, 0.0
        if parts[3] > 0:
            if transfer not in ("public", "prive"):
                raise ValueError(f"{rid} : type_transfert doit valoir public ou prive")
            if transfer == "public":
                transfer_retention = number(r, "taux_conservation_transfert", minimum=0, maximum=1)
                recruitment_ratio = number(r, "etp_destination_par_etp_transfere", minimum=0)
                transfer_source_share = number(r, "part_cout_transfert_charge_source", minimum=0, maximum=1)
            else:
                transfer_source_share, transfer_retention = 1.0, 1.0
        plans[vid].append({
            "row": r, "rate": rate, "parts": parts, "start": start, "duration": duration,
            "order": number(r, "ordre", minimum=0), "money": money,
            "recurrent_proportional": number(r, "cout_recurrent_proportionnel", default=0, minimum=0, maximum=1, integer=True) == 1,
            "inv_start": inv_start, "inv_duration": inv_duration,
            "transfer_source_share": transfer_source_share,
            "transfer_retention": transfer_retention, "recruitment_ratio": recruitment_ratio,
        })
    for vid, lst in plans.items():
        v = viviers[vid]
        base = number(v, "etp_base", minimum=0)
        number(v, "taux_departs_annuel", minimum=0, maximum=1)
        ceiling = number(v, f"plafond_reduction_{sc}", minimum=0, maximum=1) * base
        versant = v.get("versant")
        if versant not in hyp.get("couts_k_eur", {}):
            raise ValueError(f"{vid} : coûts manquants pour le versant {versant}")
        costs = hyp["couts_k_eur"][versant]
        entry = number(costs, "cout_entree_hors_pension", minimum=0)
        average = number(costs, "cout_moyen_hors_pension", minimum=0)
        if entry > average:
            raise ValueError(f"{versant} : coût d'entrée supérieur au coût moyen ; vérifier la calibration")
        lst.sort(key=lambda p: (p["order"], p["row"]["id"]))
        if len({p["order"] for p in lst}) != len(lst):
            raise ValueError(f"{vid} : ordres de priorité dupliqués")
        planned = 0.0
        for p in lst:
            target = p["rate"] * (base - planned)
            p["target"] = max(0.0, min(target, ceiling - planned))
            if p["target"] + EPS < target:
                alerts.append(f"{p['row']['id']} : cible plafonnée dans le vivier {vid} ({sc})")
            planned += p["target"]
            p["cum"] = [0.0] * 4
            p["backlog"] = 0.0
            p["cohorts"] = []
            p["result"] = {
                "id": p["row"]["id"], "intitule": p["row"]["intitule"], "vivier": vid,
                "scenario": sc, "etp_vivier_base": base, "etp_cible": p["target"],
            }
            pre_years = sum(1 for y in range(p["inv_start"], p["inv_start"] + p["inv_duration"]) if y < first)
            p["pre_invest"] = pre_years * p["money"]["invest_meur"] / p["inv_duration"]
            if p["pre_invest"] > 0:
                alerts.append(f"{p['row']['id']} : {p['pre_invest']:g} M€ d'investissements avant {first}, présentés séparément")
    if "fraction_economie_premiere_annee" not in hyp:
        alerts.append("Convention par défaut : économie en année pleine dès l'année du mouvement (fraction=1). À calibrer.")
    return list(range(first, last + 1)), plans, alerts


def run_scenario(hyp, viviers, reformes, sc):
    years, plans, alerts = prepare(hyp, viviers, reformes, sc)
    by_year = {y: defaultdict(float, {k: 0.0 for k in YEAR_FIELDS}) for y in years}
    fraction = number(hyp, "fraction_economie_premiere_annee", default=1)
    retention = number(hyp, "taux_conservation_consolide")
    factor = number(hyp, "facteur_transfert_cout")
    indemnity = number(hyp, "indemnite_depart_k_eur")
    out = []
    for vid, lst in plans.items():
        v = viviers[vid]
        base, departure_rate = number(v, "etp_base"), number(v, "taux_departs_annuel")
        average = number(hyp["couts_k_eur"][v["versant"]], "cout_moyen_hors_pension")
        reduced = 0.0
        for y in years:
            available = departure_rate * max(0.0, base - reduced)
            remaining = available
            for p in lst:
                scheduled = p["target"] / p["duration"] if p["start"] <= y < p["start"] + p["duration"] else 0.0
                p["backlog"] += scheduled * p["parts"][0]
                nr = min(p["backlog"], remaining)
                p["backlog"] = max(0.0, p["backlog"] - nr)
                remaining -= nr
                flow = [nr] + [scheduled * part for part in p["parts"][1:]]
                p["cum"] = [a + b for a, b in zip(p["cum"], flow)]
                reduced += sum(flow)
                if reduced > base + EPS:
                    raise ArithmeticError(f"{vid}/{y} : réductions supérieures au stock initial")
                p["cohorts"].append((y, flow))
                source_payroll = transfer_cost = 0.0
                for y0, cohort in p["cohorts"]:
                    weight = fraction if y == y0 else 1.0
                    source_payroll += weight * (
                        cohort[0] * cout_annuel(hyp, v["versant"], y - y0)
                        + (cohort[1] + cohort[3]) * average
                    ) / 1000.0
                    transfer_cost += weight * cohort[3] * average * factor / 1000.0
                ramp = min(1.0, max(0.0, (y - p["start"] + 1) / p["duration"]))
                effective_done = sum(p["cum"]) - (1 - fraction) * sum(flow)
                benefit_ramp = effective_done / p["target"] if p["target"] > EPS else (ramp if p["rate"] == 0 else 0.0)
                m = p["money"]
                operating = m["eco_fonct_meur"] * benefit_ramp
                # Un coût proportionnel (rétrocession aux agents) suit la réduction réalisée, pas le calendrier.
                recurrent = m["cout_recurrent_meur"] * (benefit_ramp if p["recurrent_proportional"] else ramp)
                revenue = m["effet_recettes_meur"] * benefit_ramp
                investment = m["invest_meur"] / p["inv_duration"] if p["inv_start"] <= y < p["inv_start"] + p["inv_duration"] else 0.0
                compensation = flow[1] * indemnity / 1000.0
                transfer_source_cost = transfer_cost * p["transfer_source_share"]
                gross = source_payroll + operating
                net = gross - transfer_source_cost - investment - compensation - recurrent + revenue
                consolidated = source_payroll * retention - transfer_cost * p["transfer_retention"] + operating - investment - compensation - recurrent + revenue
                public_recruits = flow[3] * p["recruitment_ratio"]
                b = by_year[y]
                values = {
                    "etp_non_remplaces": flow[0], "etp_supprimes_indemnises": flow[1],
                    "etp_redeployes": flow[2], "etp_transferes": flow[3],
                    "etp_recrutements_publics_destination": public_recruits,
                    "etp_postes_apu_en_moins": flow[0] + flow[1] + flow[3] - public_recruits,
                    "etp_postes_origine_en_moins_stock": p["cum"][0] + p["cum"][1] + p["cum"][3],
                    "etp_postes_apu_en_moins_stock": p["cum"][0] + p["cum"][1] + p["cum"][3] * (1 - p["recruitment_ratio"]),
                    "eco_masse_salariale_origine_meur": source_payroll,
                    "eco_fonctionnement_meur": operating, "eco_brute_meur": gross,
                    "cout_transferts_meur": transfer_cost, "cout_transferts_charge_source_meur": transfer_source_cost,
                    "invest_meur": investment, "indemnites_meur": compensation,
                    "cout_recurrent_meur": recurrent, "effet_recettes_meur": revenue,
                    "eco_nette_meur": net, "eco_consolidee_apu_meur": consolidated,
                }
                for key, value in values.items():
                    b[key] += value
                p["result"][f"net_{y}"] = net
                p["result"][f"consolide_{y}"] = consolidated
                p["result"][f"invest_{y}"] = investment
            by_year[y]["etp_departs_disponibles"] += available
            by_year[y]["etp_departs_utilises"] += available - remaining
        for p in lst:
            r = p["result"]
            if p["backlog"] > EPS:
                alerts.append(f"{r['id']} : {p['backlog']:,.3f} ETP de non-remplacement demandés mais non réalisés en {years[-1]} ({vid}, {sc})")
            unexecuted = max(0.0, p["target"] - sum(p["cum"]))
            if unexecuted > EPS and p["backlog"] <= EPS:
                alerts.append(f"{r['id']} : {unexecuted:,.3f} ETP de cible après l'horizon {years[-1]}")
            r.update({
                "etp_non_remplaces": p["cum"][0], "etp_supprimes_indemnises": p["cum"][1],
                "etp_redeployes": p["cum"][2], "etp_transferes": p["cum"][3],
                "etp_recrutements_publics_destination": p["cum"][3] * p["recruitment_ratio"],
                "etp_postes_en_moins": p["cum"][0] + p["cum"][1] + p["cum"][3],
                "etp_postes_apu_en_moins": p["cum"][0] + p["cum"][1] + p["cum"][3] * (1 - p["recruitment_ratio"]),
                "etp_cible_non_realisee": unexecuted,
                "cumul_net_5ans": sum(r[f"net_{y}"] for y in years[:5]) if len(years) >= 5 else None,
                "cumul_net_10ans": sum(r[f"net_{y}"] for y in years[:10]) if len(years) >= 10 else None,
                "cumul_consolide_5ans": sum(r[f"consolide_{y}"] for y in years[:5]) if len(years) >= 5 else None,
                "cumul_consolide_10ans": sum(r[f"consolide_{y}"] for y in years[:10]) if len(years) >= 10 else None,
                "cumul_net_horizon_meur": sum(r[f"net_{y}"] for y in years),
                "invest_avant_horizon_meur": p["pre_invest"],
                "cumul_net_horizon_incl_invest_avant_meur": sum(r[f"net_{y}"] for y in years) - p["pre_invest"],
                "net_annee_finale_meur": r[f"net_{years[-1]}"],
                "confiance": p["row"].get("confiance", ""),
            })
            out.append(r)
    return out, by_year, alerts


def summary(sc, per_reform, by_year):
    years = sorted(by_year)
    last = years[-1]
    five = years[:5] if len(years) >= 5 else None
    ten = years[:10] if len(years) >= 10 else None
    pre = sum(r["invest_avant_horizon_meur"] for r in per_reform)
    cumul = lambda selected, key: sum(by_year[y][key] for y in selected) if selected is not None else None
    return {
        "scenario": sc, "annees_couvertes": len(years),
        "etp_viviers_concernes": sum({r["vivier"]: r["etp_vivier_base"] for r in per_reform}.values()),
        "postes_en_moins_5ans": by_year[five[-1]]["etp_postes_origine_en_moins_stock"] if five else None,
        "postes_en_moins_10ans": by_year[ten[-1]]["etp_postes_origine_en_moins_stock"] if ten else None,
        "postes_apu_en_moins_5ans": by_year[five[-1]]["etp_postes_apu_en_moins_stock"] if five else None,
        "postes_apu_en_moins_10ans": by_year[ten[-1]]["etp_postes_apu_en_moins_stock"] if ten else None,
        "etp_redeployes_horizon": cumul(years, "etp_redeployes"),
        "recrutements_publics_destination_horizon": cumul(years, "etp_recrutements_publics_destination"),
        "eco_brute_annee5_meur": by_year[five[-1]]["eco_brute_meur"] if five else None,
        "eco_nette_annee5_meur": by_year[five[-1]]["eco_nette_meur"] if five else None,
        f"eco_nette_{last}_meur": by_year[last]["eco_nette_meur"],
        f"eco_consolidee_{last}_meur": by_year[last]["eco_consolidee_apu_meur"],
        "cumul_net_5ans_meur": cumul(five, "eco_nette_meur"),
        "cumul_net_10ans_meur": cumul(ten, "eco_nette_meur"),
        "cumul_consolide_5ans_meur": cumul(five, "eco_consolidee_apu_meur"),
        "cumul_consolide_10ans_meur": cumul(ten, "eco_consolidee_apu_meur"),
        "cumul_net_horizon_meur": cumul(years, "eco_nette_meur"),
        "invest_horizon_meur": cumul(years, "invest_meur"),
        "invest_avant_horizon_meur": pre,
        "invest_total_jusqua_fin_horizon_meur": cumul(years, "invest_meur") + pre,
        "cumul_net_5ans_incl_invest_avant_meur": cumul(five, "eco_nette_meur") - pre if five else None,
        "cumul_net_10ans_incl_invest_avant_meur": cumul(ten, "eco_nette_meur") - pre if ten else None,
    }


def write_csv(path, rows, fieldnames):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: round(v, 8) if isinstance(v, float) else v for k, v in row.items()})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--hyp", default=os.path.join(ROOT, "modele", "hypotheses.json"))
    parser.add_argument("--out", default=os.path.join(ROOT, "modele", "resultats"))
    args = parser.parse_args()
    hyp, viviers, reformes = load(args.hyp)
    runs = {sc: run_scenario(hyp, viviers, reformes, sc) for sc in SCENARIOS}
    os.makedirs(args.out, exist_ok=True)
    summaries, alerts = [], []
    for sc, (per_reform, by_year, messages) in runs.items():
        keys = list(per_reform[0]) if per_reform else ["id", "scenario", "etp_cible"]
        write_csv(os.path.join(args.out, f"reformes_{sc}.csv"), per_reform, keys)
        rows = [{"annee": y, **by_year[y]} for y in sorted(by_year)]
        write_csv(os.path.join(args.out, f"trajectoire_{sc}.csv"), rows, ["annee", *YEAR_FIELDS])
        summaries.append(summary(sc, per_reform, by_year))
        alerts.extend(f"[{sc}] {m}" for m in messages)
    write_csv(os.path.join(args.out, "synthese_scenarios.csv"), summaries, list(summaries[0]))
    with open(os.path.join(args.out, "alertes.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(alerts) + ("\n" if alerts else ""))
    print(f"{len(summaries)} scénarios ; {len(alerts)} alertes ; résultats : {args.out}")


if __name__ == "__main__":
    main()
