# Réforme R20 — Automatiser le codage, la facturation et le secrétariat hospitaliers

Vivier : **V_FPH_ADM** (Filière administrative de la fonction publique hospitalière) · ordre d'application **40** · début **2028**, durée **6 ans** · confiance **faible**.

**A. Problème identifié.** **[FAIT]** Un essai randomisé de scribes ambiants (238 médecins, 14 spécialités) mesure **−9,5 %** du temps de note avec Nabla, IC 95 % [−17,2 ; −1,8], et un effet non significatif avec DAX (−1,7 %). L'effet porte sur le temps médical de note, pas sur le personnel administratif.

**B. Organisation actuelle.** Codage des séjours, facturation et secrétariat médical assurés par les filières administrative et soignante.

**C. Comparaison internationale.** **[FAIT]** Les erreurs occasionnelles « cliniquement significatives » relevées dans l'essai imposent une vérification humaine.

**D. Réforme proposée.** Automatiser le précodage et la préparation de la facturation ; réorganiser les secrétariats ; non-remplacement des départs mesurés comme libérés.

**E. Effectifs concernés.** Vivier filière administrative FPH : 119 264 ETP.

**F. Réduction envisageable.** **[HYPOTHÈSE]** 0 / 1 / 3 / 5 % du reliquat. Taux appliqués au reliquat du vivier : 0,00 % / 1,00 % / 3,00 % / 5,00 % (prudent / intermédiaire / ambitieux / radical). Répartition : non-remplacement 100 %, redéploiement 0 %, suppression indemnisée 0 %, transfert 0 %.

**G. Économies.** Résultats du moteur financier (`modele/modele.py`), en M€ 2026 constants, par écart à une référence qui remplace tous les départs. Le non-remplacement est valorisé au coût d'entrée hors pension, croissant de 1 % par an jusqu'au coût moyen ; les postes ne disparaissent qu'au rythme des départs à la retraite du vivier.

| Indicateur | Prudent | Intermédiaire | Ambitieux | Radical |
|---|---:|---:|---:|---:|
| ETP visés (cible) | 0 | 1 157 | 3 399 | 5 486 |
| Postes en moins en 2036 | 0 | 1 157 | 3 399 | 5 486 |
| ETP redéployés | 0 | 0 | 0 | 0 |
| Cible non réalisée en 2036 (ETP) | 0 | 0 | 0 | 0 |
| Économie nette 2036 (M€) | 0,0 | 39,9 | 119,6 | 193,9 |
| Cumul net 2027-2031 (M€) | 0,0 | 18,7 | 120,6 | 215,5 |
| Cumul net 2027-2036 (M€) | 0,0 | 201,4 | 669,2 | 1 104,7 |
| Cumul consolidé APU 2027-2036 (M€) | 0,0 | 116,9 | 421,0 | 704,1 |
| Investissement total (M€) | 0,0 | 31,8 | 31,8 | 31,8 |
| Coût récurrent à terme (M€/an) | 0,0 | 1,3 | 1,3 | 1,3 |

**H. Investissements nécessaires.** **[ESTIMATION par analogie]** 267 € par ETP d'investissement et 10,5 € par ETP et par an.

**I. Conséquences sur le service.** Risque de recettes perdues si le codage se dégrade ; libération possible de temps soignant (non compté ici).

**J. Contraintes.** Données de santé, hébergement certifié, AI Act.

**K. Calendrier.** 2028-2033.

**L. Niveau de confiance.** **Faible.** Les preuves portent sur un autre métier.

**Indicateur de validation à 2-3 ans.** Temps de codage par séjour ; taux de rejets et de recodage ; ETP des services concernés.

**M. Sources et calculs.**

- [Note 09](../09_ia_preuves_internationales.md)
- [Essai randomisé de scribes ambiants, résumé Europe PMC](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:41497288%20AND%20SRC:MED&format=json&resultType=core)

Calculs : Investissement = 0,267 k€ × ETP du vivier, sur 3 ans. Paramètres nationaux : [hypotheses.json](../../modele/hypotheses.json) ; ligne `R20` de [catalogue_reformes.csv](../../data/reformes/catalogue_reformes.csv) ; vivier dans [registre_viviers.csv](../../data/reformes/registre_viviers.csv). Reproduction : `python -I scripts/11_catalogue.py`.
