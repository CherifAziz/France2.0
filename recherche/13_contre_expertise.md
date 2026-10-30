# 13 — Contre-expertise du catalogue et des scénarios

Phase 5 arrêtée au **30 octobre 2026**. Elle comprend deux volets : une **vérification indépendante de 47 chiffres décisifs** du catalogue, des hypothèses et des scénarios, relus dans leurs sources primaires ; et une **revue critique** (« équipe B ») qui cherche les faiblesses du raisonnement et chiffre leur effet. Le vérificateur `scripts/00_verification_phase5.py` lit directement les classeurs et PDF primaires. Il n'importe ni le moteur ni les scripts du catalogue : il ne lit leurs sorties que comme valeurs à contrôler.

## 1. Synthèse

1. **47 contrôles, aucun écart.** 27 chiffres sont confirmés dans leur source primaire, 18 calculs refaits indépendamment, et 2 confirmations portent une réserve. Un test de mutation vérifie que le contrôle n'est pas vide : une base de vivier faussée de 83 ETP fait échouer 5 contrôles.
2. **Une réserve de champ change la lecture du vivier de l'État.** Les trois lignes de corps administratifs et techniques de la FPE totalisent les **seuls fonctionnaires** (1 501 736). Les contractuels administratifs de l'État ne sont donc pas dans le vivier. Cela le sous-estime légèrement, mais confirme qu'il est disjoint des viviers de droit privé (France Travail, organismes de protection sociale).
3. **Le moteur est juste.** Une simulation écrite séparément retrouve exactement la réforme R17 en scénario prudent (cible de 4 448,2 ETP, 159,80 M€ nets en 2036, 788,36 M€ cumulés). Les synthèses égalent la somme des 30 réformes, et les capacités de départs comme les sept verdicts de seuils sont reproduits.
4. **L'équipe B réduit fortement l'estimation centrale.** Les fiches à confiance faible portent **66 %** des postes du scénario intermédiaire. Pondéré par une probabilité de réussite (0,3 pour une fiche à confiance faible, 0,6 pour une fiche à confiance moyenne), le scénario intermédiaire passe de **56 142 à 22 863 postes** et de **2,52 à 1,06 Md€** d'économie nette en 2036.
5. **Les verdicts de seuils sont renforcés.** Aucune objection de l'équipe B n'augmente les résultats ; plusieurs les réduisent. 500 000 postes et plus restent incompatibles avec les départs administratifs disponibles.

## 2. Vérification des chiffres décisifs

Détail ligne par ligne : `data/risques/verification_phase5.csv`.

| Thème | Contrôles | Ce qui a été relu | Résultat |
|---|---:|---|---|
| Bases des viviers | 13 | Corps FPE (figure 2, B11/B26/B37), filières FPT (S28) et FPH (T25), organismes de protection sociale (U22), DGFiP (PDF p.46-47), DEPP (3.1 D27/L27), plafond France Travail (jaune p.70), EQTP Insee (E11:E13), effectifs physiques, bases recalculées | 12 confirmés, 1 avec réserve de champ (V5-04) |
| Départs | 4 | Pensions 2025 (E5/E10/E13), fonctionnaires par versant, taux par vivier, sortants fonctionnaires (H22) et rapport 1,605 | Confirmés |
| Coûts | 5 | PAP 156 p.50 et PAP 218 p.24 (12 valeurs), pondération A/B/C, proxy FPT/FPH (salaires B11/B28), charges hors pension (17,6 %) | Confirmés |
| Faits des fiches | 15 | ISORA France 2023, taux de R01 et R02, ETPT DGFiP 2015-2025, dépenses IA de France Travail (p.618), équivalents ETP (p.236), Ravignon (p.44, 96, 100), Sénat (p.217, 231), DAE (p.46, 48, 87) et assiette de R28, RGPP 2010-2011, HCAAM (p.79-80), opérateurs (p.12, 24), PLF 2027 (p.58-59), employeurs territoriaux | 14 confirmés, 1 avec réserve |
| Moteur et seuils | 10 | R17 refaite, convention d'investissement, synthèses = sommes, capacités, verdicts, rapports 800 000 / capacités, total des viviers, taux affichés dans les 30 fiches, ordres uniques | Confirmés |

**Réserves.**

- **V5-04 — champ du vivier de l'État.** Le total de la figure des corps (1 501 736) est celui des fonctionnaires de l'État. Les contractuels administratifs, dont le nombre n'est pas isolé dans les sources lues, ne sont pas dans `V_FPE_AUTRES`. En sens inverse, la DGFiP (dont 5 910 contractuels) et la filière scolaire soustraites de ces lignes contiennent des contractuels : le vivier est donc un peu sous-estimé. Le registre est corrigé pour le dire.
- **V5-29 — Ravignon.** Le détail du tableau 10 (7,444 Md€) n'est pas extrait du PDF par la bibliothèque ; le texte de la p.44 donne 7,4 Md€, cohérent.

**Indépendance.** Le contrôle relit les mêmes documents que les auteurs : il vérifie la transcription et les calculs, pas la justesse des sources. Les contrôles du lot 3 (98 chiffres) restent valables pour les faits que les fiches reprennent des notes.

## 3. Revue critique (équipe B)

Chaque objection est relancée dans le moteur quand elle se chiffre (`scripts/13_equipe_b.py`, `data/reformes/13_equipe_b.csv`).

