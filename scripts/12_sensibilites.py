#!/usr/bin/env python3
"""Sensibilités du catalogue et test formel des seuils de postes (phase 4).

Relance modele/modele.py en mémoire sur des variantes des hypothèses, sans modifier
les fichiers d'entrée. Écrit data/reformes/12_sensibilites.csv, data/reformes/12_seuils.csv
et figures/12_tornado_*.svg. Chaque variante change un seul paramètre.
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
IA = {"R03", "R11", "R18", "R20", "R24", "R26"}
# Sorties définitives de fonctionnaires (toutes causes) / pensions de fonctionnaires civils, FP 2024-2025 (note 01b) :
# 174 655 sortants fonctionnaires pour 108 796 pensions civiles, soit 1,605.
TOUTES_SORTIES = 174655 / 108796
SEUILS = [50_000, 100_000, 200_000, 500_000, 800_000, 1_000_000, 1_500_000]


def load():
    hyp, viviers, reformes = modele.load(ROOT / "modele/hypotheses.json")
    return hyp, viviers, reformes


def run(hyp, viviers, reformes):
    out = {}
    for sc in SC:
        per, by_year, alerts = modele.run_scenario(hyp, viviers, reformes, sc)
        s = modele.summary(sc, per, by_year)
        out[sc] = {"postes_2036": s["postes_en_moins_10ans"], "net_2036": s["eco_nette_2036_meur"],
                   "cumul_net_10": s["cumul_net_10ans_meur"], "cumul_consolide_10": s["cumul_consolide_10ans_meur"],
                   "invest": s["invest_horizon_meur"], "alertes": len(alerts)}
    return out


def scale_rows(rows, keys, factor, only=None):
    rows = copy.deepcopy(rows)
    for r in rows:
        if only and r["id"] not in only:
            continue
        for k in keys:
            r[k] = str(float(r[k]) * factor)
    return rows


def variants(hyp, viviers, reformes):
    """(nom, libellé bas, libellé haut, (hyp, viviers, reformes) bas, idem haut)."""
    def h(**changes):
        x = copy.deepcopy(hyp)
        for k, v in changes.items():
            x[k] = v
        return x

    def costs(f):
        x = copy.deepcopy(hyp)
        for c in x["couts_k_eur"].values():
            c["cout_entree_hors_pension"] *= f
            c["cout_moyen_hors_pension"] *= f
        return x

    def departs(f):
        v = copy.deepcopy(viviers)
        for row in v.values():
            row["taux_departs_annuel"] = str(min(1.0, float(row["taux_departs_annuel"]) * f))
        return v

    taux = [f"taux_{s}" for s in SC]
    inv = [f"invest_meur_{s}" for s in SC]
    return [
        ("Taux de réduction des fiches", "× 0,5", "× 1,5", (hyp, viviers, scale_rows(reformes, taux, 0.5)), (hyp, viviers, scale_rows(reformes, taux, 1.5))),
        ("Coût par ETP", "× 0,8", "× 1,2", (costs(0.8), viviers, reformes), (costs(1.2), viviers, reformes)),
        ("Départs mobilisables", "retraites × 0,8", f"toutes sorties (× {TOUTES_SORTIES:.2f})".replace(".", ","),
         (hyp, departs(0.8), reformes), (hyp, departs(TOUTES_SORTIES), reformes)),
        ("Conversion du temps libéré par l'IA", "aucune", "× 2", (hyp, viviers, scale_rows(reformes, taux, 0, IA)), (hyp, viviers, scale_rows(reformes, taux, 2, IA))),
        ("Investissements", "× 0,5", "× 2", (hyp, viviers, scale_rows(reformes, inv, 0.5)), (hyp, viviers, scale_rows(reformes, inv, 2))),
        ("GVT individuel réel", "0 %", "2 %", (h(gvt_individuel_reel=0.0), viviers, reformes), (h(gvt_individuel_reel=0.02), viviers, reformes)),
        ("Conservation APU (lecture consolidée)", "0,50", "0,80", (h(taux_conservation_consolide=0.5), viviers, reformes), (h(taux_conservation_consolide=0.8), viviers, reformes)),
    ]


def capacity(viviers, years, factor=1.0):
    """Départs mobilisables cumulés si aucun départ n'est remplacé : B × (1 − (1 − r)^n)."""
    total = 0.0
    for v in viviers.values():
        r = min(1.0, float(v["taux_departs_annuel"]) * factor)
        total += float(v["etp_base"]) * (1 - (1 - r) ** years)
    return total


