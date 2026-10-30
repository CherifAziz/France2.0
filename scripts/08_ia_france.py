"""Reconstruit les bases08 à partir des lectures primaires documentées.

Les valeurs transcrites ci-dessous ont été lues dans les localisations indiquées.
Les vérifications textuelles sont des contrôles de transcription, pas une seconde étude.
Aucun paramètre national et aucune économie de postes ne sont déduits de l'exposition.
Usage : python -I scripts/08_ia_france.py
"""
from __future__ import annotations
import csv
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "data/cache/08"
OUT = ROOT / "data/reformes"
SOURCES = [
    ("08_S01", "igas_ia2026", "IGF–IGAS–IGA, déploiement de l'IA dans les administrations publiques", "IGF/IGAS/IGA", 'rapport avril 2026; publication 2026-07-02', "partiel", '709 pages téléchargées ; lecture de passages précis : PDF 1-3,17,23-30,35,94-96,110,113,135,199-201,209-214,236,247-248,610,613,617-618,624-626,695-699. Repérage plus large par index, sans lecture intégrale des 709 pages. Tableaux 24/135/236/613 rendus ; note 162 p.236 inspectée visuellement.'),
    ("08_S02", "08_igas_page", "Fiche officielle du rapport IA", "IGAS", '2026-07-02; mise à jour 2026-09-09', "integral", "Date éditoriale lue, distincte d'avril 2026 sur la couverture et des numéros de mission 2025."),
    ("08_S03", "08_ifrap2025_position", "IA générative dans l'administration : une piste d'économies ?", 'Fondation i FRAP', "2025-11-10;mise à jour2026-04-29", "integral", 'Source de position, pas preuve du nombre de postes supprimables ;430 000 dérivé de Roland Berger, non résultat du rapport IGF 2026.'),
    ("08_S04", "08_assistant_evaluation2026", "Expérimentation de l'Assistant IA : évaluation pilote usages, perceptions, impacts", 'DITP/DINUM; Labor IA-Inria/INSA/CNRS', "2026-06-16", "partiel", "PDF 22 pages ; pages 3-7,9-11,14-18,20-22 consultées. P.5 :33 participants aux focus-groups ;86% A/A+ parmi les répondants aux questionnaires, pas profil démontré des 33. P.6 :IA toujours en seconde tâche ; p.16 données d'environ 30 agents et avertissement de non-généralisation ; p.17 qualité. Pages 5,6,16,17 rendues et inspectées."),
    ("08_S05", "08_assistant_bilan2026", "L'Assistant IA : bilan de l'expérimentation", "DITP", "2026-06-16", "integral", 'Page éditoriale et lien vers la synthèse ;12%/16% sur tâches, pas sur tous les agents. Communication 10 mois et 6 ministères à distinguer de la période du PDF.'),
    ("08_S06", "08_plan_notreia2026", "Notre IA : IA utile, humaine et souveraine pour les services publics", "DINUM", "2026-06-16", "integral", "Annonce de généralisation ; n'établit pas un nombre d'utilisateurs actifs ni une économie budgétaire mesurée."),
    ("08_S07", "08_notreia_dp2026", "Dossier de presse Notre IA", "Gouvernement/DINUM", "2026-06-16", "partiel", "24 pages téléchargées ; document associé à l'annonce, non traité comme évaluation indépendante. URL source stable conservée, le renvoi de téléchargement est temporaire."),
    ("08_S08", "08_aria2026", "ARIA France services : IA au service de l'accompagnement des usagers", "DILA", "2026-10-23", "integral", "Expérimentation juin 2026 auprès d'une dizaine de conseillers ; tests jusqu'à fin 2026. Retours qualitatifs, pas bilan causal d'ETP."),
    ("08_S09", "08_rgpd22_cnil_texte", "RGPD chapitre III, article 22 republié par l'autorité de contrôle", "CNIL/Union européenne", 'règlement 2016/679; consultation 2026-10-28', "partiel", "Texte de l'article 22 lu avec exceptions et garanties ; ne pas l'étendre à toute aide rédactionnelle."),
    ("08_S10", "08_cnil_automatisation", "Profilage et décision entièrement automatisée", "CNIL", 'consultation 2026-10-28', "integral", "Principe, exceptions, intervention et droits ; distinction aide à la décision/décision exclusivement automatisée."),
    ("08_S11", "08_cc2018_commentaire", 'Commentaire officiel de la décision 2018-765 DC', "Conseil constitutionnel", 'décision 2018-06-12', "partiel", "Section décisions administratives algorithmiques ; maîtrise, explicabilité et contrôle des évolutions. Le commentaire a été ouvert, pas seulement un résultat de recherche."),
    ("08_S12", "08_ddd2024", "Algorithmes, systèmes d'IA et services publics : quels droits pour les usagers ?", "Défenseur des droits", "2024", "partiel", 'PDF 49 pages ; cadre p.3-4/11, contrôle et intervention p.14-22, transparence p.32-37, notes p.43-48. Distinguer information individuelle et publication générale des règles.'),
    ("08_S13", "08_ai_act_calendrier", "AI Act : cadre et calendrier de mise en œuvre", "Commission européenne", 'page courante consultée 2026-10-28', "integral", "Next steps : proposition19/11/2025, accord7/05/2026, entrée en vigueur27/07/2026, lienJO L_202601744. Calendrier annoncé annexeIII2/12/2027 et annexeI2/08/2028 ; texte opposable consolidé non ouvert."),
    ("08_S14", "08_ai_omnibus_entree_force", "AI Omnibus enters into force", "Commission européenne", "2026-07-27", "integral", "Article officiel effectivement ouvert : entrée en vigueur annoncée le 27/07/2026 et dates 2027/2028. Distinct d'un simple accord politique ; lecture du texte JO demeure bloquée."),
    ("08_S15", "08_ai_act_consolide", 'Tentative texte consolidé AIA ct 2026-07-27', "EUR-Lex", "2026-07-27", "inaccessible", 'HTTP 202,0 octet ; aucune lecture juridique du texte consolidé revendiquée.'),
    ("08_S16", "08_ai_omnibus_jo2026", "Tentative Journal officiel AI Omnibus L_202601744", "EUR-Lex", "2026", "inaccessible", 'HTTP 202,0 octet ; calendrier fondé sur pages Commission ouvertes, non sur une prétendue lecture du JO.'),
    ("08_S17", "08_insee_illectronisme2025", "Une personne sur trois manque de compétences numériques", 'Insee Focus 376', "2026-02-19", "integral", 'Données 2025 ;16-74 ans :7% illectronisme,27% faibles compétences,34% ensemble ;75 ans+ :82% manquent de compétences,49% non-internautes. Champs à garder distincts.'),
    ("08_S18", "08_echecs_si_senat2020", "La conduite des grands projets numériques de l'État", "Sénat/Cour des comptes", "2020-10", "partiel", "Audition et constats sur Louvois, ONP, SIRHEN.480 M€SIRHEN est un ordre de grandeur déclaré lors de l'audition, pas une évaluation financière nouvelle de l'équipe."),
    ("08_S19", "08_assistant_beta2026", "L'Assistant, fiche du produit", "beta.gouv.fr/DINUM", 'consultation 2026-10-28', "integral", "Dates de lancement différentes des autres documents ; ne pas construire une série d'adoption avec les trois chronologies sans rapprochement."),
    ("08_S20", "08_igf_page", "Ancienne URL IGF du rapport : redirection vers accueil", "IGF", 'consultation 2026-10-28', "inaccessible", "HTTP 200 mais redirection vers page d'accueil igf.gouv.fr : cette réponse n'est pas la fiche du rapport et ne prouve pas sa date."),
]


