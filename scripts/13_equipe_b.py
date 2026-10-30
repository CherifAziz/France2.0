#!/usr/bin/env python3
"""Revue critique (équipe B) : variantes défavorables du catalogue, relancées dans le moteur.

Chaque variante répond à une objection précise de la note 13. Écrit data/reformes/13_equipe_b.csv.
"""
import copy
import csv
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("modele", ROOT / "modele/modele.py")
modele = importlib.util.module_from_spec(spec)
spec.loader.exec_module(modele)
SC = modele.SCENARIOS
# [HYPOTHÈSE] Probabilité qu'une réforme produise l'effet prévu, selon son niveau de confiance.
PROBA = {"faible": 0.3, "moyen": 0.6, "élevé": 0.9}


def run(hyp, viviers, reformes):
    out = {}
    for sc in SC:
        per, by_year, _ = modele.run_scenario(hyp, viviers, reformes, sc)
        s = modele.summary(sc, per, by_year)
        out[sc] = {"postes_2036": s["postes_en_moins_10ans"], "net_2036": s["eco_nette_2036_meur"], "cumul_net_10": s["cumul_net_10ans_meur"],
                   "postes_confiance_faible": sum(r["etp_postes_en_moins"] for r in per if r["confiance"] == "faible")}
    return out


def scaled(reformes, factor_of):
    rows = copy.deepcopy(reformes)
    for r in rows:
        f = factor_of(r)
        for sc in SC:
            for k in (f"taux_{sc}", f"invest_meur_{sc}", f"cout_recurrent_meur_{sc}", f"eco_fonct_meur_{sc}", f"effet_recettes_meur_{sc}"):
                r[k] = str(float(r[k]) * f)
    return rows


def main():
    hyp, viviers, reformes = modele.load(ROOT / "modele/hypotheses.json")
    variants = [
        ("Catalogue central", reformes),
        ("Pondération par la confiance (faible 0,3 ; moyen 0,6)", scaled(reformes, lambda r: PROBA[r["confiance"]])),
        ("Sans règles descendantes (R12 un sur deux, R15 échelon)", scaled(reformes, lambda r: 0 if r["id"] in ("R12", "R15") else 1)),
        ("Sans R01 (tendance DGFiP possiblement déjà dans la référence)", scaled(reformes, lambda r: 0 if r["id"] == "R01" else 1)),
        ("Seulement les fiches de confiance moyenne", scaled(reformes, lambda r: 1 if r["confiance"] != "faible" else 0)),
    ]
    rows = []
    for name, rf in variants:
        res = run(hyp, viviers, rf)
        rows += [{"variante": name, "scenario": sc, **{k: round(v, 1) for k, v in res[sc].items()}} for sc in SC]
    with open(ROOT / "data/reformes/13_equipe_b.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    for r in rows:
        print(f"{r['variante'][:58]:58} {r['scenario'][:6]:6} {r['postes_2036']:>10,.0f} {r['net_2036']:>8,.0f} {r['cumul_net_10']:>9,.0f} faible:{r['postes_confiance_faible']:>9,.0f}")


if __name__ == "__main__":
    main()
