# Réforme R05 — Allouer les effectifs de l'État territorial selon des besoins mesurés

Vivier : **V_FPE_AUTRES** (Autres corps administratifs et techniques de la FPE (ministères et EPA, dont opérateurs)) · ordre d'application **11** · début **2028**, durée **5 ans** · confiance **faible**.

**A. Problème identifié.** **[FAIT]** La Cour relève **11 763 ETPT de moins dans l'État territorial entre 2012 et 2020**, en partie compensés par des contrats courts, et juge certaines coupes irréalistes. Les allocations reposent largement sur des équilibres historiques.

**B. Organisation actuelle.** Préfectures, directions départementales interministérielles et services régionaux ; transferts de missions qui brouillent les comparaisons dans le temps.

**C. Comparaison internationale.** **[FAIT]** Au Royaume-Uni, la fonction publique centrale a baissé de **20,17 %** entre 2010 et 2016, puis a regagné **36,20 %** jusqu'en 2026. Des coupes non adossées aux missions n'ont pas été durables.

**D. Réforme proposée.** Construire un modèle d'allocation par activité (volumes de titres, contrôles, dossiers) ; réduire les effectifs là où la charge mesurée est inférieure à l'allocation ; supprimer les missions sans base légale actuelle.

**E. Effectifs concernés.** Vivier « autres administratifs et techniques de l'État » : 231 659 ETP, dont la part territoriale n'est pas isolée dans les sources.

**F. Réduction envisageable.** **[HYPOTHÈSE]** 0 % en prudent (la Cour juge les coupes passées irréalistes), 1 / 2 / 4 % ensuite, par non-remplacement. Taux appliqués au reliquat du vivier : 0,00 % / 1,00 % / 2,00 % / 4,00 % (prudent / intermédiaire / ambitieux / radical). Répartition : non-remplacement 100 %, redéploiement 0 %, suppression indemnisée 0 %, transfert 0 %.

**G. Économies.** Résultats du moteur financier (`modele/modele.py`), en M€ 2026 constants, par écart à une référence qui remplace tous les départs. Le non-remplacement est valorisé au coût d'entrée hors pension, croissant de 1 % par an jusqu'au coût moyen ; les postes ne disparaissent qu'au rythme des départs à la retraite du vivier.

| Indicateur | Prudent | Intermédiaire | Ambitieux | Radical |
|---|---:|---:|---:|---:|
| ETP visés (cible) | 0 | 2 282 | 4 494 | 8 710 |
| Postes en moins en 2036 | 0 | 2 282 | 4 494 | 8 710 |
| ETP redéployés | 0 | 0 | 0 | 0 |
| Cible non réalisée en 2036 (ETP) | 0 | 0 | 0 | 0 |
| Économie nette 2036 (M€) | 0,0 | 106,7 | 210,2 | 407,3 |
| Cumul net 2027-2031 (M€) | 0,0 | −38,2 | −75,2 | −145,8 |
| Cumul net 2027-2036 (M€) | 0,0 | 474,8 | 935,2 | 1 812,6 |
| Cumul consolidé APU 2027-2036 (M€) | 0,0 | 238,3 | 469,3 | 909,6 |
| Investissement total (M€) | 0,0 | 201,0 | 395,9 | 767,4 |
| Coût récurrent à terme (M€/an) | 0,0 | 0,0 | 0,0 | 0,0 |

**H. Investissements nécessaires.** **[HYPOTHÈSE de convention]** Deux années d'économie brute (outil d'allocation, comptabilité d'activité).

**I. Conséquences sur le service.** Risque de dégradation des délais en préfecture et des contrôles de terrain si l'outil sous-estime la charge.

**J. Contraintes.** Réorganisations par décret ; implantations territoriales politiquement sensibles.

**K. Calendrier.** Outil d'allocation 2027 ; application 2028-2032.

**L. Niveau de confiance.** **Faible.** Le précédent français montre des compensations par contrats courts.

**Indicateur de validation à 2-3 ans.** ETPT par activité mesurée (titres, contrôles) dans chaque département ; délais ; part des contrats courts.

**M. Sources et calculs.**

- [Note 06](../06_doublons_structures.md)
- [Note 05](../05_reformes_etrangeres.md)
- [ONS, série C9KQ](https://www.ons.gov.uk/generator?format=csv&uri=/employmentandlabourmarket/peopleinwork/publicsectorpersonnel/timeseries/c9kq/pse)

Calculs : Aucun calcul de base au-delà du vivier ; taux directement en part du reliquat. Paramètres nationaux : [hypotheses.json](../../modele/hypotheses.json) ; ligne `R05` de [catalogue_reformes.csv](../../data/reformes/catalogue_reformes.csv) ; vivier dans [registre_viviers.csv](../../data/reformes/registre_viviers.csv). Reproduction : `python -I scripts/11_catalogue.py`.
