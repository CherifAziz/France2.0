#!/usr/bin/env python3
"""Contre-lecture05 : sources natives relues sans l'extracteur de l'auteur.

Les comparaisons confirment la transcription et ses unités, pas l'attribution
causale ni le caractère budgétaire net des montants publiés.
"""
import csv
import gzip
import hashlib
import io
import json
import re
import sys
from decimal import Decimal as D
from html import unescape
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT/".cache/python_deps"))
from pypdf import PdfReader


def main():
 with (ROOT/"data/reformes/05_indicateurs.csv").open(encoding="utf-8-sig",newline="") as f:claims={r["id"]:r for r in csv.DictReader(f)}
 rows=[]
 def meta(key):return json.loads((ROOT/f"data/raw/05/{key}.meta.json").read_text(encoding="utf-8"))
 def page(key,n):
  m=meta(key);p=ROOT/m["local_path"]
  assert hashlib.sha256(p.read_bytes()).hexdigest()==m["sha256_stored"]
  return PdfReader(p).pages[n-1].extract_text()
 def check(key,source,loc,note="",bound=False):
  r=claims[key];assert D(r["valeur"])==D(str(source)),(key,r["valeur"],source)
  val=(">" if bound else "")+r["valeur"]
  rows.append(dict(id=f"05V{len(rows)+1:02d}",theme="Réformes étrangères",indicateur=r["indicateur"],annee=r["annee"],valeur_publiee=val,
                   valeur_source=(">" if bound else "")+str(source),unite=r["unite"],source_url=r["source_url"],source_localisation=loc,
                   statut_controle="CONFORME_BORNE" if bound else "CONFORME",note=note))
 b=page("DK_POST",3)
 check("DK_POST_CREDIT",re.search(r'DKK\s+(\d+)\s+million\s+in\s+2015',b).group(1),"PDF3, conclusion","Crédits réduits en2015, montant approximatif ; pas tout le secteur public")
 check("DK_POST_CIBLE",re.search(r'potential of\s+DKK\s+(\d+)\s+million',b).group(1),"PDF3, conclusion","Potentiel estimé pour administration centrale, pas économie constatée")

 m=meta("UK_ONS");data=gzip.decompress((ROOT/m["local_path"]).read_bytes()).decode("utf-8-sig")
 source={r[0].strip():r[1] for r in csv.reader(io.StringIO(data)) if len(r)>1}
 for quarter in ["2010 Q2","2016 Q2","2026 Q2"]:
  check("UK_ONS_"+quarter.replace(" ",""),source[quarter],"CSV C9KQ, "+quarter,"Milliers d'ETP, série révisée, pas personnes physiques ; même définition aux trois dates")

 b=page("CA_MODERN26_PDF",3)
 for key,pattern in [("CA_PH_BACK",r'over\s+([\d,]+)\s+pay transactions'),("CA_PH_USERS",r'over\s+([\d,]+)\s+employees')]:
  value=re.search(pattern,b).group(1).replace(",","")
  check(key,value,"PDF3, Overall message, situation30/09/2025","Borne inférieure : plus de, et non égal ; transactions distinctes des personnes",True)
 b=page("CA_MODERN26_PDF",4)
 m=re.search(r'(?:over|more than)\s*\$?\s*(4\.2)\s*billion',b,re.I)
 if not m:
  raise ValueError("Qualifier et coût Dayforce à relire : "+b[-1600:])
 check("CA_PH_NEXT",D(m.group(1))*1000,"PDF4, Key facts and findings","Estimation future incomplète du successeur, pas coût annuel constaté ni économie",True)

 b=page("KR_KONEPS",49);compact=" ".join(b.split())
 for key,pattern in [("KR_PUBLIC",r'Public sector 123\.8 872\.4 166\.3 58\.5 ([\d.]+)'),
                     ("KR_PRIVATE",r'Private sector 826\.9 4074\.6 691\.0 11\.4 ([\d.]+)'),
                     ("KR_TOTAL",r'Total 950\.7 4947\.0 857\.3 69\.9 ([\d.]+)')]:
  check(key,re.search(pattern,compact).group(1),"PDF49 / imprimée48, tableau2.6","USD millions/an d'économies de transaction estimées ; privé/public séparés ; pas un net budgétaire observé")
 assert D(claims["KR_PUBLIC"]["valeur"])+D(claims["KR_PRIVATE"]["valeur"])==D(claims["KR_TOTAL"]["valeur"])

 b=page("JP_RESULT24",2)
 m=re.search(r'合計\(26省庁1,082シ\s*ステム\)\s*([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+▲(\d+)%',b)
 assert m,"Ligne totale japonaise à relire"
 for key,value in zip(["JP_BASE","JP_ADJUSTED","JP_NOMINAL","JP_EXOG","JP_REPORTED"],m.groups()):
  check(key,value.replace(",",""),"PDF2, 合計(26省庁1,082システム), A/B/C/D et pourcentage","Millions JPY pour les coûts ;14% est le retraitement publié, pas la variation nominale ; cible et résultat distincts")
 residual=D(claims["JP_NOMINAL"]["valeur"])-D(claims["JP_EXOG"]["valeur"])-D(claims["JP_ADJUSTED"]["valeur"])
 assert residual==1,"Rapprochement japonais à réexaminer"
 for row in rows:
  if row["source_localisation"].startswith("PDF2, 合計"):
   row["statut_controle"]="CONFORME_RESERVE_ARRONDI"
   row["note"]+=" ; résidu C−D−B=+1 MJPY. La note3 du document signale des arrondis ; compatibilité, sans correction des totaux publiés."

 # Chiffres d'une image : lecture humaine de la figure et verrouillage SHA.
 figure=ROOT/"data/cache/05/US_OPM_figure_2.png"
 for key,value in [("US_OPM_BEFORE",3037),("US_OPM_AFTER",1985)]:
  assert hashlib.sha256(figure.read_bytes()).hexdigest()==claims[key]["figure_sha256"]
  check(key,value,"PDF1, figure OPM, image2 SHA256="+hashlib.sha256(figure.read_bytes()).hexdigest(),"Transcription visuelle indépendante : seule agenceOPM, décembre2024/mars2026 ; pas tout l'emploi fédéral")

 m=meta("US_DOGE");html=gzip.decompress((ROOT/m["local_path"]).read_bytes()).decode("utf-8")
 clean=lambda x:" ".join(unescape(re.sub(r'<[^>]+>',' ',x)).split())
 tables=[clean(t) for t in re.findall(r'<table\b.*?</table>',html,re.S|re.I)]
 table=next(t for t in tables if "DOGE followed its stated methodology" in t and "Unknown due to missing contract identifiers" in t)
 for key,pattern in [("US_METHOD_PCT",r'DOGE did not follow its stated methodology\s*b?\s*3,910\s*\$37\.0\s*(60\.7)'),
                     ("US_CONTRACTS",r'Total\s+13,476\s*\$(61\.0)\s*100\.0')]:
  check(key,re.search(pattern,table).group(1),"GAO26-108615, tableau4, cliché DOGE07/07/2026 et FPDSavril2026","60,7% des sommes de contrats : méthode différente/indéterminée pour contrats appariés ;11,8% supplémentaires sans identifiants. Respecter la méthode annoncée ne certifie pas une économie nette.")

 target=ROOT/"data/risques/verification_05_lot3.csv"
 with target.open("w",encoding="utf-8",newline="") as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 print(f"05 : {len(rows)} contrôles conformes, dont trois bornes strictes ; aucun extracteur auteur utilisé")


if __name__=="__main__":main()
