"""Collectes ciblées primaires du chantier 04c (aucune dépendance autre que requests).

Usage : python -I scripts/04c_collect_sources.py --refresh-oecd
Ne remplace jamais les fichiers hérités. Les tentatives, même infructueuses, ont un manifeste.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/raw/04c"


def collect(url: str, name: str, accept: str | None = None) -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    meta = {"source_url": url, "date_consultation": "2026-10-28",
            "retrieved_at_utc": dt.datetime.now(dt.timezone.utc).isoformat()}
    headers = {"User-Agent": "Mozilla/5.0"}
    if accept:
        headers["Accept"] = accept
    try:
        r = requests.get(url, headers=headers, timeout=50)
        meta.update(http_status=r.status_code, content_type=r.headers.get("Content-Type"),
                    final_url=r.url, bytes=len(r.content), sha256=hashlib.sha256(r.content).hexdigest())
        valid = r.ok and r.text.startswith("DATAFLOW,")
        meta["acces"] = "integral" if valid else "inaccessible"
        target = OUT / (name + (".csv" if valid else ".error.txt"))
        target.write_bytes(r.content)
        meta["raw_path"] = str(target.relative_to(ROOT))
    except requests.RequestException as exc:
        meta.update(acces="inaccessible", erreur=f"{type(exc).__name__}: {exc}")
    (OUT / (name + ".meta.json")).write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    return meta


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh-oecd", action="store_true")
    args = parser.parse_args()
    if args.refresh_oecd:
        with (ROOT / "data/raw/04/oecd_sha_hc7.csv").open(encoding="utf-8-sig", newline="") as f:
            countries = sorted({row["REF_AREA: Reference area"].split(":")[0] for row in csv.DictReader(f)})
        country = "+".join(countries)
        base = "https://sdmx.oecd.org/public/rest/data/OECD.ELS.HD,DSD_SHA@DF_SHA,1.1/"
        # Ordre des 12 dimensions vérifié dans oecd_sha_structure.xml.
        jobs = [
            ("oecd_sha_current_total", [country, "A", "EXP_HEALTH", "XDC+PT_EXP_HLTH+PT_B1GQ+USD_PPP_PS", "_T", "_Z", "HC7+HC71+HC72+_T", "_T", "_T", "_Z", "_Z", ""]),
            ("oecd_sha_current_schemes", [country, "A", "EXP_HEALTH", "XDC+PT_EXP_HLTH+USD_PPP_PS", "_T+HF1+HF11+HF12HF13+HF121+HF122+HF2+HF21+HF3", "_Z", "HC7+_T", "_T", "_T", "_Z", "_Z", ""]),
        ]
        for name, dims in jobs:
            u = base + ".".join(dims) + "?startPeriod=2023&endPeriod=2024"
            result = collect(u, name, "application/vnd.sdmx.data+csv; charset=utf-8; labels=both")
            print(name, result["acces"], result.get("http_status"), result.get("bytes"))


if __name__ == "__main__":
    main()
