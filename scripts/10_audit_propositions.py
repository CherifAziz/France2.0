#!/usr/bin/env python3
"""Audit documentaire des montants annoncés et illustration du calendrier.

Les valeurs politiques sont des annonces, jamais des économies nettes validées.
Les transcriptions PDF signalées ne calibrent pas le moteur national.
"""
import csv
import gzip
import hashlib
import json
import re
from decimal import Decimal as D
from html import unescape
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CACHE=ROOT/"data/cache/10"
RAW=ROOT/"data/raw/10"
OUT=ROOT/"data/reformes"
DATE="2026-10-28"
SITE="https://www.budget2027.fr/"

# Paraphrases de l'auditeur : le texte politique intégral reste dans l'archive.
LABELS=[
 (1,"Effectifs", "Recrutements évités sur cinq ans", "Emplois", "Vivier administratif, départs définitifs, coût d'entrée et calendrier non établis ; trois périmètres de pensions à distinguer"),
 (2,"Effectifs", "Productivité administrative par IA", "Gestion", "Source IGF–IGAS2025 non identifiée avec certitude ; exposition et temps libéré ne prouvent pas une économie ; recouvrement possible avec01"),
 (3,"Prestations", "Condition de nationalité pour des aides non contributives", "Prestations", "Baisse de prestations, pas coût administratif ; population et droits actuels à préciser, réactions et recouvrements avec04/05"),
 (4,"Prestations", "Durée du RSA plafonnée pour certains allocataires", "Prestations", "Articulation avec03, entrées-sorties et reprise d'emploi à mesurer ; pas cinq années d'économie immédiate"),
 (5,"Prestations", "Fraudes et exclusions de certaines aides", "Prestations/recouvrement", "Fraude estimée, droits suspendus et sommes effectivement recouvrées sont distincts ; contrôler les populations déjà exclues par03/04"),
 (6,"Structures", "Arrêt de certains soutiens énergétiques", "Interventions", "Contrats et engagements existants, prix de marché et compensation à instruire ; exclusion déclarée de la ligne09 à réconcilier"),
 (7,"Structures", "Fin des dispositifs de politique urbaine", "Interventions", "Périmètre interministériel/local et financements associatifs à consolider ; pas une simple économie de personnel"),
 (8,"Structures", "Fermeture de l'opérateur du logement Anah", "Institution/interventions", "Aides distribuées et coût propre distincts ; missions reprises, engagements et paie éventuellement incluse en01 à traiter"),
 (9,"Structures", "Fermeture de l'Ademe, avec exclusion énergétique annoncée", "Institution/interventions", "Exclusion de06 revendiquée mais pont comptable absent ; budget d'intervention distinct des supports ; postes potentiellement visés en01"),
 (10,"Structures", "Retrait de l'activité de placement de France Travail", "Service public", "Budget de l'organisme, placement LMP et masse salariale ne sont pas le même champ ; usagers, droits, prestataires et reconversion à traiter"),
 (11,"Structures", "Disparition des ARS", "Institution", "Suppression juridique sans description de reprise des missions ; coût transféré et éventuels effectifs également visés en01 à déduire"),
 (12,"Structures", "Suppression d'une liste d'organismes et commissions", "Institution", "Liste ouverte et coût non ventilé ; vérifier les organismes déjà remplacés, missions transférées et recouvrement avec01"),
 (13,"Structures", "Suppression du CESE et des conseils régionaux associés", "Institution", "Budgets État/régions, indemnités, agents, patrimoine et obligations de transition à consolider"),
 (14,"International", "Arrêt de l'aide au développement et de l'AFD", "Interventions/instruments financiers", "APD statistique, prêts, dons, remboursements et budget de l'agence distincts ; participation multilatérale et contribution UE à rapprocher"),
 (15,"International", "Contribution européenne ramenée à une référence antérieure", "Transfert", "Année de référence et engagements européens à préciser ; pas baisse automatique des frais administratifs ; contrôler la composante APD de14"),
 (16,"International", "Frais d'études accrus pour des étudiants étrangers", "Recettes/service", "Recette de tarification distincte d'économie ; droits déjà perçus et exonérations, demande, accessibilité et coût marginal à établir"),
 (17,"International", "Suppression de l'AME", "Prestation/service de santé", "Baisse brute du dispositif distincte du coût net de soins urgents ou différés et des missions reprises ; pas coût administratif intégral"),
 (18,"International", "Hausse du tarif des visas", "Recettes", "Différence de tarif multipliée par volumes effectifs et taux de recouvrement ; demande, exemptions et frais consulaires à déduire"),
 (19,"International", "Restriction de l'hébergement d'urgence", "Prestation/service", "Population, dépenses réellement évitables, obligations actuelles et report vers d'autres dispositifs à établir"),
 (20,"International", "Condition de nationalité pour l'aide juridictionnelle", "Prestation/accès aux droits", "Dépense de dossiers concernés, exceptions et modifications du droit à documenter ; pas budget total de la justice"),
 (21,"Médias", "Cession du secteur audiovisuel public", "Financement/service/actifs", "Dotations récurrentes et prix ponctuel des actifs séparés ; obligations maintenues, passifs, personnel et coûts de cession à établir"),
 (22,"Médias", "Réduction d'aides associatives sur critère politique", "Interventions", "Critère de sélection et bénéficiaires non définis ; prestations publiques déléguées et recouvrements avec07/23 à identifier"),
 (23,"Médias", "Arrêt des soutiens à la presse", "Interventions/dépenses fiscales", "Identifier aides directes et avantages fiscaux, montants réellement annulables et bénéficiaires déjà visés par22"),
 (24,"Médias", "Arrêt de financements syndicaux", "Financement/dialogue social", "Subventions, financement paritaire et décharges de personnel distincts ; contrôler le recouvrement avec01"),
]


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def write_csv(name,rows):
 OUT.mkdir(parents=True,exist_ok=True)
 with (OUT/name).open("w",encoding="utf-8",newline="") as s:
  w=csv.DictWriter(s,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)


