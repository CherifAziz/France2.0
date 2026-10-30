# Contre-vérification du troisième lot

Contrôle arrêté au **30 octobre 2026**. Le lot couvre les réformes étrangères évaluées, les structures et précédents français, la simplification, l'IA en France, les preuves internationales sur l'IA et l'audit des propositions chiffrées. Cette étape vérifie la **transcription et la localisation des chiffres décisifs** dans leurs sources primaires. Elle ne valide pas les futures économies nationales.

## 1. Résultat

**98 contrôles indépendants ont été effectués. Aucun chiffre des notes n'est contredit par sa source.** Trois corrections de formulation ou de localisation ont été reportées dans les notes 08 et 09. Une anomalie a été trouvée dans une source primaire : elle est documentée, et la note 06 ne la reprend pas. Trois limites d'accès restent ouvertes.

| Volet | Contrôles | Résultat | Sources primaires relues |
|---|---:|---|---|
| 05 — Réformes étrangères | 20 | 12 conformes, 3 bornes strictes (« plus de »), 5 conformes avec réserve d'arrondi (Japon, résidu de 1 MJPY) | Rapports d'audit canadiens, Trésor canadien, Agence numérique japonaise et autres PDF/HTML du cache 05 |
| 06–07 — Structures et simplification | 20 | 19 confirmés dans leur champ, dont 4 avec qualification ; 1 non vérifiable (rapport CNEN inaccessible) | Jaunes opérateurs 2026 et 2027, Sénat, Cour des comptes, OFGL, AN, inspections RGPP, DINUM |
| 08–09 — IA France et international | 38 | 31 confirmés, 3 calculs confirmés, 1 limite d'accès, 3 confirmations avec réserve | Rapport IGF–IGAS–IGA (709 p.), DITP, DINUM, Insee, iFRAP, Commission, Sénat, études académiques et évaluations publiques étrangères |
| 10 — Audit des propositions | 20 | 7 confirmés, 3 calculs confirmés, 3 cohérences avec 06, 6 confirmés sur un projet de loi, 1 limite d'accès ; aucun écart | Instantané HTML de budget2027.fr, jaune opérateurs, dossier PLF 2027, fiche éditeur |

Le CSV fusionné `data/risques/verification_chiffres_lot3.csv` conserve les **98 lignes** avec valeur publiée, passage source, unité, année, URL, localisation, statut et remarque. `data/risques/verification_lot3_resume.json` donne les effectifs par statut et les empreintes des quatre fichiers de contrôle. Certaines lignes vérifient un ensemble de valeurs ou un calcul : « 98 contrôles » ne signifie pas 98 observations statistiques indépendantes.

## 2. Corrections et anomalies

**Note 08, pilote « L'Assistant ».** La note parlait d'un pilote de « 10 000 licences ». Le communiqué DINUM du 16 juin 2026 et la fiche produit parlent de **10 000 agents**. La formulation est corrigée ; aucun chiffre ne change. Trace : **V0809-15**.

**Note 08, coût de Sirhen.** Les **480 M€** sont une déclaration orale à l'audition de la Cour devant le Sénat en 2020. Le même rapport sénatorial cite Sirhen pour **188,1 M€** comme valeur comptable d'un projet en service. Les deux montants ne mesurent pas la même chose ; la note le précise désormais. Trace : **V0809-20**.

**Note 09, évaluation DBT.** Les 1 000 licences figurent p.6-7 du PDF, et non p.4-5. La localisation est corrigée. Trace : **V0809-29**.

**Anomalie primaire, jaune opérateurs 2027.** Le commentaire p.24 annonce une baisse apparente des crédits d'intervention de 28 M€. Le tableau donne pourtant une **hausse de 27,585 M€**. La note 06 retient le tableau et ne reprend pas le signe erroné du commentaire. Trace : **V0607-06**, note [06–07](00_verification_06_07_lot3.md).

Un contrôle a aussi écarté une fausse réserve. Les **430 000 emplois** de l'iFRAP sont bien la part publique (53,7 %) des 800 000 emplois automatisables, public et privé confondus, de l'étude Roland Berger reprise par l'iFRAP. La note 08 les présentait correctement. Trace : **V0809-17**.

## 3. Réserves confirmées

