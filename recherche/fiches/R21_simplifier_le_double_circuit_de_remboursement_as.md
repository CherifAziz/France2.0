# Réforme R21 — Simplifier le double circuit de remboursement assurance maladie et complémentaires

Vivier : **V_OPS** (Organismes de protection sociale (droit privé, financement public prédominant)) · ordre d'application **20** · début **2028**, durée **5 ans** · confiance **faible**.

**A. Problème identifié.** **[FAIT]** Les frais de gestion de la santé atteignent **17,616 Md€ en 2025**, dont **7,229 Md€** pour les régimes de Sécurité sociale et **9,176 Md€** pour les organismes complémentaires (52,09 %). Le HCAAM décrit dès 2021 les doubles circuits AMO-AMC.

**B. Organisation actuelle.** Assurance maladie obligatoire et complémentaires traitent chacune les mêmes soins ; flux de données partiels.

**C. Comparaison internationale.** **[FAIT]** En ESSPROS, l'administration de la protection sociale représente **3,83 %** des dépenses en France contre 3,60 % en Allemagne et 5,35 % aux Pays-Bas : la France n'est pas systématiquement plus coûteuse.

**D. Réforme proposée.** Flux unique de remboursement et de données entre caisses et complémentaires ; tiers payant intégral simplifié ; non-remplacement des postes de traitement doublonnés dans les caisses.

**E. Effectifs concernés.** Vivier organismes de protection sociale : **162 623 personnes** fin 2024 (DGAFP, organismes privés à financement public prédominant), utilisées comme majorant des ETP.

**F. Réduction envisageable.** **[HYPOTHÈSE]** 0 / 1 / 2 / 4 %. Le scénario HCAAM le plus intégré évite **5,4 Md€** de charges mais transfère **22,5 Md€** de prise en charge vers les finances publiques : il n'est pas retenu comme économie. Taux appliqués au reliquat du vivier : 0,00 % / 1,00 % / 2,00 % / 4,00 % (prudent / intermédiaire / ambitieux / radical). Répartition : non-remplacement 100 %, redéploiement 0 %, suppression indemnisée 0 %, transfert 0 %.

**G. Économies.** Résultats du moteur financier (`modele/modele.py`), en M€ 2026 constants, par écart à une référence qui remplace tous les départs. Le non-remplacement est valorisé au coût d'entrée hors pension, croissant de 1 % par an jusqu'au coût moyen ; les postes ne disparaissent qu'au rythme des départs à la retraite du vivier.

| Indicateur | Prudent | Intermédiaire | Ambitieux | Radical |
|---|---:|---:|---:|---:|
| ETP visés (cible) | 0 | 1 626 | 3 252 | 6 505 |
| Postes en moins en 2036 | 0 | 1 626 | 3 252 | 6 505 |
| ETP redéployés | 0 | 0 | 0 | 0 |
| Cible non réalisée en 2036 (ETP) | 0 | 0 | 0 | 0 |
| Économie nette 2036 (M€) | 0,0 | 76,0 | 152,1 | 304,2 |
| Cumul net 2027-2031 (M€) | 0,0 | −27,2 | −54,4 | −108,9 |
| Cumul net 2027-2036 (M€) | 0,0 | 338,4 | 676,8 | 1 353,7 |
| Cumul consolidé APU 2027-2036 (M€) | 0,0 | 169,8 | 339,7 | 679,3 |
| Investissement total (M€) | 0,0 | 143,3 | 286,5 | 573,1 |
| Coût récurrent à terme (M€/an) | 0,0 | 0,0 | 0,0 | 0,0 |

**H. Investissements nécessaires.** **[HYPOTHÈSE de convention]** Deux années d'économie brute.

**I. Conséquences sur le service.** Moins de démarches pour assurés et soignants ; l'essentiel du gain irait aux complémentaires privées, hors dépense publique.

**J. Contraintes.** Concurrence entre organismes complémentaires ; droit des contrats ; financement.

**K. Calendrier.** 2028-2032.

**L. Niveau de confiance.** **Faible.** Gain public mal identifié.

**Indicateur de validation à 2-3 ans.** Coût de gestion par décompte dans les caisses ; délais de remboursement ; frais de gestion des complémentaires.

**M. Sources et calculs.**

- [Note 04c](../04c_sante_protection_sociale.md)
- [DREES, comptes de la santé 2026, fiche 28](https://drees.solidarites-sante.gouv.fr/sites/default/files/2026-09/CNS2026%20-%20Partie%203%20DCSi%20par%20composante.xlsx)
- [HCAAM, janvier 2022, p. 79-80](https://www.strategie-plan.gouv.fr/files/files/Publications/2021%20SP/2022-01-14%20-%20HCAAM%20-%20Quatre%20sc%C3%A9narios%20polaires%20d%27%C3%A9volution%20de%20l%27articulation/rapport_hcaam-_quatre_scenarios_articulation_amo-amc_-_janvier_2022_0.pdf)

Calculs : Taux en part du vivier de 162 623. Paramètres nationaux : [hypotheses.json](../../modele/hypotheses.json) ; ligne `R21` de [catalogue_reformes.csv](../../data/reformes/catalogue_reformes.csv) ; vivier dans [registre_viviers.csv](../../data/reformes/registre_viviers.csv). Reproduction : `python -I scripts/11_catalogue.py`.
