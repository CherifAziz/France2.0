# Réforme R13 — Mutualiser et automatiser la gestion administrative des personnels de l'Éducation nationale

Vivier : **V_MEN_ADM** (Filière administrative de l'Éducation nationale) · ordre d'application **30** · début **2028**, durée **5 ans** · confiance **faible**.

**A. Problème identifié.** **[FAIT]** La filière administrative scolaire compte **52 432 personnes et 50 849 ETP** au 30 novembre 2025, soit 16,35 % des non-enseignants. Le rapport IA cite Cassandre (gestion RH des enseignants à Versailles) : dossiers traités et deux heures gagnées par instruction optimisée.

**B. Organisation actuelle.** Rectorats, services départementaux et établissements ; gestion des personnels enseignants très largement manuelle selon les retours du rapport IA (non chiffrée nationalement).

**C. Comparaison internationale.** **[FAIT]** Aucun précédent étranger mesuré sur ce périmètre précis dans les sources ouvertes. Les hypothèses de gains RH de 5 à 10 % (Ravignon) sont le seul repère chiffré.

**D. Réforme proposée.** Généraliser les outils de type Cassandre, mutualiser la gestion des actes collectifs au niveau académique, ne pas remplacer les départs correspondants.

**E. Effectifs concernés.** Vivier administration scolaire : **50 849 ETP** (DEPP, 30 novembre 2025).

**F. Réduction envisageable.** **[HYPOTHÈSE]** 0 / 3 / 6 / 10 %. Les bornes Ravignon (5-10 %) encadrent l'intermédiaire et l'ambitieux. Taux appliqués au reliquat du vivier : 0,00 % / 3,00 % / 6,00 % / 10,00 % (prudent / intermédiaire / ambitieux / radical). Répartition : non-remplacement 100 %, redéploiement 0 %, suppression indemnisée 0 %, transfert 0 %.

**G. Économies.** Résultats du moteur financier (`modele/modele.py`), en M€ 2026 constants, par écart à une référence qui remplace tous les départs. Le non-remplacement est valorisé au coût d'entrée hors pension, croissant de 1 % par an jusqu'au coût moyen ; les postes ne disparaissent qu'au rythme des départs à la retraite du vivier.

| Indicateur | Prudent | Intermédiaire | Ambitieux | Radical |
|---|---:|---:|---:|---:|
| ETP visés (cible) | 0 | 1 525 | 3 051 | 5 085 |
| Postes en moins en 2036 | 0 | 1 525 | 3 051 | 5 085 |
| ETP redéployés | 0 | 0 | 0 | 0 |
| Cible non réalisée en 2036 (ETP) | 0 | 0 | 0 | 0 |
| Économie nette 2036 (M€) | 0,0 | 71,3 | 142,7 | 237,8 |
| Cumul net 2027-2031 (M€) | 0,0 | −25,5 | −51,1 | −85,1 |
| Cumul net 2027-2036 (M€) | 0,0 | 317,4 | 634,9 | 1 058,2 |
| Cumul consolidé APU 2027-2036 (M€) | 0,0 | 159,3 | 318,6 | 531,0 |
| Investissement total (M€) | 0,0 | 134,4 | 268,8 | 448,0 |
| Coût récurrent à terme (M€/an) | 0,0 | 0,0 | 0,0 | 0,0 |

**H. Investissements nécessaires.** **[HYPOTHÈSE de convention]** Deux années d'économie brute.

**I. Conséquences sur le service.** Délais de mutation et d'affectation des enseignants à surveiller ; recours des agents.

**J. Contraintes.** Calendrier scolaire ; volume des mouvements annuels ; dialogue social.

**K. Calendrier.** 2028-2032.

**L. Niveau de confiance.** **Faible.** Un seul retour d'expérience local.

**Indicateur de validation à 2-3 ans.** ETP de gestion par enseignant géré ; délais d'affectation ; recours.

**M. Sources et calculs.**

- [Note 02 — métiers](../02_metiers_classification.md)
- [Note 08](../08_ia_france.md)
- [Note 04d](../04d_territoires_fonctions_support.md)
- [DEPP, personnels non enseignants, tableau 3.1](https://www.education.gouv.fr/sites/default/files/document/chapitre-3-les-personnels-non-enseignants-520477.xlsx)

Calculs : Taux en part du vivier de 50 849 ETP. Paramètres nationaux : [hypotheses.json](../../modele/hypotheses.json) ; ligne `R13` de [catalogue_reformes.csv](../../data/reformes/catalogue_reformes.csv) ; vivier dans [registre_viviers.csv](../../data/reformes/registre_viviers.csv). Reproduction : `python -I scripts/11_catalogue.py`.
