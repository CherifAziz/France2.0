"""Equipe 04 - interroge l'API SDMX de l'OCDE (sdmx.oecd.org) et enregistre le CSV avec libelles.
Usage: python3 -I 04_oecd_fetch.py AGENCY,DSD@DF,VERSION KEY "extra_params" out.csv
KEY peut valoir AUTO:<pays+pays> : la cle est construite a partir de la structure (pays sur REF_AREA, le reste en joker)."""
import sys, re, requests
flow, key, extra, out = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
H = {"User-Agent": "Mozilla/5.0"}
if key.startswith("AUTO:"):
    ag, df, ver = flow.split(",")
    s = requests.get(f"https://sdmx.oecd.org/public/rest/dataflow/{ag}/{df}/{ver}?references=datastructure", headers=H, timeout=300).text
    dims = sorted(re.findall(r'<structure:Dimension id="([^"]+)"[^>]*position="(\d+)"', s), key=lambda x: int(x[1]))
    parts = ["" for _ in dims]
    for i, (d, _) in enumerate(dims):
        if d == "REF_AREA":
            parts[i] = key[5:]
    key = ".".join(parts)
    print("dims:", [d for d, _ in dims])
url = f"https://sdmx.oecd.org/public/rest/data/{flow}/{key}?{extra}"
r = requests.get(url, headers={"Accept": "application/vnd.sdmx.data+csv; charset=utf-8; labels=both", **H}, timeout=600)
open(out, "wb").write(r.content)
print(r.status_code, len(r.content), url[:300])
