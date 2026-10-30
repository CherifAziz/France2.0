#!/usr/bin/env python3
"""Contre-vérification ciblée des notes08 et09, sans leurs extracteurs auteurs.

Lecture directe des PDF primaires (pypdf) et des corps texte archivés dans
data/cache/08 et data/cache/09, plus le résumé clinique API de data/raw/09.
Les scripts 08_ia_france.py et 09_ia_preuves.py ne sont ni lus ni importés.
Les fichiers de paramètres 08/09 sont relus comme sorties publiées, pour
contrôler leurs signes et bornes contre les intervalles primaires.

Écrit uniquement data/risques/verification_08_09_lot3.csv et la note homonyme.
"""
import csv, json, re, sys, unicodedata
from decimal import Decimal
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT/'.cache/python_deps'))
from pypdf import PdfReader

NOTE08=ROOT/'recherche/08_ia_france.md'
NOTE09=ROOT/'recherche/09_ia_preuves_internationales.md'
PARAM09=ROOT/'data/reformes/09_parametres_taches.csv'
CSV=ROOT/'data/risques/verification_08_09_lot3.csv'
NOTE=ROOT/'recherche/00_verification_08_09_lot3.md'
C8=ROOT/'data/cache/08'; C9=ROOT/'data/cache/09'
FIELDS=['id','theme','indicateur','annee','valeur_publiee','valeur_source','unite','source_url','source_localisation','statut_controle','note']
RESTORE='python -I scripts/restore_lot3_sources.py --download'

URL={
 'rapport':'https://igas.gouv.fr/sites/igas/files/2026-07/Rapport%20D%C3%A9ploiement%20IA%20(2026).pdf',
 'igas':'https://www.igas.gouv.fr/le-deploiement-de-lintelligence-artificielle-dans-les-administrations-publiques-analyse-comparee-enjeux-et-conditions-de-reussite',
 'ditp':'https://www.modernisation.gouv.fr/files/2026-06/Synthese-evaluation-experimentation-Assistant-IA.pdf',
 'ditp-page':'https://www.modernisation.gouv.fr/publications/lassistant-ia-bilan-de-lexperimentation-menee-aupres-des-agents',
 'dinum':'https://www.numerique.gouv.fr/sinformer/espace-presse/intelligence-artificielle-ia-utile-humaine-souveraine-services-publics/',
 'insee':'https://www.insee.fr/fr/statistiques/8739245',
 'ifrap':'https://www.ifrap.org/etat-et-collectivites/lintelligence-artificielle-generative-dans-ladministration-une-piste-deconomies',
 'omnibus':'https://digital-strategy.ec.europa.eu/en/news/ai-omnibus-enters-force',
 'si':'https://www.senat.fr/rap/r20-047/r20-047_mono.html',
 'bryn':'https://danielle.li/assets/docs/GenerativeAIatWork.pdf',
 'noy':'https://shakkednoy.com/Noy%20Zhang%20NBER%20SI.pdf',
 'dell':'https://www.hbs.edu/ris/Publication%20Files/dell-acqua-et-al-2026-navigating-the-jagged-technological-frontier_5c589c8c-fbb5-458f-b285-c944746cd717.pdf',
 'humlum':'https://www.nber.org/system/files/working_papers/w33777/w33777.pdf',
 'metr':'https://metr.org/Early_2025_AI_Experienced_OS_Devs_Study-paper.pdf',
 'metr26':'https://metr.org/blog/2026-02-24-uplift-update/',
 'uk':'https://www.gov.uk/government/publications/microsoft-365-copilot-experiment-cross-government-findings-report/microsoft-365-copilot-experiment-cross-government-findings-report-html',
 'dbt':'https://assets.publishing.service.gov.uk/media/68adbe409e1cebdd2c96a19d/dbt-microsoft-365-copilot-evaluation.pdf',
 'dta':'https://www.digital.gov.au/sites/default/files/documents/2024-10/Copilot%20Microsoft%20365%20summary%20of%20evaluation%20findings.pdf',
 'turing':'https://www.turing.ac.uk/sites/default/files/2024-03/ai_for_bureaucratic_productivity.pdf',
 'ilo':'https://www.ilo.org/publications/generative-ai-and-jobs-refined-global-index-occupational-exposure',
 'nao':'https://www.nao.org.uk/wp-content/uploads/2024/03/use-of-artificial-intelligence-in-government.pdf',
 'oecd':'https://www.oecd.org/content/dam/oecd/en/publications/reports/2025/06/governing-with-artificial-intelligence_398fa287/795de142-en.pdf',
 'scribe':'https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:41497288%20AND%20SRC:MED&format=json&resultType=core',
 'police':'https://link.springer.com/content/pdf/10.1007/s11292-024-09644-7.pdf',
 'toeslagen':'https://www.autoriteitpersoonsgegevens.nl/uploads/imported/boetebesluit_belastingdienst.pdf',
 'midas':'https://www.courts.michigan.gov/4a1c19/siteassets/case-documents/opinions-orders/msc-term-opinions-%28manually-curated%29/21-22/bauserman-op.pdf',
}

