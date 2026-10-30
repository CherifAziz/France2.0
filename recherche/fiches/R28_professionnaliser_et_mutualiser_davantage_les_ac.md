# Réforme R28 — Professionnaliser et mutualiser davantage les achats publics

Vivier : **V_FONCT** (Dépenses de fonctionnement sans effectif (achats, immobilier, instances)) · ordre d'application **10** · début **2027**, durée **5 ans** · confiance **moyen**.

**A. Problème identifié.** **[FAIT]** Les achats de l'État représentent **50,245 Md€ en 2025**, dont **24,364 Md€ hors défense et sécurité**. La DAE calcule **412,53 M€** d'économies d'achats en 2025, selon une méthode de prix de référence qu'elle distingue elle-même des économies budgétaires.

**B. Organisation actuelle.** Direction des achats de l'État, plateformes régionales, ministères et établissements publics ; 44 agents ont expérimenté des outils d'IA d'achat (gains pouvant dépasser 60 % sur certaines tâches).

**C. Comparaison internationale.** **[ESTIMATION]** Corée : KONEPS gère un volume de 6,82 Md USD dans le tableau OCDE, dont 82,11 % privé, sans économie nette réconciliée.

**D. Réforme proposée.** Étendre les marchés mutualisés, standardiser les besoins courants, convertir une part des économies calculées en baisses de crédits effectives.

**E. Effectifs concernés.** Aucun effectif ; dépenses d'achats hors défense de 24,364 Md€.

**F. Réduction envisageable.** Sans réduction d'effectifs. Taux appliqués au reliquat du vivier : 0,00 % / 0,00 % / 0,00 % / 0,00 % (prudent / intermédiaire / ambitieux / radical). Répartition : non-remplacement 100 %, redéploiement 0 %, suppression indemnisée 0 %, transfert 0 %.

**G. Économies.** Résultats du moteur financier (`modele/modele.py`), en M€ 2026 constants, par écart à une référence qui remplace tous les départs. Le non-remplacement est valorisé au coût d'entrée hors pension, croissant de 1 % par an jusqu'au coût moyen ; les postes ne disparaissent qu'au rythme des départs à la retraite du vivier.

| Indicateur | Prudent | Intermédiaire | Ambitieux | Radical |
|---|---:|---:|---:|---:|
| ETP visés (cible) | 0 | 0 | 0 | 0 |
| Postes en moins en 2036 | 0 | 0 | 0 | 0 |
| ETP redéployés | 0 | 0 | 0 | 0 |
| Cible non réalisée en 2036 (ETP) | 0 | 0 | 0 | 0 |
| Économie nette 2036 (M€) | 61,0 | 122,0 | 244,0 | 365,0 |
| Cumul net 2027-2031 (M€) | 183,0 | 366,0 | 732,0 | 1 095,0 |
| Cumul net 2027-2036 (M€) | 488,0 | 976,0 | 1 952,0 | 2 920,0 |
| Cumul consolidé APU 2027-2036 (M€) | 488,0 | 976,0 | 1 952,0 | 2 920,0 |
| Investissement total (M€) | 0,0 | 0,0 | 0,0 | 0,0 |
| Coût récurrent à terme (M€/an) | 0,0 | 0,0 | 0,0 | 0,0 |

**H. Investissements nécessaires.** Coûts de professionnalisation non chiffrés ; supposés couverts par les équipes existantes.

**I. Conséquences sur le service.** Risque d'éviction des PME et d'allongement des délais d'achat.

**J. Contraintes.** Code de la commande publique ; régulation des crédits.

**K. Calendrier.** 2027-2031.

**L. Niveau de confiance.** **Moyen.** Assiette documentée ; conversion budgétaire hypothétique.

**Indicateur de validation à 2-3 ans.** Économies budgétaires constatées (crédits annulés) par rapport aux économies calculées par la DAE ; prix unitaires des achats courants.

**M. Sources et calculs.**

- [Note 04d](../04d_territoires_fonctions_support.md)
- [Note 05](../05_reformes_etrangeres.md)

Calculs : **[HYPOTHÈSE]** Économie budgétaire supplémentaire de 0,25 / 0,5 / 1 / 1,5 % des 24 364 M€ d'achats hors défense : 61 / 122 / 244 / 365 M€/an à terme. Paramètres nationaux : [hypotheses.json](../../modele/hypotheses.json) ; ligne `R28` de [catalogue_reformes.csv](../../data/reformes/catalogue_reformes.csv) ; vivier dans [registre_viviers.csv](../../data/reformes/registre_viviers.csv). Reproduction : `python -I scripts/11_catalogue.py`.
