# Réforme R29 — Réduire les surfaces de bureaux au-delà de la foncière de l'État

Vivier : **V_FONCT** (Dépenses de fonctionnement sans effectif (achats, immobilier, instances)) · ordre d'application **11** · début **2030**, durée **5 ans** · confiance **faible**.

**A. Problème identifié.** **[HYPOTHÈSE externe]** Le projet immobilier de 2025 vise **−25 % de surfaces à 2032** sur 20 millions de m² éligibles, pour **1 Md€ de gains annuels à terme**. La loi créant la foncière a été promulguée le **18 août 2026** : ce gain appartient à la trajectoire de référence.

**B. Organisation actuelle.** Parc immobilier de l'État et de ses opérateurs, en cours de transfert à une foncière.

**C. Comparaison internationale.** **[NON TROUVÉ]** Aucun bilan étranger de réduction de surfaces ouvert dans ce dossier.

**D. Réforme proposée.** Au-delà de l'objectif engagé, réduction supplémentaire liée aux effectifs supprimés par les autres fiches et au télétravail.

**E. Effectifs concernés.** Aucun effectif.

**F. Réduction envisageable.** Sans réduction d'effectifs. Taux appliqués au reliquat du vivier : 0,00 % / 0,00 % / 0,00 % / 0,00 % (prudent / intermédiaire / ambitieux / radical). Répartition : non-remplacement 100 %, redéploiement 0 %, suppression indemnisée 0 %, transfert 0 %.

**G. Économies.** Résultats du moteur financier (`modele/modele.py`), en M€ 2026 constants, par écart à une référence qui remplace tous les départs. Le non-remplacement est valorisé au coût d'entrée hors pension, croissant de 1 % par an jusqu'au coût moyen ; les postes ne disparaissent qu'au rythme des départs à la retraite du vivier.

| Indicateur | Prudent | Intermédiaire | Ambitieux | Radical |
|---|---:|---:|---:|---:|
| ETP visés (cible) | 0 | 0 | 0 | 0 |
| Postes en moins en 2036 | 0 | 0 | 0 | 0 |
| ETP redéployés | 0 | 0 | 0 | 0 |
| Cible non réalisée en 2036 (ETP) | 0 | 0 | 0 | 0 |
| Économie nette 2036 (M€) | 0,0 | 0,0 | 100,0 | 250,0 |
| Cumul net 2027-2031 (M€) | 0,0 | 0,0 | 60,0 | 150,0 |
| Cumul net 2027-2036 (M€) | 0,0 | 0,0 | 500,0 | 1 250,0 |
| Cumul consolidé APU 2027-2036 (M€) | 0,0 | 0,0 | 500,0 | 1 250,0 |
| Investissement total (M€) | 0,0 | 0,0 | 0,0 | 0,0 |
| Coût récurrent à terme (M€/an) | 0,0 | 0,0 | 0,0 | 0,0 |

**H. Investissements nécessaires.** Coûts de déménagement et de travaux non chiffrés.

**I. Conséquences sur le service.** Conditions de travail à préserver.

**J. Contraintes.** Marché immobilier ; baux en cours.

**K. Calendrier.** Après 2030, une fois l'objectif engagé atteint.

**L. Niveau de confiance.** **Faible.** Gain additionnel hypothétique.

**Indicateur de validation à 2-3 ans.** Surfaces par agent ; loyers et charges d'entretien constatés.

**M. Sources et calculs.**

- [Note 04d](../04d_territoires_fonctions_support.md)
- [Synthèse du lot 3](../00_synthese_lot3.md)

Calculs : **[HYPOTHÈSE]** 0 / 0 / 100 / 250 M€/an additionnels, soit 0 à 25 % du gain déjà engagé de 1 Md€. Paramètres nationaux : [hypotheses.json](../../modele/hypotheses.json) ; ligne `R29` de [catalogue_reformes.csv](../../data/reformes/catalogue_reformes.csv) ; vivier dans [registre_viviers.csv](../../data/reformes/registre_viviers.csv). Reproduction : `python -I scripts/11_catalogue.py`.
