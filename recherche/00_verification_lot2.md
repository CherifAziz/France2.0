# Contre-vérification du deuxième lot

Contrôle arrêté au **28 octobre 2026**. Le lot couvre les comparaisons par fonction : fiscalité et emploi, éducation/police/justice, santé/protection sociale, territoires et supports. Cette étape porte sur les **bases de diagnostic**, pas sur les futures économies nationales.

## 1. Résultat

**63 contrôles indépendants ont été effectués. Deux formulations ont été corrigées ; aucune erreur numérique restante n'a été identifiée dans cet échantillon.** Les réserves de source, d'unité ou de périmètre demeurent attachées aux valeurs.

| Volet | Contrôles | Résultat final | Sources primaires relues |
|---|---:|---|---|
| 04a — Fiscalité et emploi | 16 | 13 conformes, un champ distinct confirmé, une convention monétaire réservée, un arrondi confirmé après correction | Export ISORA, XML des codes, questionnaire PDF, export LMP et métadonnées |
| 04b — Éducation, police, justice | 15 | 15 conformes ; erreurs standard TALIS relues en complément | CSV OCDE/Eurostat, note TALIS, métadonnées police et PDF CEPEJ |
| 04c — Santé/protection sociale | 17 | 17 confirmés | Cellules DREES2026, neuf postes de gestion2025, part OC, identité totale et six régimes SHA |
| 04d — Territoires et supports | 15 | 14 confirmés et une rédaction de périmètre confirmée après correction | XLSX DGCL, CSV WOFI, PDF Ravignon/Sénat/DAE et page législative du Sénat |

Le CSV fusionné `data/risques/verification_chiffres_lot2.csv` conserve les **63 lignes**, avec valeur publiée, valeur source, unité, année, URL, localisation, résultat et commentaire. `verification_lot2_resume.json` donne les effectifs de statuts et les empreintes des quatre fichiers de contrôle. Certaines lignes vérifient un ensemble ou une identité ; « 63 contrôles » ne signifie pas 63 observations statistiques indépendantes.

Les statuts finaux comprennent **28 CONFORME**, **31 CONFIRME**, **deux CONFIRME_APRES_CORRECTION**, **un CONFORME_CHAMP_DISTINCT** et **un CONFORME_VALEUR_RESERVE_UNITE**. Ces deux derniers statuts sont des réserves importantes, pas des autorisations à mélanger les champs.

## 2. Corrections apportées

**Arrondi britannique fiscal.** La première rédaction de la synthèse04a indiquait 0,858 ETP fiscaux par millier d'habitants, alors que le tableau et le CSV indiquaient correctement 0,857. Le brut donne `58 587 × 1 000 / 68 350 000 = 0,857161667886`. La synthèse est corrigée à **0,857**, puis relue par le vérificateur. Aucun calcul du CSV n'a changé. Trace : contrôle **04aV16**.

**Raccordement des coûts RH Ravignon.** Le texte primaire publie **2 047,3 M€**, alors que la somme A/B/C du tableau25 vaut **1 432,7 M€**. Le texte ajoute par ailleurs des agents CNFPT/CDG à son décompte d'agents ; il ne permet pas de prouver que tout l'écart entre les deux coûts s'explique par ces organismes. La note04d et son CSV disent désormais **raccordement non reconstitué**, sans qualifier une « base élargie » démontrée. Les montants restent ceux de la source. Trace : contrôle **V04d_09**.

## 3. Réserves confirmées

