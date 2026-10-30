# Réforme R17 — Mutualiser les fonctions support entre communes et intercommunalités

Vivier : **V_FPT_ADM** (Filière administrative de la fonction publique territoriale) · ordre d'application **30** · début **2027**, durée **6 ans** · confiance **moyen**.

**A. Problème identifié.** **[FAIT]** **34 871 communes** sont déjà membres d'un EPCI ou de la métropole de Lyon ; seules quatre sont isolées. La coopération existe, mais les fonctions support (paie, achats, finances, RH) restent souvent gérées commune par commune. Le rapport Ravignon compte **31 040 agents RH** en 2021, et 44 640 avec le CNFPT et les centres de gestion.

**B. Organisation actuelle.** Communes (1 041 290 agents), EPCI à fiscalité propre (309 577) et autres structures intercommunales (91 825), fin 2024. Services communs facultatifs.

**C. Comparaison internationale.** **[ESTIMATION]** Danemark : −10,4 % de coûts administratifs relatifs quatre ans après les fusions, gains réaffectés. Le rapport Ravignon suppose 5 à 10 % de gains sur la fonction RH.

**D. Réforme proposée.** Services communs obligatoires au-delà d'un seuil de population pour la paie, la comptabilité, les marchés et la gestion RH ; non-remplacement des postes support libérés.

**E. Effectifs concernés.** Vivier filière administrative FPT : 444 817 ETP.

**F. Réduction envisageable.** **[HYPOTHÈSE]** 1 / 3 / 5 / 8 %. Le scénario radical approche l'économie administrative danoise (10,4 %) appliquée à la seule filière administrative. Taux appliqués au reliquat du vivier : 1,00 % / 3,00 % / 5,00 % / 8,00 % (prudent / intermédiaire / ambitieux / radical). Répartition : non-remplacement 100 %, redéploiement 0 %, suppression indemnisée 0 %, transfert 0 %.

**G. Économies.** Résultats du moteur financier (`modele/modele.py`), en M€ 2026 constants, par écart à une référence qui remplace tous les départs. Le non-remplacement est valorisé au coût d'entrée hors pension, croissant de 1 % par an jusqu'au coût moyen ; les postes ne disparaissent qu'au rythme des départs à la retraite du vivier.

| Indicateur | Prudent | Intermédiaire | Ambitieux | Radical |
|---|---:|---:|---:|---:|
| ETP visés (cible) | 4 448 | 13 145 | 21 578 | 31 805 |
| Postes en moins en 2036 | 4 448 | 13 145 | 21 578 | 31 805 |
| ETP redéployés | 0 | 0 | 0 | 0 |
| Cible non réalisée en 2036 (ETP) | 0 | 0 | 0 | 0 |
| Économie nette 2036 (M€) | 159,8 | 472,2 | 775,2 | 1 142,3 |
| Cumul net 2027-2031 (M€) | 17,5 | 51,7 | 84,9 | 122,6 |
| Cumul net 2027-2036 (M€) | 788,4 | 2 329,7 | 3 824,3 | 5 604,5 |
| Cumul consolidé APU 2027-2036 (M€) | 407,6 | 1 204,5 | 1 977,3 | 2 893,3 |
| Investissement total (M€) | 299,5 | 885,2 | 1 453,1 | 2 141,7 |
| Coût récurrent à terme (M€/an) | 0,0 | 0,0 | 0,0 | 0,0 |

**H. Investissements nécessaires.** **[HYPOTHÈSE de convention]** Deux années d'économie brute.

**I. Conséquences sur le service.** Éloignement possible des services de gestion des petites communes ; professionnalisation des achats et de la paie.

**J. Contraintes.** Libre administration ; harmonisation des régimes indemnitaires entre employeurs.

**K. Calendrier.** 2027-2032, par seuils de population.

**L. Niveau de confiance.** **Moyen.** Mécanisme et précédent documentés ; risque de réaffectation des gains.

**Indicateur de validation à 2-3 ans.** Dépenses de fonctionnement et ETP administratifs des blocs communaux à périmètre constant ; coûts de paie et d'achat par unité.

**M. Sources et calculs.**

- [Note 04d](../04d_territoires_fonctions_support.md)
- [Note 05](../05_reformes_etrangeres.md)
- [Note 01](../01_emploi_public_france.md)
- [Blom-Hansen, Houlberg, Serritzlew, 2014, PDF 13](https://joeornstein.github.io/pols-4641/readings/Blom-Hansen%2C%20Houlberg%2C%20Serritzlew%20-%202014%20-%20Size%2C%20Democracy%2C%20and%20the%20Economic%20Costs%20of%20Running%20the%20Political%20System.pdf)
- [Houlberg, Politik, 2016](https://tidsskrift.dk/politik/article/view/27404)
- [Données 01 — effectifs par employeur fin 2024](../../data/france/01_effectifs_employeurs.csv)

Calculs : Taux en part du reliquat. Paramètres nationaux : [hypotheses.json](../../modele/hypotheses.json) ; ligne `R17` de [catalogue_reformes.csv](../../data/reformes/catalogue_reformes.csv) ; vivier dans [registre_viviers.csv](../../data/reformes/registre_viviers.csv). Reproduction : `python -I scripts/11_catalogue.py`.
