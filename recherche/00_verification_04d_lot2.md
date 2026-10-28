# Contre-vérification du volet 04d — territoires et fonctions support

Contrôle arrêté au **28 octobre 2026**. Note examinée : `recherche/04d_territoires_fonctions_support.md`, rédigée par un autre agent. Le vérificateur n'a pas participé à sa rédaction et n'a ni importé ni exécuté `scripts/04d_territoires_support.py`. Il a relu directement les sources primaires archivées : cellules DGCL, CSV SDMX WOFI, pages des PDF Ravignon/Sénat/DAE et page parlementaire de procédure. Cette indépendance de lecture **ne constitue pas une seconde observation statistique indépendante**.

## Résultat

**[FAIT de contrôle] Les 15 ensembles de chiffres contrôlés sont confirmés sur le plan numérique. Une formulation de périmètre a été corrigée par l'auteur de la note après signalement.** Aucun montant erroné restant à corriger n'a été identifié dans cet échantillon. La confirmation de la transcription ne transforme pas les estimations ou hypothèses des sources en économies budgétaires observées.

Les références de pages distinguent le numéro de page du fichier PDF et la pagination imprimée. L'unité et les réserves de champ sont détaillées dans `data/risques/verification_04d_lot2.csv`.

| Contrôle | Affirmation examinée | Lecture du primaire | Résultat |
|---|---|---|---|
| V04d_01 | 34 875 communes au 1/1/2026 | DGCL, `2.2 nb CL!F8`, année F5 ; 34 746 métropole +129 outre-mer | Confirmé |
| V04d_02 | 1 252 EPCI à fiscalité propre | DGCL, `2.5a EPCI!F9` ; 21+14+230+987 ; Lyon distinct F10 ; 34 871 communes regroupées et 4 isolées | Confirmé |
| V04d_03 | WOFI : 90 observations, année 2020 seulement | Toutes les valeurs TIME_PERIOD du CSV primaire valent2020, malgré la requête jusqu'à 2026 | Confirmé |
| V04d_04 | France WOFI : 34 955 municipalités | FRA, MUN, SNGU, UNIT_MULT0, année 2020 | Confirmé |
| V04d_05 | Taille moyenne française1 927,95 habitants | MUN_SIZE=1 927,952568, opération MEAN, unité PS ; arrondi exact | Confirmé |
| V04d_06 | Ravignon : 178 collectivités/groupements, dont 11 intercommunalités, et 54 services État | PDF p.43, imprimée36 : 155 communes+11 groupements+9 départements+3 régions ; opérateurs non interrogés | Confirmé comme méthode d'estimation |
| V04d_07 | Enchevêtrement7,444 Md€ | PDF p.45-46, imprimées38-39, tableau 10 : total7 443 997 405 € | Confirmé comme estimation externe |
| V04d_08 | RH : 31 040+13 600=44 640 agents | PDF p.96, imprimée89 ; métiers et total du tableau 25 p.98 | Confirmé ; ETP non établi |
| V04d_09 | Texte RH2 047,3 M€ et tableau 25 à 1 432,7 M€ | PDF p.97-98, imprimées90-91 : trois coûts376,7+463,5+592,5 ; écart614,6 M€ | Confirmé après correction de périmètre |
| V04d_10 | Gains RH5 % et 10 %, soit 102,4 et 204,7 M€ | PDF p.100, imprimée93, tableau 26 ; calcul arrondi sur 2 047,3 M€ | Confirmé comme hypothèses externes |
| V04d_11 | Support opérateurs2,7 Md€ et réduction20 %=540 M€ | Sénat PDF p.231 ; base estimée avec ratio10 %, hors interventions, universités et centres de recherche | Confirmé comme hypothèses externes |
| V04d_12 | DAE 412,53 M€ d'économies achats en 2025 | DAE PDF p.87 : somme indépendante des 12 contributions ; p.86 : volumes estimés et distinction économies budgétaires | Confirmé, concept non budgétaire préservé |
| V04d_13 | Achats50,245 Md€ dont 24,364 hors D&S et 25,881 D&S | DAE PDF p.46, graphique et tableau ; identité additive confirmée | Confirmé, dépenses et performance distinctes |
| V04d_14 | Loi2026-795 du18 août2026 | Page Sénat « La loi en clair », titre et chronologie de promulgation | Confirmé sur l'état de procédure |
| V04d_15 | Immobilier :20 millions m², −25 % d'ici2032,5 millions m²,1 Md€/an à terme | Sénat PDF p.217, dont la moitié en baux et la moitié en cessions ; estimation gouvernementale rapportée | Confirmé comme objectif et estimation historiques |

