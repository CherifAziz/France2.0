# Contre-vérification indépendante 04b — lot 2

Date : **28 octobre 2026**. Quinze indicateurs décisifs de la note enseignement, police et justice sont relus directement dans les CSV hérités et les PDF primaires. Le script extracteur `04b_education_securite_justice.py` n'est ni lu, ni importé, ni appelé. Les chiffres publiés sont extraits de la note ; les deux erreurs standard sont rapprochées du CSV de résultat après lecture indépendante du brut. Aucun fichier 04b n'est modifié.

**Résultat : 15 contrôles conformes sur 15 ; 0 divergence numérique.** Les arrondis publiés concordent. L'échantillon ne certifie pas tout le lot et n'établit aucun sureffectif ou potentiel d'économie.

## Chiffres contrôlés

- **04bV01** : France primaire tous établissements (2024) ; publié **17.87**, source **17.8731** eleves_ETP_par_enseignant_ETP ; `CONFORME`.
- **04bV02** : OCDE primaire tous établissements (2024) ; publié **13.71**, source **13.7102884594595** eleves_ETP_par_enseignant_ETP ; `CONFORME`.
- **04bV03** : France second cycle secondaire tous établissements (2024) ; publié **11.48**, source **11.48378** eleves_ETP_par_enseignant_ETP ; `CONFORME`.
- **04bV04** : OCDE second cycle secondaire tous établissements (2024) ; publié **12.78**, source **12.7794275833333** eleves_ETP_par_enseignant_ETP ; `CONFORME`.
- **04bV05** : France primaire établissements publics (2024) ; publié **17.48**, source **17.47926** eleves_ETP_par_enseignant_ETP ; `CONFORME`.
- **04bV06** : France second cycle secondaire établissements publics (2024) ; publié **11.33**, source **11.32534** eleves_ETP_par_enseignant_ETP ; `CONFORME`.
- **04bV07** : France tâches administratives enseignants à temps plein (2024) ; publié **1.5**, source **1.5** heures_de_60_minutes_par_semaine ; `CONFORME`.
- **04bV08** : OCDE tâches administratives enseignants à temps plein (2024) ; publié **3.0**, source **3** heures_de_60_minutes_par_semaine ; `CONFORME`.
- **04bV09** : France travail total tous enseignants (2024) ; publié **37.23**, source **37.22539548** heures_de_60_minutes_par_semaine ; `CONFORME`.
- **04bV10** : France enseignement tous enseignants (2024) ; publié **18.96**, source **18.96158896** heures_de_60_minutes_par_semaine ; `CONFORME`.
- **04bV11** : France policiers effectif (2022) ; publié **245983**, source **245983** personnes ; `CONFORME`.
- **04bV12** : France policiers densité (2022) ; publié **361.25**, source **361.25** policiers_par_100000_habitants ; `CONFORME`.
- **04bV13** : France personnel non-juge dans les tribunaux (2022) ; publié **37.3**, source **37.3** ETP_par_100000_habitants ; `CONFORME`.
- **04bV14** : Médiane Conseil de l'Europe personnel non-juge dans les tribunaux (2022) ; publié **57.9**, source **57.9** ETP_par_100000_habitants ; `CONFORME`.
- **04bV15** : France Q52 catégorie administrative et gestion des tribunaux (2022) ; publié **3424**, source **3424** ETP_occupes ; `CONFORME`.

## Vérifications de champ et réserves