| Variante | Prudent | Intermédiaire | Ambitieux | Radical |
|---|---:|---:|---:|---:|
| Catalogue central : postes 2036 | 11 106 | 56 142 | 120 250 | 194 476 |
| — économie nette 2036 (M€) | 618 | 2 517 | 5 280 | 8 430 |
| Pondéré par la confiance : postes 2036 | 5 449 | 22 863 | 47 460 | 86 050 |
| — économie nette 2036 (M€) | 318 | 1 059 | 2 148 | 3 785 |
| Seulement les 6 fiches à confiance moyenne : postes 2036 | 7 047 | 19 445 | 34 373 | 56 355 |
| Sans règles descendantes (R12, R15) : postes 2036 | 11 106 | 56 142 | 114 428 | 180 458 |
| Sans R01 (risque de double compte avec la référence) : postes 2036 | 10 587 | 55 107 | 118 186 | 191 388 |

**O1 — Les gisements sont des hypothèses.** 24 fiches sur 30 sont à confiance faible et portent 66 % des postes du scénario intermédiaire (36 941 sur 56 142), 73 % du radical. **[HYPOTHÈSE]** Pondérer chaque fiche par une probabilité de réussite (0,3 en confiance faible, 0,6 en confiance moyenne) donne une espérance de **22 863 postes et 1,06 Md€ par an** en scénario intermédiaire. Ces probabilités ne sont pas mesurées ; elles traduisent l'écart, documenté en note 05, entre annonces et économies vérifiées (19,67 % du potentiel pour Digital Post, 33 à 40 % de net pour la RGPP).

**O2 — Le vivier de l'État a un champ imparfait.** Il ne compte que des fonctionnaires et mêle administratifs et techniques. Les deux biais jouent en sens contraires ; leur solde n'est pas mesurable avec les sources lues. Les cibles étant proportionnelles à la base, une erreur de 10 % sur la base déplace d'autant les postes des fiches R04 à R12.

**O3 — La référence peut déjà contenir une partie des gains.** La DGFiP a perdu 15 % de ses ETPT entre 2015 et 2025 ; si cette tendance figure dans la trajectoire budgétaire de référence, R01 la compterait deux fois. Retirer R01 enlève 519 à 3 088 postes selon le scénario.

**O4 — Les règles descendantes rapportent peu.** Sans R12 (un départ sur deux) ni R15 (suppression d'un échelon), le radical perd 14 018 postes mais **gagne** 675 M€ d'économie cumulée sur dix ans : ces deux réformes coûtent davantage (investissement, rétrocession) qu'elles ne rapportent dans l'horizon.

**O5 — Le moteur ne modélise pas de rebond.** Le Royaume-Uni a regagné 36,2 % d'effectifs après 2016 et l'Irlande a retrouvé 317 495 WTE dès 2017 après −9,6 %. Les postes du catalogue sont donc des réductions **maximales**, non des réductions durables garanties.

**O6 — Les investissements sont sans doute sous-estimés.** La convention de deux années d'économie brute s'inspire du meilleur cas observé (timbre électronique). Phénix et Sirhen montrent des dépassements d'un autre ordre. Doubler les investissements réduit d'un tiers l'économie cumulée du scénario intermédiaire (de 12,6 à 8,7 Md€, note 12).

**O7 — Les coûts des organismes de droit privé sont des proxys.** Organismes de protection sociale et France Travail reprennent le coût de la FPE, faute de donnée publiée ; la sensibilité ±20 % de la note 12 couvre cet écart sans changer les ordres de grandeur.

**O8 — Le taux de départ est homogène par versant.** La pyramide des âges des filières administratives n'est pas publiée dans les sources lues : si ces filières sont plus âgées que la moyenne, la capacité de départs est sous-estimée, et inversement. Le verdict « incompatible » pour 500 000 postes résiste même en ne remplaçant aucune sortie de fonctionnaire (434 949 en dix ans).

**O9 — La lecture consolidée est plus basse.** Pour les administrations publiques dans leur ensemble, l'économie 2036 est environ un tiers plus faible que pour l'employeur (1,71 contre 2,52 Md€ en intermédiaire), car cotisations, CSG et retenues reviennent aux APU.

## 4. Conclusion de la contre-expertise

- **Fourchette défendable.** En 2036, entre **5 000 et 23 000 postes en moins**, pour **0,3 à 1,1 Md€ d'économie nette annuelle**, soit les espérances pondérées des scénarios prudent et intermédiaire.
- **Haut de fourchette plausible mais non démontré.** Le scénario intermédiaire non pondéré (56 142 postes, 2,5 Md€) suppose que toutes les réformes réussissent.
- **Scénarios ambitieux et radical : hypothèses de travail.** Ils servent à tester les limites ; aucune preuve observée ne les étaye.
- **Seuils inchangés.** 50 000 et 100 000 restent conditionnels ; 200 000 non démontré ; 500 000, 800 000, 1 million et 1,5 million incompatibles dans le périmètre administratif.
- **Pas de correction chiffrée.** Le registre précise désormais le champ du vivier de l'État et la disjonction des viviers de droit privé.

## 5. Reproduction

```powershell
python -I scripts/00_verification_phase5.py
python -I scripts/13_equipe_b.py
```

Le vérificateur réécrit `data/risques/verification_phase5.csv` et renvoie un code d'erreur au premier écart. Il exige les caches `data/cache/01c`, `02`, `04c`, `04d`, `06`, `08` et `10` ; leur restauration passe par les scripts `restore_lot*_sources.py`.
