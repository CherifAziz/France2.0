#!/usr/bin/env python3
"""Vérifie ou restaure le cache documentaire du lot2, sans toucher aux bruts.

Le manifeste versionné reprend les empreintes des téléchargements initiaux. Une
nouvelle distribution différente provoque un arrêt ; elle ne devient jamais la
source d'un ancien chiffre sans revue. --build-manifest est réservé à la collecte.
"""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/"sources/04_manifestes_cache.json"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_manifest():
    records=[]
    for part in "abcd":
        for path in sorted((ROOT/f"data/raw/04{part}").glob("*.meta.json")):
            records.append(json.loads(path.read_text(encoding="utf-8")))
    records.extend(json.loads((ROOT/"data/raw/04c/manifestes_collecte.json").read_text(encoding="utf-8")))
    records.extend(json.loads((ROOT/"data/raw/04d/documents_support.json").read_text(encoding="utf-8")))
    selected={}
    for item in records:
        path=item.get("raw_path","").replace("\\","/")
        if not path.startswith("data/cache/") or item.get("acces")!="integral" or not item.get("sha256"):
            continue
        entry={k:item.get(k) for k in ["source_url","date_consultation","http_status","sha256","bytes","conversion"]}
        entry["raw_path"]=path
        if path in selected and selected[path]["sha256"]!=entry["sha256"]:
            raise ValueError(f"Conflit de versions : {path}")
        selected[path]=entry
    entries=[selected[k] for k in sorted(selected)]
    MANIFEST.write_text(json.dumps(entries,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return entries


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build-manifest",action="store_true")
    parser.add_argument("--download",action="store_true",help="Télécharger les seuls fichiers absents")
    args=parser.parse_args()
    entries=build_manifest() if args.build_manifest else json.loads(MANIFEST.read_text(encoding="utf-8"))
    present=0;missing=[]
    for item in entries:
        target=(ROOT/item["raw_path"]).resolve()
        target.relative_to((ROOT/"data/cache").resolve())
        if target.exists() and sha(target)!=item["sha256"]:
            raise ValueError(f"Archive locale différente : {target}")
        if not target.exists() or not target.with_suffix(".txt").exists():
            if args.download:
                subprocess.run([sys.executable,str(ROOT/"scripts/fetch.py"),item["source_url"],target.stem,
                                "--out-dir",str(target.parent),"--timeout","90"],check=True)
                if sha(target)!=item["sha256"]:
                    raise ValueError(f"Source distante modifiée : {target}; ancien millésime non reproduit")
            else:
                missing.append(item["raw_path"])
                continue
        present+=1
    print(json.dumps({"archives_attendues":len(entries),"archives_et_textes_verifies":present,"cache_a_restaurer":missing},ensure_ascii=False))
    if missing:
        raise SystemExit(2)


if __name__=="__main__":
    main()