def archive_site():
 RAW.mkdir(parents=True,exist_ok=True)
 path=RAW/"budget2027_20261028.html.gz"
 if not path.exists():
  source=CACHE/"budget2027_actualisation.html"
  data=source.read_bytes();path.write_bytes(gzip.compress(data,mtime=0))
  m=json.loads(source.with_suffix(".meta.json").read_text(encoding="utf-8"))
  m.update(raw_path=path.relative_to(ROOT).as_posix(),sha256=sha(path),sha256_http_body=hashlib.sha256(data).hexdigest(),compression="gzip sans perte, mtime0",bytes=path.stat().st_size,original_bytes=len(data))
  path.with_name(path.name+".meta.json").write_text(json.dumps(m,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 m=json.loads(path.with_name(path.name+".meta.json").read_text(encoding="utf-8"))
 assert sha(path)==m["sha256"]
 data=gzip.decompress(path.read_bytes());assert hashlib.sha256(data).hexdigest()==m["sha256_http_body"]
 return data.decode("utf-8"),m


def announced():
 text,meta=archive_site(); rows=[]
 items=re.findall(r'<li\b([^>]*class="mesure"[^>]*)>(.*?)</li>',text,re.S)
 assert len(items)==24
 for attrs,body in items:
  def content(cls):
   m=re.search(r'<(?:span|p) class="'+cls+r'">(.*?)</(?:span|p)>',body,re.S)
   return unescape(re.sub(r'<[^>]+>','',m.group(1))).strip()
  number=int(content("mesure-num")); label=LABELS[number-1];assert label[0]==number
  amount=content("mesure-montant")
  nums=[D(x.replace(",",".")) for x in re.findall(r'\d+(?:,\d+)?',amount)]
  factor=D("0.001") if "Md" not in amount else D(1)
  low=nums[0]*factor;high=nums[1]*factor if " à " in amount else low
  counter=D(re.search(r'data-valeur="([^"]+)"',attrs).group(1))
  assert counter==(low+high)/2
  rows.append(dict(id=f"K{number:02d}",bloc=label[1],mesure=label[2],nature=label[3],
                   annonce_min_MdEUR=str(low),annonce_max_MdEUR=str(high),valeur_attribut_compteur_MdEUR=str(counter),
                   cession_actifs_ponctuelle_en_plus=number==21,economie_nette_APU_validee_MdEUR="",
                   diagnostic=label[4],annee="NON PRÉCISÉE ; bandeau Budget2026, URL budget2027",
                   source_url=SITE,source_localisation=f"li.mesure numéro{number}; span.mesure-montant; data-valeur",statut="FAIT",
                   note="Fait sur l'annonce uniquement ; aucun montant net réalisable validé ; prix et horizon de valorisation non explicités",date_consultation=DATE,sha256_corps_HTTP=meta["sha256_http_body"]))
 write_csv("10_plan_annonces.csv",rows)
 totals=[]
 for bloc in ["Effectifs","Prestations","Structures","International","Médias","TOTAL"]:
  subset=rows if bloc=="TOTAL" else [r for r in rows if r["bloc"]==bloc]
  totals.append(dict(bloc=bloc,borne_basse_annonces_MdEUR=str(sum(D(r["annonce_min_MdEUR"]) for r in subset)),
                     borne_haute_annonces_MdEUR=str(sum(D(r["annonce_max_MdEUR"]) for r in subset)),
                     somme_attributs_compteur_MdEUR=str(sum(D(r["valeur_attribut_compteur_MdEUR"]) for r in subset)),
                     cible_totale_affichee_MdEUR="140" if bloc=="TOTAL" else "",annee="horizon non explicité",
                     source_url=SITE,source_localisation="24 lignes, montants en MdEUR, hors prix ponctuel de cession",statut="ESTIMATION",
                     note="Addition des annonces, pas addition d'économies nettes ou indépendantes ; attributs du compteur = milieux de fourchettes"))
 assert D(totals[-1]["borne_basse_annonces_MdEUR"])==D("138.366")
 assert D(totals[-1]["borne_haute_annonces_MdEUR"])==D("145.366")
 assert D(totals[-1]["somme_attributs_compteur_MdEUR"])==D("141.866")
 write_csv("10_sommes_annonces.csv",totals)
 return rows


def calendar():
 rows=[]
 for convention,weight in [("année pleine",D(1)),("départs répartis à mi-année",D("0.5"))]:
  cumulative=D(0)
  for year in range(1,6):
   new=D(160000);previous=new*(year-1);average=previous+new*weight
   saving=average*D(50000)/D(10)**9;cumulative+=saving
   rows.append(dict(convention=convention,annee=2026+year,flux_annuel_postes_illustratif=new,stock_fin_annee_postes=previous+new,
                    poste_annee_valorises=average,cout_unitaire_implicite_EUR=50000,economie_brute_illustrative_MdEUR=saving,
                    cumul_brut_illustratif_MdEUR=cumulative,economie_nette_validee="",source_url=SITE,
                    source_localisation="K01 ; hypothèse propre : 800000/5 chaque année, 40Md/800000=50000EUR",
                    statut="HYPOTHÈSE",note="Illustration arithmétique sans validation du vivier, des départs, du coût d'entrée, des pensions, du GVT ou des transitions ; pas un scénario national"))
  assert cumulative==(D(120) if weight==1 else D(100))
 write_csv("10_calendrier_800000_illustration.csv",rows)


def overlaps():
 edges=[("K01","K02","Temps administratif et postes évités","Levier de réalisation du même objectif ou vivier additionnel à préciser"),
        *[("K01",f"K{i:02d}","Effectifs ou tâches potentiellement communs au vivier et à l'institution","Vérifier d'abord le champ FP/APU/statuts de l'organisme, puis identifier les postes communs ; inclusion non présumée") for i in [8,9,10,11,12,13]],
        ("K03","K04","Allocataires RSA concernés par deux critères","Appliquer le second critère aux seuls droits encore servis après le premier"),
        ("K03","K05","Droits supprimés et fraude sur les mêmes aides","Éviter de recouvrer une somme déjà supprimée dans le contrefactuel"),
        ("K06","K09","Soutien énergétique et interventions Ademe","Exclusion annoncée dansK09 ; exiger le pont comptable par dispositif, pas supposer une double économie certaine"),
        ("K07","K22","Subventions associatives de politique urbaine","Apparier les bénéficiaires et dispositifs"),
        ("K14","K15","APD multilatérale et contribution européenne","Vérifier si la contribution statistique d'aide est déjà affectée à la réduction européenne"),
        ("K22","K23","Bénéficiaires associatifs des aides à la presse","Identifier les personnes morales et les lignes de financement concernées")]
 write_csv("10_recouvrements_a_instruire.csv",[dict(mesure_a=a,mesure_b=b,intersection=c,regle=d,montant_deduplication_MdEUR="",annee="horizon non explicité",statut="HYPOTHÈSE",source_url=SITE,source_localisation=f"Mesures {a}/{b}",note="Risque à instruire, pas montant de double compte démontré") for a,b,c,d in edges])


def primary():
 rows=[]; name="dp_budget2027";m=json.loads((CACHE/(name+".meta.json")).read_text(encoding="utf-8"))
 path=ROOT/m["raw_path"];assert sha(path)==m["sha256"]
 text=path.with_suffix(".txt").read_text(encoding="utf-8")
 entries=[(29,"Effort total proposé",54,"MdEUR", "54 Md€"),(29,"Mesures dans PLF et PLFSS",43,"MdEUR","43 Md€"),
          (30,"Réforme formation initiale enseignants",4742,"ETP de schéma d'emplois","4 742"),(30,"Marche LPM",2150,"ETP de schéma d'emplois","2 150"),
          (31,"Effort net des caisses SS",-1000,"postes annoncés, référence au schéma final","1 000"),
          (59,"État, budget général et annexes",8025,"ETP de schéma d'emplois","8 025"),(59,"Opérateurs",-1209,"ETP de schéma d'emplois","-1 209"),
          (59,"État et opérateurs, sous-total",6816,"ETP de schéma d'emplois","6 816"),(59,"Administration centrale, sous-ensemble",-812,"ETP de schéma d'emplois","-812"),
          (59,"Numérique réinternalisé, sous-ensemble",404,"ETP de schéma d'emplois","+404"),
          (59,"Plafond État",2032750,"ETPT plafonnés","2 032 750"),(59,"Plafond opérateurs",397282,"ETPT plafonnés","397 282"),
          (59,"Total général, périmètre retraité",-1076,"ETP y.c.caisses SS, hors formation et marche LPM","-1 076")]
 compact=lambda t: re.sub(r"\s+","",t)
 for page,label,value,unit,anchor in entries:
  body=re.search(r"\[PAGE "+str(page)+r"\](.*?)(?=\[PAGE |\Z)",text,re.S).group(1)
  assert compact(anchor) in compact(body),(page,anchor)
  rows.append(dict(indicateur=label,valeur=value,unite=unit,annee=2027,champ="Projet de budget présenté en octobre2026 ; pas exécution",source_url=m["source_url"],source_localisation=f"PDF p.{page}; imprimée{page-19 if page<58 else page-50}",statut="FAIT",methode="Transcription manuelle avec ancre ; double page58–59 inspectée visuellement",note="FAIT de projet publié ; flux, plafonds et sous-ensembles ne s'additionnent pas",sha256=m["sha256"]))
 assert 8025-1209==6816 and 6816-4742-2150-1000==-1076
 # Le HTML est déclaré UTF8 dans sa balise meta ; pas de lecture du livre.
 p=CACHE/"fayard_casse.html";html=p.read_bytes().decode("utf-8")
 objects=[]
 def walk(x):
  if isinstance(x,dict):
   if x.get("isbn")=="9782213733135" and "datePublished" in x:objects.append(x)
   for v in x.values():walk(v)
  elif isinstance(x,list):
   for v in x:walk(v)
 for payload in re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',html,re.S):walk(json.loads(unescape(payload)))
 book=next(x for x in objects if "numberOfPages" in x)
 assert book["datePublished"]=="2026-09-02" and book["numberOfPages"]==286
 for key in ["datePublished","numberOfPages"]:
  rows.append(dict(indicateur="Livre, métadonnée éditeur "+key,valeur=book[key],unite="date" if key=="datePublished" else "pages déclarées",annee=2026,champ="Fiche éditeur et JSON-LD, pas texte du livre",source_url="https://www.fayard.fr/livre/le-casse-du-siecle-9782213733135/",source_localisation="script application/ld+json ; Book."+key,statut="FAIT",methode="JSON-LD UTF8",note="Ni lecture intégrale ni validation des chiffres du livre",sha256=sha(p)))
 # Source partagée avec06, lue directement ici : BI2026 dans le jaune2027.
 opmeta=json.loads((ROOT/"data/cache/06/operateurs_plf2027.meta.json").read_text(encoding="utf-8"))
 op=ROOT/opmeta["raw_path"];assert sha(op)==opmeta["sha256"]
 optxt=op.with_suffix(".txt").read_text(encoding="utf-8")
 for page,operator,values in [(226,"Ademe",[104788,175907,1322880,1603575]),(246,"Anah",[25000,175854,3450687,3651541]),(458,"France Travail",[3886736,1030052,1972446,6889234])]:
  body=re.search(r"\[PAGE "+str(page)+r"\](.*?)(?=\[PAGE |\Z)",optxt,re.S).group(1)
  assert "2026" in body and "Initial" in body and sum(values[:3])==values[3]
  for label,value in zip(["Personnel","Fonctionnement hors personnel","Intervention","Total charges"],values):
   assert str(value) in compact(body)
   rows.append(dict(indicateur=operator+" / "+label,valeur=str(D(value)/1000),unite="M EUR; compte de résultat",annee=2026,champ="Budget initial2026 présenté dans le jaune opérateurs PLF2027, pas exécution2026 ni budget2027",source_url=opmeta["source_url"],source_localisation=f"PDF p.{page}; compte de résultat; milliers EUR source",statut="FAIT",methode="Transcription manuelle et contrôle d'ancre/somme, distinct de l'extracteur06",note="Interventions, charges propres et financements ne sont pas des économies nettes ; ne pas ajouter les CP au compte de résultat",sha256=opmeta["sha256"]))
 write_csv("10_indicateurs_primaires.csv",rows)


def registry():
 publication={"budget2027_actualisation":"NON TROUVÉ; page Budget2026 sur URL2027", "budget2027":"NON TROUVÉ",
              "bercy_plf2027_presentation":"2026-10-01", "dp_budget2027":"2026-10-01", "dp_budget2027_page":"2026-10-01",
              "fayard_casse":"2026-09-02 pour le livre; date de la fiche NON TROUVÉE", "montaigne_bilan2021":"2021-10", "montaigne_presidentielle2017":"2017; jour exact NON TROUVÉ",
              "senat_lfi2026":"2026-02-19 pour la loi; rectificatif2026-10-10", "operateurs_plf2027":"2026-10-12"}
 consulted={"dp_budget2027":"PDF29–31 et double page58–59 lus; recherche ciblée sur montants; pas lecture exhaustive des147pages",
            "budget2027_actualisation":"24 annonces et comparaison, liens inspectés ; aucun lien de source par mesure trouvé",
            "budget2027":"Instantané antérieur identique; pas une seconde observation indépendante",
            "fayard_casse":"Métadonnées JSON-LD et lien de feuilletage; texte intégral non lu",
            "hachette_feuilletage":"Coquille HTML de lecteur seulement ; aucun texte du livre lu",
            "montaigne_bilan2021":"PDF p.4–5, engagement120000 et contexte; position d'un think tank, pas compte public exécuté",
            "montaigne_macron_chiffrage2017":"Lien cible reçu en HTTP200 mais article sans rapport avec la fiche demandée ; méthode du chiffrage non retrouvée sur ce lien",
            "operateurs_plf2027":"Réemploi de source06; PDF226/246/458 comptes de résultat BI2026, sommes relues; pas comptes2027"}
 out=[];manifest=[]
 paths=sorted(CACHE.glob("*.meta.json"))+[ROOT/"data/cache/06/operateurs_plf2027.meta.json"]
 for p in paths:
  item=json.loads(p.read_text(encoding="utf-8"));stem=p.name.removesuffix(".meta.json")
  institution="Bercy" if stem.startswith(("dp_","bercy_","operateurs_")) else "Institut Montaigne" if stem.startswith("montaigne") else "Sénat" if stem.startswith("senat_") else "Fayard/Hachette" if stem.startswith(("fayard_","hachette_")) else "HCFP/Légifrance" if stem.startswith("hcfp") else "Gouvernement" if stem.startswith(("bayrou_","conseil_")) else "Site politique Sarah Knafo"
  access="partiel" if stem=="montaigne_macron_chiffrage2017" else item.get("acces","inaccessible")
  out.append(dict(id="10_"+stem,titre=stem.replace("_"," "),institution=institution,date_publication=publication.get(stem,"NON TROUVÉ"),url=item["source_url"],date_consultation=item["date_consultation"],acces=access,sha256_16=item.get("sha256","")[:16],notes=consulted.get(stem,"Lecture ciblée de la page si accessible ; tentative signalée sinon"),archive=item.get("raw_path",""),sha256=item.get("sha256","")))
  manifest.append(dict(item,lecture=consulted.get(stem,"Voir registre")))
 p=RAW/"hcfp_2026_5_extraits_recherche.json"
 out.append(dict(id="10_hcfp_extrait",titre="HCFP2026-5, réponse de recherche indexée",institution="HCFP/Légifrance",date_publication="2026-09-25; JORF2026-10-02",url="https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000054939509",date_consultation=DATE,acces="extrait_recherche",sha256_16=sha(p)[:16],notes="L'ouverture primaire a échoué403, HCFP timeout; empreinte du conteneur de recherche, pas PDF authentifié; aucune promotion en lecture intégrale",archive=p.relative_to(ROOT).as_posix(),sha256=sha(p)))
 target=ROOT/"sources/registre_10.csv"
 with target.open("w",encoding="utf-8",newline="") as s:
  w=csv.DictWriter(s,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
 (ROOT/"sources/10_manifestes_collecte.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")


def main():
 rows=announced();calendar();overlaps();primary();registry()
 result={"annonces":len(rows),"totaux_controles":6,"ligne_calendrier_illustratif":10,"identites_PLF2027":2,"validation_economies_nationales":False}
 (OUT/"10_controles.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(json.dumps(result,ensure_ascii=False))


if __name__=="__main__":main()
