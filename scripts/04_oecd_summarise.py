"""Equipe 04 - resume un CSV SDMX OCDE (labels=both): valeurs distinctes par dimension.
Usage: python3 -I 04_oecd_summarise.py file.csv [maxvals]"""
import sys, csv, collections
rows = list(csv.DictReader(open(sys.argv[1], encoding="utf-8")))
mx = int(sys.argv[2]) if len(sys.argv) > 2 else 25
print("rows", len(rows))
if rows:
    for k in rows[0]:
        if k in ("OBS_VALUE",) or k.startswith("TIME_PERIOD"):
            continue
        c = collections.Counter(r[k] for r in rows)
        if len(c) > 1 or k.startswith("UNIT") or k.startswith("MEASURE"):
            print(" ", k, len(c), [x for x, _ in c.most_common(mx)])
    print("  years", sorted(set(r[[k for k in rows[0] if k.startswith("TIME_PERIOD")][0]] for r in rows)))
