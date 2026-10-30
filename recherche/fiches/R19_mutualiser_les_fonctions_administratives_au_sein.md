# Réforme R19 — Mutualiser les fonctions administratives au sein des groupements hospitaliers

Vivier : **V_FPH_ADM** (Filière administrative de la fonction publique hospitalière) · ordre d'application **30** · début **2028**, durée **5 ans** · confiance **faible**.

**A. Problème identifié.** **[FAIT]** La filière administrative de la FPH compte **121 829 agents** fin 2024, soit 9,76 % du total FPH. La SAE recense **110 089 postes administratifs** dans les établissements publics de santé. L'administration interne des hôpitaux est hors du ratio international HC7.

**B. Organisation actuelle.** Chaque établissement gère ses admissions, sa facturation, sa paie et ses achats ; les groupements hospitaliers de territoire ne sont pas documentés dans les sources lues (effectifs mutualisés NON TROUVÉS).

**C. Comparaison internationale.** **[NON TROUVÉ]** Aucune évaluation étrangère de mutualisation administrative hospitalière n'a été ouverte dans ce dossier.

**D. Réforme proposée.** Centres de gestion communs par groupement pour la paie, la facturation, les achats et la gestion RH ; non-remplacement des postes libérés.

**E. Effectifs concernés.** Vivier filière administrative FPH : **119 264 ETP** (121 829 × 0,9789).

**F. Réduction envisageable.** **[HYPOTHÈSE]** 1 / 3 / 5 / 8 %, comme la mutualisation communale (R17), faute de repère propre. Taux appliqués au reliquat du vivier : 1,00 % / 3,00 % / 5,00 % / 8,00 % (prudent / intermédiaire / ambitieux / radical). Répartition : non-remplacement 100 %, redéploiement 0 %, suppression indemnisée 0 %, transfert 0 %.

**G. Économies.** Résultats du moteur financier (`modele/modele.py`), en M€ 2026 constants, par écart à une référence qui remplace tous les départs. Le non-remplacement est valorisé au coût d'entrée hors pension, croissant de 1 % par an jusqu'au coût moyen ; les postes ne disparaissent qu'au rythme des départs à la retraite du vivier.

| Indicateur | Prudent | Intermédiaire | Ambitieux | Radical |
|---|---:|---:|---:|---:|
| ETP visés (cible) | 1 193 | 3 578 | 5 963 | 9 541 |
| Postes en moins en 2036 | 1 193 | 3 578 | 5 963 | 9 541 |
| ETP redéployés | 0 | 0 | 0 | 0 |
| Cible non réalisée en 2036 (ETP) | 0 | 0 | 0 | 0 |
| Économie nette 2036 (M€) | 42,6 | 127,9 | 213,2 | 341,0 |
| Cumul net 2027-2031 (M€) | −15,3 | −45,8 | −76,3 | −122,0 |
| Cumul net 2027-2036 (M€) | 189,7 | 569,1 | 948,5 | 1 517,6 |
| Cumul consolidé APU 2027-2036 (M€) | 95,2 | 285,6 | 476,0 | 761,6 |
| Investissement total (M€) | 80,3 | 240,9 | 401,6 | 642,5 |
| Coût récurrent à terme (M€/an) | 0,0 | 0,0 | 0,0 | 0,0 |

**H. Investissements nécessaires.** **[HYPOTHÈSE de convention]** Deux années d'économie brute.

**I. Conséquences sur le service.** Risque sur la facturation et donc les recettes hospitalières ; délais d'admission.

**J. Contraintes.** Autonomie des établissements ; systèmes d'information hospitaliers hétérogènes.

**K. Calendrier.** 2028-2032.

**L. Niveau de confiance.** **Faible.** Pas de mesure de l'existant ni de précédent.

**Indicateur de validation à 2-3 ans.** ETP administratifs par séjour ; délais de facturation ; rejets de facturation.

**M. Sources et calculs.**

- [Note 02](../02_metiers_classification.md)
- [Note 04c — santé et protection sociale](../04c_sante_protection_sociale.md)
- [DGAFP, rapport annuel 2026, caractéristiques des postes](https://www.fonction-publique.gouv.fr/files/files/publications/vue-rapport-annuel/2026/ra_2026_postes.zip)

Calculs : Base 121 829 × 1 222 300 / 1 248 591 = 119 264 ETP. Paramètres nationaux : [hypotheses.json](../../modele/hypotheses.json) ; ligne `R19` de [catalogue_reformes.csv](../../data/reformes/catalogue_reformes.csv) ; vivier dans [registre_viviers.csv](../../data/reformes/registre_viviers.csv). Reproduction : `python -I scripts/11_catalogue.py`.