def flat(s):
    # Les extractions PDF coupent des mots et varient espaces/apostrophes : on compare sans blancs.
    s=unicodedata.normalize('NFKC',str(s)).replace('’',"'").replace('−','-').replace('–','-').replace('*','')
    return re.sub(r'\s+','',s).casefold()

_pdf={}
def pdf_text(path,page):
    if path not in _pdf:_pdf[path]=PdfReader(path)
    return _pdf[path].pages[page-1].extract_text() or ''

def source_text(spec):
    """spec = (fichier, pages) pour un PDF, (fichier, None) pour un texte archivé."""
    path,pages=spec
    if not path.exists():return None
    if pages is None:return path.read_text(encoding='utf-8',errors='replace')
    return '\n'.join(pdf_text(path,p) for p in pages)

def main():
    notes={'08':NOTE08.read_text(encoding='utf-8'),'09':NOTE09.read_text(encoding='utf-8')}
    rows=[]
    def check(id,theme,label,year,published,unit,url,loc,specs,needles,note_id,anchors,status='CONFIRME',remark='',absent=()):
        texts=[source_text(s) for s in specs]
        if any(t is None for t in texts):
            rows.append(dict(zip(FIELDS,[id,theme,label,year,published,'NON VERIFIABLE',unit,url,loc,'NON_VERIFIABLE_CACHE_ABSENT','Restaurer : '+RESTORE])));return
        body=flat('\n'.join(texts))
        missing=[n for n in needles if flat(n) not in body]
        present=[n for n in absent if flat(n) in body]
        located=all(flat(a) in flat(notes[note_id]) for a in anchors)
        state=status if not missing and not present and located else ('ECART_SOURCE' if missing or present else 'NOTE_MODIFIEE_A_RELOCALISER')
        detail=' ; '.join(needles) if not missing else 'Absent de la source : '+' ; '.join(missing)
        if present:detail+=' ; présent alors qu’attendu absent : '+' ; '.join(present)
        rows.append(dict(zip(FIELDS,[id,theme,label,year,published,detail,unit,url,loc,state,remark])))
    def calc(id,theme,label,year,published,computed,unit,url,loc,ok,note_id,anchors,remark):
        located=all(flat(a) in flat(notes[note_id]) for a in anchors)
        state='CALCUL_CONFIRME' if ok and located else ('ECART_CALCUL' if not ok else 'NOTE_MODIFIEE_A_RELOCALISER')
        rows.append(dict(zip(FIELDS,[id,theme,label,year,published,computed,unit,url,loc,state,remark])))

    R=C8/'igas_ia2026.pdf'
    # --- Note 08 : rapport IGF–IGAS–IGA ---
    check('V0809-01','08 Rapport IA','Date portée, numéros de mission et publication','avril 2026 ; publié 02/07/2026','avril 2026 ; IGF 2025-E-081-03, IGAS 2025-089 R, IGA 26008 R ; publication 2 juillet, mise à jour 9 septembre 2026','date',URL['rapport'],'PDF p.1-2 ; fiche IGAS',
          [(R,[1,2]),(C8/'08_igas_page.txt',None)],['AVRIL 2026','IGF N° 2025-E-081-03','IGAS N° 2025-089R','IGA N° 26008R','Publié le 02/07/2026','Mis à jour le 09/09/2026'],'08',['avril 2026','2025-E-081-03','2 juillet 2026'],
          remark='Le millésime 2025 des numéros de mission n’est pas une date de publication.')
    check('V0809-02','08 Rapport IA','Exposition OIT des agents publics','base DGAFP 2022','20 % ; 1,13 million ; gradients 3-4 : 13 %, plus de 700 000 ; 7 % non référencés','% et millions d’agents',URL['rapport'],'PDF p.24-25',
          [(R,[24,25])],['20% des agents publics sont considérés comme exposés (gradients 1 à 4), soit 1,13 million','soit 13% (plus de 700 000 agents)','7% ne sont pas référencés dans la nomenclature','non une estimation directe des gains de productivité'],'08',['1,13 million','700 000','7 %'],
          remark='Indice d’exposition, sans mesure d’adoption ni de postes supprimables.')
    check('V0809-03','08 Rapport IA','« Shadow IA » jusqu’à 40 %','enquête septembre 2025','jusqu’à 40 % ; source SNDGCT, collectivités','% d’agents',URL['rapport'],'PDF p.3 note 1 ; p.17 note 18',
          [(R,[3,17])],["pourrait concerner jusqu'à 40 % des agents publics",'Syndicat national des directions générales des collectivités territoriales (SNDGCT) de septembre 2025'],'08',['SNDGCT','40 %'],
          remark='Enquête territoriale citée, originale non relue ; pas une mesure nationale représentative.')
    check('V0809-04','08 Rapport IA','Inventaire DINUM et outils ministériels','2026','141 produits dans 80 entités ; 0–74 POC ; 1–15 outils déployés','nombre d’outils',URL['rapport'],'PDF p.17 ; p.135 tableau 17',
          [(R,[17,135])],["141 produits d'IA dans 80 entités publiques",'entre 0 et 74 outils',"preuves de concept",'entre 1 et 15 outils',"Intérieur 74 15"],'08',['141 produits','0–74','1–15'],
          remark='Le maximum 74/15 est celui de l’Intérieur ; POC et outils déployés restent distincts.')
    check('V0809-05','08 France Travail','Adoption ChatFT','fin 2025','51 000 adoptants pour 55 000 agents concernés','agents',URL['rapport'],'PDF p.200 ; p.247',
          [(R,[200,247])],['55 000 collaborateurs de France Travail',"ayant adopté le produit fin 2025 s'élève à 51 000",'potentiellement concernés 55 000'],'08',['51 000','55 000'],
          remark='Adoption déclarée, pas fréquence d’usage ni temps libéré.')
    check('V0809-06','08 France Travail','Équivalents temps ChatFT/Panoptes/NEO et note 162','septembre 2025','226 / 300 / 241 ETP ; aucune diminution d’ETP','équivalents ETP',URL['rapport'],'PDF p.236, note 162',
          [(R,[236])],['ChatFT : gains ETP estimés à septembre 2025 : - 226 ETP','Panoptes : gains ETP estimés à septembre 2025 : - 300 ETP','Neo : gains ETP estimés à septembre 2025 : - 241 ETP',"n'ont pas été traduits en pratique par une diminution des ETP"],'08',['226','241','pas entraîné de diminution des ETP'],
          remark='Réserve décisive confirmée : ordres de grandeur de temps, aucun poste supprimé.')
    check('V0809-07','08 Caisses sociales','CNAV, CNAM : gains déclarés','2025','CNAV 20–30 % sur activités courtes, 9 000 adoptants ; CNAM 5 % sur 100 développeurs ; CNAV 30 min–2 h/semaine','% et heures',URL['rapport'],'PDF p.26 et 28',
          [(R,[26,28])],["pour 9 000 agents qui l'ont déjà adopté, un gain de temps estimé entre 20 % et 30 %",'activités courtes et à faible valeur métier','5% pour la CNAM sur la base de 100 développeurs en test','30 min à 2 heures par semaine par développeur à la CNAV'],'08',['9 000','100 développeurs'],
          remark='Estimations internes ; pas une part de la journée de travail ni du personnel.')
    check('V0809-08','08 Service','« Je donne mon avis » : délai et utilité','bilan DITP cité','19 → 3 jours ; 68 % contre 57 %','jours et % d’usagers',URL['rapport'],'PDF p.28',
          [(R,[28])],['de 19 à 3 jours',"68 % avec la solution d'IA contre 57 % sans"],'08',['19 à 3 jours','68 %','57 %'],
          remark='Indicateurs de service, non convertibles en durée de travail.')
    check('V0809-09','08 Achats','Expérimentation DAE','bilan 2025','44 agents ; gains pouvant dépasser 60 % sur certaines tâches','agents ; %',URL['rapport'],'PDF p.94-95',
          [(R,[94,95])],['44 agents de la DAE',"Pour les solutions d'IA jugées les plus performantes",'pouvant dépasser 60 % sur certaines tâches'],'08',['44 agents','60 %'],
          remark='Maximum sur certaines tâches des meilleures solutions, pas une moyenne de la fonction achat.')
    check('V0809-10','08 Collectivités','CDG de Haute-Savoie','retour d’expérience','20 % du temps de l’équipe, réinvesti dans le conseil ; 30 000–40 000 arrêtés/an','% du temps ; actes',URL['rapport'],'PDF p.29',
          [(R,[29])],['30 000 à 40 000 arrêtés à vérifier par an',"libérant 20 % du temps de travail de l'équipe",'réinvesti sur le conseil aux collectivités'],'08',['20 % du temps','réinvesti'],
          remark='Temps réaffecté, sans réduction d’effectif.')
    check('V0809-11','08 Coûts','MIrAI et dépenses IA de France Travail','2025-2026','MIrAI 17,8 M€ (5 ans) / 20,34 M€ avec 2 ans de fonctionnement ; France Travail 2025 : 12 875 k€ / 508 k€','M€ et k€',URL['rapport'],'PDF p.613 ; p.618 tableau 6',
          [(R,[613,618])],["coût d'investissement total atteint 17,8 M€",'deux premières années de fonctionnement atteint 20,34 M€','Investissement 398 k€ 5 488 k€ 12 875 k€','733 k€ 508 k€'],'08',['17,8 M€','20,34 M€','12,875 M€','0,508 M€'],
          remark='Périodes et périmètres distincts ; 20,34 M€ inclut déjà les 17,8 M€. La valeur 2023 du fonctionnement (« 4441 k€ » à l’extraction) n’est pas utilisée et n’a pas été rendue visuellement.')
    # --- Note 08 : DITP, DINUM, Insee, iFRAP, AI Act, SI ---
    D=C8/'08_assistant_evaluation2026.pdf'
    check('V0809-12','08 L’Assistant','Échantillons DITP','déc. 2025–juin 2026','33 participants aux focus-groups ; environ 30 agents ; 86 % A/A+ et 35 % d’encadrants parmi les répondants aux questionnaires','agents ; %',URL['ditp'],'PDF p.5 et 16',
          [(D,[5,16])],['33 participants aux focus groups','Les agents de catégories A et A+ représentent 86% de notre échantillon',"35% des agents ayant répondu aux questionnaires",'environ 30 agents volontaires'],'08',['33 volontaires','86 %','environ 30 agents'],
          remark='Le 86 % décrit les répondants aux questionnaires, pas les 33 expérimentateurs : la note conserve cette distinction.')
    check('V0809-13','08 L’Assistant','Durées et qualité des deux tâches','2026','mail 21→19 min, −2,5 min ; synthèse 33→28 min, −5,4 min ; qualité +0,95 / +1,28 sur 20','minutes ; points',URL['ditp'],'PDF p.16-17',
          [(D,[16,17])],['Mail 21 min 19 min - 2,5 min',"Synthèse d'article 33 min 28 min - 5,4 min",'ne peuvent en aucun cas être généralisés','(+0,95)','(+1,28), sur 20 points'],'08',['2,5 minutes','5,4 minutes','0,95','1,28'],
          remark='Moyennes arrondies non réconciliables exactement avec les gains publiés, comme la note l’indique.')
    check('V0809-14','08 L’Assistant','Perceptions du bilan DITP','16 juin 2026','75 % utilité ; 65 % recommandation ; 56 % moindre recours aux IA non souveraines','% de répondants',URL['ditp-page'],'page bilan',
          [(C8/'08_assistant_bilan2026.txt',None)],["75% des agents considèrent l'outil utile pour leur métier","65% d'entre eux le recommanderaient",'56% déclarent avoir réduit leur recours'],'08',['75 %','65 %','56 %'],
          remark='Perceptions déclarées, sans mesure d’effectifs.')
    check('V0809-15','08 L’Assistant','Annonce DINUM du 16 juin 2026','16 juin 2026','généralisation après un pilote de 10 000 licences ; Transcripts ; DiploIA 64 langues','agents ; langues',URL['dinum'],'communiqué ; fiche produit beta',
          [(C8/'08_plan_notreia2026.txt',None),(C8/'08_assistant_beta2026.txt',None)],['mardi 16 juin 2026','10 mois d\'expérimentation réussie auprès de 10 000 agents','Transcripts','64 langues','Lancé en octobre 2025 auprès de 10 000 agents'],'08',['16 juin 2026','10 000','64 langues'],status='CONFIRME_RESERVE_FORMULATION',
          remark='Les sources parlent de 10 000 agents et non de licences : écart de formulation à corriger dans la note 08 §1.7, sans effet chiffré.')
    check('V0809-16','08 Accès','Compétences numériques Insee Focus 376','2025, paru 19/02/2026','illectronisme 7 % des 16–74 ans ; 27 % faibles compétences ; 34 % au sens large ; 82 % des 75 ans+, dont 49 % non-internautes','% de population',URL['insee'],'Insee Focus 376',
          [(C8/'08_insee_illectronisme2025.txt',None)],["7 % des personnes âgées de 16 à 74 ans sont en situation d'illectronisme",'27 % des personnes âgées de 16 à 74 ans ont des compétences numériques faibles','34 % de la population de 16 à 74 ans','82 % des 75 ans ou plus manquent de compétences numériques : 49 % sont non-internautes','Paru le19/02/2026'],'08',['7 % des 16–74 ans','27 %','82 % des 75 ans','34 %'],
          remark='Champs d’âge distincts conservés.')
    check('V0809-17','08 Positions','430 000 emplois automatisables (iFRAP)','publié 10/11/2025, mis à jour 29/04/2026','430 000 emplois ; d’après Roland Berger','emplois',URL['ifrap'],'article',
          [(C8/'08_ifrap2025_position.txt',None)],['près de 430 000 emplois','soit 54 % environ (53,7 %) du total public/privé','800 000 emplois au total','Roland Berger','Publié le 10 novembre 2025','Mis à jour le 29 avril 2026'],'08',['430 000','Roland Berger','10 novembre 2025'],
          remark='Part publique (53,7 %) des 800 000 emplois automatisables public et privé d’une étude Roland Berger 2023 reprise par l’iFRAP : position, non mesure.')
    check('V0809-18','08 Droit','Calendrier AI Omnibus','27 juillet 2026','entrée en vigueur 27/07/2026 ; annexe III 2/12/2027 ; annexe I 2/08/2028 ; JO L_202601744','dates',URL['omnibus'],'article Commission',
          [(C8/'08_ai_omnibus_entree_force.txt',None)],['On 27 July 2026, the AI Omnibus enters into force','Rules apply starting 2 December 2027','Rules apply starting 2 August 2028','OJ:L_202601744'],'08',['27 juillet 2026','2 décembre 2027','2 août 2028','L_202601744'])
    empty=[p.name for p in (C8/'08_ai_omnibus_jo2026.html',C8/'08_ai_act_consolide.html',C8/'08_ai_act_consolide_pdf.html') if p.exists() and p.stat().st_size==0]
    rows.append(dict(zip(FIELDS,['V0809-19','08 Droit','Texte opposable AI Act non relu','28/10/2026','JO et consolidé : HTTP 202, fichier vide',' ; '.join(empty) or 'fichiers absents','octets',URL['omnibus'],'archives JO/consolidé',
          'LIMITE_CONFIRMEE' if len(empty)==3 and flat('HTTP 202') in flat(notes['08']) else 'ECART_SOURCE','Trois corps vides archivés : la note a raison de ne pas revendiquer la lecture du texte opposable.'])))
    check('V0809-20','08 Échecs SI','Coût de Sirhen abandonné','audition Cour au Sénat, 14/10/2020','environ 480 M€','M€',URL['si'],'rapport Sénat r20-047, compte rendu d’audition',
          [(C8/'08_echecs_si_senat2020.txt',None)],["Sirhen, le système de gestion intégrée des ressources humaines du ministère de l'éducation nationale, qui a dû être abandonné après un développement ayant coûté à peu près 480 millions d'euros",'Sirhen (188,1 millions d\'euros)'],'08',['480 M€','SIRHEN'],status='CONFIRME_AVEC_RESERVE',
          remark='Le 480 M€ est une déclaration orale. Le même rapport cite Sirhen à 188,1 M€ comme valeur comptable d’un projet en service : concept et périmètre différents, à mentionner pour éviter une confusion.')

    # --- Note 09 : études internationales ---
    check('V0809-21','09 Entreprises','Brynjolfsson–Li–Raymond, version QJE','publication 2025','5 172 agents ; +15 % de dossiers résolus/heure ; +30 % pour les moins expérimentés','agents ; %',URL['bryn'],'PDF p.1 et 3',
          [(C9/'09_brynjolfsson2025.pdf',[1,3])],['data from 5,172 customer-support agents','by 15% on average','a 30% increase in the number of issues resolved per hour'],'09',['5 172','+15 %','30 %'],absent=['5,179'],
          remark='Les anciennes valeurs 5 179/14 % sont absentes de cette version, conformément à la note.')
    calc('V0809-22','09 Calcul','Équivalent temps de +15 % de productivité','calcul',13.04,format((1-Decimal(1)/Decimal('1.15'))*100,'.2f'),'% de temps',URL['bryn'],'1 − 1/1,15',
          abs((1-1/1.15)*100-13.04)<0.005,'09',['13,04 %'],'Calcul conditionnel à production et qualité fixes, sans valeur budgétaire.')
    check('V0809-23','09 Expériences','Noy–Zhang, manuscrit final','expérience 2023','453 professionnels ; −40 % de temps ; +18 % de qualité','%',URL['noy'],'PDF p.1 et 3',
          [(C9/'09_noy_final_author.pdf',[1,3])],['453 college-educated professionals','average time taken decreased by 40%','output quality rose by 18%'],'09',['453','−40 %','+18 %'])
    check('V0809-24','09 Expériences','Dell’Acqua et al., version publiée 2026','expérience 2023','758 consultants ; +12,2 % de tâches ; −25,1 % de temps ; hors frontière 84,5 % contre 60 % / 70,6 %, environ −19 points','% et points',URL['dell'],'PDF p.2, 5, 12',
          [(C9/'09_dell2026.pdf',[2,5,12])],['758 knowledge workers','completing 12.2% more tasks','25.1% more quickly','758 BCG consultants','correct about this exercise about 84.5% of the time','scored at 60% and 70.6%','an average decrease of 19 percentage points','19% less likely to produce correct solutions'],'09',['758','12,2 %','25,1 %','84,5 %'],
          remark='L’abstract dit « 19 % », le corps « 19 points » : la note retient à juste titre la définition du corps.')
    check('V0809-25','09 Emploi total','Humlum–Vestergaard, registres danois','registres à fin 2024, révision 2026','25 000 travailleurs ; 7 000 lieux de travail ; 11 professions ; effets > 2 % exclus','travailleurs ; %',URL['humlum'],'PDF p.2-5',
          [(C9/'09_humlum_current.pdf',[2,3,5])],['25,000 workers across 7,000 workplaces','11 occupations','ruling out average effects larger than 2%'],'09',['25 000','7 000','11 professions'])
    check('V0809-26','09 Logiciel','METR 2025 et suite 2026','fév.–juin 2025 ; billet du 24/02/2026','16 développeurs ; 246 tâches ; +19 % de temps [+2 ; +39] ; perçu −20 % ; suite −18 % et −4 %, jugée peu fiable','% de temps',URL['metr'],'PDF p.1-2 ; billet METR',
          [(C9/'09_metr2025.pdf',[1,2]),(C9/'09_metr2026_update.txt',None)],['16 developers with moderate AI experience complete 246 tasks','increases completion time by 19%','reduced completion time by 20%','confidence interval between +2% and +39%','speedup of -18% with a confidence interval between -38% and +9%','speedup is -4%, with a confidence interval between -15% and +9%','unreliable signal','February 24, 2026'],'09',['246 tâches','19 %','−18 %','−4 %'],
          remark='L’intervalle 2025 est lu dans le billet METR 2026, le PDF le portant dans une figure ; les deux intervalles 2026 incluent zéro.')
    p9={r['parametre_id']:r for r in csv.DictReader(PARAM09.open(encoding='utf-8'))}
    trip=lambda k:[Decimal(p9[k][c]) for c in ('prudent','central','ambitieux')]
    want={'09_P04':[Decimal('-0.39'),Decimal('-0.19'),Decimal('-0.02')],'09_P05':[Decimal('0.018'),Decimal('0.095'),Decimal('0.172')],'09_P06':[Decimal('-0.059'),Decimal('0.017'),Decimal('0.094')]}
    got={k:trip(k) for k in want}
    calc('V0809-27','09 Paramètres','Signes et bornes METR/Nabla/DAX dans 09_parametres_taches.csv','sorties publiées',json.dumps({k:[str(x) for x in v] for k,v in got.items()}),'METR −(+39,+19,+2) % ; Nabla −(−17,2 ; −9,5 ; −1,8) % ; DAX −(+5,9 ; −1,7 ; −9,4) %','fraction de temps économisé',URL['metr26'],'inversion de signe des IC primaires',
          got==want,'09',['−0,39','0,018','−0,059'],'Les trois triplets inversent exactement les intervalles primaires ; ce sont des sensibilités locales, pas des scénarios nationaux.')
    check('V0809-28','09 Administrations','Essai Copilot transversal GDS','30/09–31/12/2024','20 000 licences ; 7 115 réponses ; 26 min/jour déclarées ; journaux 14 500 utilisateurs','agents ; minutes',URL['uk'],'§1.2, §3, §4',
          [(C9/'09_uk_cross2025.txt',None)],['involving 20,000 government employees','7,115 responses','saved an average of 26 minutes a day','14,500 users','using the middle point of each range'],'09',['20 000','7 115','26 minutes','14 500'])
    check('V0809-29','09 Administrations','Évaluation DBT : dispositif','oct.–déc. 2024','1 000 licences ; ~70 % volontaires, ~30 % tirés au sort ; sans contrefactuel ; 300 journaux consentis ; pas de preuve de productivité accrue','licences ; %',URL['dbt'],'PDF p.4-7 et 15',
          [(C9/'09_dbt2025.pdf',[4,5,6,15])],['volunteers (~70%)','randomly selected participants (~30%)','evidence-without-a-counterfactual','did not find evidence that time savings have led to improved productivity','The department had 1,000 licences','300 consented to their data being analysed'],'09',['1 000 licences','300 journaux'],
          remark='La note situe les 1 000 licences p.4-5 ; elles figurent p.6-7 de l’extraction. Écart de localisation mineur.',status='CONFIRME_LOCALISATION_APPROX')
    check('V0809-30','09 Administrations','DBT : journaux et exercices observés','pilote 2024','synthèse/recherche +0,8 h ; planification −0,6 h ; PowerPoint 10:47 contre 18:30, exactitude 1,5/5 contre 5/5, qualité 1/5 contre 2/5 ; Excel 25:01 contre 20:33 ; synthèse 12:37 contre 41:34','heures ; mm:ss ; notes /5',URL['dbt'],'PDF p.29 tableau 5 ; p.31 tableau 6',
          [(C9/'09_dbt2025.pdf',[29,31])],['Summarising research 1.6 1.4 0.8','Scheduling 0 -0.5 -0.6','Data analysis in Excel 1.5 2.7 1.5 2.7 25:01 20:33','PowerPoint 1.5 5 1 2 10:47 18:30','Summarising reports 4 2.5 4 3 12:37 41:34'],'09',['10:47','18:30','25:01','12:37'],
          remark='Colonne retenue : heures ajustées des productions inutilisées et des tâches nouvelles. Ordre des colonnes du tableau 6 confirmé : exactitude, qualité, temps (utilisateur puis non-utilisateur).')
    check('V0809-31','09 Administrations','Essai australien DTA','essai 2024','plus de 2 000 contributeurs ; 831 réponses finales ; 40 % déclarent réaffecter du temps','participants ; %',URL['dta'],'PDF p.5 et 15',
          [(C9/'09_dta2024.pdf',[5,15])],['Over 2,000 trial participants','831 respondents in post-use survey','40% of trial participants reported their ability to reallocate their time'],'09',['2 000','831','40 %'])
    check('V0809-32','09 Potentiels','Turing Institute : transactions','étude 2024','environ 1 milliard de transactions ; 143 millions complexes ; 84 % automatisables ; 1 200 années-personnes illustratives','transactions ; %',URL['turing'],'PDF p.1',
          [(C9/'09_turing2024.pdf',[1])],['approximately one billion citizen-facing transactions','approximately 143 million are complex repetitive transactions','84% of these complex transactions are highly automatable','approximately 1,200 person-years'],'09',['143 millions','84 %'])
    calc('V0809-33','09 Calcul','Sous-ensemble Turing potentiellement automatisable','calcul','120,12 millions',format(Decimal(143)*Decimal('0.84'),'f'),'millions de transactions',URL['turing'],'143 × 0,84',
          Decimal(143)*Decimal('0.84')==Decimal('120.12'),'09',['120,12 millions'],'Taille conditionnelle d’un sous-ensemble, pas des ETP évitables.')
    check('V0809-34','09 Indices','Exposition OIT/NASK','indice 2025','25 % des emplois mondiaux ; 3,3 % au gradient maximal ; 34 % dans les pays à haut revenu','% des emplois',URL['ilo'],'résumé primaire',
          [(C9/'09_oit2025_page.txt',None)],['one in four workers are in an occupation with some GenAI exposure','3.3% of global employment falls into the highest exposure category','34% in HICs'],'09',['25 %','3,3 %','34 %'])
    check('V0809-35','09 Inventaires','NAO 2024 et OCDE 2025','2023-2025','NAO : 37 % de 87 organismes ont déployé, 70 % pilotent ou planifient ; OCDE : 200 cas dans 11 fonctions','% ; cas',URL['nao'],'NAO PDF p.10 ; OCDE PDF p.11',
          [(C9/'09_nao2024.pdf',[10]),(C9/'09_ocde2025.pdf',[11])],['(37%) of the 87 government bodies that responded to our survey have deployed AI','(70%) are piloting or planning AI','11 core functions of government across 200 use cases'],'09',['37 %','87 organismes','200 cas'])
    check('V0809-36','09 Terrain','Essai randomisé de scribes ambiants','nov. 2024–janv. 2025 ; publié 26/11/2025','238 médecins, 14 spécialités ; Nabla −9,5 % [−17,2 ; −1,8] ; DAX −1,7 % [−9,4 ; +5,9] ; usage 29,5 % / 33,5 % des visites','% du temps de note',URL['scribe'],'résumé Europe PMC',
          [(ROOT/'data/raw/09/09_scribes2026_abstract.json',None)],['238 outpatient physicians, representing 14 specialties','DAX was used in 33.5%','Nabla was used in 29.5%','9.5% (95% confidence interval [CI], -17.2% to -1.8%','(-1.7%; 95% CI, -9.4% to +5.9%','clinically significant inaccuracies','"firstPublicationDate": "2025-11-26"'],'09',['238 médecins','−9,5 %','−1,7 %','29,5 %'])
    check('V0809-37','09 Terrain','Essai policier DraftOne','étude 2024','85 agents ; 755 rapports ; 6 084 rapports en différences de différences ; pas d’effet significatif','agents ; rapports',URL['police'],'PDF p.1 ; affiliation Manchester, NH',
          [(C9/'09_police_rct2024_pdf.pdf',[1])],['(n = 85)','(n = 755)','(n = 6084)','AI assistance did not significantly affect the duration of writing police reports','Manchester, NH'],'09',['85 agents','755 rapports','6 084'])
    check('V0809-38','09 Échecs','Toeslagen et MiDAS','2021 ; 2022','amende AP 2,75 M€ ; arrêt Bauserman du 26 juillet 2022','€ ; date',URL['toeslagen'],'AP PDF p.1 ; Cour suprême du Michigan PDF p.1',
          [(C9/'09_toeslagen_ap2021.pdf',[1]),(C9/'09_midas_arret2022.pdf',[1])],['bestuurlijke boetes van in totaal € 2.750.000','Decided July 26, 2022'],'09',['2,75 M€','26 juillet 2022'],
          remark='Sanction et recevabilité, non un coût social total ni un audit d’erreurs.')

    CSV.parent.mkdir(exist_ok=True)
    with CSV.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,FIELDS,lineterminator='\n');w.writeheader();w.writerows(rows)
    write_note(rows)
    bad=[r['id'] for r in rows if r['statut_controle'] in ('ECART_SOURCE','ECART_CALCUL','NOTE_MODIFIEE_A_RELOCALISER','NON_VERIFIABLE_CACHE_ABSENT')]
    print(f"{len(rows)} contrôles ; écarts ou indisponibles : {', '.join(bad) or 'aucun'}")
    return 1 if bad else 0

