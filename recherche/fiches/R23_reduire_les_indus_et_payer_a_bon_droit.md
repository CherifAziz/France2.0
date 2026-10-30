# Réforme R23 — Réduire les indus et payer à bon droit

Vivier : **V_OPS** (Organismes de protection sociale (droit privé, financement public prédominant)) · ordre d'application **21** · début **2028**, durée **4 ans** · confiance **moyen**.

**A. Problème identifié.** **[FAIT]** La Cour des comptes estime en 2025 que ramener les pertes d'indus du régime général au niveau de 2019 procurerait **plus de 100 M€ par an**. Ce sont des pertes évitées et des recettes, sans économie administrative.

**B. Organisation actuelle.** Caisses du régime général ; contrôles a priori et a posteriori, recouvrement des indus.

**C. Comparaison internationale.** **[FAIT]** Robodebt (Australie) montre qu'un recouvrement automatisé illégal coûte bien plus qu'il ne rapporte ; Toeslagen (Pays-Bas) a valu une amende de 2,75 M€ et 5,748 Md€ de réparations exécutées en 2020-2024.

**D. Réforme proposée.** Fiabiliser les données de ressources en amont, réduire les indus à la source plutôt que les recouvrer ; aucune réduction d'effectifs.

**E. Effectifs concernés.** Aucun effectif réduit ; vivier organismes de protection sociale pour rattachement.

**F. Réduction envisageable.** **[FAIT]** Aucune réduction d'effectifs. Effet recettes de **100 M€/an** à terme dans tous les scénarios, borne basse de la Cour. Taux appliqués au reliquat du vivier : 0,00 % / 0,00 % / 0,00 % / 0,00 % (prudent / intermédiaire / ambitieux / radical). Répartition : non-remplacement 100 %, redéploiement 0 %, suppression indemnisée 0 %, transfert 0 %.

**G. Économies.** Résultats du moteur financier (`modele/modele.py`), en M€ 2026 constants, par écart à une référence qui remplace tous les départs. Le non-remplacement est valorisé au coût d'entrée hors pension, croissant de 1 % par an jusqu'au coût moyen ; les postes ne disparaissent qu'au rythme des départs à la retraite du vivier.

| Indicateur | Prudent | Intermédiaire | Ambitieux | Radical |
|---|---:|---:|---:|---:|
| ETP visés (cible) | 0 | 0 | 0 | 0 |
| Postes en moins en 2036 | 0 | 0 | 0 | 0 |
| ETP redéployés | 0 | 0 | 0 | 0 |
| Cible non réalisée en 2036 (ETP) | 0 | 0 | 0 | 0 |
| Économie nette 2036 (M€) | 100,0 | 100,0 | 100,0 | 100,0 |
| Cumul net 2027-2031 (M€) | 250,0 | 250,0 | 250,0 | 250,0 |
| Cumul net 2027-2036 (M€) | 750,0 | 750,0 | 750,0 | 750,0 |
| Cumul consolidé APU 2027-2036 (M€) | 750,0 | 750,0 | 750,0 | 750,0 |
| Investissement total (M€) | 0,0 | 0,0 | 0,0 | 0,0 |
| Coût récurrent à terme (M€/an) | 0,0 | 0,0 | 0,0 | 0,0 |

**H. Investissements nécessaires.** Coût des contrôles supplémentaires **NON TROUVÉ** : l'effet net est donc surestimé.

**I. Conséquences sur le service.** Moins de dettes pour les allocataires ; risque de contrôles intrusifs ou d'erreurs automatisées.

**J. Contraintes.** Droit à l'erreur (ESSOC), garanties procédurales, RGPD.

**K. Calendrier.** 2028-2031.

**L. Niveau de confiance.** **Moyen.** Montant de la Cour, coûts de contrôle non chiffrés.

**Indicateur de validation à 2-3 ans.** Montant des indus non recouvrés ; taux d'indus à la source ; contentieux.

**M. Sources et calculs.**

- [Note 04c](../04c_sante_protection_sociale.md)
- [Note 05](../05_reformes_etrangeres.md)
- [Note 09](../09_ia_preuves_internationales.md)
- [Cour des comptes, RALFSS 2025, chapitre IX](https://www.ccomptes.fr/sites/default/files/2025-05/20250526-RALFSS-2025-Gestion-indus-par-caisses-SS-du-regime-general.pdf)

Calculs : effet_recettes = 100 M€/an (Cour des comptes, borne basse « plus de 100 M€ »). Paramètres nationaux : [hypotheses.json](../../modele/hypotheses.json) ; ligne `R23` de [catalogue_reformes.csv](../../data/reformes/catalogue_reformes.csv) ; vivier dans [registre_viviers.csv](../../data/reformes/registre_viviers.csv). Reproduction : `python -I scripts/11_catalogue.py`.
