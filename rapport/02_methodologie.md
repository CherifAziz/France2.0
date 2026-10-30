# 2. Méthodologie, définitions et limites

## 2.1 Question et démarche

La mission répond à une question précise : **combien de postes et combien de milliards d'euros la France pourrait-elle réellement économiser en réorganisant, simplifiant et automatisant ses administrations, à qualité de service comparable, et que faudrait-il changer concrètement ?**

Le travail a suivi six phases, dans l'ordre imposé par le cahier des charges : données (lot 1), diagnostic par fonction (lot 2), étude des réformes, des doublons, de la simplification et de l'IA (lot 3), chiffrage par un modèle ascendant (phases 3-4), contre-expertise (phase 5), puis rédaction. **Aucun objectif de suppressions n'a servi de point de départ** : les totaux résultent des fiches de réforme, et non l'inverse.

## 2.2 Protocole de preuve

Chaque affirmation chiffrée porte un statut, défini dans le [protocole commun](../recherche/00_PROTOCOLE.md) :

- **[FAIT]** : valeur lue dans une source primaire identifiée, avec page, tableau ou cellule ;
- **[EXTRAIT]** : valeur vue dans un extrait ou une recension, non relue dans l'original ;
- **[ESTIMATION]** : calcul reproductible à partir de faits, avec sa formule ;
- **[HYPOTHÈSE]** : paramètre choisi par la mission, justifié par un précédent mais non mesuré ;
- **[NON TROUVÉ]** : donnée cherchée et absente des sources accessibles. Une case vide documentée est préférée à un chiffre inventé.

Les sources primaires sont téléchargées et archivées avec leur URL, leur date de consultation et leur empreinte SHA-256 (`sources/registre_*.csv`). Un document qui n'a pas pu être ouvert n'est jamais présenté comme lu : c'est le cas, par exemple, du texte intégral du livre « Le Casse du siècle », du rapport 2023 de la CNEN ou du texte opposable de l'AI Omnibus.

## 2.3 Contre-vérifications

Quatre contre-vérifications indépendantes ont relu **308 chiffres** dans leurs sources primaires, sans réutiliser les scripts d'extraction des auteurs : 100 au lot 1, 63 au lot 2, 98 au lot 3 et 47 en phase 5. Aucune n'a laissé d'écart numérique non corrigé ; les corrections apportées (arrondis, formulations, localisations) sont tracées. Une seconde lecture d'un même document vérifie la transcription ; elle ne constitue pas une seconde mesure statistique indépendante. Le détail est au chapitre 17.

## 2.4 Définitions

| Notion | Définition retenue | Piège évité |
|---|---|---|
| Fonction publique (FP) | Agents des trois versants (État, territoriale, hospitalière) au sens de la DGAFP : 5 848 291 personnes fin 2024, hors contrats aidés | Confondre FP et administrations publiques (S13) |
| Administrations publiques (S13) | Secteur des comptes nationaux, incluant des organismes de droit privé non marchands : 6 531 025 salariés à titre principal fin 2024 | Comparer S13 d'un pays à FP d'un autre |
| Personnes physiques (PP), ETP, EQTP, ETPT | PP : personnes présentes à une date ; ETP/EQTP : volumes de travail ; ETPT : unité budgétaire annuelle | Additionner ou soustraire des unités différentes |
| Emploi administratif | Filières et corps administratifs (et techniques pour l'État), organismes de gestion de la protection sociale, France Travail | Assimiler tous les non-enseignants ou non-soignants à de l'administration |
| Coût d'un poste non remplacé | Coût d'entrée hors contribution aux pensions, croissant avec l'ancienneté jusqu'au coût moyen | Valoriser au salaire du partant ou au coût moyen |
| Économie nette | Écart à une trajectoire de référence qui remplace tous les départs, après investissements, coûts récurrents et recettes | Confondre dépense évitée et baisse par rapport au niveau actuel |
| Lecture consolidée APU | Économie après retour aux APU des cotisations, CSG et retenues prélevées sur les salaires | Présenter l'économie employeur comme une économie publique totale |

## 2.5 Ce que la mission ne fait pas

- **Elle ne convertit aucun écart international en sureffectif.** Une différence de ratio entre pays ne devient une piste qu'après correction du périmètre, des besoins et des résultats de service (chapitres 4 à 6).
- **Elle ne traite pas des métiers opérationnels** (enseignants, soignants, forces de sécurité, magistrats) comme gisements de suppression. Leur nombre relève de choix de politique publique et de niveau de service, pas d'une rationalisation administrative.
- **Elle ne chiffre pas ce qui n'est pas documenté.** Les cases manquantes restent vides et sont signalées.

## 2.6 Limites principales

1. **Les tâches réelles ne sont pas mesurées.** Les sources donnent des corps, des filières et des métiers, pas le temps consacré à chaque tâche. Le périmètre « administratif » repose donc sur des catégories statutaires.
2. **Les gisements sont des hypothèses.** Aucune réforme du catalogue ne s'appuie sur une mesure française de postes effectivement supprimés après une réforme comparable ; les taux sont rattachés à des précédents étrangers ou à des estimations déclarées.
3. **Les coûts territoriaux et hospitaliers sont des proxys** du coût de l'État, faute de coût d'entrée publié.
4. **Les comparaisons internationales ne sont que partiellement corrigées** : NACE/ISCO, heures, démographie et résultats de service n'ont pas pu être réunis pour tous les pays.
5. **Le travail est arrêté au 30 octobre 2026.** Les publications ultérieures ne sont pas intégrées.
