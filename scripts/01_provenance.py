#!/usr/bin/env python3
"""Rapproche les bruts hérités des distributions primaires archivées, hors réseau.

Les PDF/ZIP et HTML demeurent dans data/cache/ (ignoré). Les URL et empreintes
reproduisant chaque rapprochement sont conservées dans le dépôt.
"""
import csv
import hashlib
import json
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CACHE=ROOT/"data/cache/01"
RAW=ROOT/"data/raw/01"


def write(path,rows,fields):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def main():
    metadata=[json.loads(p.read_text(encoding="utf-8")) | {"nom":p.stem.removesuffix(".meta")} for p in sorted(CACHE.glob("*.meta.json"))]
    files={p.name:p for p in RAW.rglob("*.xlsx")}
    checks=[]
    register=[]
    for m in metadata:
        raw=ROOT/Path(m["raw_path"].replace("\\","/")) if m.get("raw_path") else None
        notes=f"HTTP {m.get('http_status','non reçu')}; {m.get('conversion','pas de conversion')}; {m.get('erreur','')}".rstrip("; ")
        publication=("2026-10-15" if "fonction-publique" in m["source_url"] else
                     "2026-08-28" if "2381404" in m["source_url"] else
                     "2026-02-10" if "insee.fr" in m["source_url"] else "")
        if not publication:
            notes += "; date de publication non vérifiée (test technique ou document annexe)"
        register.append(dict(id="01_"+m["nom"],titre=m["nom"],institution=("DGAFP" if "fonction-publique" in m["source_url"] else
                            "Insee" if "insee.fr" in m["source_url"] else "Cour des comptes" if "ccomptes" in m["source_url"] else
                            "Eurostat" if "ec.europa" in m["source_url"] else "OCDE" if "oecd" in m["source_url"] else "Sénat"),
                            date_publication=publication,url=m["source_url"],date_consultation=m["date_consultation"],acces=m["acces"],
                            sha256_16=m.get("sha256","")[:16],notes=notes))
        if not raw or m["acces"]!="integral":
            continue
        blobs=[]
        if raw.suffix==".zip":
            with zipfile.ZipFile(raw) as z:
                for n in z.namelist():
                    if Path(n).name in files:
                        blobs.append((Path(n).name,z.read(n),n))
        elif raw.suffix==".xlsx":
            inherited={"insee_ip2094_verification":"insee_IP2094_donnees.xlsx",
                       "insee_series_verification":"insee_2493501_marc-empl-eff-fonc-pub_2011-2024.xlsx",
                       "insee_depenses_verification":"insee_2381404_depenses_apu_2025.xlsx"}.get(m["nom"])
            if inherited:
                blobs.append((inherited,raw.read_bytes(),"fichier direct"))
        for name,blob,member in blobs:
            local=hashlib.sha256(files[name].read_bytes()).hexdigest()
            online=hashlib.sha256(blob).hexdigest()
            checks.append(dict(fichier=str(files[name].relative_to(ROOT)),source_url=m["source_url"],source_localisation=member,annee="2024/2025 selon tableau",
                               date_consultation=m["date_consultation"],sha256_local=local,sha256_distribution=online,
                               resultat="IDENTIQUE" if local==online else "DIFFERENT",statut="[FAIT]"))
    write(ROOT/"data/france/01_controle_provenance.csv",checks,list(checks[0]))
    write(ROOT/"sources/registre_01.csv",register,list(register[0]))
    access=[{k:m.get(k,"") for k in ["nom","source_url","date_consultation","http_status","acces","erreur","sha256"]} for m in metadata]
    write(ROOT/"sources/01_acces_internet.csv",access,list(access[0]))
    # Manifeste transportable : archives lourdes non nécessaires au dépôt.
    manifest=ROOT/"sources/01_manifest_telechargements.json"
    manifest.write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"sources":len(register),"fichiers_rapproches":len(checks),"identiques":sum(r["resultat"]=="IDENTIQUE" for r in checks)},ensure_ascii=False))
    if any(r["resultat"]!="IDENTIQUE" for r in checks):
        raise SystemExit("Un brut diffère de la distribution primaire actuelle. Ne pas l'écraser.")


if __name__=="__main__":
    main()
