#!/usr/bin/env python3
"""Fusionne les contre-vérifications indépendantes des volets du lot 3.

Ne rejoue aucun extracteur auteur. Chaque sous-contrôle relit ses sources.
Ce lot porte sur les évaluations de réformes, l'IA et l'audit des annonces :
il ne valide aucune économie nationale ni aucun scénario.
"""
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARTS = ["05", "06_07", "08_09", "10"]
# Statuts résolus : confirmations, avec ou sans réserve explicite, et limites d'accès documentées.
RESERVE_ONLY = {"NON_VERIFIABLE_SOURCE_INACCESSIBLE", "LIMITE_CONFIRMEE"}
UNRESOLVED = {"ECART_SOURCE", "ECART_CALCUL", "NOTE_MODIFIEE_A_RELOCALISER", "NON_VERIFIABLE_CACHE_ABSENT"}


def cache_checks():
    entries=json.loads((ROOT/"sources/lot3_manifestes_cache.json").read_text(encoding="utf-8"))
    checked=[]
    for item in entries:
        path=ROOT/item["raw_path"]
        if not path.is_file():
            raise SystemExit(f"Cache absent, restaurer : python -I scripts/restore_lot3_sources.py --download ({path})")
        if hashlib.sha256(path.read_bytes()).hexdigest()!=item["sha256"]:
            raise ValueError(f"Empreinte différente : {path}")
        checked.append(item["raw_path"])
    return checked


def main():
    rows=[]
    manifests=[]
    expected={"id","theme","indicateur","annee","valeur_publiee","valeur_source","unite","source_url","source_localisation","statut_controle","note"}
    for part in PARTS:
        path=ROOT/f"data/risques/verification_{part}_lot3.csv"
        if not path.exists():
            raise SystemExit(f"Contre-vérification attendue : {path}")
        with path.open(encoding="utf-8-sig",newline="") as stream:
            incoming=list(csv.DictReader(stream))
        if not incoming or set(incoming[0])!=expected:
            raise ValueError(f"Schéma de contrôle inattendu : {path}")
        rows.extend(incoming)
        manifests.append({"fichier":path.relative_to(ROOT).as_posix(),"lignes":len(incoming),"sha256":hashlib.sha256(path.read_bytes()).hexdigest()})
    assert len(rows)>=40
    assert len({r["id"] for r in rows})==len(rows),"Identifiant répété"
    assert all(r["source_url"].startswith("https://") and r["source_localisation"] for r in rows)
    unresolved=[r["id"] for r in rows if r["statut_controle"] in UNRESOLVED]
    assert not unresolved,"Contrôle non résolu ; examiner le détail avant assemblage : "+", ".join(unresolved)
    target=ROOT/"data/risques/verification_chiffres_lot3.csv"
    with target.open("w",encoding="utf-8",newline="") as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]),lineterminator="\n");writer.writeheader();writer.writerows(rows)
    cache=cache_checks()
    summary={"date":"2026-10-30","total":len(rows),"resultats":dict(sorted(Counter(r["statut_controle"] for r in rows).items())),
             "limites_acces":[r["id"] for r in rows if r["statut_controle"] in RESERVE_ONLY],
             "sources_controles":manifests,"cache_rapproche":len(cache)}
    (ROOT/"data/risques/verification_lot3_resume.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
    print(json.dumps({k:v for k,v in summary.items() if k!="sources_controles"},ensure_ascii=False))


if __name__=="__main__":
    main()
