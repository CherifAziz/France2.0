# Réforme R10 — Industrialiser la gestion RH et la paie interministérielles

Vivier : **V_FPE_AUTRES** (Autres corps administratifs et techniques de la FPE (ministères et EPA, dont opérateurs)) · ordre d'application **31** · début **2029**, durée **5 ans** · confiance **faible**.

**A. Problème identifié.** **[ESTIMATION externe]** Le rapport Ravignon identifie **31 040 agents RH** dans les collectivités en 2021 et suppose 5 à 10 % de gains ; aucune mesure équivalente n'est disponible pour l'État dans les sources consultées. Les échecs Louvois, ONP et Sirhen (environ 480 M€ déclarés pour ce dernier) montrent le risque.

**B. Organisation actuelle.** Gestion RH par ministère, paie liquidée par la DGFiP ; systèmes d'information RH multiples.

**C. Comparaison internationale.** **[FAIT]** Phénix (Canada) : 233 000 transactions en retard fin septembre 2025, successeur estimé à plus de 4,2 Md CAD. Le Japon n'a réduit ses dépenses de SI que de **14 % après retraitement**, pour une cible de −30 %.

**D. Réforme proposée.** Socle commun de gestion RH, actes standard automatisés, centres de gestion mutualisés ; migration par lots avec double run.

**E. Effectifs concernés.** Vivier « autres administratifs et techniques de l'État » : 231 659 ETP.

**F. Réduction envisageable.** **[HYPOTHÈSE]** 0 / 0,5 / 1 / 2 %, démarrage 2029 après les services partagés des opérateurs. Taux appliqués au reliquat du vivier : 0,00 % / 0,50 % / 1,00 % / 2,00 % (prudent / intermédiaire / ambitieux / radical). Répartition : non-remplacement 100 %, redéploiement 0 %, suppression indemnisée 0 %, transfert 0 %.

**G. Économies.** Résultats du moteur financier (`modele/modele.py`), en M€ 2026 constants, par écart à une référence qui remplace tous les départs. Le non-remplacement est valorisé au coût d'entrée hors pension, croissant de 1 % par an jusqu'au coût moyen ; les postes ne disparaissent qu'au rythme des départs à la retraite du vivier.

| Indicateur | Prudent | Intermédiaire | Ambitieux | Radical |
|---|---:|---:|---:|---:|
| ETP visés (cible) | 0 | 1 085 | 2 021 | 3 625 |
| Postes en moins en 2036 | 0 | 1 085 | 2 021 | 3 625 |
| ETP redéployés | 0 | 0 | 0 | 0 |
| Cible non réalisée en 2036 (ETP) | 0 | 0 | 0 | 0 |
| Économie nette 2036 (M€) | 0,0 | 50,2 | 92,4 | 79,9 |
| Cumul net 2027-2031 (M€) | 0,0 | −100,0 | −267,0 | −479,1 |
| Cumul net 2027-2036 (M€) | 0,0 | 127,3 | 124,0 | −399,3 |
| Cumul consolidé APU 2027-2036 (M€) | 0,0 | 32,5 | −12,9 | −427,2 |
| Investissement total (M€) | 0,0 | 143,4 | 267,0 | 479,1 |
| Coût récurrent à terme (M€/an) | 0,0 | 0,0 | 0,0 | 0,0 |

**H. Investissements nécessaires.** **[HYPOTHÈSE de convention]** Trois années d'économie brute, vu les précédents d'échecs.

**I. Conséquences sur le service.** Risque majeur d'erreurs de paie en cas d'échec ; amélioration des délais si réussi.

**J. Contraintes.** Complexité statutaire et indemnitaire ; dépendance aux prestataires.

**K. Calendrier.** Conception 2027-2028 ; déploiement 2029-2033.

**L. Niveau de confiance.** **Faible.** Précédents d'échecs coûteux en France et au Canada.

**Indicateur de validation à 2-3 ans.** Coût complet de gestion RH par agent ; taux d'erreurs de paie ; délais des actes.

**M. Sources et calculs.**

- [Note 04d](../04d_territoires_fonctions_support.md)
- [Note 05](../05_reformes_etrangeres.md)
- [Note 08 — IA en France](../08_ia_france.md)
- [Vérificateur général du Canada, mars 2026](https://www.canada.ca/content/dam/oag-bvg/audit-reports/documents/ag-202603-modernizing-pay-system.pdf)

Calculs : Taux en part du reliquat ; investissement = 3 × économie brute annuelle visée. Paramètres nationaux : [hypotheses.json](../../modele/hypotheses.json) ; ligne `R10` de [catalogue_reformes.csv](../../data/reformes/catalogue_reformes.csv) ; vivier dans [registre_viviers.csv](../../data/reformes/registre_viviers.csv). Reproduction : `python -I scripts/11_catalogue.py`.
