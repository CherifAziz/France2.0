# Base comparative internationale : collecte harmonisée initiale

Date de consultation : **28 octobre 2026**. Millésime commun retenu pour la lecture : **2023** ; **2024** est fourni pour tester la disponibilité et les évolutions. Les observations du Panorama OCDE 2025 conservent leur année réelle, parfois 2021 ou 2022. Cette livraison relève de la **phase de données** ; elle ne clôt pas le diagnostic international.

## 1. Synthèse

1. **[FAIT]** Le périmètre de collecte comporte **44 pays** du champ UE/OCDE retenu, Singapour compris à titre exploratoire, et l'agrégat **UE27** pour Eurostat. La moyenne OCDE publiée est conservée comme agrégat séparé. Liste exacte : dictionnaire `COUNTRIES` du script ; aucune moyenne de ce panel n'est présentée comme « moyenne OCDE ».
2. **[FAIT]** La base longue contient **3 859 lignes**, dont **3 553 valeurs disponibles** et **306 valeurs laissées vides**. Une ligne est identifiée par **source_id × pays × année × indicateur** ; plusieurs sources d'un indicateur ne sont pas additionnables.
3. **[FAIT]** Les structures des **six flux OCDE** retenus ont été lues avant de construire les clés SDMX. **Neuf réponses d'API** et le StatLink du Panorama 2025 sont archivés avec URL, empreinte et code HTTP. Les fichiers bruts et manifestes occupent moins de **1 Mo** à cette date.
4. **[FAIT]** Le flux OCDE d'emploi S13 `DF_TABLE12_EMPDC` fournit **63 observations annuelles pour 33 pays** sur 2023-2024. Le tableau volontaire Eurostat `gov_10a_emp` ne fournit ici que **16 observations pour huit pays** ; la France y est absente.
5. **[ESTIMATION]** En France, l'emploi S13 vaut **6 336 000 personnes en 2023**, pour **30 376 000 emplois intérieurs** : `100 × 6 336 000 / 30 376 000` = **20,859 % de l'emploi**. Les effectifs publiés par l'OCDE sont en milliers de personnes ; ils ont été multipliés par 1 000. Sources : `03_oecd_emp_gov.csv` et `03_oecd_emp_total.csv`, filtres FRA, 2023, EMP, PS, S13/S1.
6. **[ESTIMATION]** Rapporté aux **68 553 000 habitants** de la population annuelle OCDE, cet emploi S13 représente **92,425 personnes pour 1 000 habitants en 2023**. Source : mêmes effectifs et `03_oecd_population.csv`, FRA, 2023, POP.
7. **[FAIT / ESTIMATION]** Les données France 2024, provisoires, indiquent **6 408 000 personnes S13**, soit **20,947 % de l'emploi intérieur** et **93,172 pour 1 000 habitants**. Ce ne sont ni des ETP ni les seuls emplois administratifs.
8. **[ESTIMATION]** Avec les données actuelles et la même formule, l'emploi S13 en 2023 représente **11,802 %** de l'emploi intérieur en Allemagne, **13,529 %** en Italie et **15,765 %** en Espagne. Les différences de métiers couverts et de fourniture publique/privée restent à corriger avant toute interprétation.
9. **[ESTIMATION]** La Suède est à **28,145 %**, le Danemark à **27,331 %** et la Finlande à **25,437 %** dans cette extraction 2023. Les données suédoises présentent une divergence entre deux tables OCDE, signalée ci-dessous.
10. **[ESTIMATION]** La France est à **12,222 % du PIB** de rémunérations S13 en 2023, l'Allemagne à **8,013 %**, les Pays-Bas à **8,490 %**. D1 inclut les cotisations employeur ; il ne mesure pas une économie réalisable par non-remplacement.
11. **[ESTIMATION]** Pour **P2 + D632**, les montants sont respectivement **11,846 %**, **14,678 %** et **16,663 % du PIB**. Le classement obtenu sur la seule masse salariale ne décrit donc pas les achats de biens, services et prestations en nature financés par les administrations. Ces achats ne sont pas tous administratifs.
12. **[ESTIMATION]** Le sous-total **D1 + P2 + D632** vaut **24,067 % du PIB en France**, **22,691 % en Allemagne**, **25,153 % aux Pays-Bas** en 2023. Il ne constitue pas une mesure complète des coûts de production : consommation de capital fixe et autres composantes restent à intégrer.
13. **[FAIT]** Les données Eurostat France 2023 sont **12,2 % du PIB pour D1**, **56,8 % pour TE**, **5,6 % pour P2**, **6,3 % pour D632**. Sources : `gov_10a_main`, S13, PC_GDP. Les ratios OCDE calculés ne sont pas arrondis au dixième dans la base.
14. **[FAIT]** Le rapprochement porte sur **224 couples pays-année-indicateur** OCDE/Eurostat ; **aucun écart ne dépasse 0,15 point de PIB**. Il s'agit d'un contrôle de cohérence de diffuseurs utilisant souvent les mêmes comptes nationaux, pas de deux enquêtes indépendantes.
15. **[FAIT]** Le volet COFOG contient **2 424 observations publiées** : TE, D1, P2 et D4 pour les dix fonctions, en % du PIB, sur 2023-2024. Toutes les cellules demandées ne sont pas présentes. D1 d'une fonction n'est pas le nombre d'agents de cette fonction.
16. **[FAIT]** Les services généraux GF01 représentent **6,2 % du PIB** en France en 2023, dont **1,6 % de D1**, **0,6 % de P2** et **1,9 % de D4**. Les premières valeurs portent le drapeau provisoire `p`. Source : `gov_10a_exp`, FR, S13, GF01, PC_GDP.
17. **[NON TROUVÉ]** La décomposition fonctionnelle directe de **D41** n'a pas été trouvée dans les dimensions de `gov_10a_exp` examinées. **GF01 hors intérêts reste vide**. D4 n'est pas exclusivement D41 et toute la rubrique GF0107 « opérations concernant la dette publique » ne peut être traitée automatiquement comme des intérêts.
18. **[FAIT]** Les tables OCDE 12 et 3 donnent **51 couples comparables d'emploi S13**, avec **sept divergences** supérieures à une personne après conversion d'unité. La France est concordante entre ces deux tables, en 2023 et 2024. Détail : `03_rapprochement_emplois_s13.csv`.
19. **[FAIT]** L'écart le plus élevé de ce rapprochement est le Portugal 2024 : **830 500** dans la table 12 contre **791 946** dans la table 3, soit **38 554 personnes**. La cause de champ ou de révision reste à établir ; elle n'est pas masquée par une moyenne.
20. **[FAIT]** Le StatLink primaire du Panorama 2025 indique pour la France **20,740 % en 2023**, contre **20,859 %** dans le calcul à partir des API d'octobre 2026. Ces deux valeurs portent la même année d'observation mais des millésimes différents ; leur différence n'est pas une variation d'effectifs entre deux années.
21. **[FAIT]** Le même StatLink publie **14,560 % pour les États-Unis en 2023**, absent du flux S13 API retenu. La valeur est ajoutée comme observation publiée, avec une source distincte ; elle ne remplace pas silencieusement la case vide de l'API.
22. **[FAIT]** Sous l'en-tête 2023 du StatLink, **Norvège, Suisse, Portugal et Israël sont en réalité en 2022**, et le Costa Rica en 2021. Ces années réelles sont enregistrées dans la base.
23. **[FAIT]** Le StatLink donne **4,938 % pour le Japon en 2023**, avec une note excluant les fonds de sécurité sociale ; le calcul sur le flux actuel donne **6,141 %**. La différence doit être examinée comme une question de source, de champ ou de révision. La note du livre de 2025 ne peut être transférée automatiquement à l'API de 2026.
24. **[NON TROUVÉ]** NACE O/P/Q, ISCO4, heures, structure démographique, dépenses en PPA harmonisées, offre publique/privée par fonction et résultats des services n'ont pas encore été réunis dans cette collecte. Ils restent nécessaires aux corrections de périmètre et de besoins. **Aucun écart présenté ici n'est converti en sureffectif ou en économie.**