- **Annonces et réalisations.** Les 140 Md€ du site politique, les 2 Md€ d'économies d'agences, les 17 Md€ européens « achieved so far » et les 5 Md€/an du choc de simplification sont des annonces ou des potentiels. Les contrôles confirment leur transcription, pas leur réalisation.
- **Budgets d'opérateurs.** Les comptes Anah, Ademe et France Travail sont des **budgets initiaux 2026** en milliers d'euros. Les interventions et missions d'accompagnement n'y sont pas des frais de siège. Les contrôles V10-09 à V10-11 relisent le même original que la note 06 : ce sont des contrôles de cohérence, pas des observations nouvelles.
- **IA.** L'exposition de 20 % des agents, les 226/300/241 « ETP » de France Travail et les gains de tâche des études étrangères sont confirmés tels que publiés. Aucun n'est une mesure de postes supprimés : la note 162 du rapport dit explicitement que les estimations de France Travail n'ont pas réduit les effectifs.
- **Paramètres par tâche.** Les triplets METR, Nabla et DAX de `09_parametres_taches.csv` inversent exactement les intervalles de confiance primaires (V0809-27). Ce sont des sensibilités locales, pas trois scénarios nationaux.
- **Bornes et arrondis.** Les « plus de 233 000 transactions » Phénix sont des bornes inférieures ; les montants japonais présentent un résidu publié de 1 MJPY ; les 13,04 %, 120,12 millions et 50 000 €/poste sont des calculs conditionnels.

## 4. Limites d'accès

- **CNEN (V0607-14).** L'accueil et l'URL du rapport 2023 renvoient la même page de maintenance. Le coût récent des normes des collectivités reste non vérifiable dans ce lot.
- **AI Act opposable (V0809-19).** Le Journal officiel et la version consolidée ont répondu HTTP 202 avec un corps vide, conservé tel quel. Seul le calendrier annoncé par la Commission est confirmé.
- **Livre « Le Casse du siècle » (V10-20).** Le lecteur archivé ne fournit qu'une coquille HTML. Les métadonnées de l'éditeur sont confirmées, pas le contenu.

D'autres documents restent non lus et sont signalés comme tels dans les notes : enquête SNDGCT, bilan DAE interne, texte intégral de l'essai sur les scribes, article Choi et al., rapport intégral Robodebt.

## 5. Reproductibilité et archives

Les quatre vérificateurs relisent les sources directement, sans importer ni appeler les extracteurs auteurs. Les contrôles 05, 06–07 et 10 ont été produits le 28 octobre ; celui de 06–07 précise que son vérificateur n'a rédigé aucune des deux notes. Le contrôle 08–09 a été écrit lors de la reprise du 30 octobre 2026 par un agent qui n'avait pas rédigé ces notes ; ses trois corrections de forme ont ensuite été reportées dans les notes. Une seconde lecture du même document améliore le contrôle de transcription ; elle ne constitue pas une seconde mesure statistique.

Les trois vérificateurs existants ont été réexécutés le 30 octobre : ils reproduisent leurs CSV et notes octet pour octet. Le manifeste `sources/lot3_manifestes_cache.json` recense **78 corps HTTP** du cache 05–10, tous rapprochés de leur empreinte SHA-256. Les chapitres 06 et 07 reposent principalement sur des bruts versionnés dans `data/raw/06` et `data/raw/07`.

```powershell
python -I scripts/restore_lot3_sources.py
# Si le cache documentaire est absent :
python -I scripts/restore_lot3_sources.py --download

python -I scripts/00_verification_05_lot3.py
python -I scripts/00_verification_06_07_lot3.py
python -I scripts/00_verification_08_09_lot3.py
python -I scripts/00_verification_10_lot3.py
python -I scripts/00_verification_lot3.py
```

Notes individuelles : [06–07](00_verification_06_07_lot3.md), [08–09](00_verification_08_09_lot3.md), [10](00_verification_10_lot3.md). Le contrôle 05 est décrit ligne par ligne dans son CSV et son script.

## 6. Limite de cette étape

Ce contrôle ne clôt pas la phase 5 du cahier des charges. Les 25 fiches de réforme A–M, le registre disjoint des viviers, les départs, les coûts de transition, les sensibilités et les quatre scénarios feront l'objet d'une contre-expertise distincte d'au moins 40 chiffres décisifs. Aucun montant national n'est validé par les seuls contrôles de ce lot.
