#!/usr/bin/env python3
"""Reproduit le dossier05, ses transcriptions signalees et calculs explicites.

1. python scripts/05_collecte_sources.py  # restaure les archives manquantes
2. python scripts/05_construire_dossier.py

Aucun chiffre de France n'est calibre automatiquement. Pas d'eval de code
provenant des sources. Les transcriptions sont identifiees dans les CSV.
"""
from __future__ import annotations

import csv
import gzip
import hashlib
import json
import re
import sys
from decimal import Decimal
from html.parser import HTMLParser
from io import BytesIO, StringIO
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCAL_DEPS = ROOT / '.cache/python_deps'
if LOCAL_DEPS.is_dir():
    sys.path.append(str(LOCAL_DEPS))
from pypdf import PdfReader

OUT = ROOT / 'data/reformes'
CAT = {r['id']: r for r in json.loads((ROOT / 'sources/05_catalogue_sources.json').read_text(encoding='utf-8'))}
MAN = {p.stem.removesuffix('.meta'): json.loads(p.read_text(encoding='utf-8')) for p in (ROOT / 'data/raw/05').glob('*.meta.json')}
TEXTS: dict[str, str] = {}
PDFS: dict[str, PdfReader] = {}


def write_csv(name: str, rows: list[dict], columns: list[str] | None = None) -> None:
    assert rows, name
    with (OUT / name).open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=columns or list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def flat(value: str) -> str:
    return ''.join(value.split()).replace(',', '').replace('\u200b', '').casefold()


class TextHTML(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.hidden = 0

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'noscript'):
            self.hidden += 1
        if not self.hidden and tag in ('div', 'p', 'li', 'tr', 'br', 'h1', 'h2', 'h3'):
            self.parts.append('\n')

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'noscript') and self.hidden:
            self.hidden -= 1

    def handle_data(self, data):
        if not self.hidden:
            self.parts.append(data)


def source_text(sid: str, page: int | None = None) -> tuple[str, str, str]:
    """Texte relu du corps primaire, ou preuve OPEN expresse si HTTP bloque."""
    m, c = MAN[sid], CAT[sid]
    if m['acces'] == 'integral':
        path = ROOT / m['local_path']
        stored = path.read_bytes()
        assert hashlib.sha256(stored).hexdigest() == m['sha256_stored'], (sid, 'archive modifiée')
        body = gzip.decompress(stored) if path.suffix == '.gz' else stored
        assert hashlib.sha256(body).hexdigest() == m['sha256_body'], (sid, 'corps modifié')
        if body.startswith(b'%PDF-'):
            if sid not in PDFS:
                PDFS[sid] = PdfReader(BytesIO(body))
            reader = PDFS[sid]
            text = reader.pages[page-1].extract_text() if page is not None else '\n'.join(p.extract_text() or '' for p in reader.pages)
        else:
            if sid not in TEXTS:
                text = body.decode('utf-8-sig', errors='replace')
                if '.html' in path.name:
                    parser = TextHTML(); parser.feed(text); text = ''.join(parser.parts)
                TEXTS[sid] = text
            text = TEXTS[sid]
        return text or '', m['sha256_body'], m['local_path']
    assert c.get('preuve_web_local'), (sid, 'ni corps lisible ni OPEN primaire archivé')
    path = ROOT / c['preuve_web_local']
    text = path.read_text(encoding='utf-8')
    if sid == 'PT_IMF':
        text += (ROOT / 'sources/05_ouverture_fmi_rebond.json').read_text(encoding='utf-8')
    return text, hashlib.sha256(path.read_bytes()).hexdigest(), c['preuve_web_local']


def number(row: dict) -> Decimal:
    return Decimal(row['valeur'])


def fmt(value: Decimal | str | int, places: int = 2) -> str:
    d = Decimal(value)
    text = f'{d:,.{places}f}'.replace(',', ' ').replace('.', ',')
    if places and text.endswith(',' + '0' * places):
        text = text[:-(places+1)]
    return text


def cite(sid: str, loc: str = '') -> str:
    c = CAT[sid]
    return f"[{c['institution']}, {c['date_publication'] or 'date non précisée'}]({c['url']})" + (f', {loc}' if loc else '')


