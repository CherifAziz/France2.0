#!/usr/bin/env python3
"""Collecte reproductible des pièces : python -I scripts/06_collecte.py [--download].
Les PDF restent en cache ; les manifestes et pages effectivement lues sont versionnés.
"""
import argparse, concurrent.futures, csv, hashlib, json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PREFIX="06"
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--download",action="store_true");args=ap.parse_args()
    sources=json.loads((ROOT/f"sources/{PREFIX}_sources.json").read_text(encoding="utf-8"))
    def collect(s):
        directory=ROOT/f"data/{'cache' if s['ext']=='pdf' else 'raw'}/{PREFIX}"
        p=ROOT/s["chemin_reemploi"] if s.get("chemin_reemploi") else directory/(s["id"]+"."+s["ext"])
        if args.download and not p.exists() and not s.get("chemin_reemploi"):
            result=subprocess.run([sys.executable,"-I",str(ROOT/"scripts/fetch.py"),s["url"],s["id"],"--out-dir",str(directory),"--timeout","40"],capture_output=True,text=True,encoding="utf-8",errors="replace")
        meta=p.with_suffix(".meta.json")
        m=json.loads(meta.read_text(encoding="utf-8")) if meta.exists() else {"acces":"inaccessible","http_status":"","sha256":"","date_consultation":"2026-10-28","raw_path":str(p)}
        out=ROOT/"sources";out.mkdir(parents=True,exist_ok=True)
        pinned=out/(PREFIX+"_manifeste_"+s["id"]+".json")
        before=json.loads(pinned.read_text(encoding="utf-8")) if pinned.exists() else {}
        if before.get("acces")=="integral" and m.get("acces")=="integral" and before.get("sha256")!=m.get("sha256"):
            alternate=out/(PREFIX+"_manifeste_"+s["id"]+"_distribution_courante.json")
            alternate.write_text(json.dumps(m,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
            s["note_acces"]=s.get("note_acces","")+" EMPREINTE_MODIFIEE : manifeste initial conservé ; nouvelle distribution à revoir."
            print(f"EMPREINTE_MODIFIEE : {s['id']}",file=sys.stderr)
        else:
            pinned.write_text(json.dumps(m,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        access=s.get("acces_override") or ("partiel" if m.get("acces")=="integral" else m.get("acces","inaccessible"))
        source_hash=m.get("sha256","")[:16] if m.get("acces")=="integral" and access!="inaccessible" else ""
        return dict(id=PREFIX+"_"+s["id"],titre=s.get("titre",s["id"]),institution=s["institution"],date_publication=s["date_publication"],url=s["url"],date_consultation=m.get("date_consultation","2026-10-28"),acces=access,sha256_16=source_hash,notes=f"Archive : {m.get('raw_path',p)}. HTTP {m.get('http_status','')}. Pages/sections lues : {s['pages_lues'] or 'NON ENCORE LUES'}. Archive complète ne signifie pas lecture complète. {m.get('erreur',m.get('error',''))}. {s.get('note_acces','')}")
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: rows=list(pool.map(collect,sources))
    dest=ROOT/f"sources/registre_{PREFIX}.csv"
    with dest.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=["id","titre","institution","date_publication","url","date_consultation","acces","sha256_16","notes"]);w.writeheader();w.writerows(rows)
    print(json.dumps({"prefixe":PREFIX,"sources":len(rows),"acces":{s:sum(r["acces"]==s for r in rows) for s in set(r["acces"] for r in rows)}},ensure_ascii=False))
if __name__=="__main__":main()