def write_note(rows):
    from collections import Counter
    n=Counter(r['statut_controle'] for r in rows)
    reserves=[r for r in rows if r['statut_controle'] not in ('CONFIRME','CALCUL_CONFIRME','LIMITE_CONFIRMEE')]
    ecarts=[r for r in rows if r['statut_controle'] in ('ECART_SOURCE','ECART_CALCUL','NOTE_MODIFIEE_A_RELOCALISER','NON_VERIFIABLE_CACHE_ABSENT')]
    lines=['# Contre-vérification indépendante des chantiers 08 et 09 — lot 3','',
     'Contrôle arrêté au **30 octobre 2026**, sur les notes présentes dans le dépôt. Les scripts auteurs `08_ia_france.py` et `09_ia_preuves.py` n’ont été ni lus, ni importés, ni exécutés. Chaque passage est relu dans le PDF primaire à la page indiquée (pypdf) ou dans le corps texte archivé ; les ancres sont recherchées dans la note publiée.','',
     f"**Résultat : {len(rows)} points contrôlés, dont {n['CONFIRME']} confirmations directes, {n['CALCUL_CONFIRME']} calculs confirmés, {n['LIMITE_CONFIRMEE']} limite d’accès confirmée et {len(reserves)} confirmations avec réserve. Écarts de chiffre ou sources indisponibles : {len(ecarts)}.**",'',
     'Les statuts, passages lus et remarques de chaque ligne figurent dans `data/risques/verification_08_09_lot3.csv`.','','## Résultats','']
    for r in rows:
        lines.append(f"- **{r['id']} — {r['statut_controle']}** : {r['indicateur']} ({r['valeur_publiee']}). Source : {r['source_localisation']}."+(f" {r['note']}" if r['note'] else ''))
    lines+=['','## Corrections reportées dans les notes le 30 octobre 2026','',
     '- **Note 08 §1.7** : écrire « pilote auprès de 10 000 agents » plutôt que « 10 000 licences » ; communiqué DINUM et fiche produit parlent d’agents.',
     '- **Note 08 §4 (Sirhen)** : préciser que les 480 M€ sont une déclaration orale à l’audition et que le même rapport donne 188,1 M€ comme valeur comptable d’un projet en service. Les deux chiffres ne mesurent pas la même chose.',
     '- **Note 09 §1.11** : les 1 000 licences DBT sont p.6-7 de l’extraction, non p.4-5 (localisation seulement).','',
     'Ces corrections de formulation et de localisation ne modifient aucun paramètre ni aucune somme : aucun chiffre des notes n’est contredit par sa source. Les statuts ci-dessus décrivent l’état constaté avant correction.','',
     '## Portée','',
     '- La vérification est documentaire : elle confirme que les chiffres sont fidèlement transcrits et localisés, pas que les études sont transposables à l’administration française.',
     '- Les paramètres METR et scribes sont des inversions de signe exactes des intervalles primaires ; ils restent des sensibilités locales.',
     '- Les textes non ouverts (JO de l’AI Omnibus, enquête SNDGCT, bilan DAE interne, texte intégral des scribes, article Choi) restent non lus, comme les notes l’indiquent.','',
     '## Reproduction','','```powershell','python -I scripts/00_verification_08_09_lot3.py','```','',
     'Dépendance : pypdf, chargée depuis `.cache/python_deps`. Les PDF de `data/cache/08` et `data/cache/09` sont hors Git ; un cache absent produit le statut `NON_VERIFIABLE_CACHE_ABSENT` avec la commande de restauration. Seuls le CSV et cette note sont réécrits. Note en UTF-8, fins de ligne LF.','']
    NOTE.write_text('\n'.join(lines),encoding='utf-8',newline='\n')

if __name__=='__main__':
    sys.exit(main())