def write_csv(path: Path, rows: list[dict]) -> None:
    keys = list(dict.fromkeys(k for r in rows for k in r))
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys); w.writeheader(); w.writerows(rows)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    registry, manifest = [], []
    for sid, alias, title, institution, date, access, notes in SOURCES:
        m = json.loads((CACHE / (alias+".meta.json")).read_text(encoding="utf-8"))
        registry.append(dict(id=sid,titre=title,institution=institution,date_publication=date,url=m["source_url"],date_consultation="2026-10-28",acces=access,sha256_16=m.get("sha256", "")[:16],notes=notes))
        manifest.append(dict(id=sid,lecture=access,passages_et_limites=notes,**m))
    sr = {r["id"]:r for r in registry}
    rows = []
    def add(id_, theme, indicator, value, unit, year, scope, sid, loc, proof, limits, status="FAIT"):
        rows.append(dict(id=id_,theme=theme,indicateur=indicator,valeur=value,unite=unit,annee=year,champ=scope,
                         nature_preuve=proof,source_id=sid,source_url=sr[sid]["url"],source_localisation=loc,statut=status,
                         limites=limits,economie_nette_nationale=None,etp_effectivement_supprimes=None))
    r = "08_S01"
    facts = [
      ("01","exposition",'Agents exposés gradients 1-4',20,"% des agents",'2022, calcul rapport 2026',"Emplois FP classés d'après indicateur OIT",24,"indice_exposition","Pas un taux d'automatisation ni un gain de temps."),
      ("02","exposition","Effectif exposé correspondant",1130000,"agents",'2022, calcul rapport 2026','Base DGAFP 2022',24,"indice_exposition",'Pas des ETP entiers supprimables ; ne pas remplacer par effectif 2024 sans refaire le rapprochement.'),
      ("03","exposition",'Gradients 3-4',13,"% des agents",'2022, calcul rapport 2026',"Catégories les plus/significativement exposées",24,"indice_exposition",'Plus de 700000 selon le rapport ; aucune économie directe estimée.'),
      ("04","exposition","Non référencés",7,"% des agents",'2022, calcul rapport 2026',"Professions non cotables",24,"limite_classification","Absence de score, pas absence d'exposition."),
      ("05","exposition","Armées non cotées OIT",3,"% des agents",'2022, calcul rapport 2026',"Armées",24,"limite_classification","Leur exclusion ne démontre pas une absence de tâches augmentables."),
      ("06",'shadow IA',"Jusqu'à 40% usage clandestin",40,"% cité, borne déclarée",'enquête septembre 2025',"Collectivités, enquête SNDGCT citée par la mission",17,"declaration_enquete_reprise","Source de l'enquête non relue ; pas estimation représentative de tous les agents publics."),
      ("07","deploiement","Produits DINUM recensés",141,"produits",'mission 2026','Inventaire non exhaustif,80 entités',17,"inventaire","Produits, pas emplois ni utilisateurs actifs."),
      ("08","deploiement","Entités DINUM recensées",80,"entités",'mission 2026',"Inventaire non exhaustif",17,"inventaire","Ne mesure pas un taux de couverture de toutes les administrations."),
      ("09","deploiement","Maximum POC par ministère",74,"POC",'mission 2026','Réponses de 9 secrétariats généraux',135,"questionnaire_administrations","Plage 0-74 POC ; ce n'est pas 74 outils déployés partout."),
      ("10","deploiement","Maximum outils déployés par ministère",15,"outils",'mission 2026','Réponses de 9 secrétariats généraux',135,"questionnaire_administrations",'Plage 1-15 ; maturité et qualité hétérogènes.'),
      ("11","achats",'Gains pouvant dépasser 60% sur certaines tâches',60,"% seuil cité, pas moyenne",'bilan septembre 2025','Expérimentation DAE 44 agents, meilleures solutions/tâches',95,"experimentations_declarees",'Supérieur à 60% pour certaines tâches ; protocole causal, distribution et fréquence non publiés dans le rapport.'),
      ("12","CNAV","Gain bas activités courtes",20,"% de temps de la tâche",'mission 2026','Copilot Chat,9000 adoptants, activités courtes/faible valeur métier',26,"estimation_administration","Plage 20-30%, non tout le temps de l'agent."),
      ("13","CNAV","Gain haut activités courtes",30,"% de temps de la tâche",'mission 2026',"Même périmètre que08_F12",26,"estimation_administration","Pas une mesure causale randomisée ni une économie budgétaire."),
      ("14","CNAM","Productivité développeurs estimée",5,"% de productivité cité",'mission 2026','100 développeurs en test',28,"estimation_administration","Unité productivité non assimilée sans précision à réduction du temps ou des effectifs."),
      ("15","collectivites",'Temps libéré dans équipe CDGH aute-Savoie',20,"% du temps de l'équipe",'mission 2026','Pré-analyse RH,30000-40000 arrêtés/an',29,"retour_experience","Temps réinvesti sur le conseil, non postes supprimés ; contrefactuel non fourni."),
      ("16","DITP_usagers","Délai moyen réponse avant",19,"jours calendaires de délai",'dispositif fin 2023, bilan mission 2026',"Je donne mon avis",28,"avant_apres_declare","Délai de service, pas minutes de travail agent."),
      ("17","DITP_usagers","Délai moyen réponse après",3,"jours calendaires de délai",'dispositif fin 2023, bilan mission 2026',"Même périmètre que08_F16",28,"avant_apres_declare",'Les gains de service ne se convertissent pas en heures par simple ratio 19/3.'),
      ("18","DITP_usagers",'Réponses jugées utiles avec IA',68,"% des répondants",'bilan mission 2026','Je donne mon avis, contre 57% sans IA',28,"qualite_declaree","Composition des groupes et identification causale non détaillées ici."),
      ("19",'France Travail','Chat FT adoption fin 2025',51000,"agents ayant adopté selon FT","2025",'55000 agents potentiellement concernés',247,"declaration_adoption","Adoption ne signifie pas usage quotidien ni temps économisé homogène."),
      ("20",'France Travail','Chat FT équivalent temps estimé',226,"ETP équivalents de temps déclarés",'septembre 2025','Questionnaire France Travail',236,"estimation_equivalent_temps","Note 162 : aucune diminution pratique d'ETP ; méthodes non publiées ; recoupement entre outils non exclu."),
      ("21",'France Travail',"Panoptes équivalent temps estimé",300,"ETP équivalents de temps déclarés",'septembre 2025','Questionnaire France Travail',236,"estimation_equivalent_temps",'Même réserve note 162 ; ne pas additionner comme postes supprimés.'),
      ("22",'France Travail',"NEO équivalent temps estimé",241,"ETP équivalents de temps déclarés",'septembre 2025','Questionnaire France Travail',236,"estimation_equivalent_temps",'Même réserve note 162 ; temps réaffectable.'),
      ("23","couts",'MI r AI investissement total',17.8,"M€ d'investissement sur 5 ans",'évaluation projet 2026',"Hors fonctionnement",613,"evaluation_projet","Ce n'est pas une dépense annuelle ni un coût unitaire national par agent."),
      ("24","couts",'MI r AI coût projet incluant 2 premièresannéesrun',20.34,"M€ total projet de période composite",'évaluation projet 2026','Investissement+2 premièresannées de fonctionnement',613,"evaluation_projet",'Ne pas ajouter 17,8 M€ une seconde fois ; vérifier réalisé/prévisionnel avant calibration.'),
      ("25","couts",'France Travail investissement IA',12.875,"M€ d'investissement","2025","Questionnaire au sein du rapport",618,"depense_declaree","Ne couvre pas tout le programme numérique ni une baisse d'effectifs."),
      ("26","couts",'France Travail fonctionnement IA',.508,"M€ de fonctionnement","2025","Questionnaire au sein du rapport",618,"depense_declaree","Distinct investissement ; cumul dépend de la période et de l'assiette de charges internes."),
      ("27","education","Cassandre dossiers traités",1200,"dossiers environ",'bilan repris mission 2026',"Gestion RH enseignants à Versailles",110,"retour_experience",'Pas tous les enseignants ; gain 2 h par instruction optimisée, population éligible non exhaustive.'),
    ]
    for n,th,ind,v,u,y,ch,p,pr,li in facts:
        add("08_F"+n,th,ind,v,u,y,ch,r,f"PDF p.{p} ; pagination imprimée propre au rapport/annexe",pr,li)
    for n,ind,v,u,ch,loc,li in [
      ("28","Licences pilote",10000,"licences","Pilote DINUM","p.3",'Pas 10000 participants aux tâches expérimentales ; période PDF déc 2025-juin 2026.'),
      ("29","Participants aux focus-groups",33,"agents volontaires",'MEF et Justice',"p.5-6,16","Les 86% A/A+ décrivent les questionnaires, pas les 33 ; données de tâches d'environ 30 agents selon p.16 ; IA en seconde tâche ; population volontaire."),
      ("30","Gain moyen mail publié",2.5,"minutes par tâche","Réponse à une chaîne de mails","p.16",'Moyennes arrondies 21 min sans IA/19 avec ; ne pas reconstituer exactement 2,5 à partir des seules moyennes arrondies.'),
      ("31","Gain moyen synthèse publié",5.4,"minutes par tâche","Synthèse d'un document 6 pages","p.16",'Moyennes arrondies 33 min/28 min ; aucun IC publié ; non-généralisation explicite.'),
      ("32","Amélioration qualité mail",.95,'points sur 20',"Deux correcteurs indépendants","p.17","Comparaison de mise en situation ; pas effets sur droits ou économies."),
      ("33","Amélioration qualité synthèse",1.28,'points sur 20',"Deux correcteurs indépendants","p.17",'Notes 14,15→15,43 ; évaluation de ce corpus restreint.'),
    ]:
        add("08_F"+n,"Assistant_evaluation",ind,v,u,"2026",ch,"08_S04",loc,"mise_en_situation_petit_echantillon",li)
    for n,ind,v,ch,li in [
      ("34",'Illectronisme 16-74 ans',7,'Personnes 16-74 ans','Ne pas présenter comme 7% des 15 ans+ ni des 75 ans+.'),
      ("35",'Faibles compétences 16-74 ans',27,'Personnes 16-74 ans',"Distinct de l'illectronisme ; ensemble 34%."),
      ("36",'Manque compétences 75 ans+',82,'Personnes 75 ans+','Indicateur large, dont 49% non-internautes ; pas 82% enillectronisme selon la définition 16-74 ans.'),
    ]:
        add("08_F"+n,"inclusion",ind,v,"%","2025",ch,"08_S17",'Figure 1 et section 75 ans+',"enquete_statistique",li)
    add("08_F37","position","Potentiel annoncé par l'i FRAP",430000,"emplois potentiellement automatisables selon auteur",'article 2025',"Position issue d'une transposition Roland Berger","08_S03","Section impact administration française","position","Ni mesure IGF 2026 ni suppressions observées ; cout 60 k moyen n'est pas un coût d'entrée démontré.")
    add("08_F38",'echecs SI',"Coût SIRHEN évoqué à l'audition",480,"M€ environ",'audition 2020','Développement abandonné, ordre de grandeur cité',"08_S18",'Audition, intervention Cour citant SIRHEN',"declaration_audition","Pas IA générative ; ne pas reconstituer un coût net complet ni un taux futur d'échec à partir de ce montant.")
    write_csv(OUT / "08_constats_chiffres.csv",rows)

    deployments = []
    for actor,tools,metric,sid,loc,limit in [
      ("DINUM","L'Assistant/Transcripts/Albert API",'33 participants aux focus-groups ; tâches sur environ30 agents ; annonce de généralisation juin2026',"08_S04","p.3-6,16-17",'Licences, utilisateurs actifs et participants distincts ; chronologie des communications à rapprocher.'),
      ('DGF i P','foncier innovant, LL a Mmendements, assistant généraliste','Investissement 6,3 M€/fonctionnement 1,3 M€ en 2025 cités',"08_S01",'PDF 613',"Recettes fiscales ciblées et automatisations passées distinctes de l'IA générative ; attribution nette renvoyée à 06."),
      ('France Travail','Chat FT, Panoptes, NEO, Match FT','226/300/241 équivalents temps estimés',"08_S01",'PDF 199-201,236 note 162,247-248',"Aucune baisse réelle d'ETP selon mission ; réinvestissement possible ; somme non calibrée."),
      ("CNAF",'datamining,@doc MS, IAG pour Tous','Outils statistiques et projets génératifs de maturités différentes',"08_S01",'PDF 209-210,239-240',"Pas de gain national d'ETP net établi ; score de contrôle ne décide pas automatiquement d'une fraude."),
      ("CNAM",'Camélia, Copilotcode','5% productivité estimée sur 100 développeurs en test',"08_S01",'PDF 28,212-214','Test de tâche et estimation interne, pas suppression de 5% des agents CNAM.'),
      ("CNAV",'Copilot Chat, aide rédactionnelle','20-30% sur activités courtes,9000 adoptants selon mission',"08_S01",'PDF 26,28,618','Gainsdéclarés ; dev 30 min-2 h/semaine ; périmètre hebdomadaire non national.'),
      ("Justice",'Pred Natinf, DPIA','POC etoutilsdéployés ; qualification/aideauxagents',"08_S01",'PDF 113,135',"Pas de mesure causale de diminution d'emplois dejustice identifiée."),
      ("Education",'Cassandre, MIAS econde, Aristote','RH dossiers Vs apprentissage ; mesures hétérogènes',"08_S01",'PDF 29,110','Temps par instruction optimisée ne vaut pas temps de tous les enseignants ; TALIS renvoyé à 04 b.'),
      ("Santé",'aidecodage, plannings, documentation',"Retours d'expérience français sans ETP national net","08_S01",'PDF 28,229-231','Personnel soignant/support hospitalier hors champ administratif unique ; RCT scribes traité en 09.'),
      ("Collectivités",'CDGH aute Savoie, chatbotslocaux','20% tempséquipe CDG réinvesti dansconseil',"08_S01",'PDF 29',"Pas d'ETP supprimé ; effetsaccueil et qualité àsuivre."),
      ('France Services/DILA',"ARIA",'Dizaine de conseillers, testinitialjuin 2026',"08_S08","Phase d'expérimentation prometteuse","Pas d'évaluation représentative de toutleréseau ni économie de personnel mesurée."),
      ("DAE",'recherche documentaire, sourcing, rédaction','Expérimentation 44 agents, gaindeplus 60% sur certaines tâches',"08_S01",'PDF 94-95','Retenir le dénominateur tâche et coûtqualité ; méthodes et gainsmoyens manquants.'),
    ]:
        deployments.append(dict(acteur=actor,outils=tools,resultat_documente=metric,annee="2025-2026",source_url=sr[sid]["url"],source_localisation=loc,statut="FAIT",limites=limit,etp_supprimes_verifies=None,economie_budgetaire_nette_meur=None))
    write_csv(OUT / "08_deploiements.csv",deployments)

    params=[]
    for id_,task,unit,low,central,high,sid,loc,status,reason in [
      ("08_P01",'Mail simple, Assistant DINUM',"minutes économisées par tâche",None,2.5,None,"08_S04","p.5-6,16-17","POINT_LOCAL_NON_GENERALISABLE",'33 participants aux focus-groups ; tâches sur environ 30 agents, effectif valide par exercice non donné ; sans IA avant IA dans le schéma ; IC nonpublié ; central désigne un point local, pas une prévision nationale.'),
      ("08_P02",'Synthèse 6 pages, Assistant DINUM',"minutes économisées par tâche",None,5.4,None,"08_S04","p.5-6,16-17","POINT_LOCAL_NON_GENERALISABLE",'Même design ; fréquence, volume éligible, qualité décisionnelle et conversion budgétaire manquants.'),
      ("08_P03",'CNAV activités courtes à faible valeur métier',"fraction temps de la tâche",.20,.25,.30,"08_S01",'PDF 26',"HYPOTHESE_SENSIBILITE_PLAGE_DECLAREE","20-30% rapporté par l'administration ;25%=milieu arithmétique choisi pour sensibilité, non estimation causale ; pas de taux national."),
      ("08_P04",'CNAV développement informatique',"heures par développeur par semaine",.5,1.25,2,"08_S01",'PDF 28',"HYPOTHESE_SENSIBILITE_PLAGE_DECLAREE",'Plage 30 min-2 h/semaine ; centre 1,25 h calculé, non prévision validée ; temps hebdomadaire de référence manquant.'),
      ("08_P05",'CNAM développement informatique',"fraction temps de la tâche",None,None,None,"08_S01",'PDF 28',"NON_TROUVE",'5% est annoncé comme productivité, sansdéfinition ni contrefactuel suffisants pour calibrer un gain de temps causal.'),
      ("08_P06","DAE tâchesachat sélectionnées","fraction temps de la tâche",None,None,None,"08_S01",'PDF 94-95',"NON_TROUVE",'>60% sur certaines tâches est un seuil sélectif, pas une moyenne, ni distribution, ni plafond généralisable.'),
      ("08_P07",'France Travail troisoutils',"réduction ETP effectivement réalisée",None,None,None,"08_S01",'PDF 236 note 162',"NON_TROUVE",'226/300/241 sont équivalents de temps estimés ; mission précise absence de traduction en diminution des ETP ; méthode et recoupements inconnus.'),
      ("08_P08",'CDGH aute Savoie préanalyse RH',"fraction temps de la tâche",None,None,None,"08_S01",'PDF 29',"NON_TROUVE",'20% tempséquipe déclaré puis réaffecté ; volume éligible et contrefactuel manquants.'),
      ("08_P09","Exposition ensemble FP","taux de baisse nationale deseffectifs",None,None,None,"08_S01",'PDF 23-25,698',"NON_TROUVE",'20% exposition ne mesure pas un gain ni un nombre de postes ; pas de taux national uniforme.'),
      ("08_P10",'ARIAF rance Services',"fraction temps de la tâche",None,None,None,"08_S08","Phase d'expérimentation","NON_TROUVE","Retours qualitatifs d'une dizaine de conseillers ; pas d'effet quantitatif primaire publié dans cette page."),
    ]:
        params.append(dict(parametre_id=id_,tache=task,unite=unit,prudent=low,central=central,ambitieux=high,annee="2025-2026",statut=status,raison_et_limites=reason,part_temps_tache_dans_poste=None,taux_adoption_cible=None,taux_conversion_temps_en_postes=None,cout_deploiement_national_meur=None,source_url=sr[sid]["url"],source_localisation=loc,usage_modele_national="NON_ETAYE_SANS_TRANSPORT_VALIDATION_ET_COUTS"))
    write_csv(OUT / "08_parametres_taches.csv",params)

    legal=[]
    for id_,rule,sid,loc,meaning,limit in [
      ("08_J01","RGPD article22","08_S09","Article22 §1-4","Décisions exclusivement automatisées à effets juridiques ou significatifs : principe, exceptions et garanties","Distinguer aide rédactionnelle et décision automatique ; vérifier base juridique, exceptions et données sensibles."),
      ("08_J02","CRPA information et publication","08_S12","PDF p.32-37 et notes p.46-48","Information individuelle, communication des règles et publication générale relèvent de régimes distincts","L.311-3-1 et R.311-3-1-1/-2 se distinguent de L.312-1-3 ; ne pas reprendre sans examen le renvoi p.624 du rapport IGF."),
      ("08_J03","Conseil constitutionnel2018-765DC","08_S11","Section sur les décisions administratives algorithmiques","Maîtrise du traitement et de ses évolutions ; explication intelligible et détaillée","Source ouverte : commentaire officiel. Il ne permet pas d'affirmer une interdiction générale des aides génératives."),
      ("08_J04","Intervention humaine substantielle","08_S12","PDF p.14-22","La supervision exige compétence, moyens et pouvoir réel de corriger","Le coût complet inclut validation, erreurs, recours et explication. Une recommandation ne constitue pas elle-même un gain de temps."),
      ("08_J05","AI Act : calendrier officiel annoncé","08_S14","Article du27 juillet2026 et rubrique Next steps de la page cadre","La Commission annonce l'entrée en vigueur de l'AI Omnibus le27/07/2026 ; annexeIII le2/12/2027 et annexeI le2/08/2028","Le JO L_202601744 et le consolidé répondent202 vide. Calendrier lu sur les pages officielles, sans prétendre avoir relu la version opposable ou ses exceptions."),
    ]:
        legal.append(dict(id=id_,regle=rule,annee="état consulté2026-10-28",portee=meaning,limites=limit,source_url=sr[sid]["url"],source_localisation=loc,statut="FAIT"))
    write_csv(OUT / "08_cadre_juridique.csv",legal)

    # Contrôles de transcription sur les passages du rapport, pas sur des CSV dérivés.
    text=(CACHE/"igas_ia2026.txt").read_text(encoding="utf-8")
    pieces=re.split(r"\[PAGE (\d+)\]",text);pages={int(pieces[i]):pieces[i+1] for i in range(1,len(pieces),2)}
    assert "AVRIL 2026" in pages[1]
    assert all(x in pages[2] for x in ["2025-E-081-03","2025-089R","26008R"])
    assert all(x in pages[236] for x in ["226","300","241","diminution des ETP"])
    assert re.search(r"20,34",pages[613]) and re.search(r"17,8",pages[613])
    assert not any(row["economie_nette_nationale"] is not None for row in rows)
    assert all(r["acces"] == "inaccessible" or len(r["sha256_16"]) ==16 for r in registry)
    write_csv(ROOT/"sources/registre_08.csv",registry)
    (ROOT/"data/raw/08/08_manifestes_sources.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps({"constats":len(rows),"deploiements":len(deployments),"parametres_taches":len(params),"sources":len(registry),"chiffrage_national":"aucun"},ensure_ascii=False))


if __name__ == "__main__": main()
