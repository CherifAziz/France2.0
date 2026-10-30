# Réforme R07 — Réutiliser les données détenues et ne plus redemander les pièces

Vivier : **V_FPE_AUTRES** (Autres corps administratifs et techniques de la FPE (ministères et EPA, dont opérateurs)) · ordre d'application **20** · début **2027**, durée **5 ans** · confiance **moyen**.

**A. Problème identifié.** **[FAIT]** Dans le panel DINUM, les démarches demandant zéro ou une information passent de **78/242 en 2020 à 137/248 en 2023**. Les **320 M€/an** de gains pour l'État associés à « Dites-le-nous une fois » sont annoncés au conditionnel en 2019, sans bilan réalisé.

**B. Organisation actuelle.** Démarches instruites par les ministères et leurs opérateurs ; échanges de données (quotient familial CAF/MSA depuis 2024) encore partiels.

**C. Comparaison internationale.** **[ESTIMATION étrangère]** En Estonie, X-Road est crédité de **1 100 années de temps** en 2019, sur l'hypothèse de 15 minutes par requête humaine : ce ne sont pas 1 100 postes supprimés. Au Danemark, Digital Post n'a réduit les crédits que de **48 M DKK**, 19,67 % du potentiel annoncé.

**D. Réforme proposée.** Pour chaque démarche à fort volume, supprimer les pièces déjà détenues par une administration et automatiser leur vérification ; ne pas remplacer les postes d'instruction de pièces libérés.

**E. Effectifs concernés.** Vivier « autres administratifs et techniques de l'État » : 231 659 ETP.

**F. Réduction envisageable.** **[HYPOTHÈSE]** 0,5 / 1 / 2 / 3 %. Le repère danois incite à retenir une faible part du potentiel annoncé. Taux appliqués au reliquat du vivier : 0,50 % / 1,00 % / 2,00 % / 3,00 % (prudent / intermédiaire / ambitieux / radical). Répartition : non-remplacement 100 %, redéploiement 0 %, suppression indemnisée 0 %, transfert 0 %.

**G. Économies.** Résultats du moteur financier (`modele/modele.py`), en M€ 2026 constants, par écart à une référence qui remplace tous les départs. Le non-remplacement est valorisé au coût d'entrée hors pension, croissant de 1 % par an jusqu'au coût moyen ; les postes ne disparaissent qu'au rythme des départs à la retraite du vivier.

| Indicateur | Prudent | Intermédiaire | Ambitieux | Radical |
|---|---:|---:|---:|---:|
| ETP visés (cible) | 1 153 | 2 236 | 4 316 | 6 021 |
| Postes en moins en 2036 | 1 153 | 2 236 | 4 316 | 6 021 |
| ETP redéployés | 0 | 0 | 0 | 0 |
| Cible non réalisée en 2036 (ETP) | 0 | 0 | 0 | 0 |
| Économie nette 2036 (M€) | 54,4 | 105,6 | 203,9 | 277,5 |
| Cumul net 2027-2031 (M€) | 27,4 | 53,2 | 102,7 | −286,4 |
| Cumul net 2027-2036 (M€) | 294,3 | 571,0 | 1 102,1 | 847,7 |
| Cumul consolidé APU 2027-2036 (M€) | 155,7 | 302,2 | 583,3 | 365,4 |
| Investissement total (M€) | 101,5 | 197,0 | 380,3 | 530,4 |
| Coût récurrent à terme (M€/an) | 0,0 | 0,0 | 0,0 | 0,0 |

**H. Investissements nécessaires.** **[HYPOTHÈSE de convention]** Deux années d'économie brute (API, contrôles de qualité des données).

**I. Conséquences sur le service.** Moins de démarches et de délais pour les usagers ; risque d'erreurs propagées par des données fausses.

**J. Contraintes.** Base légale des échanges, RGPD, qualité des référentiels.

**K. Calendrier.** 2027-2031, démarche par démarche.

**L. Niveau de confiance.** **Moyen.** Mécanisme documenté ; conversion en postes non mesurée.

**Indicateur de validation à 2-3 ans.** Nombre de pièces demandées par démarche pondéré par les volumes ; temps d'instruction mesuré ; ETP d'instruction concernés.

**M. Sources et calculs.**

- [Note 07 — simplification](../07_simplification_reglementaire.md)
- [Note 05](../05_reformes_etrangeres.md)
- [Rigsrevisionen 9/2015](https://cdn.rigsrevisionen.dk/rigsrevisionen/Media/7/1/9-2015.pdf)

Calculs : Taux en part du reliquat. Paramètres nationaux : [hypotheses.json](../../modele/hypotheses.json) ; ligne `R07` de [catalogue_reformes.csv](../../data/reformes/catalogue_reformes.csv) ; vivier dans [registre_viviers.csv](../../data/reformes/registre_viviers.csv). Reproduction : `python -I scripts/11_catalogue.py`.
