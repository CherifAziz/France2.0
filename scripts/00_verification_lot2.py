#!/usr/bin/env python3
"""Fusionne les contre-vérifications indépendantes des quatre volets du lot 2.

Ne rejoue aucun extracteur auteur. Chaque sous-contrôle relit ses sources.
La présence d'au moins40 lignes ne signifie pas une contre-expertise des futurs
scénarios : ce lot porte sur les bases et périmètres fonctionnels.
"""
import csv
import gzip
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def archive_checks():
    checked=[]
    for part in "abcd":
        for path in sorted((ROOT/f"data/raw/04{part}").glob("*.meta.json")):
            item=json.loads(path.read_text(encoding="utf-8"))
            if not item.get("sha256") or item.get("acces")=="inaccessible":
                continue
            candidates=[]
            if item.get("raw_path"):
                candidates.append(ROOT/item["raw_path"].replace("\\","/"))
            base=path.name.removesuffix(".meta.json")
            candidates.extend(path.parent/(base+ext) for ext in ["", ".csv", ".json", ".xml", ".html", ".pdf", ".xlsx", ".zip"])
            candidates=list(dict.fromkeys(p for p in candidates if p.is_file()))
            matches=[p for p in candidates if hashlib.sha256(p.read_bytes()).hexdigest()==item["sha256"]]
            if len(matches)!=1:
                raise ValueError(f"Empreinte ou localisation non reproduite : {path}; {len(matches)} correspondances")
            archive=matches[0]
            if item.get("sha256_http_body"):
                body=archive.read_bytes()
                if body.startswith(b"\x1f\x8b"):
                    body=gzip.decompress(body)
                assert hashlib.sha256(body).hexdigest()==item["sha256_http_body"],archive
            checked.append({"archive":archive.relative_to(ROOT).as_posix(),"sha256":item["sha256"]})
    return checked


def main():
    rows=[]
    manifests=[]
    for part in "abcd":
        path=ROOT/f"data/risques/verification_04{part}_lot2.csv"
        if not path.exists():
            raise SystemExit(f"Contre-vérification attendue : {path}")
        with path.open(encoding="utf-8-sig",newline="") as stream:
            incoming=list(csv.DictReader(stream))
        expected={"id","theme","indicateur","annee","valeur_publiee","valeur_source","unite","source_url","source_localisation","statut_controle","note"}
        if not incoming or set(incoming[0])!=expected:
            raise ValueError(f"Schéma de contrôle inattendu : {path}")
        rows.extend(incoming)
        manifests.append({"fichier":path.relative_to(ROOT).as_posix(),"lignes":len(incoming),"sha256":hashlib.sha256(path.read_bytes()).hexdigest()})
    assert len(rows)>=40
    assert len({r['id'] for r in rows})==len(rows),"Identifiant répété"
    assert all(r["source_url"].startswith("https://") and r["source_localisation"] for r in rows)
    accepted={"CONFORME","CONFORME_CHAMP_DISTINCT","CONFORME_VALEUR_RESERVE_UNITE","CONFIRME_APRES_CORRECTION","CONFIRME"}
    assert all(r["statut_controle"] in accepted for r in rows),"Contrôle non résolu; examiner le détail avant assemblage"
    target=ROOT/"data/risques/verification_chiffres_lot2.csv"
    with target.open("w",encoding="utf-8",newline="") as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    archives=archive_checks()
    summary={"date":"2026-10-28","total":len(rows),"resultats":dict(Counter(r["statut_controle"] for r in rows)),"sources_controles":manifests,
             "archives_rapprochees":len(archives),"archives":archives}
    (ROOT/"data/risques/verification_lot2_resume.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in summary.items() if k!="archives"},ensure_ascii=False))


if __name__=="__main__":
    main()
