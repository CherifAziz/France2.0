"""Base des preuves09 et paramètres par tâche, sans extrapolation nationale.
Usage : python -I scripts/09_ia_preuves.py
Points publiés, intervalles statistiques et scénarios opérationnels sont distingués.
"""
from __future__ import annotations
import csv
import json
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CACHE=ROOT/"data/cache/09"
OUT=ROOT/"data/reformes"
SOURCES = [('09_S01',
  '09_brynjolfsson2025',
  'Generative AI at Work, QJE',
  'Brynjolfsson, Li, Raymond/OUP',
  '2025-02-04',
  'partiel',
  'Version publiée de54 pages ; PDF p.1,3-4,19 (imprimées889,891-892,907) lues. 5172 agents,+15%, différences de '
  'différences et hétérogénéité. Pas de randomisation.'),
 ('09_S02',
  '09_noy_final_author',
  'Experimental evidence on productivity effects of generative AI, manuscrit auteur Science',
  'Noy, Zhang/Science',
  '2023-07',
  'partiel',
  'Manuscrit final auteur,19 pages, lié depuis le site auteur ; p.1-4 lues. 453 professionnels,40% de temps et18% '
  'de qualité, tâches de20-30 minutes, GPT3.5, notation aveugle.'),
 ('09_S03',
  '09_noy2023',
  'Noy-Zhang, ancien working paper',
  'MIT/Noy, Zhang',
  '2023-03-02',
  'partiel',
  'Ancienne version de15 pages, p.1 lue :444 participants et document non évalué par les pairs. Conservée pour '
  'tracer les versions, pas pour étayer les chiffres finaux.'),
 ('09_S04',
  '09_dell2026',
  'Navigating the Jagged Technological Frontier',
  "Dell'Acqua etal/Organization Science",
  '2026-03-11',
  'partiel',
  'Version publiée,22 pages ; p.1-2,5,9,11-14 lues. 758 participants, groupes385/373 ;25,1% de temps,12,2% de '
  "tâches ; p.12 précise19 points de pourcentage hors frontière, malgré l'abstract ambigu."),
 ('09_S05',
  '09_humlum_current',
  'Still Waters, Rapid Currents, ancien titre Large Language Models, Small Labor Market Effects',
  'Humlum, Vestergaard/NBER 33777',
  '2025-05; révision 2026-03',
  'partiel',
  "Révision mars2026,131 pages ; p.1-5,11-12 et passage p.31 lus. Registres jusqu'à décembre2024, environ25000 "
  'répondants,7000 lieux et11 professions ; effets moyens heures/revenus proches de zéro et IC écartant '
  'environ2%.'),
 ('09_S06',
  '09_metr2025',
  'Measuring Impact Early 2025 AI on Experienced Open Source Developer Productivity',
  'METR',
  '2025-07-10',
  'partiel',
  'PDF50 pages ; résumé et méthode p.1-2 lus, passages limites et intervalles repérés. 16 développeurs,246 '
  'tâches,+19% de temps, outils de février-juin2025. Figure p.2 rendue ; pas lecture des50 pages.'),
 ('09_S07',
  '09_metr2026_update',
  'We are Changing our Developer Productivity Experiment Design',
  'METR',
  '2026-02-24',
  'integral',
  'Mise à jour ouverte : points de-18% et-4% de temps, intervalles incluant zéro. Les auteurs jugent les '
  'résultats peu fiables en raison de la sélection et de la mesure de sessions multiagents.'),
 ('09_S08',
  '09_uk_cross2025',
  'Microsoft 365 Copilot Experiment:Cross Government Findings Report',
  'UK Government Digital Service',
  '2025-06-02',
  'partiel',
  'HTML : méthode§3 et résultats§4 lus. 20000 licences,7115 réponses et14500 utilisateurs dans les journaux. '
  '26min/jour issus de classes déclarées ; pas un RCT ni une économie constatée.'),
 ('09_S09',
  '09_dbt2025',
  'Evaluation M365 Copilot Pilot DBT',
  'UK Department for Business and Trade',
  '2025-08-26',
  'partiel',
  'PDF49 pages ; p.4-5,29-31 et passages de méthode lus. 1000 licences,300 journaux consentis et32% de réponse ; '
  'évaluation principale sans contrefactuel. Tableau6 p.31 rendu et inspecté. Limite de productivité globale '
  'p.5.'),
 ('09_S10',
  '09_dta2024',
  'Whole-of-government trial Microsoft 365 Copilot:summaryevaluation',
  'Australian DTA/Nous',
  '2024-10',
  'partiel',
  'PDF22 pages ; p.4-6,15-16 lues. Volontaires non randomisés, plus de2000 contributeurs, plus de50 agences et831 '
  'réponses finales. Perceptions et réaffectations, pas postes supprimés.'),
 ('09_S11',
  '09_turing2024',
  'AI for bureaucratic productivity:potential 143 million transactions',
  'Alan Turing Institute/Straub et al.',
  '2024-03',
  'partiel',
  "PDF18 pages ; résumé p.1 et structure de l'étude lus. Environ1 milliard de transactions et400 services, "
  'dont143 millions complexes répétitives ;84% concerne ce sous-ensemble. La minute supposée gagnée est '
  'illustrative.'),
 ('09_S12',
  '09_oit2025_page',
  'Generative AI and Jobs:Refined Global Index',
  'OIT/NASK',
  '2025-05-20',
  'integral',
  "Résumé primaire effectivement ouvert : environ25% de l'emploi mondial exposé,3,3% au gradient maximal et34% "
  "dans les pays à haut revenu. Indice d'exposition et de transformation, pas suppressions observées."),
 ('09_S13',
  '09_oit2025',
  'Generative AI and Jobs, Working Paper 140',
  'OIT/NASK',
  '2025-05',
  'partiel',
  'PDF76 pages archivé ; résumé et repérage méthodologique, rapprochés du résumé primaire ouvert. Aucune lecture '
  'exhaustive revendiquée.'),
 ('09_S14',
  '09_nao2024',
  'Use of artificial intelligence in government',
  'UK National Audit Office',
  '2024-03-15',
  'partiel',
  'PDF56 pages ; p.6-10 lues. 87 organismes répondants,37% de déploiements IA et70% de pilotes/projets ; '
  'catégories chevauchantes. Ni IA générative seule ni économies mesurées.'),
 ('09_S15',
  '09_ocde2025',
  'Governing with Artificial Intelligence',
  'OCDE',
  '2025-09-18',
  'partiel',
  'PDF306 pages ; résumé p.11 lu et chapitre inventaire repéré p.60. 200 cas dans11 fonctions ; corpus '
  'descriptif, pas200 expériences causales ou échantillon représentatif de rendements.'),
 ('09_S16',
  '09_scribes2025_xml',
  'RCT two ambient AI scribes, prepublication',
  'Lukac etal/med Rxiv',
  '2025-07-10',
  'partiel',
  'XML primaire EuropePMC ouvert : introduction, méthodes et résultats. Prépublication distincte du texte publié. '
  'Essai de238 médecins,14 spécialités, du4 novembre2024 au3 janvier2025.'),
 ('09_S17',
  'RAW:09_scribes2026_abstract',
  'Ambient AIS cribes in Clinical Practice:Randomized Trial, résumé publié',
  'Lukac etal/NEJMAI, Europe PMC',
  'première publication 2025-11-26; numéro 2026',
  'partiel',
  "Résumé publié ouvert via l'API resultType=core. Nabla-9,5% de temps de note, IC[-17,2;-1,8] ; DAX-1,7%, "
  'IC[-9,4;+5,9]. Texte publié complet bloqué. Ne pas mélanger les critères secondaires avec la prépublication.'),
 ('09_S18',
  '09_police_rct2024_pdf',
  "No man's hand: AI does not improve police report writing speed",
  'Adams et al./Journal of Experimental Criminology',
  '2024',
  'partiel',
  'PDF18 pages et HTML ouverts ; résumé, méthode et résultats lus. Manchester, New Hampshire :85 policiers,755 '
  "rapports randomisés et6084 dans la robustesse DID. Pas d'effet significatif de durée ; pas une preuve d'effet "
  'exactement nul.'),
 ('09_S19',
  '09_midas_arret2022',
  'Bauserman v Unemployment Insurance Agency',
  'Michigan Supreme Court',
  '2022-07-26',
  'partiel',
  'PDF95 pages ; syllabus p.1-4 et standard de contrôle p.12 lus. Action constitutionnelle indemnitaire possible '
  "au vu des allégations, puis renvoi. Pas un audit de93% d'erreurs ni un jugement définitif de tous les faits."),
 ('09_S20',
  '09_toeslagen_ap2021',
  'Décision de sanction Belastingdienst/Toeslagen',
  'Autoriteit Persoonsgegevens',
  '2021',
  'partiel',
  'PDF25 pages ; p.1-3 lues. Amende2,75M€ pour trois usages illégaux de nationalité, dont classement de risque. '
  "Pas de l'IA générative ni un coût total du scandale."),
 ('09_S21',
  '09_horizon2025_rapport',
  'Horizon ITI nquiry, Final Report Volume 1, accessibleversion',
  'UK Post Office Horizon IT Inquiry',
  '2025-07',
  'partiel',
  'PDF réel466 pages ; p.7-10,§1.2-1.7 lus. Pertes comptables fictives et gouvernance. La page de téléchargement '
  "indique166 pages ; le fichier accessible en contient466. Volume1, pas toute l'enquête."),
 ('09_S22',
  '09_robodebt_pm2023',
  'Publication et conclusions du rapport Robodebt',
  'Prime Minister Australia',
  '2023-07-07',
  'integral',
  'Déclaration officielle ouverte, reproduisant la conclusion de la Royal Commission p.xxix. Rapport complet '
  'inaccessible sur les sites testés ; aucune prétention de lecture intégrale.'),
 ('09_S23',
  '09_robodebt_officiel',
  'Tentative rapport Robodebt',
  'Royal Commission Australia',
  '2023-07-07',
  'inaccessible',
  'Connexion fermée et rapport non lu. La source ouverte de substitution est la déclaration officielle09_S22, '
  'dont la portée est précisée.'),
 ('09_S24',
  '09_midas2017',
  'Tentative bilan administratif Mi DAS',
  'Michigan LEO/UIA',
  '2017-08-11',
  'inaccessible',
  "HTTP403. L'arrêt primaire09_S19 a été ouvert pour la portée juridique. Le chiffre médiatique de93% n'est pas "
  'retenu sur un seul extrait de recherche.'),
 ('09_S25',
  '09_scribes_rct2026',
  'Tentative texte complet du RCT publié',
  'PMC/NEJMAI',
  '2026',
  'inaccessible',
  "HTTP200 renvoyant un défi navigateur, pas l'article. Résumé primaire API09_S17 et prépublication09_S16 "
  'conservés séparément.'),
 ('09_S26',
  '09_justice_choi2024',
  'Lawyering in the Age of Artificial Intelligence',
  'Choi, Monahan, Schwarcz/Minnesota Law Review',
  '2024',
  'inaccessible',
  "Publication repérée mais PDF403. Aucun chiffre de cette étude n'est promu en fait ou utilisé pour calibrer la "
  'justice publique.'),
 ('09_S27',
  '09_justice_guidance2025',
  'Artificial Intelligence : Judicial Guidance October 2025',
  'Courts and Tribunals Judiciary',
  '2025-10',
  'partiel',
  "Page primaire de publication ouverte. Guide d'usage judiciaire, pas mesure quantitative de productivité ou "
  "d'effectifs des juridictions. PDF lié non revendiqué lu.")]


