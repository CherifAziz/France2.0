# Réforme R09 — Créer des services partagés de gestion pour les opérateurs

Vivier : **V_FPE_AUTRES** (Autres corps administratifs et techniques de la FPE (ministères et EPA, dont opérateurs)) · ordre d'application **30** · début **2028**, durée **5 ans** · confiance **faible**.

**A. Problème identifié.** **[HYPOTHÈSE externe]** Le Sénat évalue les fonctions support d'un sous-ensemble d'opérateurs à **2,7 Md€**, en supposant qu'elles pèsent 10 % des charges de personnel et de fonctionnement, et juge **très volontariste** une réduction de 20 % (540 M€).

**B. Organisation actuelle.** Chaque opérateur gère sa paie, ses achats et sa comptabilité ; quelques mutualisations existent sans recensement complet.

**C. Comparaison internationale.** **[FAIT]** En Suède, l'audit de 2021 trouve des gains de support souvent **réinvestis dans le support**. Au Canada, la centralisation de la paie (Phénix) a retiré 1 200 postes de conseillers mais coûte encore **937,5 M CAD** en 2024-25.

**D. Réforme proposée.** Centres de services partagés par réseau d'opérateurs proches (paie, achats, comptabilité), adhésion progressive, conventions de service et indicateurs de qualité ; non-remplacement des postes de gestion libérés.

**E. Effectifs concernés.** Vivier « autres administratifs et techniques de l'État » : 231 659 ETP ; part support des opérateurs inconnue (hypothèse sénatoriale de 10 % des charges).

**F. Réduction envisageable.** **[HYPOTHÈSE]** 0,5 / 1,5 / 3 / 4 %. Le scénario ambitieux correspond à peu près à l'hypothèse sénatoriale jugée très volontariste. Taux appliqués au reliquat du vivier : 0,50 % / 1,50 % / 3,00 % / 4,00 % (prudent / intermédiaire / ambitieux / radical). Répartition : non-remplacement 100 %, redéploiement 0 %, suppression indemnisée 0 %, transfert 0 %.

**G. Économies.** Résultats du moteur financier (`modele/modele.py`), en M€ 2026 constants, par écart à une référence qui remplace tous les départs. Le non-remplacement est valorisé au coût d'entrée hors pension, croissant de 1 % par an jusqu'au coût moyen ; les postes ne disparaissent qu'au rythme des départs à la retraite du vivier.

| Indicateur | Prudent | Intermédiaire | Ambitieux | Radical |
|---|---:|---:|---:|---:|
| ETP visés (cible) | 1 147 | 3 304 | 6 250 | 7 553 |
| Postes en moins en 2036 | 1 147 | 3 304 | 6 250 | 7 553 |
| ETP redéployés | 0 | 0 | 0 | 0 |
| Cible non réalisée en 2036 (ETP) | 0 | 0 | 0 | 0 |
| Économie nette 2036 (M€) | 53,6 | 154,5 | 291,9 | 311,8 |
| Cumul net 2027-2031 (M€) | −19,2 | −55,3 | −130,6 | −665,4 |
| Cumul net 2027-2036 (M€) | 238,6 | 687,7 | 1 259,3 | −142,4 |
| Cumul consolidé APU 2027-2036 (M€) | 119,8 | 345,1 | 625,8 | −325,5 |
| Investissement total (M€) | 101,0 | 291,1 | 550,6 | 665,4 |
| Coût récurrent à terme (M€/an) | 0,0 | 0,0 | 0,0 | 0,0 |

**H. Investissements nécessaires.** **[HYPOTHÈSE de convention]** Deux années d'économie brute ; risque de dépassement de type Phénix non intégré.

**I. Conséquences sur le service.** Délais de paie et de paiement fournisseurs à surveiller pendant la bascule.

**J. Contraintes.** Systèmes d'information hétérogènes ; autonomie juridique des opérateurs.

**K. Calendrier.** Pilote sur un réseau volontaire 2028 ; extension 2029-2032.

**L. Niveau de confiance.** **Faible.** Gisement supposé, précédents mitigés.

**Indicateur de validation à 2-3 ans.** Coût de gestion par agent et par facture ; délais de paiement ; erreurs de paie.

**M. Sources et calculs.**

- [Note 04d](../04d_territoires_fonctions_support.md)
- [Note 06](../06_doublons_structures.md)
- [Riksrevisionen 2021:03](https://www.riksrevisionen.se/download/18.2008b69c18bd0f6ed3f2f2a7/1618300235879/RiR%202021_03_ENG.pdf)
- [Vérificateur général du Canada, mars 2026](https://www.canada.ca/content/dam/oag-bvg/audit-reports/documents/ag-202603-modernizing-pay-system.pdf)

Calculs : Taux en part du reliquat. Paramètres nationaux : [hypotheses.json](../../modele/hypotheses.json) ; ligne `R09` de [catalogue_reformes.csv](../../data/reformes/catalogue_reformes.csv) ; vivier dans [registre_viviers.csv](../../data/reformes/registre_viviers.csv). Reproduction : `python -I scripts/11_catalogue.py`.