Sauf mention du StatLink ou d'Eurostat, les résultats de cette synthèse sont ceux des flux OCDE archivés, filtrés par les codes du dictionnaire et les années indiquées. Les URL exactes et les clés SDMX figurent dans `sources/registre_03.csv` ; les calculs sont conservés dans la colonne `formule` de la base.

## 2. Tableau d'indicateurs : lecture du millésime 2023

Toutes les valeurs ci-dessous proviennent du **calcul courant sur les API OCDE**, pas du Panorama 2025. Les taux d'emploi et ratios de dépenses sont des **[ESTIMATION]** au sens du protocole : calculs arithmétiques à partir de statistiques publiées. Les données de dépenses sont celles de l'ensemble S13, toutes fonctions. `ND` signifie indisponible dans les flux retenus, jamais zéro. Les chiffres sont arrondis ici ; la base conserve davantage de décimales pour la reproductibilité, sans prétendre à cette précision économique.

| Pays | Emploi S13 / emploi intérieur (%) | Emploi S13 pour 1 000 habitants | D1 / PIB (%) | P2 + D632 / PIB (%) | Année / source | Champ et statut |
|---|---:|---:|---:|---:|---|---|
| France | 20,86 | 92,42 | 12,22 | 11,85 | 2023, OCDE tables 12, 3 et 1 | S13, [ESTIMATION] |
| Allemagne | 11,80 | 65,05 | 8,01 | 14,68 | 2023, mêmes flux | S13, [ESTIMATION] |
| Italie | 13,53 | 59,81 | 8,78 | 8,11 | 2023, mêmes flux | S13, [ESTIMATION] |
| Espagne | 15,77 | 70,03 | 10,95 | 8,44 | 2023, mêmes flux | S13, [ESTIMATION] |
| Portugal | 15,60 | 77,23 | 10,29 | 6,98 | 2023, mêmes flux | S13, [ESTIMATION] ; divergence table 3 |
| Belgique | 18,30 | 79,11 | 12,24 | 11,88 | 2023, mêmes flux | S13, [ESTIMATION] |
| Pays-Bas | 12,44 | 70,87 | 8,49 | 16,66 | 2023, mêmes flux | S13, [ESTIMATION] ; divergence table 3 |
| Suisse | ND | ND | 7,19 | 5,94 | 2023, mêmes flux | S13, [NON TROUVÉ] pour l'emploi |
| Autriche | 16,67 | 86,41 | 10,55 | 11,21 | 2023, mêmes flux | S13, [ESTIMATION] |
| Royaume-Uni | 16,99 | 82,59 | 9,70 | 11,11 | 2023, mêmes flux | S13, [ESTIMATION] |
| Irlande | 20,12 | 102,13 | 6,03 | 5,72 | 2023, mêmes flux | S13, [ESTIMATION] ; dénominateur PIB particulier à examiner |
| Suède | 28,14 | 145,14 | 12,47 | 12,01 | 2023, mêmes flux | S13, [ESTIMATION] ; divergence table 3 |
| Danemark | 27,33 | 146,77 | 14,26 | 9,53 | 2023, mêmes flux | S13, [ESTIMATION] |
| Norvège | ND | ND | 12,40 | 9,01 | 2023, mêmes flux | S13, [NON TROUVÉ] pour l'emploi |
| Finlande | 25,44 | 126,33 | 13,18 | 14,89 | 2023, mêmes flux | S13, [ESTIMATION] |
| Pologne | 16,96 | 79,00 | 10,21 | 8,54 | 2023, mêmes flux | S13, [ESTIMATION] |
| Estonie | 23,41 | 118,17 | 11,72 | 8,72 | 2023, mêmes flux | S13, [ESTIMATION] |
| Canada | 19,93 | 103,38 | 11,87 | 9,89 | 2023, mêmes flux | S13, [ESTIMATION] |
| États-Unis | ND | ND | 8,32 | 6,75 | 2023, mêmes flux | S13, [NON TROUVÉ] pour l'emploi ; 14,56 % publié dans une autre source |
| Australie | 15,56 | 84,70 | ND | ND | 2023, mêmes flux | S13, [NON TROUVÉ] pour certaines dépenses |
| Nouvelle-Zélande | ND | ND | 9,61 | 12,33 | 2023, mêmes flux | S13, [NON TROUVÉ] pour l'emploi |
| Japon | 6,14 | 34,01 | 4,87 | 13,10 | 2023, mêmes flux | S13, [ESTIMATION] ; divergence avec publication 2025 |
| Corée | 8,65 | 47,55 | 6,61 | 9,60 | 2023, mêmes flux | S13, [ESTIMATION] |
| Singapour | ND | ND | ND | ND | 2023, mêmes flux | [NON TROUVÉ], population/PIB seuls présents |

