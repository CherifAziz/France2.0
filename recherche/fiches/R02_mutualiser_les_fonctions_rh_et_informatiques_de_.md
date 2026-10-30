# Réforme R02 — Mutualiser les fonctions RH et informatiques de la DGFiP

Vivier : **V_DGFIP** (DGFiP, titulaires et contractuels en fonction 2025) · ordre d'application **30** · début **2028**, durée **5 ans** · confiance **faible**.

**A. Problème identifié.** **[FAIT]** ISORA déclare **1 881 ETP de RH** et **2 536 ETP d'informatique** dans le champ fiscal français en 2023, soit 11,5 % des ETP fiscaux. Ces fonctions servent des réseaux distincts qui pourraient partager des outils et des centres de gestion.

**B. Organisation actuelle.** Gestion RH et informatique assurées par la DGFiP pour son propre réseau, à côté des services interministériels (DINUM, centres de services partagés). Répartition exacte par site non publiée.

**C. Comparaison internationale.** **[FAIT]** En Suède, l'audit de 2021 constate que les gains des services partagés de support ont souvent été **réinvestis dans le support** ; Statens servicecenter sert 171 agences clientes en 2025, sans bilan d'économies. Le rapport Ravignon retient des gains RH hypothétiques de **5 à 10 %** pour les collectivités.

**D. Réforme proposée.** Regrouper les actes de gestion RH répétitifs (paie, positions, actes collectifs) et les fonctions informatiques non spécifiques dans des centres partagés ; conserver la maîtrise d'ouvrage métier fiscale.

**E. Effectifs concernés.** Vivier DGFiP : 94 468 ETP. Périmètre visé : 4 417 ETP (RH 1 881 + informatique 2 536).

**F. Réduction envisageable.** **[HYPOTHÈSE]** Prudent : 5 % de la seule RH ; intermédiaire : 10 % de RH + informatique ; ambitieux 15 % ; radical 20 %, bornes du rapport Ravignon et de l'estimation sénatoriale jugée « très volontariste ». Taux appliqués au reliquat du vivier : 0,10 % / 0,47 % / 0,70 % / 0,94 % (prudent / intermédiaire / ambitieux / radical). Répartition : non-remplacement 100 %, redéploiement 0 %, suppression indemnisée 0 %, transfert 0 %.

**G. Économies.** Résultats du moteur financier (`modele/modele.py`), en M€ 2026 constants, par écart à une référence qui remplace tous les départs. Le non-remplacement est valorisé au coût d'entrée hors pension, croissant de 1 % par an jusqu'au coût moyen ; les postes ne disparaissent qu'au rythme des départs à la retraite du vivier.

| Indicateur | Prudent | Intermédiaire | Ambitieux | Radical |
|---|---:|---:|---:|---:|
| ETP visés (cible) | 94 | 439 | 647 | 859 |
| Postes en moins en 2036 | 94 | 439 | 647 | 859 |
| ETP redéployés | 0 | 0 | 0 | 0 |
| Cible non réalisée en 2036 (ETP) | 0 | 0 | 0 | 0 |
| Économie nette 2036 (M€) | 4,0 | 18,9 | 27,8 | 37,0 |
| Cumul net 2027-2031 (M€) | −1,4 | −6,8 | −10,0 | −13,2 |
| Cumul net 2027-2036 (M€) | 18,0 | 84,1 | 123,9 | 164,5 |
| Cumul consolidé APU 2027-2036 (M€) | 9,0 | 42,2 | 62,2 | 82,5 |
| Investissement total (M€) | 7,6 | 35,6 | 52,4 | 69,6 |
| Coût récurrent à terme (M€/an) | 0,0 | 0,0 | 0,0 | 0,0 |

**H. Investissements nécessaires.** **[HYPOTHÈSE de convention]** Deux années d'économie brute. Le précédent canadien Phénix (937,5 M CAD de dépenses en 2024-25) montre qu'un centre de paie mal conçu peut coûter bien davantage.

**I. Conséquences sur le service.** Risque de délais de gestion RH allongés pendant la migration ; continuité du service informatique fiscal critique pour le recouvrement.

**J. Contraintes.** Sécurité des systèmes fiscaux ; spécificités statutaires ; capacité des centres interministériels à absorber le volume.

**K. Calendrier.** Diagnostic 2027 ; migration progressive 2028-2032 ; réversibilité prévue en cas d'échec.

**L. Niveau de confiance.** **Faible.** Le précédent suédois montre des gains réinvestis ; aucun chiffrage français mesuré.

**Indicateur de validation à 2-3 ans.** Coût complet de gestion par agent géré et par poste de travail ; délais de paie et d'actes ; incidents informatiques ; ETP RH et SI dans ISORA.

**M. Sources et calculs.**

- [Note 04a](../04a_fiscalite_emploi.md)
- [Note 04d — territoires et supports](../04d_territoires_fonctions_support.md)
- [Note 05 — réformes étrangères](../05_reformes_etrangeres.md)
- [Riksrevisionen 2021:03](https://www.riksrevisionen.se/download/18.2008b69c18bd0f6ed3f2f2a7/1618300235879/RiR%202021_03_ENG.pdf)
- [Secrétariat du Conseil du Trésor, dépenses Phénix 2024-25](https://www.canada.ca/en/treasury-board-secretariat/corporate/reports/treasury-board-canada-secretariat-2024-25-departmental-results-report/phoenix-pay-system-expenditures.html)

Calculs : Prudent 1 881×0,05/94 468 = 0,0010 ; intermédiaire 4 417×0,10/94 468 = 0,0047 ; ambitieux 4 417×0,15/94 468 = 0,0070 ; radical 4 417×0,20/94 468 = 0,0094. Paramètres nationaux : [hypotheses.json](../../modele/hypotheses.json) ; ligne `R02` de [catalogue_reformes.csv](../../data/reformes/catalogue_reformes.csv) ; vivier dans [registre_viviers.csv](../../data/reformes/registre_viviers.csv). Reproduction : `python -I scripts/11_catalogue.py`.