def typography(text: str) -> str:
    """Espacement de la prose de l'equipe ; URL et code restent intacts."""
    replacements = {
        'FranceStratégie':'France Stratégie','ProgramReview':'Program Review','DigitalPost':'Digital Post',
        'PublicService':'Public Service','corePublicService':'core Public Service','Civil ServiceUK':'Civil Service UK',
        'SCMetKONEPS':'SCM et KONEPS','SCMComptent':'SCM comptent','OZGcompte':'OZG compte',
        'fonctionpaie':'fonction paie','demandes supplémentaires':'demandes supplémentaires',
        'depaie':'de paie','salariéancien':'salarié ancien','démarragedéfavorable':'démarrage défavorable',
        'aprèsdeuxans':'après deux ans','gainde':'gain de ','gainnet':'gain net','montantscontrats':'montants contrats',
        'objetdistinct':'objet distinct','dansle':'dans le ','autableau':'au tableau','surparcSIréférence':'sur parc SI de référence',
        'dépenses externesPublicService':'dépenses externes Public Service','salairebrut':'salaire brut',
        'l\'évaluationOCDE':'l\'évaluation OCDE','leFMI':'le FMI','laNorvège':'la Norvège','leCBO':'le CBO',
        'etleCBO':'et le CBO','pourFMI':'pour FMI','pourles':'pour les ','lesouvertures':'les ouvertures',
        'etdeuxpagescanadiennes':'et deux pages canadiennes','laplage':'la plage','lespages':'les pages',
        'HTMLrenvoyées':'HTML renvoyées','corpsPDFlocaux':'corps PDF locaux','serviceconnecté':'service connecté',
        'Commissionirlandaise':'Commission irlandaise','rapportprimaire':'rapport primaire','rapportméthodologiqueintégral':'rapport méthodologique intégral',
        'économienette':'économie nette','potentielfrançais':'potentiel français','chiffragefrançais':'chiffrage français',
        'parfonction':'par fonction','emplois/euros':'emplois/euros','enmilliards':'en milliards','enemplois':'en emplois',
        'demissions':'de missions','lesdatesd\'observation':'les dates d\'observation','leCSV':'le CSV',
        'etstatutdans':'et statut dans','typesde':'types de ','ne remplace':'ne remplace',
        'étatdepreuve':'état de preuve','surfaits':'sur faits','pointsd\'emploi':'points d\'emploi',
        'àsensunique':'à sens unique','parattrition':'par attrition','modalitéd\'exécution':'modalité d\'exécution',
        'identificationdes':'identification des','accèsassisté':'accès assisté','baisse salariale':'baisse salariale',
        'salaireannualiséNAO':'salaire annualisé NAO','dépenseSIjaponaise':'dépense SI japonaise',
        'l\'étude danoiseDiDest':'l\'étude danoise DiD est','nonconstants':'non constants','catégoriesdepaiePhénix':'catégories de paie Phénix',
        'àeuxseuls':'à eux seuls','nonétablie':'non établie','uneestimation':'une estimation',
        'décaissementnominal':'décaissement nominal','coopérationinterne':'coopération interne',
        'lesPDFdans':'les PDF dans','ignoréparGit':'ignoré par Git','lesHTML/CSV':'les HTML/CSV','sansperte':'sans perte',
        'permettentde':'permettent de ','Pourretélécharger':'Pour retélécharger','nouvelétat':'nouvel état',
        'lesSHAet':'les SHA et','misàjour':'mis à jour','PDF/HTMLtéléchargés':'PDF/HTML téléchargés',
        'àlaracine':'à la racine','àchaque':'à chaque','àrevoir':'à revoir','repèresne':'repères ne',
        'etproduit':'et produit','ilrelit':'il relit','preuveOPENarchivée':'preuve OPEN archivée',
        'enETP':'en ETP','enFrance':'en France','duPIB':'du PIB','enemplois':'en emplois',
        'datepar':'date par','lesautrespays':'les autres pays','Lesautrespays':'Les autres pays',
        'périmètregénéral':'périmètre général','explicitementnommés':'explicitement nommés',
        'niveauxdepreuve':'niveaux de preuve','lienexterne':'lien externe','objectifd\'échelle':'objectif d\'échelle',
        'unserviceopérationnel':'un service opérationnel','sontmarqués':'sont marqués','Lescoûts/ETPmanquants':'Les coûts/ETP manquants',
        'restentvides':'restent vides','statutd\'accès':'statut d\'accès','restepartiel':'reste partiel',
        'fichieroriginal':'fichier original','hébergéepar':'hébergée par ','l\'articleAJPSdanois':'l\'article AJPS danois',
        'SourceOCDE':'Source OCDE','d\'après':'d\'après','selonNKR':'selon NKR','état2026':'état 2026',
        'budgetCanada':'budget Canada','monétairesource':'monétaire source','cinqans':'cinq ans',
        'surcoûtbrut':'surcoût brut','de1100':'de 1100','de267':'de 267','netAPU':'net APU',
        'lespagesVITAL':'les pages VITAL','pagesVITAL':'pages VITAL','toutleterritoire':'tout le territoire',
        'Pays-BasSCM':'Pays-Bas SCM','étudeDiD':'étude DiD','tableauindicateurs':'tableau des indicateurs',
        'exécutionFinances':'exécution Finances','totalprévu':'total prévu','sérieONS':'série ONS',
        'Program ReviewCanada':'Program Review Canada','CADde':'CAD de','Mde':'M de','Mdde':'Md de',
        'Mddu':'Md du','futurDayforce':'futur Dayforce','àplusde':'à plus de','plusde':'plus de',
        'corePublic Service':'core Public Service','externesPublic Service':'externes Public Service',
        'tableauxemploi/prestataires':'tableaux emploi et prestataires','AgeofReform':'Age of Reform',
        'aprèsrestaurations':'après restaurations','règleuneentrée/cinqretraites':'règle d’une entrée pour cinq retraites',
        'pluslarge':'plus large','quotaÉtat':'quota État','Facoltàassunzionali':'Facoltà assunzionali',
        'bouquetsOZG':'bouquets OZG','sectionévaluationNAV':'section évaluation NAV',
        'tableauKONEPS':'tableau KONEPS','MdUSDdont':'Md USD dont','MdUSDaffichés':'Md USD affichés',
        'nominalFY':'nominal FY','aprèsretraitement':'après retraitement','OPMseule':'OPM seule',
        'créditsFY':'crédits FY','parzéro':'par zéro','estimationde':'estimation de','ceuxdu':'ceux du',
        'près de−':'près de −','cible−':'cible −','audelà':'au-delà','desautres':'des autres',
        'transfertde':'transfert de','revenuspour':'revenus pour','montantnet':'montant net',
    }
    protected = re.split(r'(```[\s\S]*?```|`[^`]*`|\]\([^)]*\))', text)
    for i in range(0, len(protected), 2):
        s=protected[i]
        for old,new in replacements.items(): s=s.replace(old,new)
        s=re.sub(r'(?<=[A-Za-zÀ-ÿ%€£])(?=\d)|(?<=\d)(?=[A-Za-zÀ-ÿ])',' ',s)
        s=re.sub(r'(?<=[€£%])(?=[A-Za-zÀ-ÿ])',' ',s)
        s=re.sub(r'(?<![\w.])\d{5,}(?![\w.])',lambda m:f'{int(m.group()):,}'.replace(',',' '),s)
        s=s.replace('C 9 KQ','C9KQ')
        s=re.sub(r'\bT ([1-4])\b',r'T\1',s)
        protected[i]=s
    return ''.join(protected)


