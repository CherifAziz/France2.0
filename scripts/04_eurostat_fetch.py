"""Equipe 04 - interroge l'API Eurostat (JSON-stat 2.0) et ecrit un CSV long.
Usage: python3 -I 04_eurostat_fetch.py DATASET "param1=v1&param2=v2..." out.csv
Les pays de comparaison sont ajoutes automatiquement si 'geo' n'est pas fourni."""
import sys, csv, json, itertools, requests
ds, params, out = sys.argv[1], sys.argv[2], sys.argv[3]
GEOS = "FR DE IT ES PT BE NL CH AT IE SE DK NO FI PL EE EU27_2020 UK".split()
q = params
if "geo=" not in params:
    q += "&" + "&".join("geo=" + g for g in GEOS)
url = f"https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/{ds}?format=JSON&lang=en&{q}"
r = requests.get(url, timeout=300)
d = r.json()
if "dimension" not in d:
    print("ERROR", r.status_code, str(d)[:500]); sys.exit(1)
ids, sizes = d["id"], d["size"]
cats = []
for k in ids:
    cat = d["dimension"][k]["category"]
    idx = sorted(cat["index"].items(), key=lambda x: x[1])
    cats.append([(c, cat.get("label", {}).get(c, c)) for c, _ in idx])
vals, status = d.get("value", {}), d.get("status", {})
w = csv.writer(open(out, "w", newline=""))
w.writerow(ids + [i + "_label" for i in ids] + ["value", "flag"])
for n, combo in enumerate(itertools.product(*cats)):
    v = vals.get(str(n))
    if v is None:
        continue
    w.writerow([c[0] for c in combo] + [c[1] for c in combo] + [v, status.get(str(n), "")])
print(r.status_code, url[:250], "updated=", d.get("updated"))