def fr(x, d=0):
    return f"{x:,.{d}f}".replace(",", " ").replace(".", ",")


def tornado_svg(path, title, unit, base, bars):
    """Barres horizontales autour de la valeur centrale ; bars = [(nom, bas, haut, lib_bas, lib_haut)]."""
    bars = sorted(bars, key=lambda b: -abs(b[2] - b[1]))
    lo = min(min(b[1], b[2]) for b in bars + [(0, base, base)])
    hi = max(max(b[1], b[2]) for b in bars + [(0, base, base)])
    pad = (hi - lo) * 0.22 or 1
    lo, hi = lo - pad, hi + pad
    W, left, right, row, top = 960, 290, 30, 46, 70
    H = top + row * len(bars) + 50
    x = lambda v: left + (v - lo) / (hi - lo) * (W - left - right)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Segoe UI, Arial, sans-serif" font-size="13">',
           f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
           f'<text x="20" y="28" font-size="17" font-weight="600" fill="#17232b">{title}</text>',
           f'<text x="20" y="50" fill="#53616b">Valeur centrale : {fr(base)} {unit}. Barre claire : variante basse ; barre foncée : variante haute.</text>']
    for i, (name, low, high, lab_lo, lab_hi) in enumerate(bars):
        y = top + i * row
        out.append(f'<text x="{left - 12}" y="{y + 22}" text-anchor="end" fill="#17232b">{name}</text>')
        for val, lab, color in ((low, lab_lo, "#9cc3dc"), (high, lab_hi, "#245574")):
            a, b = sorted((x(base), x(val)))
            out.append(f'<rect x="{a:.1f}" y="{y + 8}" width="{max(b - a, 1):.1f}" height="18" fill="{color}"/>')
            anchor, tx = ("end", a - 4) if val < base else ("start", b + 4)
            out.append(f'<text x="{tx:.1f}" y="{y + 22}" text-anchor="{anchor}" font-size="11" fill="#53616b">{lab} : {fr(val)}</text>')
    out.append(f'<line x1="{x(base):.1f}" y1="{top}" x2="{x(base):.1f}" y2="{top + row * len(bars)}" stroke="#17232b" stroke-width="1.5"/>')
    out.append("</svg>")
    path.write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")


