# Contrôle préparatoire des données internationales héritées

Date de consultation : **28 octobre 2026**. Ce document contrôle les fichiers reçus de la première session. Il ne constitue ni le chantier 03 achevé, ni le diagnostic comparatif du chantier 04.

## 1. Synthèse

1. **[FAIT]** Les **15 CSV** de `data/raw/04/` sont lisibles en UTF-8 et contiennent **91 857 lignes de données**, nomenclature comprise. Aucun fichier vide, aucune réponse HTML déguisée en CSV et aucune ligne de largeur incohérente n'ont été détectés. Source : inventaire et empreintes de `data/international/04_controle_fichiers.csv`.
2. **[FAIT]** Aucun doublon exact et aucune clé d'observation répétée n'ont été trouvés avec les dimensions présentes dans les en-têtes. Cette vérification ne certifie pas la complétude des séries ni l'absence de recouvrement économique entre agrégats.
3. **[FAIT]** Les trois extractions Eurostat ont été rapprochées de **trois observations témoins de l'API primaire**, avec **zéro écart** : D1PAY/S13 France 2024 = **12,4 % du PIB**, policiers France 2022 = **245 983** en unité `NR`, administration de la protection sociale France 2023 = **1,29 % du PIB**. Requêtes exactes et résultats : `04_verification_api.csv` ; réponses intégrales archivées dans `data/raw/04_controle/`.
4. **[FAIT]** `gov_10a_main` contient **584 lignes**, seulement **D1PAY et TE**, en **% du PIB**, pour **2022-2025**. Le fichier ne contient pas les montants monétaires, P2, D632 ni COFOG nécessaires au cahier des charges. Source : extraction locale et [métadonnées Eurostat, §3.1 et §18.5](https://ec.europa.eu/eurostat/cache/metadata/en/gov_10a_main_esms.htm).
5. **[FAIT]** `crim_just_job` couvre globalement **2018-2024**, mais les policiers français `OC5412` s'arrêtent à **2022** dans le fichier. Une requête témoin France 2023 a retourné une série sans observation : elle n'a pas été convertie en zéro. La date maximale du fichier ne décrit donc pas chaque série.
6. **[FAIT]** La définition Eurostat des policiers exclut les fonctions de soutien. Les notes nationales indiquent que la police locale est incluse en France. Cet indicateur ne mesure donc pas l'ensemble des salariés de la sécurité intérieure ni leur administration. Source : [Eurostat crime, §3.4 et notes nationales « Police Officers »](https://ec.europa.eu/eurostat/cache/metadata/en/crim_sims.htm).
7. **[FAIT]** `spr_exp_type` contient **612 lignes**, les types **ADM et TOTAL**, trois unités et **2019-2024**. Les régimes et leurs couvertures doivent encore être étudiés pour expliquer les écarts. Source : extraction et [métadonnées ESSPROS, §3.1 et §15.1](https://ec.europa.eu/eurostat/cache/metadata/en/spr_esms.htm).
8. **[FAIT]** `isora_selection_long.csv` contient **5 088 lignes**, **23 pays** et des périodes de **2018 à 2024**, plus **une ligne sans année**. Les valeurs textuelles « Yes », « No » et les codes spéciaux ne sont pas des effectifs.
9. **[FAIT]** Les **218 observations datées françaises** de cette sélection ont toutes une correspondance dans `isora_FRA_all_indicators.csv`, avec **zéro différence de valeur et d'échelle**. Ce contrôle est interne aux extractions héritées, pas une seconde source statistique indépendante. Détail : `04_rapprochement_isora_fra.csv`.
10. **[FAIT]** Le fichier ISORA France contient **2 314 lignes**, une ligne sans année et des réponses qualitatives. L'échelle stockée prend les codes **0 et 3** : elle doit rester associée à la valeur et être interprétée avec le dictionnaire officiel avant conversion monétaire.
11. **[FAIT]** `oecd_eag_DF_UOE_NF_PERS_STR.csv` contient **8 749 lignes** de **ratios élèves/enseignant**, pas une table complète des effectifs administratifs. Il inclut les établissements publics, privés et leurs sous-ensembles. **3 808 valeurs sont vides**.
12. **[FAIT]** `oecd_eag_staffcomp_subset.csv` contient **1 395 lignes de dépenses de rémunération**, dont enseignantes et non enseignantes, en monnaie nationale à prix courants avec **UNIT_MULT = 6 (millions)**. Son nom ne prouve pas qu'il s'agit d'effectifs ni de seuls administratifs ; **378 valeurs sont vides**.
13. **[FAIT]** `oecd_eag_perstud_subset.csv` contient **780 lignes**, des dépenses par élève à temps plein en **dollars PPA** et en **% du PIB par habitant**, pour **2021-2024**. **48 valeurs sont vides**. Ces unités ne s'additionnent pas.
14. **[FAIT]** `oecd_hosp_emp.csv` contient **3 596 lignes**, avec **personnes, ETP, ratios par habitant et pourcentages** dans le même fichier. **La Suède est absente** de cette extraction ; `UNIT_MULT` est vide. Les unités explicites doivent être sélectionnées avant tout calcul.
15. **[FAIT]** `oecd_sha_hc7.csv` comporte **7 238 lignes** : **1 876 HC7**, **1 582 HC71**, **1 526 HC72**, **2 254 total santé**. Le bon filtre est le code `HC7`, sans soulignement, et non le seul nom du fichier. HC7 et ses composantes ne s'additionnent pas.
16. **[FAIT]** `oecd_sha_hc7_by_scheme.csv` comporte **7 105 lignes**, dont **2 925 HC7** et **4 180 total santé**. Il mélange régimes totaux et catégories imbriquées : `HF1`, `HF11`, `HF12HF13`, `HF121`, `HF122`, `HF2`, `HF21`, etc. Additionner ces lignes créerait des doubles comptes.
17. **[FAIT]** `oecd_lmp.csv` contient **15 923 lignes**, dépenses et participants, en **monnaie nationale, % PIB, personnes et % de la population active**. Les programmes agrégés et détaillés doivent aussi être distingués.
18. **[FAIT]** `oecd_sngwofi_struct_all.csv` couvre **134 zones** mais uniquement l'année **2020**, avec **540 lignes**. Les nombres de gouvernements et les tailles moyennes des communes ne sont pas des nombres de salariés ; les échelons totaux et détaillés se recouvrent.
19. **[FAIT]** `oecd_talis_teacher.csv` compte **35 844 lignes**, toutes en **2024** : **17 922 erreurs standard**, **17 400 modalités de type COUNT** et **522 moyennes**. La présence du code COUNT ne signifie pas nécessairement une unité « personnes » : il faut lire conjointement `UNIT_MEASURE`.
20. **[FAIT]** TALIS ne couvre que **18 pays du groupe cible plus l'agrégat OCDE** dans cette extraction ; Canada, Suisse, Allemagne, Royaume-Uni et Irlande n'y figurent pas. Les questions Q14/Q15 présentes portent sur temps de travail total et enseignement ; cette extraction ne fournit pas à elle seule une ventilation exhaustive du temps administratif.
21. **[NON TROUVÉ]** Les URL de téléchargement originales, leurs filtres complets et leurs horodatages n'étaient pas consignés avec les CSV hérités. Les URL canoniques du registre ont été reconstruites à partir des noms de jeux et des identifiants `DATAFLOW`, en le signalant. Aucun téléchargement complet OCDE n'a été certifié ici.

Sauf lien documentaire explicite, les constats 8 à 20 proviennent des CSV officiels hérités lus intégralement. Le registre `sources/registre_04_controle.csv` associe à chaque fichier son URL canonique, son accès et son empreinte. Les métriques de couverture sont des **résultats de contrôle de fichiers**, pas des statistiques nationales supplémentaires.

## 2. Tableau des indicateurs de contrôle

Les « zones » incluent les agrégats tels que l'OCDE ou l'UE. Le nombre de zones ne signifie pas que chacune dispose de toutes les dimensions et années. Source locale : `data/raw/04/<fichier>` ; détail des URL dans le registre.

| Indicateur | Valeur | Unité | Année | Champ / définition | Source (URL) | Page/tableau | Statut | Note |
|---|---:|---|---|---|---|---|---|---|
| crim_just_job | 696 | lignes | 2018-2024 | 16 pays | [Eurostat](https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/crim_just_job) | CSV intégral | [FAIT] | France policiers : dernière année 2022 |
| gov_10a_main | 584 | lignes | 2022-2025 | 17 zones | [Eurostat](https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/gov_10a_main) | CSV intégral | [FAIT] | D1PAY/TE, % PIB seulement |
| spr_exp_type | 612 | lignes | 2019-2024 | 17 zones | [Eurostat](https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/spr_exp_type) | CSV intégral | [FAIT] | ADM/TOTAL |
| isora_codelist | 1 393 | codes | non applicable | Nomenclatures indicateurs/pays | [ISORA](https://api.imf.org/external/sdmx/2.1/data/ISORA,ISORA_LATEST_DATA_PUB,5.0.0/) | CSV intégral | [FAIT] | URL du jeu, pas URL originale du XML de nomenclature |
| isora_FRA_all_indicators | 2 314 | lignes | 2018-2024 | France | [ISORA](https://api.imf.org/external/sdmx/2.1/data/ISORA,ISORA_LATEST_DATA_PUB,5.0.0/) | CSV intégral | [FAIT] | Une ligne sans année |
| isora_selection_long | 5 088 | lignes | 2018-2024 | 23 pays | [ISORA](https://api.imf.org/external/sdmx/2.1/data/ISORA,ISORA_LATEST_DATA_PUB,5.0.0/) | CSV intégral | [FAIT] | Une ligne sans année ; valeurs qualitatives |
| eag_DF_UOE_NF_PERS_STR | 8 749 | lignes | 2020-2024 | 25 zones | [OCDE](https://sdmx.oecd.org/public/rest/data/OECD.EDU.IMEP,DSD_EAG_UOE_NON_FIN_PERS@DF_UOE_NF_PERS_STR,1.1/) | CSV intégral | [FAIT] | Ratios élèves/enseignant |
| eag_perstud_subset | 780 | lignes | 2021-2024 | 25 zones | [OCDE](https://sdmx.oecd.org/public/rest/data/OECD.EDU.IMEP,DSD_EAG_UOE_FIN@DF_UOE_INDIC_FIN_PERSTUD,3.2/) | CSV intégral | [FAIT] | Deux unités de dépenses par élève |
| eag_staffcomp_subset | 1 395 | lignes | 2020-2024 | 23 pays | [OCDE](https://sdmx.oecd.org/public/rest/data/OECD.EDU.IMEP,DSD_EAG_UOE_FIN@DF_UOE_FIN_NATURE_STAFF,3.2/) | CSV intégral | [FAIT] | Dépenses, millions de monnaie nationale |
| hosp_emp | 3 596 | lignes | 2019-2025 | 22 pays | [OCDE](https://sdmx.oecd.org/public/rest/data/OECD.ELS.HD,DSD_HEALTH_REAC_EMP@DF_HOSP_EMP,1.1/) | CSV intégral | [FAIT] | Suède absente ; personnes et ETP |
| lmp | 15 923 | lignes | 2019-2024 | 24 zones | [OCDE](https://sdmx.oecd.org/public/rest/data/OECD.ELS.JAI,DSD_LMP@DF_LMP,1.0/) | CSV intégral | [FAIT] | Dépenses et participants |
| sha_hc7 | 7 238 | lignes | 2019-2025 | 23 pays | [OCDE](https://sdmx.oecd.org/public/rest/data/OECD.ELS.HD,DSD_SHA@DF_SHA,1.1/) | CSV intégral | [FAIT] | Quatre fonctions, dont total santé |
| sha_hc7_by_scheme | 7 105 | lignes | 2021-2025 | 23 pays | [OCDE](https://sdmx.oecd.org/public/rest/data/OECD.ELS.HD,DSD_SHA@DF_SHA,1.1/) | CSV intégral | [FAIT] | Régimes imbriqués |
| sngwofi_struct_all | 540 | lignes | 2020 | 134 zones | [OCDE](https://sdmx.oecd.org/public/rest/data/OECD.CFE.RDG,DSD_SNG_WOFI@DF_SNG_STRUCT,1.0/) | CSV intégral | [FAIT] | Structures territoriales, aucun emploi |
| talis_teacher | 35 844 | lignes | 2024 | 19 zones | [OCDE](https://sdmx.oecd.org/public/rest/data/OECD.EDU.ECS,DSD_TALIS@DF_TALIS_TEACHER_PROFILE,1.0/) | CSV intégral | [FAIT] | Erreurs standard, moyennes et modalités |

Les versions des URL OCDE sont celles du champ DATAFLOW des fichiers. Une URL canonique reconstruite n'est pas une preuve que l'ensemble du jeu a été téléchargé ou que cette version demeure la dernière.

## 3. Analyse technique et règles de préparation

### 3.1 Clés et dimensions

Le contrôle construit la clé Eurostat avec les dimensions précédant les libellés, période incluse. Pour les CSV OCDE à libellés doubles, il conserve les colonnes situées entre DATAFLOW et TIME_PERIOD. Pour ISORA, il utilise juridiction, indicateur, fréquence lorsque disponible et période. Les attributs d'observation restent distincts de la clé.

Il conserve **toutes les dimensions**, notamment établissement public/privé, sexe, profession, statut d'activité, unité et opération statistique. Réduire une table à pays-année sans les sélectionner produirait de faux doublons et pourrait additionner des quantités incompatibles. Les noms de colonnes « code: libellé » sont traités comme des noms complets ; les codes sont séparés des libellés sans supposer que l'intitulé traduit est stable.

Pour SHA, filtrer par exemple la fonction `HC7`, le régime `_T`, une unité identique et une même année ; vérifier ensuite les dimensions restantes. Pour comparer les régimes, choisir des composantes disjointes ou leur agrégat, sans garder simultanément les parents et enfants. La part d'administration dans la santé ne fournit pas automatiquement un écart d'effectifs administratifs.

Pour EAG, les établissements publics, privés, privés subventionnés et « tous établissements » ne sont pas disjoints. Les niveaux CITE agrégés recouvrent également leurs composantes. Les rémunérations des non-enseignants comprennent d'autres métiers que l'administration ; aucune conversion en postes administratifs n'est justifiée par ces seules dépenses.

### 3.2 Unités et données manquantes

Les valeurs OCDE conservent `UNIT_MEASURE`, `UNIT_MULT`, `PRICE_BASE`, `CURRENCY` et `BASE_PER` lorsqu'ils existent. **Une valeur avec UNIT_MULT=6 exprime des millions de l'unité correspondante**, pas des unités simples. Les conversions de monnaies nationales ne doivent intervenir qu'après choix du taux ou de la PPA, de l'année et du champ.

Les champs de valeur vides restent manquants. Les codes spéciaux ISORA, dont `D`, restent des codes jusqu'à lecture du dictionnaire ; ils ne deviennent ni zéro ni estimation. Les réponses qualitatives « Yes » et « No » sont des observations valides pour certaines questions. Les deux lignes ISORA sans période ne peuvent entrer dans une comparaison annuelle.

Les drapeaux Eurostat et attributs OCDE de statut sont conservés dans l'inventaire. L'absence de valeur manquante dans un fichier ne certifie pas une série complète : le script Eurostat original omet les cellules sans valeur.

### 3.3 Couverture réelle

Les fichiers Eurostat n'incluent pas le Royaume-Uni. La collecte des statistiques de police couvre 16 pays du groupe retenu, sans agrégat UE. Il faut tester la disponibilité **pays × indicateur × unité × année**, pas simplement la présence d'un pays quelque part dans un fichier.

La base ne contient pas encore les tables d'emploi des administrations publiques S13, NACE O/P/Q, ISCO4, la démographie et les heures nécessaires aux corrections, ni les résultats de service requis par le cahier des charges. Ces éléments restent à collecter. Le jeu Eurostat `gov_10a_emp`, mentionné dans les métadonnées `gov_10a_main`, constitue une piste primaire pour l'emploi S13 ; son champ et sa couverture volontaire devront être contrôlés.

### 3.4 Fragilités des scripts hérités

- `04_oecd_fetch.py` écrit le corps HTTP sans `raise_for_status`, sans validation des colonnes CSV et sans journal de requête. Une erreur HTTP pourrait être sauvegardée comme donnée lors d'une prochaine exécution. Les fichiers présents ont passé le contrôle de format.
- Sa construction automatique de clé lit la structure par expression régulière ; elle doit être confrontée à l'ordre effectif des dimensions et à la version du flux avant de relancer une collecte.
- `04_eurostat_fetch.py` suppose que `value` et `status` sont des dictionnaires, alors que JSON-stat peut aussi employer une représentation dense. Il omet les cellules sans observation et ne conserve pas la réponse JSON ni l'horodatage `updated` dans le CSV.
- `04_isora_fetch.py` perd des attributs présents dans la réponse complète et tronque les notes de bas de page à 300 caractères. La réponse multinationale brute annoncée par le script n'est pas présente dans les fichiers hérités ; on ne peut pas récupérer les notes tronquées à partir du seul CSV long.
- `04_isora_codelist.py` produit une liste code/libellé, sans conserver le XML source ni imposer explicitement une langue. La nomenclature locale permet de nommer des indicateurs, pas de prouver tous leurs champs.
- Aucun de ces scripts ne produit un manifeste complet avec URL exacte, heure d'acquisition, code HTTP, empreinte du corps brut et versions des paramètres. Cette absence réduit l'auditabilité du téléchargement initial.

Les scripts historiques et données brutes n'ont pas été modifiés. Les réparations à faire sont identifiées pour une collecte ultérieure avec l'outil d'archivage commun.

## 4. Limites, contradictions et décisions pour la suite

1. **Complétude API non démontrée.** Le contrôle certifie la lecture des fichiers, pas l'exhaustivité de chaque extraction ou sa fraîcheur en ligne. Trois observations témoins ne valident pas 91 857 lignes.
2. **Années non alignées.** SNG-WOFI 2020, TALIS 2024, autres séries variables et policiers France 2022 ne doivent pas former un classement présenté comme un millésime unique.
3. **Métadonnées nationales à compléter.** Les métadonnées de police signalent notamment des écarts de date de référence, de couverture et d'unité selon les pays ; le code `NR` ne dispense donc pas de lire ces notes, en particulier pour les juges. Les seules notes communes ne suffisent pas à certifier toutes les comparaisons bilatérales.
4. **Deux extractions ISORA ne sont pas deux sources indépendantes.** Leur accord montre la cohérence des transformations, pas une réplication statistique indépendante. La date de publication incluse dans le CSV France est le 10 juillet 2025, pour toutes les lignes ; elle n'a pas été vérifiée ailleurs dans ce contrôle.
5. **Pas de chiffrage d'économies.** Aucun de ces contrôles n'établit de sureffectif ni de potentiel de réduction. Les quatre niveaux d'écart requis — brut, périmètre, besoins, potentiel — restent à construire.

Décision : les fichiers peuvent être utilisés comme **matière première contrôlée**, après filtres documentés. Les noms de fichiers, les dates maximales et les simples totaux de lignes ne peuvent servir d'indicateurs comparatifs.

## 5. Sources consultées et reproduction

Les **15 fichiers locaux** ont été lus intégralement. Leur empreinte complète et leur couverture figurent dans `data/international/04_controle_fichiers.csv`. Le registre `sources/registre_04_controle.csv` comprend également les réponses API témoins et les pages de métadonnées archivées.

Sources en ligne lues :

- [Eurostat — Government revenue, expenditure and main aggregates](https://ec.europa.eu/eurostat/cache/metadata/en/gov_10a_main_esms.htm), mise à jour 21 octobre 2026, sections 3.1 et 18.5.
- [Eurostat — Crime and criminal justice](https://ec.europa.eu/eurostat/cache/metadata/en/crim_sims.htm), mise à jour 29 avril 2026, sections 3.4, 3.7 et notes nationales.
- [Eurostat — Social protection](https://ec.europa.eu/eurostat/cache/metadata/en/spr_esms.htm), mise à jour 31 octobre 2025, sections 3.1 et 15.1.

La première URL de métadonnées crime essayée, `crim_esms.htm`, renvoyait 404 ; l'URL correcte `crim_sims.htm` a ensuite été obtenue depuis l'annotation officielle de l'API. L'indisponibilité de policiers France 2023 a été constatée avant de choisir l'observation témoin 2022, présente dans le fichier.

Reproduction hors réseau, avec les instantanés archivés :

```text
python -I scripts/04_audit_raw.py --date 2026-10-28
```

Rafraîchissement volontaire des trois témoins et pages de métadonnées :

```text
python -I scripts/04_audit_raw.py --date 2026-10-28 --refresh-api
```

Le rafraîchissement peut faire apparaître des révisions depuis la date de ce contrôle. Il ne remplace pas les CSV hérités. Les documents téléchargés restent des données non exécutées.
