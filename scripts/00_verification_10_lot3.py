#!/usr/bin/env python3
"""Contre-vérification ciblée de la note10, sans son extracteur auteur.

Lecture directe : HTML politique gzip versionné, HTML éditeur/lecteur et PDF
primaires. Les contrôles d'opérateurs réemploient la source06 : contrôle de
cohérence documentaire, pas seconde observation statistique indépendante.

Écrit uniquement data/risques/verification_10_lot3.csv et la note homonyme.
Les rendus visuels du PDF58-59 ont été inspectés le28/10/2026 hors dépôt.
"""
import csv, gzip, hashlib, json, re, unicodedata
from collections import Counter
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from bs4 import BeautifulSoup
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
PUB=ROOT/'recherche/10_audit_propositions.md'
CSV=ROOT/'data/risques/verification_10_lot3.csv'
NOTE=ROOT/'recherche/00_verification_10_lot3.md'
SITE='https://www.budget2027.fr/'
JAUNE='https://www.budget.gouv.fr/documentation/file-download/34432'
PLF='https://presse.economie.gouv.fr/download?n=1076%20-%20DP%20-%20Budget%202027-pdf&id=184723'
FAYARD='https://www.fayard.fr/livre/le-casse-du-siecle-9782213733135/'
LECTEUR='https://www.liseuse-hachette.fr/ean/9782213732329'
FIELDS=['id','theme','indicateur','annee','valeur_publiee','valeur_source','unite','source_url','source_localisation','statut_controle','note']

def flat(s):
    return re.sub(r'\s+','',unicodedata.normalize('NFKC',str(s))).replace('−','-').casefold()
def dump(v):
    if isinstance(v,Decimal):return format(v,'f')
    if isinstance(v,(list,tuple,dict)):return json.dumps(v,ensure_ascii=False,default=lambda x:format(x,'f') if isinstance(x,Decimal) else str(x))
    return str(v)
def amount_range(text):
    # Un seul champ de montant ; retire la mention d'actifs qui n'a pas de prix.
    text=text.split('+')[0]
    values=[Decimal(x.replace(',','.')) for x in re.findall(r'\d+(?:[.,]\d+)?',text)]
    scale=Decimal('0.001') if 'M€' in text and 'Md€' not in text else Decimal(1)
    if len(values) not in (1,2):raise ValueError('Champ monétaire ambigu : '+text)
    return (values[0]*scale,values[-1]*scale)
def numbers(text):
    raw=re.findall(r'(?<![A-Za-z0-9])[+−-]?\d+(?:[ \u202f\u00a0]\d{3})*(?:[.,]\d+)?',text)
    return [Decimal(re.sub(r'[ \u202f\u00a0]','',x).replace('−','-').replace(',','.')) for x in raw]

def clean(s):
    parts=re.split(r'(https?://[^\s)]+|`[^`]*`|\b(?:scripts|data|recherche|sources)/[^\s`)]+|\bbeautifulsoup4\b|\bV10-\d+\b|\b0\d[a-z]\b)',str(s))
    for i in range(0,len(parts),2):
        parts[i]=re.sub(r'(?<=[A-Za-zÀ-ÿ])(?=\d)|(?<=\d)(?=[A-Za-zÀ-ÿ])',' ',parts[i])
        parts[i]=re.sub(r'\bp\.(?=\d)','p. ',parts[i])
        parts[i]=re.sub(r'(?<=\d)(?=[€%])',' ',parts[i])
        parts[i]=re.sub(r':(?=\d)',': ',parts[i])
        for a,b in {'HTMLavec':'HTML avec','HTMLarchivé':'HTML archivé','ressourcesJavaScript':'ressources JavaScript','bandeauBudget':'bandeau Budget','surURL':'sur URL','ligneLF':'ligne LF','enUTF':'en UTF','jauneopérateurs':'jaune opérateurs','ISBNnumérique':'ISBN numérique','ressourcesJS':'ressources JS','deJavaScript':'de JavaScript','annéepleine':'année pleine','jaunePLF':'jaune PLF','dossierPLF':'dossier PLF','exceptionsPDF':'exceptions PDF','textePDF':'texte PDF','décodageUTF':'décodage UTF','coquilleHTML':'coquille HTML'}.items():parts[i]=parts[i].replace(a,b)
    return ''.join(parts)

