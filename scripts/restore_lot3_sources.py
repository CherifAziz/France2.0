#!/usr/bin/env python3
"""Vérifie/restaure les corps HTTP du cache05–10 ; ne remplace pas les lectures.

Les extraits indexés et ouvertures primaires connectées ont leurs propres
archives. Ce script ne prétend pas pouvoir en recréer le corps HTTP original.
"""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/"sources/lot3_manifestes_cache.json"


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def build():
 selected={}
 for chapter in ["05","06","07","08","09","10"]:
  paths=sorted((ROOT/"data/cache"/chapter).glob("*.meta.json"))+sorted((ROOT/"data/raw"/chapter).glob("*.meta.json"))
  for path in paths:
   item=json.loads(path.read_text(encoding="utf-8"))
   rawpath=item.get("raw_path") or item.get("local_path")
   fingerprint=item.get("sha256_stored") or item.get("sha256")
   if item.get("acces")!="integral" or item.get("http_status")!=200 or not rawpath or not fingerprint:continue
   raw=rawpath.replace("\\","/")
   if not raw.startswith("data/cache/"):continue
   target=(ROOT/raw).resolve();target.relative_to((ROOT/"data/cache").resolve())
   if not target.is_file() or target.suffix.lower() not in [".pdf",".html",".xml",".xlsx",".zip"]:continue
   if sha(target)!=fingerprint:raise ValueError(f"Archive modifiée : {target}")
   entry={k:item.get(k) for k in ["source_url","date_consultation","sha256","bytes","conversion","content_type"]}
   entry.update(source_url=item.get("source_url") or item.get("url"),sha256=fingerprint,bytes=item.get("bytes") or item.get("body_bytes"))
   entry["raw_path"]=raw
   selected[raw]=entry
 entries=[selected[k] for k in sorted(selected)]
 MANIFEST.write_text(json.dumps(entries,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 return entries


def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument("--build-manifest",action="store_true");p.add_argument("--download",action="store_true");a=p.parse_args()
 entries=build() if a.build_manifest else json.loads(MANIFEST.read_text(encoding="utf-8"))
 missing=[]
 for item in entries:
  target=(ROOT/item["raw_path"]).resolve();target.relative_to((ROOT/"data/cache").resolve())
  if target.exists() and sha(target)!=item["sha256"]:raise ValueError(f"Empreinte différente : {target}")
  need_text=bool(item.get("conversion")) and target.suffix.lower() in [".pdf",".html",".xml"]
  if not target.exists() or (need_text and not target.with_suffix(".txt").exists()):
   if not a.download:missing.append(item["raw_path"]);continue
   subprocess.run([sys.executable,str(ROOT/"scripts/fetch.py"),item["source_url"],target.stem,"--out-dir",str(target.parent),"--timeout","90"],check=True)
   if sha(target)!=item["sha256"]:raise ValueError(f"Distribution distante modifiée : {target}; millésime non reproduit")
 print(json.dumps({"corps_HTTP_attendus":len(entries),"cache_a_restaurer":missing,"autres_canaux":"Voir registres et archives d'ouvertures primaires ; pas d'assimilation à un téléchargement original"},ensure_ascii=False))
 if missing:raise SystemExit(2)


if __name__=="__main__":main()
