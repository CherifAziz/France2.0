# Réforme R15 — Supprimer un échelon d'administration territoriale (transformation radicale)

Vivier : **V_FPT_ADM** (Filière administrative de la fonction publique territoriale) · ordre d'application **11** · début **2030**, durée **6 ans** · confiance **faible**.

**A. Problème identifié.** **[FAIT]** Les départements emploient **286 800 personnes** et les régions **98 916** fin 2024 (tous métiers). La taille municipale moyenne est de 1 928 habitants en France contre 59 504 au Danemark (OCDE, 2020).

**B. Organisation actuelle.** Quatre niveaux d'administration locale (commune, intercommunalité, département, région), plus l'État territorial.

**C. Comparaison internationale.** **[ESTIMATION]** Danemark 2007 : suppression des comtés et fusion des communes ; économie administrative de 10,4 % après quatre ans, réaffectée selon la synthèse de 2016. Aucun pays de l'échantillon n'a supprimé un échelon de cette taille avec un bilan net publié.

**D. Réforme proposée.** Fusion des départements dans les régions ou les métropoles, avec transfert des compétences sociales ; non-remplacement des fonctions de gestion doublonnées.

**E. Effectifs concernés.** Vivier filière administrative FPT : 444 817 ETP ; part départementale de la filière non isolée.

**F. Réduction envisageable.** **[HYPOTHÈSE]** Uniquement en scénario radical : **5 %** du reliquat, dont 80 % non remplacés et 20 % redéployés. Les autres scénarios retiennent zéro, faute de démonstration. Taux appliqués au reliquat du vivier : 0,00 % / 0,00 % / 0,00 % / 5,00 % (prudent / intermédiaire / ambitieux / radical). Répartition : non-remplacement 80 %, redéploiement 20 %, suppression indemnisée 0 %, transfert 0 %.

**G. Économies.** Résultats du moteur financier (`modele/modele.py`), en M€ 2026 constants, par écart à une référence qui remplace tous les départs. Le non-remplacement est valorisé au coût d'entrée hors pension, croissant de 1 % par an jusqu'au coût moyen ; les postes ne disparaissent qu'au rythme des départs à la retraite du vivier.

| Indicateur | Prudent | Intermédiaire | Ambitieux | Radical |
|---|---:|---:|---:|---:|
| ETP visés (cible) | 0 | 0 | 0 | 21 351 |
| Postes en moins en 2036 | 0 | 0 | 0 | 17 081 |
| ETP redéployés | 0 | 0 | 0 | 4 270 |
| Cible non réalisée en 2036 (ETP) | 0 | 0 | 0 | 0 |
| Économie nette 2036 (M€) | 0,0 | 0,0 | 0,0 | 595,6 |
| Cumul net 2027-2031 (M€) | 0,0 | 0,0 | 0,0 | −1 532,7 |
| Cumul net 2027-2036 (M€) | 0,0 | 0,0 | 0,0 | 629,5 |
| Cumul consolidé APU 2027-2036 (M€) | 0,0 | 0,0 | 0,0 | −194,7 |
| Investissement total (M€) | 0,0 | 0,0 | 0,0 | 1 725,3 |
| Coût récurrent à terme (M€/an) | 0,0 | 0,0 | 0,0 | 0,0 |

**H. Investissements nécessaires.** **[HYPOTHÈSE de convention]** Trois années d'économie brute (harmonisation des régimes indemnitaires, systèmes d'information, immobilier).

**I. Conséquences sur le service.** Risque de rupture des prestations sociales départementales (RSA, aide sociale à l'enfance) pendant la transition.

**J. Contraintes.** Révision constitutionnelle probable ; harmonisation des rémunérations à la hausse, qui peut annuler l'économie.

**K. Calendrier.** Réforme institutionnelle 2028-2030 ; mise en œuvre 2030-2035.

**L. Niveau de confiance.** **Faible.** Hors des précédents mesurés ; testée seulement en scénario radical.

**Indicateur de validation à 2-3 ans.** Dépenses de gestion des collectivités consolidées ; ETP administratifs par habitant ; délais des prestations sociales.

**M. Sources et calculs.**

- [Note 04d](../04d_territoires_fonctions_support.md)
- [Note 05](../05_reformes_etrangeres.md)
- [Note 01 — emploi public](../01_emploi_public_france.md)
- [Blom-Hansen, Houlberg, Serritzlew, 2014, PDF 13](https://joeornstein.github.io/pols-4641/readings/Blom-Hansen%2C%20Houlberg%2C%20Serritzlew%20-%202014%20-%20Size%2C%20Democracy%2C%20and%20the%20Economic%20Costs%20of%20Running%20the%20Political%20System.pdf)
- [Données 01 — effectifs par employeur fin 2024](../../data/france/01_effectifs_employeurs.csv)

Calculs : Taux en part du reliquat ; investissement = 3 × économie brute annuelle visée. Paramètres nationaux : [hypotheses.json](../../modele/hypotheses.json) ; ligne `R15` de [catalogue_reformes.csv](../../data/reformes/catalogue_reformes.csv) ; vivier dans [registre_viviers.csv](../../data/reformes/registre_viviers.csv). Reproduction : `python -I scripts/11_catalogue.py`.