def main():
    pub=PUB.read_text(encoding='utf8')
    rows=[]
    def put(id,theme,label,year,published,source,unit,url,loc,ok,note='',status='CONFIRME',anchors=()):
        located=all(flat(a) in flat(pub) for a in anchors)
        state=status if ok and located else ('ECART_SOURCE' if not ok else 'NOTE_MODIFIEE_A_RELOCALISER')
        rows.append(dict(zip(FIELDS,[id,theme,label,year,dump(published),dump(source),unit,url,loc,state,note])))
    def absent(id,theme,label,year,published,unit,url,loc,command):
        rows.append(dict(zip(FIELDS,[id,theme,label,year,dump(published),'NON VERIFIABLE',unit,url,loc,'NON_VERIFIABLE_CACHE_ABSENT','Restaurer : '+command])))
    archive=ROOT/'data/raw/10/budget2027_20261028.html.gz'
    if not archive.exists():raise SystemExit('Instantané politique versionné absent : '+str(archive))
    body=gzip.open(archive,'rb').read()
    html=BeautifulSoup(body.decode('utf8'),'html.parser')
    lis=html.select('li.mesure')
    sranges=[amount_range(x.select_one('.mesure-montant').get_text(' ',strip=True)) for x in lis]
    displayed=[]
    for line in pub.splitlines():
        m=re.match(r'\|\s*(\d{2})\s*\|[^|]+\|\s*([^|]+)\|',line)
        if m:
            # La note exprime les24lignes en Md€ ; la ligne13 vaut0,066Md€.
            lo,hi=amount_range(m.group(2)+' Md€')
            displayed.append((int(m.group(1)),lo,hi))
    expected=[(i+1,*r) for i,r in enumerate(sranges)]
    put('V10-01','Annonces','24 montants, unité et bornes de chaque ligne','millésime non explicité, instantané28/10/2026',displayed,expected,'Md€ annuels annoncés',SITE,'HTML li.mesure1-24 ; conversion66M€ en0,066Md€',displayed==expected and len(lis)==24,'Vérifie les24lignes ; aucune validation des économies, de leur indépendance ou du calendrier.',anchors=('24 annonces','66 M€') if '66 M€' in pub else ('24 annonces','0,066'))
    low=sum((x[0] for x in sranges),Decimal(0));high=sum((x[1] for x in sranges),Decimal(0))
    p_low=Decimal(re.search(r'bornes basses.*?\*\*([\d,]+)\s*Md',pub).group(1).replace(',','.'))
    p_high=Decimal(re.search(r'bornes hautes.*?\*\*([\d,]+)\s*Md',pub).group(1).replace(',','.'))
    put('V10-02','Sommes','Borne basse des24montants','instantané28/10/2026',p_low,low,'Md€/an annoncés',SITE,'Somme des bornes basses lues dans les spans de montant',p_low==low,'Produit de cession non chiffré exclu ; addition ne prouve pas absence de double compte.')
    put('V10-03','Sommes','Borne haute des24montants','instantané28/10/2026',p_high,high,'Md€/an annoncés',SITE,'Somme des bornes hautes lues dans les spans de montant',p_high==high,'Les fourchettes ne sont pas des intervalles de confiance.')
    counter=sum((Decimal(x['data-valeur']) for x in lis),Decimal(0))
    p_counter=Decimal(re.search(r'totalisent\s*\*\*([\d,]+)\s*Md',pub).group(1).replace(',','.'))
    put('V10-04','Sommes','Attributs numériques du compteur','instantané28/10/2026',p_counter,counter,'Md€/an annoncés',SITE,'24 attributs data-valeur, lus sans script auteur',p_counter==counter and counter==(low+high)/2,'Milieux des trois fourchettes ; ne valide pas un budget net de140Md€.')
    badges=[s.strip() for s in html.find_all(string=re.compile(r'Budget\s*2026',re.I))]
    put('V10-05','Millésime','Bandeau Budget2026 sur URL2027','non précisée','Budget2026 sur budget2027.fr',badges,'libellé',SITE,'Bandeau span, distinct du titre HTML140milliards',bool(badges),'Le titre HTML est140milliards ; Budget2026 est le bandeau. Date de publication/exercice non déduits.',anchors=('Budget 2026','budget2027.fr'))
    price=sranges[0][0]*Decimal(10)**9/Decimal(800000)
    put('V10-06','Effectifs','Coût implicite par poste à terme','hypothèse politique non datée',50000,price,'€/poste/an',SITE,'Mesure1 :40Md€ et800000départs non remplacés',price==50000,'Identité exacte ; coût marginal, cotisations, pensions et métier non établis.',status='CALCUL_CONFIRME',anchors=('50 000','800 000'))
    rate=(Decimal(800000)/Decimal(2300000)*100).quantize(Decimal('.01'),rounding=ROUND_HALF_UP)
    put('V10-07','Effectifs','Part de800000dans2,3millions', 'hypothèse politique non datée',Decimal('34.78'),rate,'%',SITE,'Mesure1, quotient des deux nombres',rate==Decimal('34.78'),'Ne prouve ni répartition administrative ni départs définitifs disponibles.',status='CALCUL_CONFIRME',anchors=('34,78','2,3 millions'))
    sequences=re.findall(r'\*\*((?:\d+,){4}\d+) Md€\*\*, cumul (\d+) Md€',pub)
    annual=Decimal(800000)/5
    full=[annual*price*y/Decimal(10)**9 for y in range(1,6)]
    half=[annual*price*(Decimal(y)-Decimal('.5'))/Decimal(10)**9 for y in range(1,6)]
    parsed=[([Decimal(t) for t in seq.split(',')],Decimal(total)) for seq,total in sequences]
    actual=[(full,sum(full)),(half,sum(half))]
    put('V10-08','Calendrier','Séquences et cumuls des deux conventions illustratives','cinq années hypothétiques',parsed,actual,'Md€ annuels puis cumul',SITE,'Contre-calcul indépendant160000postes/an×50000€ ; conventions annéepleine/mi-année',parsed==actual,'Hypothèse illustrative assumée, aucune prévision française ni réalisation ; sous-activité/transition absentes.',status='CALCUL_CONFIRME_HYPOTHESE')

    jaune=ROOT/'data/cache/06/operateurs_plf2027.pdf'
    if jaune.exists():
        pdf=PdfReader(jaune)
        for id,name,page,published in [
            ('V10-09','Anah',246,[Decimal('3651.541'),Decimal('3450.687'),Decimal('25.000')]),
            ('V10-10','Ademe',226,[Decimal('1603.575'),Decimal('1322.880'),Decimal('104.788')]),
            ('V10-11','France Travail',458,[Decimal('6889.234'),Decimal('1972.446'),Decimal('3886.736')])]:
            text=pdf.pages[page-1].extract_text(extraction_mode='layout')
            labels=['Total des charges','Intervention (le cas échéant)','Personnel']
            vals=[]
            for label in labels:
                line=next(x for x in text.splitlines() if x.strip().startswith(label))
                vals.append(numbers(line)[0]/1000)
            put(id,'Opérateurs',name+': charges/intervention/personnel du compte de résultat','BI2026',published,vals,'M€ de charges, BI2026',JAUNE,'PDF p.'+str(page)+' ; en milliers d’euros ; lecture directe',vals==published and '2026' in text,'Même original que06 : cohérence documentaire, pas seconde observation statistique. Les budgets ne sont ni comptes2027 ni coûts de siège.',status='CONFIRME_COHERENCE_06',anchors=(str(published[0]).replace('.',','),))
    else:
        for id,name in [('V10-09','Anah'),('V10-10','Ademe'),('V10-11','France Travail')]:
            absent(id,'Opérateurs',name+' BI2026','2026','voir note10','M€ de charges',JAUNE,'PDF p.246/226/458','python -I scripts/fetch.py "'+JAUNE+'" operateurs_plf2027 --out-dir data/cache/06')

    budget=ROOT/'data/cache/10/dp_budget2027.pdf'
    if budget.exists():
        r=PdfReader(budget)
        p29=r.pages[28].extract_text(extraction_mode='layout')
        p30=r.pages[29].extract_text(extraction_mode='layout')
        p31=r.pages[30].extract_text(extraction_mode='layout')
        table=r.pages[58].extract_text(extraction_mode='layout')
        # Lire la page59une seule fois : les objets PDF58/59 incluent le tableau
        # hors cadre et pypdf peut ainsi restituer deux fois la même table.
        subtotal=next(x for x in table.splitlines() if x.strip().startswith('SOUS TOTAL'))
        cells=numbers(subtotal)
        expected_cells=[Decimal(x) for x in [8025,404,-812,2032750,-1209,397282,6816]]
        if cells!=expected_cells:raise ValueError('Géométrie ou transcription du sous-total à revoir : '+repr(cells))
        effort=bool(re.search(r'54\s*Md€.*?43\s*Md€',p29,re.S))
        put('V10-12','PLF2027','Effort54, mesures43, différence11','PLF2027, projet',[54,43,11],[54,43,54-43],'Md€ de redressement',PLF,'PDF p.29, imprimée10 ; premier paragraphe',effort,'Proposition par rapport à une référence ; montée en charge de mesures2026 ; pas54Md€ de masse salariale évitée.',status='CONFIRME_PROJET',anchors=('54 Md€','43 Md€','11 Md€'))
        put('V10-13','PLF2027','Schémas État/opérateurs et sous-total','PLF2027, projet',[8025,-1209,6816],[cells[0],cells[4],cells[6]],'ETP, flux proposés',PLF,'PDF59, sous-total ; libellés/notes sur PDF58',cells[0]+cells[4]==cells[6],'Sous-ensembles dont administration centrale/numérique déjà inclus ; double page rendue visuellement le28/10/2026.',status='CONFIRME_PROJET',anchors=('+8 025','−1 209','+6 816'))
        total_line=next(x for x in table.splitlines() if x.strip().startswith('TOTAL GENERAL'))
        total=numbers(total_line)[0]
        identity=cells[6]-4742-2150-1000
        excluded=all(flat(a) in flat(p30+p31) for a in ['+4 742','+2 150','1 000 suppressions'])
        put('V10-14','PLF2027','Total retraité avec caisses sociales','PLF2027, projet',-1076,total,'ETP, flux retraité',PLF,'PDF59 TOTAL GENERAL ; exceptionsPDF30-31 ; 6816−4742−2150−1000',total==identity==Decimal(-1076) and excluded,'Retrait de la réforme enseignants et marche LPM ; caisses sociales comprises ; pas comparaison directe à un plafond.',status='CONFIRME_PROJET',anchors=('−1 076','formation initiale'))
        put('V10-15','PLF2027','Administration centrale, tableau et arrondi de texte','PLF2027, projet',-812,cells[2],'ETP, sous-ensemble',PLF,'PDF59 colonne dont Administration centrale ; textePDF30−800',cells[2]==-812 and flat('−800 ETP') in flat(p30),'La note retient812du tableau ; le texte source arrondit à800. Même sous-ensemble, pas un ajout au total.',status='CONFIRME_PROJET',anchors=('−812','administration centrale'))
        put('V10-16','PLF2027','Numérique réinternalisé, tableau et arrondi','PLF2027, projet',404,cells[1],'ETP, sous-ensemble',PLF,'PDF59 colonne dont Emplois numériques réinternalisés ; PDF31 plus400',cells[1]==404 and flat('plus de 400 agents') in flat(p31),'Déjà inclus dans le flux État ; peut remplacer une prestation, pas créer mécaniquement un surcoût égal au salaire.',status='CONFIRME_PROJET',anchors=('+404','numériques'))
        put('V10-17','PLF2027','Plafonds État et opérateurs','PLF2027, projet',[2032750,397282],[cells[3],cells[5]],'ETPT, plafonds proposés',PLF,'PDF59 colonnes plafonds ; note2 PDF58/59',cells[3]==2032750 and cells[5]==397282 and 'ETPT' in table,'Stocks autorisés annuels, distincts des ETP de schéma ; opérateurs identiques au jaune réemployé06.',status='CONFIRME_PROJET',anchors=('2 032 750','397 282','ETPT'))
    else:
        for i in range(12,18):absent(f'V10-{i:02}','PLF2027','Contrôle documentaire budgétaire','2027','voir note10','ETP/ETPT/Md€ selon ligne',PLF,'PDF29-31,58-59','python -I scripts/fetch.py "'+PLF+'" dp_budget2027 --out-dir data/cache/10')

    sha=hashlib.sha256(body).hexdigest()
    copies=[p for p in [ROOT/'data/cache/10/budget2027.html',ROOT/'data/cache/10/budget2027_actualisation.html'] if p.exists()]
    same=all(p.read_bytes()==body for p in copies)
    put('V10-18','Instantané','Taille, empreinte et copies du corps HTML','consultation28/10/2026',[113850,'3fa12a84'],[len(body),sha],'octets et SHA-256',SITE,'Gzip versionné décompressé sans transformation ; copies cache si présentes',len(body)==113850 and sha.startswith('3fa12a84') and same,'Les copies ne sont pas des sources indépendantes. Copies locales comparées :'+str(len(copies))+'.',anchors=('113 850','3fa12a84'))
    book=ROOT/'data/cache/10/fayard_casse.html'
    if book.exists():
        soup=BeautifulSoup(book.read_bytes().decode('utf8'),'html.parser')
        books=[]
        for script in soup.select('script[type="application/ld+json"]'):
            obj=json.loads(script.get_text())
            books.extend(x for x in obj.get('@graph',[]) if x.get('@type')=='Book')
        b=next(x for x in books if 'numberOfPages' in x)
        actual=[b['datePublished'],b['numberOfPages'],b['isbn']]
        expected=['2026-09-02',286,'9782213733135']
        put('V10-19','Livre','Publication, pagination déclarée et ISBN','2026',expected,actual,'date ; pages déclarées ; ISBN',FAYARD,'JSON-LD @graph, Book principal ; décodageUTF-8',actual==expected,'Métadonnées éditeur uniquement. Ne prouve pas lecture du texte ni validation de ses arguments ; ISBNnumérique9782213732329 distinct.',anchors=('2 septembre 2026','286 pages'))
    else:absent('V10-19','Livre','MétadonnéesFayard','2026',['2026-09-02',286],'date/pages/ISBN',FAYARD,'JSON-LD Book','python -I scripts/fetch.py "'+FAYARD+'" fayard_casse --out-dir data/cache/10')
    preview=ROOT/'data/cache/10/hachette_feuilletage.html'
    if preview.exists():
        p=BeautifulSoup(preview.read_bytes(),'html.parser')
        t=p.get_text(' ',strip=True)
        has_js=len(p.select('script[src]'))
        put('V10-20','Livre','Limite du feuilletage archivé','consultation28/10/2026','Coquille de lecteur ; aucun chapitre lu',{'texte_html':t,'scripts_externes':has_js,'octets':preview.stat().st_size},'contenu reçu',LECTEUR,'HTMLarchivé du lecteur, sans exécution deJavaScript',len(t)<100 and has_js>0,'La réponse initiale ne contient pas le livre. Le script ne suit pas les ressourcesJS ; l’absence de lecture du texte intégral reste explicite.',status='LIMITE_CONFIRMEE',anchors=('coquille de lecteur','aucun extrait textuel'))
    else:absent('V10-20','Livre','Limite du lecteur','2026','Texte non lu','contenu',LECTEUR,'Archive du lecteur','python -I scripts/fetch.py "'+LECTEUR+'" hachette_feuilletage --out-dir data/cache/10')

    assert len(rows)==20 and len({r['id'] for r in rows})==20
    rows=[{k:(v if k=='source_url' else clean(v)) for k,v in r.items()} for r in rows]
    CSV.parent.mkdir(parents=True,exist_ok=True)
    with CSV.open('w',encoding='utf8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(rows)
    counts=Counter(x['statut_controle'] for x in rows)
    bad=[x for x in rows if x['statut_controle'].startswith(('ECART','NOTE_MODIFIEE'))]
    missing=[x for x in rows if x['statut_controle']=='NON_VERIFIABLE_CACHE_ABSENT']
    lines=['# Contre-vérification indépendante du chantier10 — lot3','','Contrôle arrêté au **28 octobre 2026**, sur la note finale présente dans le dépôt. Le code auteur du volet10 n’a été ni lu, ni importé, ni exécuté. Les24montants sont reparsés dans l’HTML primaire gzip ; les PDF et le JSON-LD éditeur sont relus directement.','','**Résultat : '+str(len(rows))+' points contrôlés, '+str(len(bad))+' écart de chiffre ou de localisation détecté.** Les statuts et réserves de chaque ligne figurent dans `data/risques/verification_10_lot3.csv`.','','## Résultats décisifs','']
    for x in rows:lines.append('- **'+x['id']+' — '+x['statut_controle']+'** : '+x['indicateur']+'. Source : '+x['source_localisation']+'.')
    lines.extend(['','Les bornes de138,366/145,366Md€ et les attributs141,866Md€ sont des additions exactes d’annonces. Le quotient50000€/poste/an et les cumuls illustratifs100/120Md€ sont confirmés comme calculs conditionnels, sans validation du vivier, du coût marginal ni de l’additionnalité.','','Les budgets Anah/Ademe/France Travail sont les **BI2026** du jaunePLF2027, en milliers d’euros au tableau source. Les trois lignes sont un **contrôle de cohérence avec le même original réemployé dans06**, pas trois nouvelles observations statistiques indépendantes. Personnel de mission, interventions et frais de siège ne sont pas assimilés.','','Le tableau d’emplois est une double page : PDF58 porte les libellés, PDF59 les colonnes numériques. Les objets PDF restituent des éléments hors cadre sur les deux pages ; un rendu visuel avec Poppler a été inspecté séparément pour éviter un double compte. Le script retient une seule ligne de sous-total, puis vérifie6816−4742−2150−1000=−1076. Les sous-ensembles−812/+404 et plafonds2032750/397282ETPT restent distincts du flux net.','','La fiche Fayard confirme les métadonnées du livre, non son contenu. Le lecteur archivé ne reçoit qu’une coquilleHTML avec ressourcesJavaScript externes ; aucun texte intégral n’est considéré comme lu. Aucun montant de cession non publié n’est ajouté aux économies annuelles.','','## Réserves conservées','','- Date/exercice de la page politique non explicités ; bandeauBudget2026 surURL2027.','- Annonces, objectifs, effets en régime permanent et exécution budgétaire restent distincts.','- Départs définitifs par métier, coût d’entrée, pensions, transition et doubles comptes ne sont pas validés par cette contre-lecture.','- Le budget d’un organisme et la masse salariale de ses agents de mission ne donnent pas ses frais administratifs supprimables.','- Aucune correction de la note10 n’est appliquée directement ; tout écart éventuel doit être traité par son auteur.','','## Reproduction','','```powershell','python -I scripts/00_verification_10_lot3.py','```','','Dépendances déjà disponibles : beautifulsoup4 et pypdf. Seuls les deux livrables de contrôle sont réécrits ; les bruts primaires restent inchangés. Un cache absent produit un statut explicite avec la commande exacte utilisant le collecteur commun `scripts/fetch.py`. La note est écrite enUTF-8, fins de ligneLF.','','Sources : [page politique]('+SITE+'), [jauneopérateurs]('+JAUNE+'), [dossierPLF2027]('+PLF+'), [éditeur]('+FAYARD+'), [lecteur]('+LECTEUR+').',''])
    availability='**Archives nécessaires toutes présentes.**' if not missing else '**Archives manquantes : '+str(len(missing))+' ; lignes non vérifiables, sans confirmation.**'
    lines[6:6]=[availability,'']
    NOTE.write_text('\n'.join(clean(x) for x in lines),encoding='utf-8',newline='\n')
    print(json.dumps({'controles':len(rows),'statuts':dict(counts),'ecarts':len(bad),'non_verifiables':len(missing)},ensure_ascii=False))
    if bad:raise SystemExit('Écarts à signaler : '+', '.join(x['id'] for x in bad))
if __name__=='__main__':main()