Sources exactes : [DGCL, chapitre 2 du millésime 2026](https://www.collectivites-locales.gouv.fr/files/files/Etudes-et-statistiques/DESL/2026/CLC/Chapitre%202%20-%20Les%20collectivit%C3%A9s%20locales%20et%20leur%20population-2026.xlsx), [OCDE WOFI, requête primaire2020-2026](https://sdmx.oecd.org/public/rest/v1/data/OECD.CFE.RDG,DSD_SNG_WOFI@DF_SNG_STRUCT,1.0/FRA+DEU+ITA+ESP+PRT+BEL+NLD+CHE+AUT+GBR+IRL+SWE+DNK+NOR+FIN+POL+EST+CAN+USA+AUS+NZL+JPN+KOR....MUN+SUB+REG+MUN_SIZE....?startPeriod=2020&endPeriod=2026), [Ravignon, rapport primaire](https://presse.economie.gouv.fr/download?n=1900%20-%20Rapport%20de%20Boris%20Ravignon%20sur%20le%20co%C3%BBt%20du%20millefeuille%20administratif-pdf&id=132915), [Sénat rapport 807, tome1](https://www.senat.fr/rap/r24-807-1/r24-807-11.pdf), [DAE rapport d'activité2025](https://www.economie.gouv.fr/files/files/directions_services/dae/media-document/Rapport_activite_2025_en_telechargement.pdf), [Sénat, loi de foncière](https://www.senat.fr/travaux-parlementaires/textes-legislatifs/la-loi-en-clair/proposition-de-loi-visant-a-moderniser-la-gestion-du-patrimoine-immobilier-de-letat.html).

## Correction coordonnée du périmètre RH

La synthèse initiale indiquait que le texte chiffrait une **« base élargie à 2 047,3 M€ »**. Or le paragraphe de la page97 publie ce coût sans expliciter l'inclusion exacte du CNFPT/CDG. La page96 ajoute bien13 600 agents aux31 040 agents des collectivités, mais cela ne suffit pas à démontrer le périmètre du montant2 047,3 M€. Le tableau 25 de la page98 donne1 432,7 M€, et son titre apparaît effectivement tronqué sur le rendu visuel du PDF. Aucun complément de titre n'a été inventé.

La réserve a été signalée à l'auteur, qui a modifié le **point 9 de synthèse, le tableau des indicateurs, l'analyse et ses données dérivées** : le chiffre est désormais présenté comme un **coût publié dans le texte, dont le raccordement au tableau 25 et l'inclusion exacte du CNFPT/CDG ne sont pas reconstitués**. La rédaction finale du point 9, du tableau et de l'analyse a été relue. Le contrôle V04d_09 porte le statut **CONFIRME_APRES_CORRECTION**, avec la formulation initiale et la correction conservées dans sa note. Aucun montant n'a été modifié par le vérificateur.

## Portée et limites

- Les cellules DGCL donnent des **institutions**, sans effectif de personnel. Le champ Lyon et les communes regroupées sont vérifiés, sans déduire qu'une coopération juridique implique une mutualisation complète.
- WOFI est confirmé dans les dimensions et l'année diffusées par la source. Ce contrôle ne reconstitue pas une population ou une compétence comparable à partir d'une taille moyenne municipale, et ne prétend pas disposer de valeurs2026.
- Les coûts Ravignon restent des **valorisations extrapolées**. Le montant global contient de la coordination nécessaire et des sous-lignes, dont patrimoine/RH/finances et relations DGFiP ; les sommes ne peuvent être additionnées une seconde fois. Le présent contrôle ne valide ni la représentativité ni un taux national d'économie.
- Les5 %/10 % RH et 20 % support sont bien des **hypothèses des sources**. Leur arithmétique est confirmée ; leur réalisation ou leur caractère net de la transition ne le sont pas.
- Les pages46 et 87 du rapport DAE et les tableaux Ravignon ont aussi été inspectés visuellement. L'extraction pypdf signale une dépendance de police CFF optionnelle absente dans le Python système ; les chiffres décisifs des tableaux ont donc été rapprochés de leur rendu, sans assimiler un avertissement de police à une erreur statistique.
- La date de promulgation est vérifiée dans une page primaire parlementaire. L'accès Légifrance403 et l'absence de lecture intégrale de la loi restent explicitement signalés dans la note 04d ; le contrôle ne les transforme pas en lecture juridique exhaustive.
- Le1 Md€/an immobilier est une **estimation gouvernementale ancienne rapportée au Sénat**, pas une réalisation2026 ni une économie additionnelle entièrement disponible. Le statut institutionnel de la foncière, les loyers internes, les cessions et les coûts de transition doivent rester séparés avant calibration.

## Reproduction

Commande : `python -I scripts/00_verification_04d_lot2.py` avec `openpyxl` et `pypdf`. Le script relit les fichiers primaires archivés et produit les 15 lignes du CSV. Il ne modifie pas la note auditée, ne lit pas les CSV analytiques04d et n'exécute pas le script auteur. `valeur_publiee` désigne l'affirmation de la note auditée ; `valeur_source` désigne la lecture directe ou le calcul de contrôle à partir du primaire.

Les vérifications sont ciblées sur les chiffres décisifs demandés, sans prétendre à un audit exhaustif de toutes les données du volet.