def write(path,rows):
    keys=list(dict.fromkeys(k for r in rows for k in r))
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(rows)


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    registry=[];manifest=[]
    for id_,alias,title,inst,date,access,notes in SOURCES:
        folder=ROOT/"data/raw/09" if alias.startswith("RAW:") else CACHE
        alias=alias.removeprefix("RAW:")
        m=json.loads((folder/(alias+".meta.json")).read_text(encoding="utf-8"))
        if "raw_path" not in m and (folder/(alias+".json")).exists():
            m["raw_path"]=str((folder/(alias+".json")).relative_to(ROOT))
        registry.append(dict(id=id_,titre=title,institution=inst,date_publication=date,url=m["source_url"],date_consultation="2026-10-28",acces=access,sha256_16=m.get("sha256","")[:16],notes=notes))
        manifest.append(dict(id=id_,lecture_effective=access,passages_et_limites=notes,**m))
    sr={r["id"]:r for r in registry};rows=[]
    def add(id_,study,metric,value,unit,period,scope,method,sid,loc,limit,status="FAIT"):
        rows.append(dict(id=id_,etude=study,indicateur=metric,valeur=value,unite=unit,annee=period,champ=scope,nature_preuve=method,source_url=sr[sid]["url"],source_localisation=loc,statut=status,limites=limit,etp_supprimes_observes=None,economie_publique_nette_observee=None))
    records=[
      ("01","Brynjolfsson–Li–Raymond","Échantillon",5172,"agents de support clientèle","publication QJE2025","Une entreprise logicielle","quasi_experience_DID","09_S01","PDF p.1,3-4","Versions antérieures à5179 agents et14% distinctes de la publication finale."),
      ("02","Brynjolfsson–Li–Raymond","Productivité moyenne",15,"% de dossiers résolus par heure","publication QJE2025","Assistance aux tâches de support clientèle","quasi_experience_DID","09_S01","PDF p.1,3 et19, tableauII","Pas15% de temps sur tout le poste. Effets hétérogènes selon expérience et compétence."),
      ("03","Brynjolfsson–Li–Raymond","Novices et faible compétence initiale",30,"% de dossiers résolus par heure","publication QJE2025","Sous-groupe de la version publiée","heterogeneite_DID","09_S01","PDF p.3","Ne pas généraliser l'effet des novices aux experts, ni reprendre34% d'une ancienne version."),
      ("04","Noy–Zhang","Échantillon final",453,"professionnels diplômés","2023","Tâches rédactionnelles de20-30 minutes, GPT3.5","experience_randomisee","09_S02","PDF p.1,3","Le premier préprint de mars2023 comporte444 participants ; versions distinctes."),
      ("05","Noy–Zhang","Réduction du temps",40,"% du temps par tâche","2023","Rédaction professionnelle, plateforme Prolific","experience_randomisee","09_S02","PDF p.1,4","Expérience en ligne, pas tout le temps de travail. Durées et réductions publiées arrondies."),
      ("06","Noy–Zhang","Qualité",18,"% de la note de qualité","2023","Évaluation aveugle par des professionnels","experience_randomisee","09_S02","PDF p.1,3-4","Variation de note, ni production nationale ni économie nette."),
      ("07","Dell'Acqua et al.","Échantillon",758,"consultants BCG","expérience2023, publication2026","Sous-échantillons385 et373 selon tâche","experience_randomisee","09_S04","PDF p.2,5,12","758 n'est pas le nombre de participants à chaque type de tâche."),
      ("08","Dell'Acqua et al.","Réduction du temps dans la frontière",25.1,"% de temps sur les tâches","expérience2023, publication2026","18 tâches réalistes dans les capacités de GPT-4","experience_randomisee","09_S04","PDF p.2 et11, tableau6","Temps pour atteindre la tâche finale en conditions expérimentales professionnelles."),
      ("09","Dell'Acqua et al.","Tâches supplémentaires",12.2,"% du nombre de tâches réalisées","expérience2023, publication2026","Dans la frontière technique","experience_randomisee","09_S04","PDF p.2,9","Quantité et temps sont deux mesures distinctes ; ne pas additionner leurs effets."),
      ("10","Dell'Acqua et al.","Bonnes réponses hors frontière",-19,"points de pourcentage environ","publication2026","Conseil stratégique, n373 ; contrôle84,5%, groupes IA60% et70,6%","experience_randomisee","09_S04","PDF p.12, tableau7 et texte","Le corps précise des points ; l'abstract dit19% de manière ambiguë. Garder la définition du texte."),
      ("11","Humlum–Vestergaard","Répondants environ",25000,"travailleurs","enquête fin2024, révision mars2026","Danemark,11 professions et7000 lieux de travail","enquete_liee_registres_DID","09_S05","PDF p.3,11","Pas des données françaises ni une observation après2024."),
      ("12","Humlum–Vestergaard","Borne d'effet moyen écartée",2,"% sur heures et revenus environ","données jusqu'à décembre2024","Intervalles des estimations autour de zéro","enquete_liee_registres_DID","09_S05","PDF p.2,5","Résultat sur les moyennes enregistrées ; ne signifie pas zéro gain de tâche ni absence d'effet futur."),
      ("13","METR2025","Développeurs",16,"développeurs expérimentés","février-juin2025","Environ5 ans d'expérience sur leurs propres projets","experience_randomisee_taches","09_S06","PDF p.1-2","Petit échantillon de spécialistes de projets complexes ; pas tous les développeurs."),
      ("14","METR2025","Tâches",246,"tâches","février-juin2025","Maintenance de projets open source connus","experience_randomisee_taches","09_S06","PDF p.1-2","Assignation autorisant ou non l'IA, notamment Cursor et Claude3.5/3.7."),
      ("15","METR2025","Variation mesurée du temps",19,"% de temps supplémentaire","février-juin2025","Intervalle[+2;+39]%","experience_randomisee_taches","09_S06","PDF p.1-2, figure1","Ralentissement dans ce contexte ; pas une constante de l'IA disponible en2026."),
      ("16","METR2025","Temps estimé après expérience",-20,"% de temps selon les participants","2025","À comparer à l'effet mesuré de+19%","perception_post_experience","09_S06","PDF p.1-2","Dissonance entre perception et mesure ; pas démonstration d'une surestimation universelle."),
      ("17","METR suite2026","Point chez les anciens participants",-18,"% de temps, IC[-38;+9]","suite fin2025, publication février2026","Sous-échantillon des anciens développeurs","experience_selection_forte","09_S07","Raw results et limitations","Les auteurs jugent le signal peu fiable ; sélection des personnes/tâches et IC incluant zéro."),
      ("18","METR suite2026","Point chez les nouveaux participants",-4,"% de temps, IC[-15;+9]","suite fin2025, publication février2026","Nouveaux développeurs","experience_selection_forte","09_S07","Raw results et limitations","Ne valide pas un coefficient prévisionnel généralisé de18% ou4%."),
      ("19","Copilot GDS britannique","Licences",20000,"agents dotés d'une licence","30/09-31/12/2024, rapport2025","Essai intergouvernemental","deploiement_enquete","09_S08","§1.1 et2.2","Licences, répondants et utilisateurs actifs ont des dénominateurs distincts."),
      ("20","Copilot GDS britannique","Répondants",7115,"réponses","rapport2025","Enquête de fin d'essai","enquete","09_S08","§3, méthode","Les journaux d'usage sont disponibles pour14500 utilisateurs ; ne pas confondre les populations."),
      ("21","Copilot GDS britannique","Temps gagné déclaré",26,"minutes par jour","rapport2025","Moyenne de milieux de classes de l'enquête","autodeclaration","09_S08","§4.4, time savings","Ni chronométrage causal ni13 jours de rémunération évitée observés ; temps réaffecté non identifié."),
      ("22","Copilot DBT","Licences",1000,"licences","octobre-décembre2024","70% volontaires et30% pour la représentation","pilote_sans_contrefactuel_principal","09_S09","PDF p.4","Une attribution aléatoire partielle des licences ne transforme pas l'évaluation principale en RCT de productivité."),
      ("23","Copilot DBT","Journaux consentis",300,"journaux","octobre-décembre2024","312 soumis,300 consentis, taux de réponse32%","autodeclaration_ajustee","09_S09","PDF p.4 et29-30, méthode des journaux","1411 observations de tâches ; biais de réponse et temps sans IA estimé."),
      ("24","Copilot DBT","Synthèse/recherche : temps gagné ajusté",.8,"heure gagnée par tâche, déclarée","2024, rapport2025","Ajustement des productions inutilisées et tâches nouvelles","autodeclaration_ajustee","09_S09","PDF p.29, tableau5","Ni moyenne quotidienne ni économie annuelle sans fréquence de tâches."),
      ("25","Copilot DBT","Planification : temps gagné ajusté",-.6,"heure gagnée par tâche, déclarée","2024, rapport2025","Temps supplémentaire de planification","autodeclaration_ajustee","09_S09","PDF p.29, tableau5","Valeur défavorable conservée, sans troncature à zéro."),
      ("26","DTA Australie","Réponses à l'enquête finale",831,"réponses","essai2024","Plus de2000 contributeurs et50 agences","enquete_non_aleatoire","09_S10","PDF p.15-16","Sélection volontaire, versions et contextes différents ; pas un essai randomisé."),
      ("27","DTA Australie","Managers percevant une amélioration",64,"% des managers répondants","2024","Efficience et qualité perçues","autodeclaration","09_S10","PDF p.5","Perception, pas démonstration de64% de temps gagné."),
      ("28","DTA Australie","Réaffectation de temps déclarée",40,"% des participants","2024","Participants déclarant réaffecter le temps vers des tâches de plus grande valeur","autodeclaration","09_S10","PDF p.5","Ni40% du temps ni40% d'emplois évitables."),
      ("29","Turing","Transactions complexes répétitives",143000000,"transactions par an environ","estimation2024","Sous-ensemble d'environ1 milliard de transactions et400 services centraux UK","estimation_potentiel_transactions","09_S11","PDF p.1, résumé","Volume estimé, pas automatisation observée."),
      ("30","Turing","Transactions potentiellement automatisables",84,"% des143 millions de transactions complexes","estimation2024","Pas toutes les transactions ni le personnel","classification_potentiel","09_S11","PDF p.1, résumé","Temps initial, fiabilité et mise à l'échelle manquants pour une économie budgétaire."),
      ("31","OIT/NASK","Emplois présentant une exposition",25,"% de l'emploi mondial environ","indice2025","Environ un quart dans des occupations exposées","indice_exposition","09_S12","Résumé primaire","Pas25% d'emplois supprimables ; transformation plus probable que substitution intégrale."),
      ("32","OIT/NASK","Gradient maximal",3.3,"% de l'emploi mondial","indice2025","Gradient4","indice_exposition","09_S12","Résumé primaire","Cotation de tâches ; pas observation de suppressions d'emplois."),
      ("33","OIT/NASK","Exposition dans les pays à haut revenu",34,"% de l'emploi de ces pays","indice2025","Tous gradients","indice_exposition","09_S12","Résumé primaire","Ni fraction d'heures ni mesure propre à la fonction publique française."),
      ("34","NAO","Répondants",87,"organismes publics","enquête2023, rapport2024","Royaume-Uni","audit_enquete","09_S14","PDF p.10","Organismes répondants, pas nombre de salariés."),
      ("35","NAO","Organismes ayant déployé l'IA",37,"% des organismes répondants","rapport2024","IA au total, typiquement1-2 cas d'usage","audit_enquete","09_S14","PDF p.6,10","70% pilotent/prévoient ; groupes chevauchants. Ni IA générative seule ni gains mesurés."),
      ("36","OCDE","Cas analysés",200,"cas d'usage","2025","11 fonctions gouvernementales","inventaire_descriptif","09_S15","PDF p.11 et chapitre3 p.60","Pas200 RCT ; sélection des cas, contextes et niveaux de preuve hétérogènes."),
      ("37","Scribes RCT","Médecins",238,"médecins","novembre2024-janvier2025, publication2025/26","14 spécialités et3 groupes randomisés","RCT_pragmatique","09_S17","Résumé publié, Methods et Results, API primaire","Résumé publié lu ; texte publié complet bloqué. Méthodes accessibles dans la prépublication distincte."),
      ("38","Scribes RCT Nabla","Réduction du temps de note",9.5,"% du temps de note","2024-2025","IC95% du gain[1,8;17,2]","RCT_pragmatique","09_S17","Résumé publié, Results","Pas9,5% de la journée ou des médecins. Erreurs occasionnelles nécessitant un contrôle."),
      ("39","Scribes RCT DAX","Réduction du temps de note",1.7,"% du temps de note","2024-2025","IC95% du gain[-5,9;+9,4]","RCT_pragmatique","09_S17","Résumé publié, Results","Effet non significatif et possibilité de ralentissement ; pas effet exactement nul."),
      ("40","Scribes RCT","Usage Nabla",29.5,"% des23653 visites","2024-2025","Bras Nabla","adoption_dans_RCT","09_S17","Résumé publié, Results","Adoption incluse dans les mécanismes de l'essai ; ne pas multiplier encore l'effet sans définir son estimand."),
      ("41","Police","Policiers de l'essai",85,"policiers","étude2024","Manchester, New Hampshire ; DraftOne","experience_randomisee","09_S18","Résumé et méthode RMS","Pas Utah. Qualité juridique et temps d'audience non évalués par la durée RMS."),
      ("42","Police","Rapports de l'essai",755,"rapports","étude2024","6084 rapports dans le contrôle de robustesse annuel DID","experience_randomisee","09_S18","Résumé et résultats","Absence d'amélioration significative de durée ; ne prouve pas zéro effet partout."),
      ("43","Toeslagen","Amende de l'autorité",2.75,"M€ de sanction","2021","Traitements illégaux de nationalité, risque et double nationalité","decision_autorite_controle","09_S20","PDF p.1-3","Sanction constatée, pas coût total du système. Pas de l'IA générative."),
    ]
    for n,st,metric,v,u,y,ch,method,sid,loc,limit in records:add("09_F"+n,st,metric,v,u,y,ch,method,sid,loc,limit)
    write(OUT/"09_etudes_chiffres.csv",rows)

    # Cas de risques : ne pas substituer les chiffres médiatiques aux constatations réellement ouvertes.
    risks=[]
    for id_,name,sid,loc,tech,finding,limit in [
      ("09_R01","Robodebt","09_S22","Déclaration officielle7 juillet2023, reproduisant le rapport p.xxix","Automatisation administrative antérieure aux LLM","Le gouvernement relaie la conclusion de la Royal Commission : illégalité et échec humain et économique","Rapport complet inaccessible. Aucun coût total ou taux de faux positifs extrait. La source ouverte est une déclaration officielle, pas le rapport intégral."),
      ("09_R02","Toeslagen","09_S20","PDF p.1-3","Bases de données, classement de risque et pratiques institutionnelles","Autorité de protection des données : traitements illégaux de nationalité, dont indicateur de risque ; sanction de2,75M€","Scandale combinant légalité, données, recours et pratiques. Ne pas attribuer tout le dommage à un modèle unique ou à l'IA générative."),
      ("09_R03","MiDAS","09_S19","PDF p.1-4 et12","Automatisation du déclenchement de fraude et du recouvrement","Cour : action constitutionnelle indemnitaire possible au vu des allégations ; renvoi pour poursuite de la procédure","Faits tenus pour vrais au stade du contrôle de recevabilité p.12. Ni audit de93% d'erreurs ni jugement définitif de tous les faits dans cet arrêt."),
      ("09_R04","Horizon","09_S21","PDF p.7-10, §1.2-1.7","Logiciel comptable, infrastructure et gouvernance antérieurs aux LLM","L'enquête retient des défauts produisant des pertes comptables fictives et leur utilisation comme présomption de détournement","Volume1 : réparation et impact humain. Lecture des passages cités, pas des466 pages. Aucune fréquence probabiliste future d'échec de l'IA générative déduite."),
    ]:
        risks.append(dict(id=id_,cas=name,annee="dates des sources2021-2025",technologie=tech,constat=finding,limites=limit,cout_total_echec=None,source_url=sr[sid]["url"],source_localisation=loc,statut="FAIT",indicateurs_a_suivre="faux positifs ; notification ; recours ; erreurs corrigées ; délais ; coût de validation ; réparations ; traçabilité"))
    write(OUT/"09_echecs_et_garde_fous.csv",risks)

    params=[]
    for id_,task,unit,lo,mid,hi,sid,loc,kind,reason in [
      ("09_P01","Rédaction professionnelle courte, Noy","fraction de temps économisé",None,.40,None,"09_S02","PDF p.1-4","POINT_RCT_CONTEXTE_LOCAL","Pas d'intervalle exploitable pour trois scénarios. GPT3.5, tâches de20-30 minutes, pas une activité annuelle complète."),
      ("09_P02","Conseil dans la frontière, Dell'Acqua","fraction de temps économisé",None,.251,None,"09_S04","PDF p.2 et11","POINT_RCT_CONTEXTE_LOCAL","Aucune distribution de prévision pour la France. Hors frontière, baisse d'environ19 points de bonnes réponses. Le contrôle peut absorber du temps."),
      ("09_P03","Support clientèle, Brynjolfsson","taux de productivité en dossiers par heure",None,.15,None,"09_S01","PDF p.1,3 et19","POINT_DID_CONTEXTE_LOCAL","15% de productivité ne signifie pas15% de temps. Équivalent conditionnel à production fixe :1-1/1,15 ; calcul séparé."),
      ("09_P04","Code connu, outils février-juin2025, METR","fraction de temps économisé",-.39,-.19,-.02,"09_S06","PDF p.1-2 ; intervalle repris dans la suite2026","SENSIBILITE_STATISTIQUE_EXPERIENCE_PAS_PREVISION","Bornes de l'effet local. Gain négatif : ralentissement. La suite2026 signale changement technique, sélections et difficultés de mesure."),
      ("09_P05","Note clinique, Nabla","fraction du temps de note économisé",.018,.095,.172,"09_S17","Résumé publié, Results, IC95%","SENSIBILITE_STATISTIQUE_EXPERIENCE_PAS_PREVISION","Bornes d'IC, pas trois prévisions budgétaires. L'effet est mesuré dans l'adoption de l'essai. Contrôle des erreurs nécessaire ; médecins ambulatoires US."),
      ("09_P06","Note clinique, DAX","fraction du temps de note économisé",-.059,.017,.094,"09_S17","Résumé publié, Results, IC95%","SENSIBILITE_STATISTIQUE_EXPERIENCE_PAS_PREVISION","IC incluant une dégradation et zéro ; effet non significatif. Aucun poste entier déduit. La borne défavorable reste visible."),
      ("09_P07","Copilot généraliste britannique","minutes par jour autodéclarées",None,26,None,"09_S08","§4.4","POINT_ENQUETE_PAS_CALIBRATION_CAUSALE","7115 réponses, milieux de classes. Ni durée effective tracée de manière causale ni fréquence de tâche stable pour une extrapolation française."),
      ("09_P08","Synthèse/recherche, Copilot DBT","heure gagnée par tâche, déclarée",None,.8,None,"09_S09","PDF p.29, tableau5","POINT_ENQUETE_AJUSTEE","Temps sans IA estimé ; production non utilisée et tâches nouvelles ajustées. Aucune preuve de productivité globale dans le rapport p.5."),
      ("09_P09","Planification, Copilot DBT","heure gagnée par tâche, déclarée",None,-.6,None,"09_S09","PDF p.29, tableau5","POINT_ENQUETE_AJUSTEE","Temps supplémentaire et tâches parfois nouvelles. Résultat défavorable conservé ; pas une référence causale pour la France."),
      ("09_P10","Copilot généraliste australien","fraction de temps économisé",None,None,None,"09_S10","PDF p.5 et15-16","NON_TROUVE","Temps perçus sur certaines tâches et échantillon volontaire. Aucun ratio annuel causal pouvant être calibré."),
      ("09_P11","Transactions publiques britanniques, Turing","fraction de temps économisé",None,None,None,"09_S11","PDF p.1","NON_TROUVE","84% classe le potentiel de143 millions de transactions. Aucun temps uniforme observé ; une minute gagnée est une illustration hypothétique."),
      ("09_P12","Police, DraftOne","fraction de temps économisé",None,None,None,"09_S18","Résumé et résultats","NON_TROUVE","Une absence d'effet significatif ne fixe pas le gain exact à zéro. Pas de distribution transportable à la police française."),
      ("09_P13","Emploi et heures totales, Humlum","taux de postes supprimables",None,None,None,"09_S05","PDF p.2-5","NON_TROUVE","Effet moyen nul et précis sur revenus/heures au Danemark jusqu'à2024. Ni taux français ni garantie sur l'avenir."),
      ("09_P14","Emplois exposés, OIT","taux de postes supprimables",None,None,None,"09_S12","Résumé primaire","NON_TROUVE","Exposition partielle des tâches et automatisation du poste sont distinctes. Les25%,3,3% et34% mesurent d'autres objets."),
      ("09_P15","Justice publique","fraction du temps de tâche économisé",None,None,None,"09_S27","Page de publication du guide","NON_TROUVE","Guide d'usage sans mesure causale de capacité des juridictions. Choi2024 repéré mais PDF403 ; aucun résultat non lu n'est utilisé."),
    ]:
        params.append(dict(parametre_id=id_,tache=task,unite=unit,prudent=lo,central=mid,ambitieux=hi,annee="versions2023-2026",type_calibration=kind,statut="NON_TROUVE" if kind=="NON_TROUVE" else "HYPOTHESE_DE_TRANSPORT_NON_VALIDEE",raison_et_limites=reason,part_temps_tache_dans_poste=None,adoption_cible=None,conversion_temps_en_etp=None,cout_net_national=None,source_url=sr[sid]["url"],source_localisation=loc,usage_modele_national="NON_ETAYE_SANS_TEST_LOCAL_COUTS_ET_CONVERSION"))
    write(OUT/"09_parametres_taches.csv",params)

    # Quelques calculs explicites, séparés des mesures publiées.
    derived=[
      dict(id="09_C01",indicateur="Temps conditionnel équivalent à+15% de productivité",valeur=1-1/1.15,unite="fraction du temps",annee="calcul sur QJE2025",formule="1-1/(1+0,15)",source_url=sr["09_S01"]["url"],source_localisation="PDF p.1",statut="ESTIMATION",note="À production et qualité fixes, sans tâche nouvelle. Aucune baisse budgétaire observée déduite."),
      dict(id="09_C02",indicateur="Transactions Turing classées potentiellement automatisables",valeur=143e6*.84,unite="transactions/an",annee="calcul sur étude2024",formule="143000000*0,84",source_url=sr["09_S11"]["url"],source_localisation="PDF p.1",statut="ESTIMATION",note="120,12 millions potentielles, à partir de volumes arrondis. Ne signifie pas des transactions automatisées en production."),
      dict(id="09_C03",indicateur="DBT PowerPoint : gain relatif du temps seul",valeur=1-(10*60+47)/(18*60+30),unite="fraction du temps",annee="pilote2024",formule="1-647/1110",source_url=sr["09_S09"]["url"],source_localisation="PDF p.31, tableau6",statut="ESTIMATION",note="Plus rapide mais exactitude1,5/5 contre5/5 et qualité1/5 contre2/5. Pas un gain démontré à qualité constante."),
    ]
    write(OUT/"09_calculs_controles.csv",derived)
    # Le résumé publié primaire de l'essai clinique est un JSON, pas une page de défi navigateur.
    j=json.loads((ROOT/"data/raw/09/09_scribes2026_abstract.json").read_text(encoding="utf-8"))
    result=j["resultList"]["result"][0]
    assert "9.5%" in result["abstractText"] and "238" in result["abstractText"] and result["firstPublicationDate"]=="2025-11-26"
    assert all(r["cout_net_national"] is None for r in params)
    assert all(r["acces"] == "inaccessible" or len(r["sha256_16"]) ==16 for r in registry)
    write(ROOT/"sources/registre_09.csv",registry)
    (ROOT/"data/raw/09/09_manifestes_sources.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps({"constats":len(rows),"cas_risques":len(risks),"parametres_taches":len(params),"sources":len(registry),"chiffrage_national":"aucun"},ensure_ascii=False))


if __name__=="__main__":main()
