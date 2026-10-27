"""Equipe 04 - telecharge des indicateurs ISORA (API SDMX FMI, dataflow ISORA_LATEST_DATA_PUB 5.0.0)
pour la France et les pays de comparaison, et produit un CSV long simplifie.
Usage: python3 -I 04_isora_fetch.py out_raw.csv out_long.csv codes.csv"""
import sys, csv, io, requests
COUNTRIES = "FRA DEU ITA ESP PRT BEL NLD CHE AUT GBR IRL SWE DNK NOR FIN POL EST CAN USA AUS NZL JPN KOR".split()
IND = """337_010 337_011 337_012 337_013 337_014 337_015 337_180 83835_28 337_176 337_177 337_017 337_018 337_166 337_167
337_250 337_251 337_252 337_022 111_200 111_201 111_202 337_225 337_214 337_098 95910 80040_3 80240_3 80240_4 80240_0
86280 86290 86310 86320 86330 86340 91410 91420 93770 95020 398_003 96210_4 337_091 80080_3 91320_3 95100_3 80250_3""".split()
url = ("https://api.imf.org/external/sdmx/2.1/data/ISORA,ISORA_LATEST_DATA_PUB,5.0.0/"
       + "+".join(COUNTRIES) + "." + "+".join(IND) + ".A")
r = requests.get(url, headers={"Accept": "application/vnd.sdmx.data+csv;version=1.0.0", "User-Agent": "Mozilla/5.0"}, timeout=600)
print(r.status_code, len(r.content))
open(sys.argv[1], "wb").write(r.content)
names = {}
for row in csv.DictReader(open(sys.argv[3])):
    if row["codelist"] == "CL_ISORA_TAX":
        names[row["code"]] = row["name"]
rd = csv.DictReader(io.StringIO(r.content.decode("utf-8")))
w = csv.writer(open(sys.argv[2], "w", newline=""))
w.writerow(["jurisdiction", "indicator", "indicator_name", "year", "value", "scale", "footnote"])
for row in rd:
    w.writerow([row["JURISDICTION"], row["INDICATOR"], names.get(row["INDICATOR"], ""), row["TIME_PERIOD"], row["OBS_VALUE"], row["SCALE"], (row.get("FOOTNOTE") or "")[:300]])
print("url=", url[:200])
