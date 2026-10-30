# Réforme R14 — Désigner un chef de file unique par politique cofinancée entre collectivités

Vivier : **V_FPT_ADM** (Filière administrative de la fonction publique territoriale) · ordre d'application **10** · début **2028**, durée **5 ans** · confiance **faible**.

**A. Problème identifié.** **[ESTIMATION externe]** Le rapport Ravignon valorise l'enchevêtrement des compétences à **7,444 Md€ par an**, dont **1,857 Md€** pour patrimoine, RH et gestion financière. Ce montant inclut de la coordination nécessaire et ne mesure pas des crédits supprimables. Il repose sur 178 collectivités répondantes, dont 11 intercommunalités.

**B. Organisation actuelle.** Communes, EPCI, départements et régions interviennent ensemble sur de nombreux dispositifs, avec instructions et reportings parallèles. La DGCL recense 34 875 communes, 1 252 EPCI à fiscalité propre et 8 113 syndicats au 1er janvier 2026.

**C. Comparaison internationale.** **[ESTIMATION]** Au Danemark, la réforme de 2007 a ramené les communes de 271 à 98 et supprimé les comtés : l'économie administrative relative atteint **10,4 %** en 2011 selon une étude en différences de différences, mais une synthèse de 2016 ne trouve **pas d'économie sur les dépenses municipales totales**.

**D. Réforme proposée.** Pour chaque politique cofinancée, un seul instructeur, un seul dossier et un seul reporting ; les autres financeurs délèguent ou se retirent ; non-remplacement des postes d'instruction doublonnés.

**E. Effectifs concernés.** Vivier filière administrative FPT : **444 817 ETP** (453 224 PP × 0,9815, rapport EQTP/PP de la FPT 2024).

**F. Réduction envisageable.** **[HYPOTHÈSE]** 0 / 1 / 2 / 4 %. Le précédent danois montre que des gains administratifs peuvent être réaffectés plutôt qu'économisés. Taux appliqués au reliquat du vivier : 0,00 % / 1,00 % / 2,00 % / 4,00 % (prudent / intermédiaire / ambitieux / radical). Répartition : non-remplacement 100 %, redéploiement 0 %, suppression indemnisée 0 %, transfert 0 %.

**G. Économies.** Résultats du moteur financier (`modele/modele.py`), en M€ 2026 constants, par écart à une référence qui remplace tous les départs. Le non-remplacement est valorisé au coût d'entrée hors pension, croissant de 1 % par an jusqu'au coût moyen ; les postes ne disparaissent qu'au rythme des départs à la retraite du vivier.

| Indicateur | Prudent | Intermédiaire | Ambitieux | Radical |
|---|---:|---:|---:|---:|
| ETP visés (cible) | 0 | 4 448 | 8 896 | 17 793 |
| Postes en moins en 2036 | 0 | 4 448 | 8 896 | 17 793 |
| ETP redéployés | 0 | 0 | 0 | 0 |
| Cible non réalisée en 2036 (ETP) | 0 | 0 | 0 | 0 |
| Économie nette 2036 (M€) | 0,0 | 159,0 | 318,0 | 636,0 |
| Cumul net 2027-2031 (M€) | 0,0 | −56,9 | −113,8 | −227,6 |
| Cumul net 2027-2036 (M€) | 0,0 | 707,5 | 1 415,1 | 2 830,1 |
| Cumul consolidé APU 2027-2036 (M€) | 0,0 | 355,1 | 710,1 | 1 420,2 |
| Investissement total (M€) | 0,0 | 299,5 | 599,1 | 1 198,2 |
| Coût récurrent à terme (M€/an) | 0,0 | 0,0 | 0,0 | 0,0 |

**H. Investissements nécessaires.** **[HYPOTHÈSE de convention]** Deux années d'économie brute.

**I. Conséquences sur le service.** Lisibilité accrue pour les porteurs de projets ; risque de perte de compétences locales chez les financeurs qui se retirent.

**J. Contraintes.** Libre administration des collectivités ; loi nécessaire pour attribuer des chefs de file contraignants.

**K. Calendrier.** Loi 2027-2028 ; mise en œuvre 2028-2032.

**L. Niveau de confiance.** **Faible.** Montant externe déclaré, non mesuré.

**Indicateur de validation à 2-3 ans.** Nombre de financeurs et de dossiers par projet ; délais d'instruction ; ETP d'instruction par euro versé.

**M. Sources et calculs.**

- [Note 04d](../04d_territoires_fonctions_support.md)
- [Note 05](../05_reformes_etrangeres.md)
- [Blom-Hansen, Houlberg, Serritzlew, 2014, PDF 13](https://joeornstein.github.io/pols-4641/readings/Blom-Hansen%2C%20Houlberg%2C%20Serritzlew%20-%202014%20-%20Size%2C%20Democracy%2C%20and%20the%20Economic%20Costs%20of%20Running%20the%20Political%20System.pdf)
- [Houlberg, Politik, 2016](https://tidsskrift.dk/politik/article/view/27404)
- [DGAFP, rapport annuel 2026, caractéristiques des postes](https://www.fonction-publique.gouv.fr/files/files/publications/vue-rapport-annuel/2026/ra_2026_postes.zip)

Calculs : Base 453 224 × 1 980 400 / 2 017 830 = 444 817 ETP. Paramètres nationaux : [hypotheses.json](../../modele/hypotheses.json) ; ligne `R14` de [catalogue_reformes.csv](../../data/reformes/catalogue_reformes.csv) ; vivier dans [registre_viviers.csv](../../data/reformes/registre_viviers.csv). Reproduction : `python -I scripts/11_catalogue.py`.
