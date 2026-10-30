# Réforme R04 — Revoir les missions des opérateurs et regrouper ceux qui se recouvrent

Vivier : **V_FPE_AUTRES** (Autres corps administratifs et techniques de la FPE (ministères et EPA, dont opérateurs)) · ordre d'application **10** · début **2027**, durée **5 ans** · confiance **moyen**.

**A. Problème identifié.** **[FAIT]** Le jaune du PLF 2027 compte **423 opérateurs** (431 au PLF 2026), et **537 organismes nationaux non opérateurs**. Les concours publics atteignent **72,572 Md€**, dont l'essentiel finance des missions et des aides. Les opérateurs rémunèrent **481 336 ETPT** au total prévisionnel 2027.

**B. Organisation actuelle.** Opérateurs de statuts variés (universités, organismes de recherche, agences d'intervention, établissements de service). Leurs fonctions de gestion ne sont pas comptabilisées de façon homogène ; aucune base ne donne leurs effectifs administratifs par opérateur.

**C. Comparaison internationale.** **[FAIT]** Au Canada, la Program Review a réduit d'environ **45 000 personnes** l'emploi fédéral en cinq ans, dont **8 000 transferts** hors périmètre, avec 1 Md CAD de restructuration. En Nouvelle-Zélande, la baisse récente des ETP s'est accompagnée d'une hausse de **7,18 %** des dépenses externes.

**D. Réforme proposée.** Revue de chaque opérateur : missions, base légale, coûts de gestion, recouvrements avec d'autres organismes ; fusion ou réintégration lorsque deux organismes servent les mêmes usagers ; non-remplacement des postes de gestion devenus doubles, redéploiement des autres.

**E. Effectifs concernés.** Vivier « autres administratifs et techniques de l'État » : **231 659 ETP** (corps administratifs et techniques A/B/C de la FPE, 378 909 PP, moins DGFiP et administration scolaire, × 0,9989). Inclut les administratifs des opérateurs.

**F. Réduction envisageable.** **[HYPOTHÈSE]** 0,5 / 1,5 / 3 / 6 % du vivier, dont 80 % par non-remplacement et 20 % redéployés. Repère : le passage de 431 à 423 opérateurs s'est fait par regroupements et reprises de missions, sans économie nette publiée ; les 2 Md€ d'économies d'agences annoncés en 2025 ne sont pas validés par le SGG. Taux appliqués au reliquat du vivier : 0,50 % / 1,50 % / 3,00 % / 6,00 % (prudent / intermédiaire / ambitieux / radical). Répartition : non-remplacement 80 %, redéploiement 20 %, suppression indemnisée 0 %, transfert 0 %.

**G. Économies.** Résultats du moteur financier (`modele/modele.py`), en M€ 2026 constants, par écart à une référence qui remplace tous les départs. Le non-remplacement est valorisé au coût d'entrée hors pension, croissant de 1 % par an jusqu'au coût moyen ; les postes ne disparaissent qu'au rythme des départs à la retraite du vivier.

| Indicateur | Prudent | Intermédiaire | Ambitieux | Radical |
|---|---:|---:|---:|---:|
| ETP visés (cible) | 1 158 | 3 475 | 6 950 | 13 900 |
| Postes en moins en 2036 | 927 | 2 780 | 5 560 | 11 120 |
| ETP redéployés | 232 | 695 | 1 390 | 2 780 |
| Cible non réalisée en 2036 (ETP) | 0 | 0 | 0 | 0 |
| Économie nette 2036 (M€) | 43,8 | 131,3 | 262,6 | 525,2 |
| Cumul net 2027-2031 (M€) | 22,1 | 66,2 | 132,3 | 264,7 |
| Cumul net 2027-2036 (M€) | 236,6 | 709,8 | 1 419,6 | 2 839,2 |
| Cumul consolidé APU 2027-2036 (M€) | 125,2 | 375,6 | 751,3 | 1 502,6 |
| Investissement total (M€) | 81,6 | 244,9 | 489,8 | 979,6 |
| Coût récurrent à terme (M€/an) | 0,0 | 0,0 | 0,0 | 0,0 |

**H. Investissements nécessaires.** **[HYPOTHÈSE de convention]** Deux années d'économie brute (systèmes d'information, déménagements, harmonisation des statuts).

**I. Conséquences sur le service.** Risque de perte d'expertise et de rupture de service pendant les fusions ; amélioration possible de la lisibilité pour les usagers.

**J. Contraintes.** Lois constitutives des opérateurs ; statuts et rémunérations à harmoniser ; résistance des tutelles.

**K. Calendrier.** Revue 2027 ; décisions par vagues 2028-2031.

**L. Niveau de confiance.** **Moyen.** L'existence de recouvrements est documentée ; leur coût de gestion ne l'est pas.

**Indicateur de validation à 2-3 ans.** Nombre d'opérateurs et d'ETPT sous plafond, à périmètre de missions constant ; coût de gestion par euro d'intervention ; délais de traitement des usagers.

**M. Sources et calculs.**

- [Note 06](../06_doublons_structures.md)
- [Note 05](../05_reformes_etrangeres.md)
- [Jaune « Opérateurs de l'État », PLF 2027](https://www.budget.gouv.fr/documentation/file-download/34432)
- [DGAFP, rapport annuel 2026, caractéristiques des postes](https://www.fonction-publique.gouv.fr/files/files/publications/vue-rapport-annuel/2026/ra_2026_postes.zip)

Calculs : Base 378 909 − 94 569 (DGFiP) − 52 432 (scolaire) = 231 908 PP ; × 0,9989 (EQTP/PP FPE 2024) = 231 659 ETP. Paramètres nationaux : [hypotheses.json](../../modele/hypotheses.json) ; ligne `R04` de [catalogue_reformes.csv](../../data/reformes/catalogue_reformes.csv) ; vivier dans [registre_viviers.csv](../../data/reformes/registre_viviers.csv). Reproduction : `python -I scripts/11_catalogue.py`.
