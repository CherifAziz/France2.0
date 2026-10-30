# Réforme R22 — Mutualiser les fonctions support des caisses de Sécurité sociale

Vivier : **V_OPS** (Organismes de protection sociale (droit privé, financement public prédominant)) · ordre d'application **30** · début **2028**, durée **5 ans** · confiance **faible**.

**A. Problème identifié.** **[FAIT]** Les régimes de Sécurité sociale portent **7,229 Md€** de frais de gestion de la santé en 2025 ; l'administration de tous les régimes de protection sociale représente **1,29 % du PIB** en 2023 (ESSPROS). La part des fonctions support n'est pas publiée dans les sources lues.

**B. Organisation actuelle.** Réseaux de caisses par branche et par territoire, chacun avec ses fonctions support.

**C. Comparaison internationale.** **[FAIT]** Suède : gains des services partagés souvent réinvestis. Aucun précédent mesuré propre à la Sécurité sociale n'a été ouvert.

**D. Réforme proposée.** Centres de services partagés interbranches (paie, achats, immobilier, informatique non métier) ; non-remplacement des postes libérés.

**E. Effectifs concernés.** Vivier organismes de protection sociale : 162 623 personnes.

**F. Réduction envisageable.** **[HYPOTHÈSE]** 1 / 2 / 4 / 6 %. Taux appliqués au reliquat du vivier : 1,00 % / 2,00 % / 4,00 % / 6,00 % (prudent / intermédiaire / ambitieux / radical). Répartition : non-remplacement 100 %, redéploiement 0 %, suppression indemnisée 0 %, transfert 0 %.

**G. Économies.** Résultats du moteur financier (`modele/modele.py`), en M€ 2026 constants, par écart à une référence qui remplace tous les départs. Le non-remplacement est valorisé au coût d'entrée hors pension, croissant de 1 % par an jusqu'au coût moyen ; les postes ne disparaissent qu'au rythme des départs à la retraite du vivier.

| Indicateur | Prudent | Intermédiaire | Ambitieux | Radical |
|---|---:|---:|---:|---:|
| ETP visés (cible) | 1 626 | 3 220 | 6 375 | 9 367 |
| Postes en moins en 2036 | 1 626 | 3 220 | 6 375 | 9 367 |
| ETP redéployés | 0 | 0 | 0 | 0 |
| Cible non réalisée en 2036 (ETP) | 0 | 0 | 0 | 0 |
| Économie nette 2036 (M€) | 76,0 | 150,6 | 298,1 | 438,0 |
| Cumul net 2027-2031 (M€) | −27,2 | −53,9 | −106,7 | −156,8 |
| Cumul net 2027-2036 (M€) | 338,4 | 670,1 | 1 326,6 | 1 949,3 |
| Cumul consolidé APU 2027-2036 (M€) | 169,8 | 336,3 | 665,7 | 978,2 |
| Investissement total (M€) | 143,3 | 283,7 | 561,6 | 825,2 |
| Coût récurrent à terme (M€/an) | 0,0 | 0,0 | 0,0 | 0,0 |

**H. Investissements nécessaires.** **[HYPOTHÈSE de convention]** Deux années d'économie brute.

**I. Conséquences sur le service.** Peu d'effet direct sur les assurés si les métiers de prestation sont préservés.

**J. Contraintes.** Conventions d'objectifs et de gestion ; gouvernance paritaire.

**K. Calendrier.** 2028-2032.

**L. Niveau de confiance.** **Faible.** Gisement non mesuré.

**Indicateur de validation à 2-3 ans.** Coût de support par agent ; ETP support des caisses publiés dans les conventions d'objectifs.

**M. Sources et calculs.**

- [Note 04c](../04c_sante_protection_sociale.md)
- [Note 05](../05_reformes_etrangeres.md)

Calculs : Taux en part du reliquat. Paramètres nationaux : [hypotheses.json](../../modele/hypotheses.json) ; ligne `R22` de [catalogue_reformes.csv](../../data/reformes/catalogue_reformes.csv) ; vivier dans [registre_viviers.csv](../../data/reformes/registre_viviers.csv). Reproduction : `python -I scripts/11_catalogue.py`.