def registry() -> None:
    columns = ['id','titre','institution','date_publication','url','date_consultation','acces','sha256_16','notes']
    rows = []
    for sid in sorted(MAN):
        m, c = MAN[sid], CAT[sid]
        row = {key: m.get(key, '') for key in columns}
        row['sha256_16'] = m.get('sha256_body', '')[:16]
        row['notes'] = f"Cas {c['cas']} ; HTTP {m.get('http_status','échec')} ; {m.get('local_path','')} ; SHA256corps={m.get('sha256_body','')} ; SHA256stockage={m.get('sha256_stored','')} ; {m.get('error','')}"
        if m['acces'] != 'integral' and c.get('preuve_web_local'):
            proof = ROOT / c['preuve_web_local']
            row['acces'] = c.get('acces_web', 'partiel')
            row['sha256_16'] = hashlib.sha256(proof.read_bytes()).hexdigest()[:16]
            row['notes'] += f" ; {c.get('note_web','')} ; SHA16 de la preuve OPEN={c['preuve_web_local']}"
        rows.append(row)
    with (ROOT / 'sources/registre_05.csv').open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, lineterminator='\n'); writer.writeheader(); writer.writerows(rows)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    indicators = json.loads((ROOT / 'sources/05_transcriptions.json').read_text(encoding='utf-8'))['indicateurs']
    cases = json.loads((ROOT / 'sources/05_dossier_cas.json').read_text(encoding='utf-8'))['cas']
    checks = []
    for row in indicators:
        sid = row['source_id']
        page_match = re.search(r'PDF\s*(\d+)', row['source_localisation'])
        page = int(page_match.group(1)) if page_match else None
        text, digest, path = source_text(sid, page)
        row.setdefault('figure_sha256','')
        present = flat(row['repere_source']) in flat(text)
        status='CONFORME' if present else 'A_REVOIR'
        control='repere_transcription_sur_page_source'
        if row['mode_extraction']=='TRANSCRIPTION_MANUELLE_FIGURE_IMAGE':
            # Les deux nombres OPM sont dans une image, absents de la couche
            # texte. La figure a ete inspectee visuellement, sans OCR invente.
            matches=[img for img in PDFS[sid].pages[page-1].images if hashlib.sha256(img.data).hexdigest()==row['figure_sha256']]
            assert len(matches)==1,(sid,'figure differente ou manquante')
            destination=ROOT/'data/cache/05/US_OPM_figure_2.png'
            if not destination.exists(): destination.write_bytes(matches[0].data)
            assert hashlib.sha256(destination.read_bytes()).hexdigest()==row['figure_sha256']
            present=True;status='CONFORME_TRANSCRIPTION_IMAGE_MANUELLE';control='empreinte_figure_source_identique_valeur_lue_visuellement'
        checks.append(dict(id=row['id'],controle=control,resultat=str(present),statut=status,note=row['repere_source'],annee=row['annee'],source_url=CAT[sid]['url'],source_localisation=row['source_localisation']))
        row.update(source_url=CAT[sid]['url'],date_consultation='2026-10-28',preuve_locale=path,preuve_sha256=digest)

    # Serie ONS lue directement dans le corps CSV, sans transcription manuelle.
    csv_text, digest, path = source_text('UK_ONS')
    series = {r[0]: r[1] for r in csv.reader(StringIO(csv_text)) if len(r) >= 2}
    for period in ['2010 Q2','2016 Q2','2026 Q2']:
        indicators.append(dict(id='UK_ONS_'+period.replace(' ',''),cas_id='UK_CIVIL',pays='GBR',indicateur='Civil Service UK FTE série C9KQ',annee=period,valeur=series[period],unite='milliers_ETP',source_id='UK_ONS',source_localisation=f'CSV C9KQ, ligne période {period}, publication15/09/2026',nature_mesure='effectif_vintage_2026',statut='FAIT',comparateur='=',mode_extraction='CSV_AUTOMATIQUE',repere_source=period,note='Série actuelle révisée, arrondie au millier ; ne pas raccorder sans correction aux niveaux du rapport NAO2015.',figure_sha256='',source_url=CAT['UK_ONS']['url'],date_consultation='2026-10-28',preuve_locale=path,preuve_sha256=digest))
    by_id = {r['id']: r for r in indicators}
    assert len(by_id) == len(indicators)
    assert {r['statut'] for r in indicators} <= {'FAIT','EXTRAIT','ESTIMATION','HYPOTHÈSE','NON TROUVÉ'}

    calculations = []
    def calc(cid: str, cas: str, a: str, b: str, op: str, unit: str, note: str = '', budget_2015_vs_potentiel_annuel: bool = False) -> Decimal:
        av, bv = number(by_id[a]), number(by_id[b])
        if by_id[a]['unite'] != by_id[b]['unite']:
            assert budget_2015_vs_potentiel_annuel and cas=='DK_POST' and op=='part_pct', (a,b,'unités incompatibles')
        assert op in ['difference','variation_pct','part_pct']
        val = av-bv if op == 'difference' else (av/bv-1)*100 if op == 'variation_pct' else av/bv*100
        formula = f'{a} - {b}' if op=='difference' else f'100 * ({a} / {b} - 1)' if op=='variation_pct' else f'100 * {a} / {b}'
        calculations.append(dict(id=cid,cas_id=cas,indicateur=cid,annee=f"{by_id[b]['annee']} / {by_id[a]['annee']}",valeur=format(val,'.12f').rstrip('0').rstrip('.'),unite=unit,formule=formula,entrees=f'{a};{b}',statut='ESTIMATION',note=note,source_url=by_id[a]['source_url'],source_localisation=by_id[a]['source_localisation']+' ; '+by_id[b]['source_localisation']))
        return val
    calc('DK_STRUCT_DIFF','DK_COMMUNES','DK_COM_AP','DK_COM_AV','difference','communes','Structures, pas emplois.')
    calc('DK_STRUCT_PCT','DK_COMMUNES','DK_COM_AP','DK_COM_AV','variation_pct','pct_communes','Structures, pas emplois.')
    calc('DK_POST_PART','DK_POST','DK_POST_CREDIT','DK_POST_CIBLE','part_pct','pct_potentiel_central','Crédits du seul budget annuel2015 comparés au potentiel central annuel, comme dans audit ; pas taux du milliard sectoriel.',budget_2015_vs_potentiel_annuel=True)
    for cid, a, b in [('UK_1016','UK_ONS_2016Q2','UK_ONS_2010Q2'),('UK_1626','UK_ONS_2026Q2','UK_ONS_2016Q2'),('UK_1026','UK_ONS_2026Q2','UK_ONS_2010Q2')]:
        calc(cid+'_DIFF','UK_CIVIL',a,b,'difference','milliers_ETP')
        calc(cid+'_PCT','UK_CIVIL',a,b,'variation_pct','pct_ETP','Champ ONS et vintage2026 constant ; non causal.')
    for cid,cas,a,b in [('IE_0814','IE_MORATOIRE','IE_WTE14','IE_WTE08'),('IE_1417','IE_MORATOIRE','IE_WTE17','IE_WTE14'),('IE_0817','IE_MORATOIRE','IE_WTE17','IE_WTE08'),('NZ_2325','NZ_RECENT','NZ_FTE_LOW','NZ_FTE_PEAK'),('NZ_2526','NZ_RECENT','NZ_FTE_LAST','NZ_FTE_LOW'),('PT_1014','PT_TROIKA','PT_EMP14','PT_EMP10'),('US_OPM','US_DOGE','US_OPM_AFTER','US_OPM_BEFORE')]:
        calc(cid+'_DIFF',cas,a,b,'difference',by_id[a]['unite'])
        calc(cid+'_PCT',cas,a,b,'variation_pct','pct_effectif','Valeurs sources arrondies pourPortugal ; OPMseule pourUSA ; changements de périmètre résiduels possibles.')
    calc('NZ_EXT_PCT','NZ_RECENT','NZ_EXT_26','NZ_EXT_25','variation_pct','pct_depenses_externes','OPEX+CAPEX, PublicService ; pas causalité démontrée.')
    calc('KR_PART_PRIVEE','KR_KONEPS','KR_PRIVATE','KR_TOTAL','part_pct','pct_couts_transaction','Part de coûts de transaction estimés, pas épargne fiscale.')
    calc('KR_ECART_RESUME','KR_KONEPS','KR_HEAD','KR_TOTAL','difference','millions_USD_par_an','Discordance publiée non réconciliée ; les deux valeurs sont gardées.')
    calc('JP_NOMINAL_DIFF','JP_IT','JP_NOMINAL','JP_BASE','difference','millions_JPY','Variation nominale sur parc de référence ; hors nouveau portefeuille.')
    calc('JP_NOMINAL_PCT','JP_IT','JP_NOMINAL','JP_BASE','variation_pct','pct_depenses_reference')
    calc('JP_RET_PCT','JP_IT','JP_ADJUSTED','JP_BASE','variation_pct','pct_depenses_reference','Retraitements exogènes source, pas décaissement nominal.')
    derived = {r['id']: Decimal(r['valeur']) for r in calculations}

    for cid,value,expected,status,note in [
        ('KR_SOMME',number(by_id['KR_PUBLIC'])+number(by_id['KR_PRIVATE']),number(by_id['KR_TOTAL']),'CONFORME','Public+privé=total du tableau2.6 ; ne prouve pas résultat net.'),
        ('JP_ARRONDI',abs(derived['JP_RET_PCT']).quantize(Decimal('1')),number(by_id['JP_REPORTED']),'CONFORME','13,537% arrondis à14%.'),
        ('JP_RESIDU_ARRONDI',number(by_id['JP_NOMINAL'])-number(by_id['JP_ADJUSTED'])-number(by_id['JP_EXOG']),Decimal('1'),'ECART_PUBLIE_CONSERVE','Résidu1MJPY, source précise valeurs arrondies ; aucune correction artificielle.'),
        ('CA_CUMUL_ARRONDI',number(by_id['CA_REV_F1'])+number(by_id['CA_REV_F2'])+number(by_id['CA_REV_F3'])-number(by_id['CA_REV_OBJ']),Decimal('100'),'ECART_PUBLIE_CONSERVE','Budgets affichés3,9+5,9+7,2=17,0Md vs total16,9Md ;100MCAD d’écart entre nombres arrondis, non redistribués.'),
        ('US_SOMME_METHODES',number(by_id['US_METHOD_OK'])+number(by_id['US_METHOD_OTHER'])+number(by_id['US_METHOD_UNKNOWN']),number(by_id['US_CONTRACTS']),'CONFORME','16,8+37,0+7,2=61,0Md USD ; non certification des économies.'),
    ]:
        checks.append(dict(id=cid,controle='arithmetique_source',resultat=str(value),statut=status if value==expected else 'ERREUR',note=note,annee='voir sources',source_url='',source_localisation='IDs dans05_indicateurs.csv'))
    assert len(cases) == 22 and len({c['pays'] for c in cases}) == 17
    for c in cases:
        for key in ['economie_nette_valeur','potentiel_france_etp','potentiel_france_eur']:
            assert c[key] == '', (c['cas_id'],key,'Ne pas remplacer le manque par zéro')
        a,b = c['effectifs_avant_id'],c['effectifs_apres_id']
        c.update(effectifs_avant=by_id[a]['valeur'] if a else '',effectifs_apres=by_id[b]['valeur'] if b else '',date_avant=by_id[a]['annee'] if a else '',date_apres=by_id[b]['annee'] if b else '',
                 economie_brute_valeur='',economie_brute_unite='',economie_brute_type='',statut_economie_nette='NON TROUVÉ',
                 annee=c['periode'],statut='FAIT / ESTIMATION / NON TROUVÉ selon cellule et état de preuve',source_url=' ; '.join(CAT[s]['url'] for s in c['sources_ids'].split(';')),
                 source_localisation='Voir observations et localisations dans05_indicateurs.csv ; étatdepreuve/limites dansnote05')
        if c['cas_id']=='DK_POST':
            c.update(economie_brute_valeur='48',economie_brute_unite='millions_DKK_2015',economie_brute_type='Crédits centraux réduits, mesure partielle ; pas bénéfice économique net complet')
        if c['cas_id']=='UK_CIVIL':
            c.update(economie_brute_valeur='2490',economie_brute_unite='millions_GBP_reels_par_an_2014',economie_brute_type='Baisse salariale annualisée champ corrigé2010-14 ; pas coût complet de réforme')
        if c['cas_id']=='JP_IT':
            c.update(economie_brute_valeur=str(-derived['JP_NOMINAL_DIFF']),economie_brute_unite='millions_JPY_2024',economie_brute_type='Baisse nominale dépense parc de référenceFY2020 ; pas tout portefeuille ni coût net de transition')
    checks.append(dict(id='COUVERTURE',controle='22cas_17pays_manquants_non_zero',resultat='22 cas ; 17 pays ; 22 économies nettes vides',statut='CONFORME',note='La preuve disponible n’identifie pas de coefficient directement importable en emplois français.',annee='2026',source_url='',source_localisation='05_cas.csv'))
    write_csv('05_indicateurs.csv',indicators)
    write_csv('05_calculs.csv',calculations)
    write_csv('05_cas.csv',cases)
    write_csv('05_controles.csv',checks)
    dictionary = [
        ('statut','FAIT=lu dans source ; EXTRAIT=étude sous-jacente non lue ; ESTIMATION=calcul source/équipe explicitement identifié ; HYPOTHÈSE=paramètre supposé.'),
        ('comparateur','= valeur affichée ; ≈ nombre approximatif ; > borne inférieure publiée, jamais égalité précise.'),
        ('mode_extraction','TRANSCRIPTION_MANUELLE signalée dans fichier source05_transcriptions.json ; CSV_AUTOMATIQUE pour ONS.'),
        ('preuve_sha256','SHA256 du corpsHTTP primaire archivé ; si HTTP direct bloqué et OPEN primaire réussi, SHA256 du fichier preuve connecté explicitement nommé.'),
        ('annee','Date/période de l’observation ; ne pas confondre avec date de publication ou de consultation.'),
        ('nature_mesure','Sépare objectif, prévision, dépense exécutée, crédit réduit, temps valorisé, transfert, effectif et effet causal estimé.'),
        ('unite','Monnaies nationales et prix source conservés ; pas de somme transfrontalière ni conversion en euros contemporains non justifiée.'),
        ('economie_brute_valeur','Seulement trois mesures financières partielles observées, avec objet différent précisé dans economie_brute_type ; non additionnables.'),
        ('economie_nette_valeur','Vide=non identifiée sur un périmètre complet coûts de transition/récurrence/transfert/qualité ; jamais zéro.'),
        ('effectifs_avant_apres','Deux points fournis quand disponibles ; dates/unités/champ explicites. NZhistorique et paiePhénix ont des catégories différentes : pas de taux calculé.'),
        ('potentiel_france','Les expériences n’identifient pas seules un nombre d’ETP ou une somme réalisable enFrance. Colonnes vides, pas de chiffrage importé.'),
        ('pages_lignes','PDF=pagephysique àpartirde1 ; pageimprimée ajoutée seulement si vérifiée. HTML=section ; preuveOPEN=passage/pageexacte, pas snippet de recherche.'),
    ]
    write_csv('05_dictionnaire.csv',[dict(variable=k,definition=v,annee='2026',statut='CONVENTION_EQUIPE',source_url='',source_localisation='Protocole00 et scripts05') for k,v in dictionary])
    registry()
    build_note(indicators,by_id,cases,calculations,derived,checks)
    errors=[r for r in checks if r['statut'] in ['A_REVOIR','ERREUR']]
    print(f"05 : {len(indicators)} observations, {len(calculations)} calculs, {len(cases)} cas, {len(checks)} contrôles, {len(errors)} à revoir.")
    for row in errors:
        print(row['id'],row['source_localisation'],row['note'])
    if errors:
        raise SystemExit(1)