**Ratios d'enseignement.** Les six lignes sélectionnent explicitement 2024, `STU_PERS`, `ST_TCHR`, `UNIT_MULT=0`, CITE 1 ou 3, total et établissements publics selon le cas. Les 17,87 et 11,48 tous établissements deviennent bien 17,48 et 11,33 dans le public. Ces ratios portent sur les enseignants et élèves ETP ; les séries ne dénombrent pas l'administration scolaire. Le code OCDE est l'agrégat publié, sans recalcul d'une moyenne des seuls pays retenus. [Source OCDE](https://sdmx.oecd.org/public/rest/data/OECD.EDU.IMEP,DSD_EAG_UOE_NON_FIN_PERS@DF_UOE_NF_PERS_STR,1.1/).

**TALIS : population et erreurs standard.** Les **1,5 h France / 3 h OCDE** de tâches administratives sont confirmées dans la [note primaire, PDF 11 / page imprimée 10](https://www.oecd.org/content/dam/oecd/en/publications/reports/2025/10/results-from-talis-2024-country-notes_eafd703e/france_714d7439/50507701-en.pdf). Elles concernent les seuls enseignants à temps plein du premier cycle secondaire. La même page confirme 38,7/41 h de travail total et 20,1/22,7 h d'enseignement. Le CSV, CITE 2 et tous profils `_T`, porte sur tous les enseignants, temps partiel inclus : Q14_1 : moyenne 37.22539548 h, SE **0.258215233 h** (ligne source 35309) ; Q15_1 : moyenne 18.96158896 h, SE **0.120957487 h** (ligne source 35652). Les deux SE correspondent exactement aux lignes du CSV de résultat ; elles ne s'appliquent pas aux 1,5/3 h ni aux 38,7/41 h du sous-groupe temps plein. La page pays ne donne pas ces SE. Un écart de population ne constitue donc pas une incohérence de chiffres. Les réponses restent déclaratives et les heures par tâche ne forment pas une partition comptable.

**Police : effectif opérationnel et champ national.** Les deux cellules françaises 2022 sont retrouvées directement dans `crim_just_job`, métier `OC5412`, sexe total, unités `NR` et `P_HTHAB`. Aucune valeur française 2023 n'est présente dans le brut. Le [HTML primaire Eurostat](https://ec.europa.eu/eurostat/cache/metadata/en/crim_sims.htm) confirme l'exclusion du personnel de soutien, dont secrétaires et employés de bureau (§3.4), l'inclusion de la police locale française et la date allemande du 30 juin, fonctionnaires hors stagiaires (§15.1). Les territoires ultramarins français énumérés sont exclus (§3.7). Ces notes empêchent de lire le nombre comme celui de tous les administratifs du ministère. Le taux publié Eurostat est conservé ; la population d'une autre source n'est pas substituée.

**Justice : catégories et résidu conservé.** Les **37,3 et 57,9 ETP/100 000 habitants** correspondent au personnel non-juge des tribunaux et à la médiane CoE, non à la seule administration. Le [profil France, PDF 67](https://rm.coe.int/fiche-pays-partie-2-en/1680b21e99) et la [notice Q52, PDF 31](https://rm.coe.int/explanatory-note-2024-cycle-cepej-2023-2-en/1680aae30a) distinguent assistance judiciaire, Rechtspfleger, administration/gestion, technique et autres ; le personnel du parquet est suivi séparément à Q60. La [réponse française, PDF 30](https://rm.coe.int/france-2024-2022-/1680b1f6cd) donne 25388 ETP au total, 20190 d'assistance, 3424 d'administration, 898 techniques et 874 autres. La somme des catégories numériques est 25386, avec un résidu publié de 2 ETP. La catégorie Rechtspfleger est non applicable : aucune valeur zéro n'est créée pour la remplir. La note 04b conserve correctement ce résidu. Les comparaisons de catégories administratives requièrent toujours l'examen des greffes, missions et externalisations.

## Reproduction et limites

Exécuter à la racine : `python scripts/00_verification_04b_lot2.py` (Python 3 et `pypdf`). Le script utilise seulement `csv`, `decimal`, `hashlib`, `re`, `pathlib` et `pypdf`. Il impose une cellule unique par sélection, vérifie les unités et définitions, compare selon la précision affichée et sort en erreur si une divergence est trouvée. Il produit uniquement `data/risques/verification_04b_lot2.csv` et cette note. Les pages PDF désignent l'index physique à partir de 1. Les lignes CSV comptent l'en-tête comme ligne 1 ; les dimensions explicites restent la référence si une valeur textuelle contient un saut de ligne.

Le contrôle est réalisé sur les archives locales ; les PDF TALIS et CEPEJ ont également été ouverts auprès des éditeurs pendant la contre-lecture. Les CSV hérités ne contiennent pas l'horodatage et l'URL exacte de leur requête initiale : l'accord confirme la fidélité au brut, sans certifier que toutes les séries sont les dernières disponibles. Les empreintes suivantes rendent l'état contrôlé identifiable. Aucun correctif numérique n'est demandé sur ces quinze indicateurs ; les réserves de champ restent nécessaires.

## Empreintes SHA-256 des entrées

- `recherche/04b_education_securite_justice.md` : `d0a211c7600449c75ae951ed9e9d9ac9b6197448747ef9c8f320d01830474a04`
- `data/raw/04/oecd_eag_DF_UOE_NF_PERS_STR.csv` : `f970bbeab9e9ead2c0a3db8578cb8a7baec507d5125c2994f6d8a221b529db0b`
- `data/raw/04/oecd_talis_teacher.csv` : `ed6e3ab6df1bc23c384cade0802b128d0fe2b1c872e1c1f3ce1d9c52d43d3907`
- `data/raw/04/eurostat_crim_just_job.csv` : `397e41e86bd5f4b0b9fea7576c6afd343a4ce2563fbb34f0c16323177d5a3847`
- `data/raw/04b/eurostat_crim_metadata.html` : `9e5399d0399ff1f55fc97944fa733c0724f366379d997bd510b6ce9ffd373bfa`
- `data/international/04b_talis2024.csv` : `26a17b92282a7a194fbde81b110a1c6ae6762dd960b7318f3fdc4de47c3ceb27`
- `data/cache/04b/oecd_talis2024_france.pdf` : `8aae2a2862293c3b85d136086d562f85b87426d533ba54ddf5d67ec61c46dd86`
- `data/cache/04b/cepej2024_profils.pdf` : `710a53b8b1365e873a6c98591d64575be438d405f46a2faa2477c79ad102cd0e`
- `data/cache/04b/cepej2024_reponses_france.pdf` : `cd931f5db6ad20921deced04efc499c2b36875153444751a04be14ecf9945351`
- `data/cache/04b/cepej2024_notice.pdf` : `3bdb799ba6ea527b66dcc2f62a7880e6bab65262f9c1a9aa9040de455a67a856`
