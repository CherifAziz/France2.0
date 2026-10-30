# Réforme R16 — Évaluer a posteriori et alléger les normes imposées aux collectivités

Vivier : **V_FPT_ADM** (Filière administrative de la fonction publique territoriale) · ordre d'application **20** · début **2028**, durée **5 ans** · confiance **faible**.

**A. Problème identifié.** **[NON TROUVÉ]** Aucun coût récent, réalisé et net, des normes applicables aux collectivités n'a pu être vérifié : le rapport de la CNEN est inaccessible. Les saisines en urgence de la CNEN passent de **26 % en 2022 à 5 % en 2025** selon le Premier ministre.

**B. Organisation actuelle.** La CNEN examine les projets de normes ex ante ; aucun contrôle ex post systématique des coûts exécutés.

**C. Comparaison internationale.** **[FAIT]** Les Pays-Bas ont mesuré la charge d'information avec le Standard Cost Model ; la Commission européenne calcule le coût des obligations nouvelles moins celui des obligations retirées (outil 58). Ces méthodes visent surtout la charge privée.

**D. Réforme proposée.** Confronter les coûts annoncés des normes aux comptes exécutés sur un échantillon ; abroger ou simplifier les normes dont le coût administratif dépasse l'utilité démontrée.

**E. Effectifs concernés.** Vivier filière administrative FPT : 444 817 ETP.

**F. Réduction envisageable.** **[HYPOTHÈSE]** 0 / 0,5 / 1 / 2 % du reliquat. Taux appliqués au reliquat du vivier : 0,00 % / 0,50 % / 1,00 % / 2,00 % (prudent / intermédiaire / ambitieux / radical). Répartition : non-remplacement 100 %, redéploiement 0 %, suppression indemnisée 0 %, transfert 0 %.

**G. Économies.** Résultats du moteur financier (`modele/modele.py`), en M€ 2026 constants, par écart à une référence qui remplace tous les départs. Le non-remplacement est valorisé au coût d'entrée hors pension, croissant de 1 % par an jusqu'au coût moyen ; les postes ne disparaissent qu'au rythme des départs à la retraite du vivier.

| Indicateur | Prudent | Intermédiaire | Ambitieux | Radical |
|---|---:|---:|---:|---:|
| ETP visés (cible) | 0 | 2 202 | 4 359 | 8 113 |
| Postes en moins en 2036 | 0 | 2 202 | 4 359 | 8 113 |
| ETP redéployés | 0 | 0 | 0 | 0 |
| Cible non réalisée en 2036 (ETP) | 0 | 0 | 0 | 0 |
| Économie nette 2036 (M€) | 0,0 | 78,7 | 155,8 | 290,0 |
| Cumul net 2027-2031 (M€) | 0,0 | −28,2 | −55,8 | −103,8 |
| Cumul net 2027-2036 (M€) | 0,0 | 350,2 | 693,4 | 1 290,5 |
| Cumul consolidé APU 2027-2036 (M€) | 0,0 | 175,8 | 348,0 | 647,6 |
| Investissement total (M€) | 0,0 | 148,3 | 293,5 | 546,4 |
| Coût récurrent à terme (M€/an) | 0,0 | 0,0 | 0,0 | 0,0 |

**H. Investissements nécessaires.** **[HYPOTHÈSE de convention]** Deux années d'économie brute.

**I. Conséquences sur le service.** Allègement des tâches d'application ; risque de recul de protections (sécurité, environnement) si la sélection est mal faite.

**J. Contraintes.** Normes européennes et législatives ; consensus nécessaire avec les associations d'élus.

**K. Calendrier.** Évaluations 2027-2028 ; abrogations 2028-2032.

**L. Niveau de confiance.** **Faible.** Base de coût inaccessible.

**Indicateur de validation à 2-3 ans.** Coût exécuté des normes évaluées ; temps des agents consacré à leur application ; nombre de normes abrogées.

**M. Sources et calculs.**

- [Note 07](../07_simplification_reglementaire.md)
- [Contre-vérification 06-07](../00_verification_06_07_lot3.md)

Calculs : Taux en part du reliquat. Paramètres nationaux : [hypotheses.json](../../modele/hypotheses.json) ; ligne `R16` de [catalogue_reformes.csv](../../data/reformes/catalogue_reformes.csv) ; vivier dans [registre_viviers.csv](../../data/reformes/registre_viviers.csv). Reproduction : `python -I scripts/11_catalogue.py`.