def build_note(indicators,by_id,cases,calculations,d,checks):
    # Synthèse bornée : valeurs source et calculs, sans paramètre d’économie française.
    points = [
        f"**[FAIT]** France Stratégie compare **88,5 emplois APU/1 000 habitants en 2015**, et demande de regarder aussi l'emploi financé indirectement et les consommations intermédiaires. Ce repère historique n'est pas un diagnostic actuel. {cite('FS2017_PDF','PDF9 / p7 ; pp5-6 et13-15')}.",
        f"**[FAIT / ESTIMATION]** Danemark : **271→98 communes en 2007**, soit **{fmt(d['DK_STRUCT_PCT'])}%** de structures. Cela ne représente pas autant de postes en moins. {cite('DK_STAT','nomenclature2007')}.",
        f"**[ESTIMATION]** Fusions danoises : économie relative administrative **0,1%en2007 puis10,4%en2011** dans l'étudeDiD ; les effets apparaissent après2–3ans. L'investissement et l'amortissement sont exclus. {cite('DK_DID','PDF13 / p801')}.",
        f"**[FAIT]** Une synthèse danoise2016 ne trouve pas d'économie sur les dépenses municipales totales : gains administratifs réaffectés. Réduire un support et réduire le budget total sont deux résultats différents. {cite('DK_FUSIONS','résumé et article')}.",
        f"**[FAIT / ESTIMATION]** Digital Post : **48M DKK** de crédits centraux réduits2015, face à244Mde potentiel, soit **{fmt(d['DK_POST_PART'])}%**. Le milliard annuel sectoriel annoncé n'est pas confirmé. {cite('DK_POST','PDF3 / p2')}.",
        f"**[ESTIMATION / HYPOTHÈSE]** X-Road : **1100années de temps** estimées pour2019 reposent notamment sur15minutes par requête humaine ; elles ne constituent pas1100emplois publics supprimés. {cite('EE_RIA','PDF15')}.",
        f"**[FAIT / ESTIMATION]** Pays-BasSCM : cible **−25%**, résultat normé affiché **près de−20%au01/03/2007**, base2002. Il s'agit de charges d'information des entreprises. {cite('NL_SCM','article7, tableauindicateurs')}.",
        f"**[FAIT]** Allocations néerlandaises : **5,748Md€exécutés2020-24** sur11,479Md€estimés, dont1,260Md€d'exécutionFinances déjà dépensés. Le totalprévu n'est pas une dépense annuelle observée. {cite('NL_TOESLAGEN_PDF','PDF22, tableau8')}.",
        f"**[FAIT]** Fin2024, **1276demandes supplémentaires achevées sur8370déposées** ; le coût d'une erreur doit inclure la réparation et les délais de recours. {cite('NL_TOESLAGEN','rubrique réparation')}.",
        f"**[FAIT / ESTIMATION]** Civil ServiceUK, sérieONS révisée : **481000ETP2010T2→384000en2016T2**, soit **{fmt(d['UK_1016_PCT'])}%**, puis523000en2026T2, **+{fmt(d['UK_1626_PCT'])}%depuis2016**. {cite('UK_ONS','CSV C9KQ')}.",
        f"**[FAIT]** NAO : **2,49Md£de baisse salariale annualisée réelle2010-2014**, corrigée du périmètre ; ce n'est pas un bilan net complet des réformes. Son millésime d'effectifs reste séparé de l'ONS actuel. {cite('UK_NAO','PDF6-8 / pp4-6')}.",
        f"**[FAIT]** Program ReviewCanada : environ **45000personnes en moins en cinqans**, dont8000transférées hors périmètre, et1Md CADde restructuration. Le **16,9Md CAD** du Budget1995 est un cumul prévisionnel triennal. {cite('CA_REVIEW','Workforce')}; {cite('CA_BUDGET95','PDF9')}.",
        f"**[FAIT]** Phénix : **1200postes de conseillers retirés/550postes créés au centre**, catégories différentes ; cible70M CAD/an. Pas de réduction harmonisée démontrée de toute la fonctionpaie. {cite('CA_MODERN26_PDF','PDF6 / p1')}; {cite('CA_PHOENIX_PARL','PDF9')}.",
        f"**[FAIT]** Phénix : **937,5M CADde dépenses2024-25**, fonctionnement et surcoûts mêlés, hors successeur/dommages. Audit2026 : **plus de233000transactions** et133000personnes concernées fin09/2025 ; futurDayforce estimé àplusde4,2Md CAD. {cite('CA_PHOENIX25','tableau')}; {cite('CA_MODERN26_PDF','PDF3-4')}.",
        f"**[FAIT]** Nouvelle-Zélande historique : **88507personnes1986/36374corePublicService1993** ne prouvent pas une réduction équivalente de l'État financé ; entreprises publiques et missions ont changé de champ. {cite('NZ_REFORMS','AgeofReform')}; {cite('NZ_TRENDS','tendances')}.",
        f"**[FAIT / ESTIMATION]** Nouvelle-Zélande récente : **65699ETP12/2023→62654en06/2025→63912en06/2026**. Dépenses externesPublicService **611,1→655,0M NZD**, **+{fmt(d['NZ_EXT_PCT'])}%**, sans causalité de substitution établie. {cite('NZ_ACTUEL','tableauxemploi/prestataires')}.",
        f"**[FAIT]** Suède : audit2021, gains de support souvent réinvestis dans le support. **171agences clientes en2025** ne valent pas un bilan d'économies ; les125guichets d'accueil relèvent d'une autre activité. {cite('SE_AGENCIES','PDF1-2')}; {cite('SE_CENTRE','2025')}.",
        f"**[FAIT / ESTIMATION]** Irlande : **320387→289643WTE2008-2014**, **{fmt(d['IE_0814_PCT'])}%**, puis317495en2017. Le recul2007-2014 du salairebrut,−11%, n'isole pas le moratoire. {cite('IE_COMMISSION','PDF21 / p13, tableau2.2')}.",
        f"**[EXTRAIT]** Simplex : communiqué2019 attribuant **plus de267M€/an à40mesures**, tous bénéficiaires ; le rapport d'évaluation intégral n'a pas été lu. Aucun montant netAPU n'est retenu. {cite('PT_SIMPLEX','bilan05/07/2019')}.",
        f"**[FAIT / ESTIMATION]** Portugal : environ **750000→660000personnes2010-2014**,−12% ; salaire/PIB−2,4points2010-2015 ; emploi+1,2%fin2014-fin2016 aprèsrestaurations. Prix, heures et missions empêchent un coefficient unique. {cite('PT_IMF','PDF18-19 et24 / pp17-18 et23')}.",
        f"**[FAIT]** Grèce : règleuneentrée/cinqretraites, cible **150000personnes** d'ici2015 annoncée atteinte2013par l'évaluationOCDE. Aucune économie nette attribuable n'est isolée ici. {cite('GR_ESM','PDF21, encadré2')}.",
        f"**[FAIT]** Italie : plusde350000personnes en moins2001-2018, période pluslarge que le blocage ; quotaÉtat **25%de dépense des sortants2016-18→100%en2019**, pas quota identique de personnes. {cite('IT_BANK','PDF13 / p11')}; {cite('IT_CAMERA','Facoltàassunzionali')}.",
        f"**[FAIT]** Allemagne : fin2022, **33bouquetsOZG/575** disponibles nationalement selonNKR, soit5,74%. Ce constat de couverture historique n'est ni l'état2026 ni une économie enETP. {cite('DE_NKR','PDF5')}.",
        f"**[FAIT]** NAV : synthèse2014 décrit démarragedéfavorable et progrès hétérogènes aprèsdeuxans. **50M NOK** financent l'évaluation, pas le coût de transition ; bilan net manquant. {cite('NO_NAV','sectionévaluationNAV')}.",
        f"**[FAIT / ESTIMATION]** Singapour : VITAL sert **plusde100agences** ; aucun gainnet vérifié. Corée : tableauKONEPS **6,8249MdUSDdont82,11%privé**, face à8Mddu récit, non réconciliés. {cite('SG_VITAL_HOME','Services')}; {cite('KR_KONEPS','PDF48-49 / pp47-48')}.",
        f"**[FAIT / ESTIMATION]** Japon : **538430→527477MJPY** surparcSIréférence2020,−2,03%nominalFY2024 ; **−14%aprèsretraitement**, cible−30%. {cite('JP_RESULT24','PDF2')}.",
        f"**[FAIT]** DOGE : GAO ne certifie pas110,34MdUSDaffichés. Sur61Mdde contrats déclarés, **37Md(60,7%)** relèvent d'autres méthodes ou de méthodes indéterminées ; **7,2Md(11,8%)** ont en plus des identifiants absents. OPMseule :3037→1985personnes ; CBO :7,9Mdde créditsFY2025annulés, objetdistinct. {cite('US_DOGE','tableaux2/4')}; {cite('US_OPM','PDF1')}; {cite('US_CBO','§loi119-28')}.",
    ]
    # Espacement des nombres dans la prose générée, sans changer les codes/URL.
    def prose(s):
        return re.sub(r'(?<=[A-Za-zÀ-ÿ%])(?=\d)|(?<=\d)(?=[A-Za-zÀ-ÿ])', ' ', s)
    # Ne jamais normaliser l'intérieur des URL : le texte des points est déjà
    # valide Markdown et les sources sont des liens directs conservés tels quels.
    summary = '\n\n'.join(f'{i}. {s}' for i,s in enumerate(points,1))
    summary_words = len(re.findall(r'\S+',re.sub(r'\]\([^)]*\)',']',typography(summary))))
    assert 15 <= len(points) <= 30 and summary_words <= 1500, summary_words
    selected = ['DK_DID_11','DK_POST_CREDIT','EE_X_TEMPS','NL_SCM_RESULT','NL_TOES_SPENT','UK_ONS_2016Q2','UK_NAO_DIFF','CA_REV_OBJ','CA_PH_EXP25','CA_PH_BACK','NZ_FTE_LAST','NZ_EXT_26','SE_CLIENTS','IE_WTE14','PT_SIMPLEX_TOT','PT_EMP14','GR_TARGET','IT_JOBS','DE_OZG_DONE','NO_EVAL_BUD','SG_CLIENTS','KR_TOTAL','JP_NOMINAL','JP_ADJUSTED','US_CLAIMS','US_OPM_AFTER','US_RESCISSION']
    table = ['| Indicateur | Valeur | Unité | Année | Champ / définition | Source (URL) | Page/tableau | Statut | Note |','|---|---:|---|---|---|---|---|---|---|']
    for iid in selected:
        r=by_id[iid]
        table.append('| '+' | '.join(str(v).replace('|','/') for v in [r['pays']+' — '+r['indicateur'],r['comparateur']+' '+fmt(r['valeur']),r['unite'],r['annee'],r['nature_mesure'],f"[{r['source_id']}]({r['source_url']})",r['source_localisation'],r['statut'],r['note']])+' |')
    blocks=[]
    for i,c in enumerate(cases,1):
        citations=' ; '.join(cite(s) for s in c['sources_ids'].split(';'))
        blocks.append(f"""### 3.{i}. {c['pays']} — {c['reforme']}

**Institution, missions et preuve ({c['periode']}).** {c['institutions_missions']} {c['etat_preuve']} Sources : {citations}. Les pages et objets chiffrés sont repris dans le tableau et `05_indicateurs.csv`.

**Avant/après et finances.** {c['finances']}

**Transition et périmètre.** {c['couts_transition']} {c['rebond_externalisation']}

**Service et causalité.** {c['service']} {c['causalite']}

**[HYPOTHÈSE de réforme à tester en France].** {c['transposabilite_france']} **Validation à2–3ans :** {c['validation_2_3_ans']}

**Confiance :** `{c['confiance']}`. **[NON TROUVÉ]** Bénéfice net complet comparable : case vide, sans valeur nulle ; potentielfrançais national enemplois/euros non identifié.
""")
    source_list='\n'.join(f"- **{sid}** — {cite(sid)} ; accès `{('partiel via OPEN primaire' if CAT[sid].get('preuve_web_local') and MAN[sid]['acces']!='integral' else MAN[sid]['acces'])}` ; archive/manifeste : `{MAN[sid].get('local_path','pas de corps téléchargé')}` ; localisations chiffrées dansCSV." for sid in sorted({r['source_id'] for r in indicators}|{s for c in cases for s in c['sources_ids'].split(';')}))
    not_ok=[c for c in checks if c['statut'] in ['A_REVOIR','ERREUR']]
    report=f"""# Réformes étrangères : résultats observés, coûts, périmètres et conditions de transposition

Consultation : **28 octobre2026**. Le dossier couvre **22cas dans17pays** demandés au chantier05 : Danemark, Estonie, Pays-Bas, Royaume-Uni, Canada, Nouvelle-Zélande, Suède, Irlande, Portugal, Grèce, Italie, Allemagne, Norvège, Singapour, Corée et Japon, États-Unis. FranceStratégie2017 sert de référence méthodologique. Ce lot étudie des réformes ; il ne remplace pas la base harmonisée03, les autres comparaisons parfonction04 ou le chiffragefrançais ultérieur.

## 1. Synthèse

{summary}

La synthèse contient {len(points)}résultats et {summary_words}mots selon le compteur reproductible du script, liens exclus du comptage. **Aucune case nette manquante n'est remplacée parzéro et aucun écart étranger n'est converti automatiquement en postes français supprimables.**

## 2. Tableau des indicateurs décisifs

Les qualificatifs d'objet sont essentiels : une prévision, une estimationde temps, un crédit réduit et une dépense exécutée ne sont pas interchangeables. `>` et `≈` conservent les bornes et approximations de la source. L'unité monétaire et les prix restent ceuxdu document ; aucun total transnational n'est calculé.

{chr(10).join(table)}

Les **{len(indicators)}observations** complètes sont dans `data/reformes/05_indicateurs.csv` ; **{len(calculations)}calculs** sont dans `05_calculs.csv` avec formule et identifiants d'entrée. Les comparaisons entre stocks avec champs nonconstants (Nouvelle-Zélande historique, catégoriesdepaiePhénix) ne produisent pas un pourcentage d'efficacité.

## 3. Monographies et dossiers de réforme

{chr(10).join(blocks)}

## 4. Enseignements utilisables et test français

**[FAIT de méthode]** Les cas décrivent au moins six objets : suppression ou transfert d'une mission ; contraction d'effectifs ; baisse salariale ; simplification d'une obligation ; interconnexion numérique ; mutualisation d'un support. Leur mécanisme doit être précisé avant tout chiffrage. ProgramReviewcomprend des décisions de périmètre ; SCMetKONEPScomptent surtout des coûts de transaction ; OZGcompte une couverture de services. Ils ne sont pas des mesures de la même quantité d'administration.

**[ESTIMATION, formule proposée]** Pour un pilote français donné : `gain annuel brut de trésorerie = dépense réellement évitée par rapport à un contrefactuel explicite`, puis `gain net = gain brut − investissements annualisés − transition − fonctionnement supplémentaire − coût des transferts et marchés de remplacement − coûts de correction des erreurs`. Les coûts ne sont déduits qu'une fois. Un gain de temps qui améliore le service est identifié comme capacité réaffectée ; il n'entre dans une économie budgétaire que si crédits ou recrutement sont réellement évités.

La réduction de recrutement utilise le coût d'entrée évité, et non le coût moyen des agents partis. Les pensions déjà dues ne disparaissent pas. Les cotisations et impôts requièrent ensuite un rapprochement APU consolidé ; un gouvernement étranger transférant une mission à une commune, une entreprise ou un prestataire n'a pas nécessairement réduit son coût économique. Le dossier ne renseigne aucun paramètre national français de baisse d'effectifs par imitation.

**[HYPOTHÈSE d'organisation]** Les mécanismes les mieux testables sont : mutualisation de procédures administratives homogènes avec périmètre constant ; suppression légale d'une pièce ou ressaisie ; interconnexion de registres fiables ; rapprochement de fonctions de paie/finance après standardisation ; revue de missions débouchant sur une décision explicite. La réduction parattrition est une modalitéd'exécution après identificationdes tâches qui disparaissent ; elle ne remplace pas ce diagnostic.

**Validation à24–36mois.** Un pilote fixe au départ un tableau de coûts internes et externes, investissement et récurrence, volumes, complexité, heures et postes, puis des résultats de service. Le suivi publié distingue temps gagné chez l'usager et chez l'agent, effectifs enETP et personnes, qualité des décisions, erreurs et délais. Un groupe de comparaison ou un déploiement échelonné permet d'améliorer l'attribution ; l'évolution du budget total et du stock de dossiers empêche de masquer un déplacement de charge. Le seuil d'acceptation de chaque indicateur doit être décidé avant le test, avec maintien des droits et accèsassisté.

## 5. Limites, données manquantes et contradictions

- **Aucune économie nette complète homogène** n'est reconstituée pourles22cas. Cela ne signifie pas économie nulle ; la donnée nécessaire manque. Trois mesures partielles sont conservées dans les colonnes brutes du fichiercas avec leur objet précis : créditsDigitalPost, salaireannualiséNAO, dépenseSIjaponaise de référence. Elles ne s'additionnent pas.
- **Causalité hétérogène.** L'étude danoiseDiDest plus informative sur un effet local de coûts administratifs qu'une simple variation de stock ; ses résultats ne concernent pas tous les services ni un coût complet. Les moratoires sous crise et changements demissions simultanés ne fournissent pas une productivité causale globale.
- **Coûts et rebond.** Les programmes canadiens, néozélandais et britanniques ont changé de périmètre et demissions. Les salaires peuvent être restaurés, les recrutements reprendre et les fonctions réapparaître chez des prestataires. Sans coût complet et indicateurs de résultat, ni la baisse ni le rebond ne prouvent àeuxseuls réussite ou échec global.
- **Contradictions gardées.** KONEPS :8MdUSDdansle récit contre6,8249Mdautableau2.6 ; explication monétaire/temporelle nonétablie dans les passages lus. Japon :résidu1MJPYentre totaux retraités et montant exogène ; budgetCanada1995 :100MCADd'écart entre somme de mesures arrondies et total triennal. Aucun résidu n'est distribué arbitrairement.
- **Fraîcheur et portée.** Lesdatesd'observation sont conservées :DigitalPost2015, OZG2022etétudeKONEPS2009ne décrivent pas un état2026. Le rapport FranceStratégie2017 porte souvent sur2015. Les données récentes2025–26 sont mobilisées quand consultables, mais les suivis contemporains ne réévaluent pas causalement les réformes anciennes.
- **Accès.** L'HTTPdirect échoue notamment pourcertainsPDFcanadiens, leFMI, laNorvège etleCBO ; les erreurs sont archivées, ycompris les pagesHTMLrenvoyées àlaplace d'unPDF. PourFMI/NAV/CBOetdeuxpagescanadiennes, le serviceconnecté a effectivement réussi des commandes`OPEN` de sources primaires. Les réponses exactes, passages et pages sont conservés dans `sources/05_ouvertures_primaires.json` et le complémentFMI. Il ne s'agit pas de simples snippets de recherche ni de corpsPDFlocaux. Le statutd'accès restepartiel lorsque le fichieroriginal n'a pas été téléchargé.
- **Provenance des copies.** Le document de laCommissionirlandaise2018 est une copie du rapportprimaire hébergéeparPNA ; l'articleAJPSdanois est une copie universitaire, avec titre, auteurs, pages etDOIidentifiables. Cela est signalé ; aucun avis syndical n'est utilisé comme preuve indépendante.
- **Simplex et Singapour.** Le rapportméthodologiqueintégral des40mesuresSimplex n'a pas été obtenu : les montants du communiqué sontmarqués`EXTRAIT`. Les pagesVITALdémontrent unserviceopérationnel et unobjectifd'échelle, sans évaluation indépendante de son gain net. Lescoûts/ETPmanquants restentvides.
- **Champ de couverture.** Les17pays explicitementnommés au chantier05 sont couverts ; ce dossier ne prétend pas constituer une monographie profonde de chaque pays de l'OCDE/UE. Lesautrespays du périmètregénéral relèvent d'abord de03 et04. Les17casnationaux ont des niveauxdepreuve différents, détaillés individuellement.

## 6. Sources, accès et reproduction

Chaque chiffre possède `source_url`, `source_localisation`, année, unité, nature etstatutdans leCSV. Les transcriptions manuelles sont signalées dans `sources/05_transcriptions.json` ; l'analyse est dans `05_dossier_cas.json`. Le script relit les corpsCSV/HTMLgzip ouPDFvalidés parSHA256, contrôle les repères de page etproduit les calculs explicites. Pour lesouvertures connectées seulement, ilrelit la preuveOPENarchivée. Ce contrôle de repèresne remplace pas une double transcription indépendante ; il garantit la traçabilité et évite une erreur de format ou de page silencieuse.

Commandes àlaracine :

```powershell
python scripts/05_collecte_sources.py
python scripts/05_construire_dossier.py
```

Le premier script conserve les corpsHTTP etSHA256, compresse lesHTML/CSV sansperte et place lesPDFdans `data/cache/05` ignoréparGit. `sources/05_catalogue_sources.json`, `05_manifestes.json` et les manifestes adjacents permettentde restaurer les archives. Pourretélécharger une source : `python scripts/05_collecte_sources.py ID --refresh`. Un nouvelétat peut différer ; lesSHAet le millésime sont alors misàjour et les valeurs doivent être recontrôlées. LesPDF/HTMLtéléchargés ne sont jamais exécutés. Aucun commit/push n'est effectué par ces scripts.

Contrôle du présent état : **{len(checks)}contrôles**, dont **{len(not_ok)}àrevoir** ; les deux résidus d'arrondi publiés sont explicitement conservés. Le schéma et les92observations sont vérifiés àchaque exécution ; les colonnes de potentiel français et économie nette restent vides.

{source_list}
"""
    # Nettoyage de prose hors liens/fences, sans modifier URL, codes ou données.
    # Les corrections typographiques détaillées sont conservées dans les entrées
    # de l'équipe ; les valeurs sources et dimensions ne sont jamais modifiées.
    report=typography(report)
    report=report.replace('résumé et article.','résumé scientifique consulté, texte intégral de l’article non lu.')
    (ROOT / 'recherche/05_reformes_etrangeres.md').write_text(report,encoding='utf-8',newline='\n')


if __name__ == '__main__':
    main()