- **ISORA et unités.** Les ETP fiscaux annuels et le stock de personnel en fin d'exercice restent deux mesures différentes. Pour les montants français, le quotient coût/recettes confirme la convention de l'export, mais il ne suffit pas à certifier un contrat universel de conversion par SCALE : les recettes sont déjà exportées en unités alors que les dépenses dérivées se comportent comme des milliers. Cette réserve est explicitement conservée.
- **Population TALIS.** Les 1,5/3,0 heures administratives concernent les temps pleins du premier cycle secondaire. Les totaux du CSV hérité et leurs erreurs standard concernent l'ensemble des enseignants du champ, temps partiels compris. Les deux populations ne sont pas fusionnées. Deux erreurs standard ont été relues en complément des quinze lignes du volet04b.
- **Métiers opérationnels.** La série police exclut les personnels de soutien. Les non-juges CEPEJ comprennent surtout l'assistance judiciaire ; leur total ne désigne pas une administration interne supprimable.
- **Régimes de santé.** HF1 inclut l'assurance privée obligatoire. HF11+HF121 est une restriction par régime, pas une certification du secteur S13 de tous les pays. HC7 exclut les fonctions administratives internes aux soins.
- **Estimations de support.** Le coût de coordination de Ravignon et les hypothèses RH, opérateurs ou immobilier ne deviennent pas des gains budgétaires constatés après relecture. L'indicateur DAE d'économies achats reste distinct de la dépense exécutée et des économies effectivement réalisées.

Les anomalies des sources ne sont pas effacées : résidu de deux ETP CEPEJ France, écart d'un million de monnaie nationale dans une identité SHA allemande2024, sous-ligne Santé incohérente chez Ravignon, différences de millésimes DREES/SHA et raccordement incomplet des deux coûts RH. Elles ne sont pas traitées comme autant d'erreurs de transcription à corriger arbitrairement.

## 4. Reproductibilité et archives

Les quatre vérificateurs relisent les sources directement, sans importer ou appeler les fonctions des extracteurs auteurs. Les volets04a, 04b et04d ont été vérifiés par un autre agent ; le directeur de mission a contrôlé04c après sa rédaction par un spécialiste. Une seconde lecture du même document améliore le contrôle de transcription, mais ne constitue pas une deuxième mesure statistique indépendante.

Les cinq scripts analytiques du lot ont été réexécutés : **36 CSV d'indicateurs et de registres sont reproduits octet pour octet**. Le contrôle des métadonnées rapproche **37 archives primaires** de leur empreinte ; les gzip concernés sont aussi vérifiés après décompression. La commande de restauration vérifie en outre **31 documents du cache et leurs textes**, dont certains figurent déjà parmi les 37 : ces décomptes ne s'additionnent pas. Les **104 fichiers bruts versionnés** du lot ont été rapprochés octet pour octet de l'index Git. Les règles d'attributs préservent les octets des sorties référencées par empreinte et fixent les LF des notes assemblées, afin de ne pas invalider les manifestes lors d'un clonage sur un autre système.

```powershell
python -I scripts/restore_lot2_sources.py
# Si le cache documentaire est absent :
python -I scripts/restore_lot2_sources.py --download

python -I scripts/00_verification_04a_lot2.py
python -I scripts/00_verification_04b_lot2.py
python -I scripts/00_verification_04c_lot2.py
python -I scripts/00_verification_04d_lot2.py
python -I scripts/00_verification_lot2.py
```

Le contrôle des empreintes certifie la stabilité des fichiers lus ; il ne valide pas toutes les conventions économiques de leurs auteurs. La restauration ne substitue pas une distribution modifiée à l'archive attendue : elle signale un échec ou une empreinte différente pour revue.

Notes individuelles : [04a](00_verification_04a_lot2.md), [04b](00_verification_04b_lot2.md), [04d](00_verification_04d_lot2.md). Le contrôle04c est décrit ligne par ligne dans son CSV et son script séparés.

## 5. Limite de cette étape

Ce contrôle ne clôt pas la phase5 du cahier des charges. Les économies finales, les 25 fiches A–M, les viviers disjoints, les départs, les coûts de transition, les sensibilités et les quatre scénarios devront faire l'objet d'une autre contre-expertise. Aucun montant national n'est validé par les seuls contrôles de ce lot.