def main():
    hyp, viviers, reformes = load()
    base = run(hyp, viviers, reformes)
    rows = [{"variante": "Centrale", "sens": "", "libelle": "", "scenario": sc, **base[sc]} for sc in SC]
    tornado = {"cumul_net_10": [], "postes_2036": []}
    results = {}
    for name, lab_lo, lab_hi, low, high in variants(hyp, viviers, reformes):
        r_lo, r_hi = run(*low), run(*high)
        results[name] = (r_lo, r_hi)
        for sens, lab, res in (("bas", lab_lo, r_lo), ("haut", lab_hi, r_hi)):
            rows += [{"variante": name, "sens": sens, "libelle": lab, "scenario": sc, **res[sc]} for sc in SC]
        tornado["cumul_net_10"].append((name, r_lo["intermediaire"]["cumul_net_10"], r_hi["intermediaire"]["cumul_net_10"], lab_lo, lab_hi))
        tornado["postes_2036"].append((name, r_lo["radical"]["postes_2036"], r_hi["radical"]["postes_2036"], lab_lo, lab_hi))
    with open(ROOT / "data/reformes/12_sensibilites.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows({k: (round(v, 1) if isinstance(v, float) else v) for k, v in r.items()} for r in rows)
    figs = ROOT / "figures"
    tornado_svg(figs / "12_tornado_cumul_net.svg", "Scénario intermédiaire — économie nette cumulée 2027-2036",
                "M€", base["intermediaire"]["cumul_net_10"], [b for b in tornado["cumul_net_10"] if abs(b[2] - b[1]) > 0.5])
    tornado_svg(figs / "12_tornado_postes_radical.svg", "Scénario radical — postes en moins en 2036",
                "postes", base["radical"]["postes_2036"], [b for b in tornado["postes_2036"] if abs(b[2] - b[1]) > 0.5])

    # Seuils : catalogue central, catalogue sous hypothèses favorables cumulées, et capacités structurelles.
    favorable = (hyp, {k: {**v, "taux_departs_annuel": str(min(1.0, float(v["taux_departs_annuel"]) * TOUTES_SORTIES))} for k, v in viviers.items()},
                 scale_rows(reformes, [f"taux_{s}" for s in SC], 1.5))
    fav = run(*favorable)
    base_total = sum(float(v["etp_base"]) for v in viviers.values())
    cap = {(n, f): capacity(viviers, n, f) for n in (5, 10) for f in (1.0, TOUTES_SORTIES)}
    seuils = []
    for s in SEUILS:
        if base["intermediaire"]["postes_2036"] >= s:
            verdict, why = "conditionnel", "atteint dès le scénario intermédiaire, sur des taux hypothétiques à confiance faible ou moyenne"
        elif base["radical"]["postes_2036"] >= s:
            verdict, why = "conditionnel", "atteint seulement dans les scénarios ambitieux ou radical"
        elif fav["radical"]["postes_2036"] >= s:
            verdict, why = "non démontré", "atteint seulement en cumulant hypothèses favorables (taux × 1,5, toutes sorties non remplacées)"
        elif cap[(10, TOUTES_SORTIES)] >= s:
            verdict, why = "non démontré", "arithmétiquement possible si aucun départ administratif n'était remplacé pendant dix ans, sans réforme qui le justifie"
        elif base_total >= s:
            verdict, why = "incompatible", "supérieur à tous les départs administratifs possibles en dix ans ; exigerait des licenciements ou d'autres métiers"
        else:
            verdict, why = "incompatible", "supérieur à l'effectif administratif total des viviers"
        seuils.append({"seuil": s, "verdict": verdict, "justification": why,
                       "catalogue_intermediaire_2036": round(base["intermediaire"]["postes_2036"]),
                       "catalogue_radical_2036": round(base["radical"]["postes_2036"]),
                       "radical_favorable_2036": round(fav["radical"]["postes_2036"]),
                       "capacite_retraites_5ans": round(cap[(5, 1.0)]), "capacite_retraites_10ans": round(cap[(10, 1.0)]),
                       "capacite_toutes_sorties_5ans": round(cap[(5, TOUTES_SORTIES)]), "capacite_toutes_sorties_10ans": round(cap[(10, TOUTES_SORTIES)]),
                       "viviers_administratifs_total": round(base_total)})
    with open(ROOT / "data/reformes/12_seuils.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(seuils[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(seuils)
    print(json.dumps({"centrale": {k: round(v["postes_2036"]) for k, v in base.items()},
                      "radical_favorable": round(fav["radical"]["postes_2036"]),
                      "radical_favorable_net_2036": round(fav["radical"]["net_2036"]),
                      "capacites": {f"{n}ans_x{f:.2f}": round(c) for (n, f), c in cap.items()},
                      "seuils": {s["seuil"]: s["verdict"] for s in seuils}}, ensure_ascii=False, indent=1))
    for name, (lo, hi) in results.items():
        print(f"{name}: cumul net 10 ans intermédiaire {lo['intermediaire']['cumul_net_10']:.0f} / {hi['intermediaire']['cumul_net_10']:.0f} ; postes {lo['intermediaire']['postes_2036']:.0f} / {hi['intermediaire']['postes_2036']:.0f}")


if __name__ == "__main__":
    main()
