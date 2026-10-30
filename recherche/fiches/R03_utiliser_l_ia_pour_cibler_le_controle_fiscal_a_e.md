# Réforme R03 — Utiliser l'IA pour cibler le contrôle fiscal, à effectifs redéployés

Vivier : **V_DGFIP** (DGFiP, titulaires et contractuels en fonction 2025) · ordre d'application **40** · début **2028**, durée **5 ans** · confiance **faible**.

**A. Problème identifié.** **[FAIT]** ISORA déclare **10 153 ETP d'audit et vérification**, **6 302 de recouvrement forcé** et **4 933 de contentieux** en 2023. Ces fonctions rapportent des recettes : réduire leurs effectifs n'est pas une économie nette évidente.

**B. Organisation actuelle.** Contrôle fiscal et recouvrement assurés par les services de la DGFiP ; outils de ciblage par analyse de données déjà utilisés (non chiffrés dans les sources lues).

**C. Comparaison internationale.** **[FAIT]** Aucune étude ouverte dans ce dossier ne mesure l'effet causal de l'IA sur le rendement du contrôle fiscal. Les gains de tâche mesurés ailleurs portent sur la rédaction ou le support client (−40 % de temps chez Noy–Zhang ; +15 % de dossiers résolus par heure chez Brynjolfsson–Li–Raymond).

**D. Réforme proposée.** Déployer l'aide documentaire et la priorisation des dossiers ; **réaffecter** la capacité libérée vers les contrôles à meilleur rendement net, sans baisse d'effectifs.

**E. Effectifs concernés.** Vivier DGFiP : 94 468 ETP ; fonctions visées : 21 388 ETP (audit, recouvrement forcé, contentieux).

**F. Réduction envisageable.** **[HYPOTHÈSE]** 0 / 1 / 2 / 3 % du reliquat du vivier, **entièrement redéployés**. Cette fiche ne produit aucune économie de masse salariale ; elle documente l'usage du temps libéré. Taux appliqués au reliquat du vivier : 0,00 % / 1,00 % / 2,00 % / 3,00 % (prudent / intermédiaire / ambitieux / radical). Répartition : non-remplacement 0 %, redéploiement 100 %, suppression indemnisée 0 %, transfert 0 %.

**G. Économies.** Résultats du moteur financier (`modele/modele.py`), en M€ 2026 constants, par écart à une référence qui remplace tous les départs. Le non-remplacement est valorisé au coût d'entrée hors pension, croissant de 1 % par an jusqu'au coût moyen ; les postes ne disparaissent qu'au rythme des départs à la retraite du vivier.

| Indicateur | Prudent | Intermédiaire | Ambitieux | Radical |
|---|---:|---:|---:|---:|
| ETP visés (cible) | 0 | 930 | 1 835 | 2 715 |
| Postes en moins en 2036 | 0 | 0 | 0 | 0 |
| ETP redéployés | 0 | 930 | 1 835 | 2 715 |
| Cible non réalisée en 2036 (ETP) | 0 | 0 | 0 | 0 |
| Économie nette 2036 (M€) | 0,0 | −1,0 | −1,0 | −1,0 |
| Cumul net 2027-2031 (M€) | 0,0 | −27,2 | −27,2 | −27,2 |
| Cumul net 2027-2036 (M€) | 0,0 | −32,2 | −32,2 | −32,2 |
| Cumul consolidé APU 2027-2036 (M€) | 0,0 | −32,2 | −32,2 | −32,2 |
| Investissement total (M€) | 0,0 | 25,2 | 25,2 | 25,2 |
| Coût récurrent à terme (M€/an) | 0,0 | 1,0 | 1,0 | 1,0 |

**H. Investissements nécessaires.** **[ESTIMATION par analogie]** France Travail a investi 12,875 M€ en IA en 2025 pour environ 48 232 ETPT, soit 267 € par ETP ; appliqué au vivier sur trois ans. Coût de fonctionnement : 10,5 € par ETP et par an, même source (probablement sous-estimé).

**I. Conséquences sur le service.** Gain potentiel de recettes et d'équité si le ciblage est juste ; risque de biais et de contestation des contrôles fondés sur des scores.

**J. Contraintes.** Motivation des décisions, droit à l'explication (CRPA), RGPD art. 22, secret fiscal.

**K. Calendrier.** Pilotes 2028 ; évaluation à 24-36 mois ; extension conditionnée au rendement net mesuré.

**L. Niveau de confiance.** **Faible.** Aucune mesure française publique du rendement ; effet sur les recettes non chiffré, donc laissé à zéro.

**Indicateur de validation à 2-3 ans.** Rendement net par contrôle (droits et pénalités recouvrés moins coûts) ; taux de contentieux perdus ; part des dossiers ciblés par l'outil, comparée à un groupe témoin.

**M. Sources et calculs.**

- [Note 04a](../04a_fiscalite_emploi.md)
- [Note 09 — preuves internationales IA](../09_ia_preuves_internationales.md)
- [Rapport IGF–IGAS–IGA, avril 2026](https://igas.gouv.fr/sites/igas/files/2026-07/Rapport%20D%C3%A9ploiement%20IA%20(2026).pdf)

Calculs : Aucune économie salariale (redéploiement) ; effet recettes non chiffré = 0. Paramètres nationaux : [hypotheses.json](../../modele/hypotheses.json) ; ligne `R03` de [catalogue_reformes.csv](../../data/reformes/catalogue_reformes.csv) ; vivier dans [registre_viviers.csv](../../data/reformes/registre_viviers.csv). Reproduction : `python -I scripts/11_catalogue.py`.
