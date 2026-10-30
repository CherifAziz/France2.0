#!/usr/bin/env python3
"""Transcriptions contrôlées et calculs, sans extrapolation nationale.
Les faits PDF sont des transcriptions manuelles documentées, pas un parseur sémantique.
python -I scripts/07_analyse.py [--download]
Une preuve lue via outil web est exportée avec cette limite ; elle n'est pas déclarée
recontrôlée localement. Les fichiers absents ne sont jamais remplacés par zéro.
"""
import argparse, csv, hashlib, json, re, subprocess, sys, unicodedata
from collections import Counter
from pathlib import Path
from pypdf import PdfReader
ROOT = Path(__file__).resolve().parents[1]
PREFIX = "07"
OUT = ROOT / "data/reformes"
def canon(s):
    return re.sub(r"\s+", "", unicodedata.normalize("NFKC", str(s))).casefold()
def write_csv(name, rows):
    if not rows:
        return
    cols = list(dict.fromkeys(k for r in rows for k in r))
    with (OUT / (PREFIX + "_" + name + ".csv")).open("w", encoding="utf-8", newline="") as f:
        w=csv.DictWriter(f,fieldnames=cols);w.writeheader();w.writerows(rows)
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--download",action="store_true");args=ap.parse_args()
    if args.download:
        subprocess.run([sys.executable,"-I",str(ROOT/f"scripts/{PREFIX}_collecte.py"),"--download"],check=True)
    sources = {s["id"]: s for s in json.loads((ROOT/f"sources/{PREFIX}_sources.json").read_text(encoding="utf-8"))}
    bundle = json.loads((ROOT/f"sources/{PREFIX}_donnees_controlees.json").read_text(encoding="utf-8"))
    OUT.mkdir(parents=True,exist_ok=True)
    readers, controls = {}, []
    def enrich(row):
        row=dict(row)
        sid=row.pop("source_id", "")
        s=sources.get(sid)
        if not s:
            raise ValueError(f"Source inconnue : {sid}")
        row["source_url"]=s["url"]
        row.setdefault("date_publication",s["date_publication"])
        row.setdefault("date_consultation","2026-10-28")
        p=ROOT/s["chemin_reemploi"] if s.get("chemin_reemploi") else ROOT/f"data/{'cache' if s['ext']=='pdf' else 'raw'}/{PREFIX}/{sid}.{s['ext']}"
        meta=p.with_suffix(".meta.json")
        m=json.loads(meta.read_text(encoding="utf-8")) if meta.exists() else {}
        valid=p.exists() and m.get("acces")=="integral" and s.get("acces_override")!="inaccessible"
        # Les pièces 04d peuvent utiliser un nom de manifeste différent ; elles restent
        # identifiées comme réemploi, jamais comme nouvel inventaire indépendant.
        if s.get("chemin_reemploi") and p.exists():
            valid=True
        anchor=row.pop("ancre", "")
        page=row.get("page_pdf")
        state="SANS_ANCRE_TRANSCRIPTION_MANUELLE"
        if valid:
            digest=hashlib.sha256(p.read_bytes()).hexdigest()
            row["sha256_16"]=digest[:16]
            pinned=ROOT/f"sources/{PREFIX}_manifeste_{sid}.json"
            locked=json.loads(pinned.read_text(encoding="utf-8")) if pinned.exists() else {}
            mismatch=locked.get("acces")=="integral" and locked.get("sha256") and locked["sha256"]!=digest
            if anchor:
                if p.suffix==".pdf":
                    if not page:raise ValueError(f"Page manquante : {row.get('id')}")
                    if sid not in readers:readers[sid]=PdfReader(p)
                    body=readers[sid].pages[int(page)-1].extract_text(extraction_mode="layout")
                else:
                    txt=p.with_suffix(".txt")
                    body=txt.read_text(encoding="utf-8") if txt.exists() else p.read_text(encoding="utf-8",errors="replace")
                state="ANCRE_CONFIRMEE" if canon(anchor) in canon(body) else "ECHEC_ANCRE"
            if mismatch:state="ECHEC_EMPREINTE"
        elif s.get("acces_override")=="partiel" and ("web" in s.get("note_acces","").lower() or "web" in s.get("pages_lues","").lower()):
            state="LECTURE_WEB_DOCUMENTEE_SANS_RECONTROLE_LOCAL"
        elif row.get("statut") in ("EXTRAIT","NON TROUVÉ"):
            state="LIMITATION_DECLAREE"
        else:
            state="ARCHIVE_ABSENTE_OU_INACCESSIBLE"
        row["controle_archive"]=state
        row.setdefault("sha256_16","")
        row["restauration"]=f"python -I scripts/{PREFIX}_collecte.py --download" if not valid else ""
        controls.append(dict(id=row.get("id",""),controle="ancre et disponibilité de la source",resultat=state,source_url=s["url"],source_localisation=row.get("source_localisation",""),annee=row.get("annee",""),statut=row.get("statut",""),note=row.get("restauration","")))
        return row
    datasets={}
    for name,rows in bundle.items():
        if name.startswith("_"):
            continue
        datasets[name]=[enrich(r) for r in rows]
    facts=datasets.get("indicateurs",[])
    d={r["id"]:r for r in facts}
    def value(k):return float(d[k]["valeur"])
    def check(name,passed,note):
        controls.append(dict(id=name,controle="identité arithmétique",resultat="CONFIRME" if passed else "ECHEC_IDENTITE",source_url="",source_localisation="sources/"+PREFIX+"_donnees_controlees.json",annee="",statut="ESTIMATION",note=note))
    def computed(id,label,v,unit,year,formula,parents,note=""):
        source=d[parents[0]]
        facts.append(dict(id=id,theme="Calcul de contrôle",indicateur=label,annee=year,valeur=round(v,9),unite=unit,champ=source["champ"],nature_mesure="calcul, pas économie potentielle",statut="ESTIMATION",source_localisation=formula,source_url=source["source_url"],date_publication=source["date_publication"],date_consultation="2026-10-28",controle_archive="CALCUL_A_PARTIR_DES_TRANSCRIPTIONS",sha256_16="",note=note))
    if PREFIX=="06":
        check("mouvements_operateurs",431-3+1-4-1-1==423,"431 - 3 sorties + 1 entrée - 4 IRA - 1 IPEV - 1 Ensemble intercontemporain =423 ; mouvements de personnes morales, pas agents")
        check("decomposition_plafond",401389-235-998+34+1+339-3248==397282,"Extension -235, impact schéma -998, transferts+34, périmètre+1, corrections+339, abattement technique -3248 ETPT")
        computed("plafond_delta","Variation du plafond sous plafond",value("plafond_2027")-value("plafond_2026"),"ETPT","2026-2027","397282 - 401389",["plafond_2027"])
        computed("vacance_part_delta","Part de l'abattement technique dans la baisse de plafond",100*3248/4107,"%","2027","100 ×3248 /4107",["vacance_abattement"],"Ce ratio ne convertit pas la vacance en emplois réels supprimés.")
        computed("scsp_hors_asc_delta","Variation SCSP après seule neutralisation ASC",(33102810903-33969713197+460098952)/1e6,"M€ CP","2026-2027","(33102810903 -33969713197 +460098952)/1000000",["scsp_2027"],"Correction partielle ; la comparaison de périmètre complète donne une autre base.")
        computed("scsp_perimetre_delta","Variation SCSP au périmètre complet 2027",(33102810903-33519966787)/1e6,"M€ CP","2026-2027","(33102810903 -33519966787)/1000000",["scsp_2027"])
        computed("financement_delta","Variation financement public annoncé",(72572274321-73637270504)/1e6,"M€ CP et taxes","2026-2027","(72572274321 -73637270504)/1000000",["financement_2027"],"Projet et LFI ; aucune attribution causale à une réforme de gestion.")
        computed("dgfip_etpt_delta","Variation ETPT DGFiP 2015-2025",91064-107202,"ETPT","2015-2025","91064 -107202",["dgfip_etpt_2025"],"Ne pas confondre cette série RH avec les emplois du tableau Cour 2008-2022 ou les PP ISORA.")
        computed("spf_etp_delta","Variation des ETP SPF",3164-3382,"ETP","2021-2023","3164 -3382",["spf_etp_2023"],"Source arrondit la baisse à220 ; calcul exact des deux points transcrits =218. Non attribuable au seul ANF.")
        for operator in ("ADEME","ANAH"):
            rows=[r for r in datasets["fiches_operateurs"] if r["operateur"]==operator and r["type_tableau"]=="autorisations budgétaires" and r["unite"]=="k€ CP"]
            by={r["indicateur"]:float(r["valeur"]) for r in rows}
            check("budget_"+operator,abs(sum(by[k] for k in ["Personnel","Fonctionnement","Intervention","Investissement"])-by["Total dépenses"])<=1,"Somme des CP par nature ; tolérance1k€ pour arrondis")
        rows=[r for r in datasets["fiches_operateurs"] if r["operateur"]=="France Travail" and r["type_tableau"]=="compte de résultat"]
        by={r["indicateur"]:float(r["valeur"]) for r in rows}
        check("charges_France_Travail",sum(by[k] for k in ["Personnel","Fonctionnement","Intervention"])==by["Total charges"],"Charges BI2026, pas coût administratif central.")
        check("15_domaines",len(datasets.get("domaines",[]))==15,"Couverture des15domaines ; aucune preuve d'exhaustivité des viviers ou de suppression.")
    else:
        check("dlnuf_2020",78+34+18+77+35==242,"Somme des5classes du tableau5 Cour2024")
        check("dlnuf_2023",137+28+31+29+23==248,"Somme des5classes ; six démarches ajoutées, cohortes différentes")
        computed("dlnuf_hausse_pp","Hausse de la part à zéro ou une information",55.2-32.2,"points de pourcentage","2020-2023","55.2 -32.2",["dlnuf_simple_2023"],"Évolution descriptive, changement de cohorte et d'évaluation ; pas gain ETP.")
        computed("sva_part_2015","Part des procédures État soumises au SVA en2015",100*1200/3600,"% des procédures","2015","100 ×1200 /3600",["sva_procedures"],"Pas un taux de demandes, ni la règle observée en2026.")
        computed("essoc_moyenne","Moyenne annuelle des régularisations sur2019-2021",116500/3,"procédures/an","2019-2021","116500 /3",["essoc_regularisations"],"Ne pas comparer un cumul de3ans à3800par an ; résultat descriptif, pas causal ni économie.")
    for name,rows in datasets.items():write_csv(name,rows)
    write_csv("controles",controls)
    counts=Counter(c["resultat"] for c in controls)
    print(json.dumps(dict(prefixe=PREFIX,lignes={k:len(v) for k,v in datasets.items()},controles=dict(counts)),ensure_ascii=False))
    if counts["ECHEC_ANCRE"] or counts["ECHEC_IDENTITE"] or counts["ECHEC_EMPREINTE"]:
        raise SystemExit("Échec des contrôles : voir CSV ; aucune réparation silencieuse.")
if __name__=="__main__":main()