Sources directes : [emploi S13, table 12](https://sdmx.oecd.org/public/rest/v1/dataflow/OECD.SDD.NAD/DSD_NASEC10@DF_TABLE12_EMPDC/1.1?references=datastructure), [emploi intérieur, table 3](https://sdmx.oecd.org/public/rest/v1/dataflow/OECD.SDD.NAD/DSD_NAMAIN10@DF_TABLE3_EMPDC/2.0?references=datastructure), [comptes publics de dépenses](https://sdmx.oecd.org/public/rest/v1/dataflow/OECD.SDD.NAD/DSD_NASEC10@DF_TABLE12_EXP/1.1?references=datastructure). Les URL de données complètes, longues car filtrées par pays et dimensions, sont conservées dans le registre et chaque ligne de la base.

## 3. Construction et contrôles

### 3.1 Emploi et population

Le numérateur est `EMP`, secteur `S13`, unité `PS`, transformation `N`, fréquence annuelle. Le flux table 12 est retenu comme série de collecte principale car sa couverture est plus large que celle de la table 3 par secteurs. Ce choix n'établit pas qu'il soit plus exact dans les cas divergents. Le contrôle alternatif est livré sans moyenne des deux séries.

Le dénominateur du taux d'emploi provient de `DF_TABLE3_EMPDC`, secteur S1, activité totale `_T`, transaction EMP, personnes. Le flux `DF_TABLE3_EMP_SECTOR` est utilisé pour le rapprochement des numérateurs, sans se substituer silencieusement au flux de total intérieur retenu. Les deux tables de total intérieur peuvent être révisées à des rythmes différents : pour la France 2023, l'une indique 30 376 milliers de personnes, l'autre 30 395. La source du ratio est donc précisée plutôt qu'une fausse valeur nationale unique.

La population vient de `DF_TABLE3_POP_EMPNC`, transaction POP, unité PS. Le script applique **10 puissance UNIT_MULT** à chaque montant. Les valeurs d'emploi sont des grandeurs annuelles ; elles ne doivent pas être additionnées au stock SIASP du 31 décembre ou assimilées à des ETP. Des valeurs fractionnaires peuvent résulter de moyennes annuelles.

Le rapport à la population est une mesure d'intensité territoriale, pas une part de la population active. L'emploi intérieur peut comprendre des frontaliers non résidents. Les périmètres territoriaux et calendriers nationaux doivent être vérifiés pour les comparaisons fines ; un code d'année identique ne garantit pas à lui seul une parfaite synchronisation de périodes budgétaires.

### 3.2 Comptes publics

Les ratios OCDE sont calculés à partir du montant S13 et du PIB en monnaie nationale à prix courants :

`ratio = 100 × (OBS_VALUE_dépense × 10^UNIT_MULT_dépense) / (OBS_VALUE_PIB × 10^UNIT_MULT_PIB)`.

Le calcul exige la même année et une monnaie identique, explicitement renseignée dans les deux lignes. Le flux de PIB est `DF_TABLE1_EXPENDITURE`, transaction B1GQ, S1, XDC, prix courants V. Aucun ratio n'est produit si un composant manque ou si la monnaie ne concorde pas.

Les ratios Eurostat publiés restent séparés, avec leur arrondi au dixième. Les colonnes de drapeaux sources sont conservées ; `A` signifie valeur normale, `P` ou `p` provisoire. Un drapeau provisoire ne signifie pas une donnée inutilisable, mais doit accompagner sa présentation.

La rubrique D1 comprend salaires et cotisations employeur. L'écart de D1 entre pays dépend des effectifs, des rémunérations, des cotisations, des fonctions couvertes et du traitement des pensions. **D1 divisé par un effectif moyen ne donne pas le coût budgétaire d'entrée évité par un non-remplacement.**

P2 inclut les consommations intermédiaires de toutes les fonctions publiques ; D632 inclut des prestations sociales en nature achetées au secteur marchand. Ce sont des éléments nécessaires à une lecture économique élargie. Ils ne constituent pas un inventaire des prestataires administratifs, et leur somme n'identifie pas à elle seule une inefficacité ou un transfert organisationnel précis. Un zéro publié, tel le D632 américain dans cette extraction, est conservé comme tel ; sa signification comptable demande une vérification nationale avant d'en déduire l'absence de financement public de soins ou d'autres prestations.

### 3.3 COFOG et GF01

Les fonctions GF01 à GF10 sont collectées pour TE, D1, P2 et D4. Les dépenses de personnel de la santé ou de l'enseignement ne sont pas le nombre d'administratifs de ces secteurs. Inversement, les fonctions de gestion peuvent se trouver dans plusieurs fonctions COFOG.

La catégorie GF01 n'est pas un proxy des seules « tâches administratives » : elle comprend des fonctions institutionnelles et financières. Faute de D41 directement ventilé dans l'extraction, aucune soustraction approximative n'est présentée comme GF01 hors intérêts. Une extraction complémentaire ou une justification normative de la ventilation des intérêts sera nécessaire pour remplir cet indicateur.

### 3.4 Sources, versions et contradictions

Chaque réponse d'API est archivée sans exécution dans `data/raw/03/`, avec un manifeste `*.meta.json` comprenant URL exacte, URL finale, code HTTP, type MIME et SHA256. L'ordre des dimensions provient de XML structurés, et non d'une clé construite de mémoire. Les réponses CSV sont contrôlées pour la présence d'OBS_VALUE ; les erreurs HTTP ne sont pas enregistrées comme données.

Le [StatLink de la figure 13.1 du Panorama 2025](https://stat.link/8htodn) a été lu intégralement avec ses notes et sa feuille « About this file ». Les dérogations d'années du fichier sont reprises explicitement. Les ratios de cette édition restent des observations distinctes, y compris lorsqu'ils portent le même pays et la même année que les API actuelles. La différence entre sources ou millésimes figure dans `03_rapprochement_panorama2025.csv`.

Les sept écarts S13 entre tables 12 et 3 sont : Italie 2024 (+17 800), Pays-Bas 2023 (+5 000), Portugal 2023 (+33 068) et 2024 (+38 554), Roumanie 2024 (−7 100), Suède 2023 (−10 600) et 2024 (−11 600 personnes), calculés **table 12 moins table 3**. Les indicateurs dérivés concernés portent une note et le drapeau `ECART_TABLE3_NON_RESOLU`. L'origine exacte de ces écarts reste **[NON TROUVÉ]** dans cette phase.

## 4. Limites et travail restant avant le diagnostic

Les quatre niveaux exigés par le cahier des charges sont distingués :

1. **Écart statistique brut :** les niveaux et unités sont maintenant collectés ; aucun classement synthétique de performance n'est construit.
2. **Après correction du périmètre :** non calculé à ce stade. Il faut identifier le poids du privé, des organismes sans but lucratif, des prestataires et des retraites dans chaque fonction.
3. **Après correction des besoins :** non calculé. Démographie, morbidité, élèves, règles de prestations, heures travaillées, décentralisation et accès territorial restent nécessaires.
4. **Potentiel de productivité ou de réduction :** non calculé. Il doit venir des tâches, organisations et réformes démontrées, puis de la qualité de service mesurée.

Les absences principales sont les emplois NACE O/P/Q et ISCO4, la comparabilité des heures, les PPA et salaires d'entrée, les corrections de santé et d'enseignement, les prestations et les indicateurs de résultats. Les données 2020 de SNG-WOFI et 2024 de TALIS restent disponibles dans le chantier 04 contrôlé ; elles n'ont pas été assemblées artificiellement en un millésime 2023 unique.

Le cas irlandais nécessite une lecture attentive du dénominateur PIB avant de comparer l'effort public ; le présent document ne remplace pas ce dénominateur par une autre grandeur sans source et convention explicites. Pour les pays où la fonction est essentiellement réalisée par des acteurs privés financés publiquement, l'analyse fonctionnelle doit précéder toute inférence sur un écart d'effectifs.

**Conclusion de collecte :** il existe désormais une base traçable des ordres de grandeur et des absences. Elle permet de préparer les comparaisons par fonction ; elle ne permet pas encore de déduire un nombre de postes supprimables ni des économies nationales.

## 5. Fichiers et reproduction

- `data/international/03_base_comparative.csv` : données longues, sources, années, champs, formules et statuts.
- `data/international/03_dictionnaire_indicateurs.csv` : définition et unité des indicateurs.
- `data/international/03_dictionnaire_variables.csv` : définition des colonnes et traitement des absences.
- `data/international/03_rapprochement_emplois_s13.csv` : tables OCDE 12 et 3.
- `data/international/03_rapprochement_finances.csv` : ratios OCDE calculés et ratios Eurostat publiés.
- `data/international/03_rapprochement_panorama2025.csv` : publication 2025 et API consultées en 2026.
- `sources/registre_03.csv` : registre des réponses primaires et structures.
- `scripts/03_collecte_harmonisee.py` : acquisition, conversion, contrôles et calculs.

Reproduction à partir des instantanés déjà présents :

```text
python -I scripts/03_collecte_harmonisee.py
```

Rafraîchissement explicite :

```text
python -I scripts/03_collecte_harmonisee.py --refresh
```

La date de mission est une constante explicite `DATE` du script. Une collecte future doit changer cette date et consigner les révisions ; les tableaux du présent document ne se mettent pas à jour automatiquement. Dépendances : Python 3, `requests` et `openpyxl`. Aucun brut de la session précédente n'a été écrasé.
