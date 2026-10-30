# Réforme R06 — Resserrer les administrations centrales au-delà du PLF 2027

Vivier : **V_FPE_AUTRES** (Autres corps administratifs et techniques de la FPE (ministères et EPA, dont opérateurs)) · ordre d'application **12** · début **2028**, durée **4 ans** · confiance **faible**.

**A. Problème identifié.** **[FAIT]** Le PLF 2027 prévoit **−812 ETP d'administration centrale** et **+404 ETP numériques réinternalisés**, déjà inclus dans ses schémas d'emplois. Ces mouvements appartiennent à la trajectoire de référence et ne sont pas recomptés ici.

**B. Organisation actuelle.** Directions d'administration centrale des ministères ; effectif total des centrales non isolé dans les sources consultées.

**C. Comparaison internationale.** **[FAIT]** Le NAO mesure **2,49 Md£ de baisse salariale annualisée réelle** entre 2010 et 2014 dans l'administration centrale britannique, corrigée du périmètre ; la série ONS montre ensuite un rebond.

**D. Réforme proposée.** Supprimer les fonctions doublonnées entre centrales et opérateurs (tutelle, études, communication) ; réduire les niveaux hiérarchiques ; non-remplacement ciblé.

**E. Effectifs concernés.** Vivier « autres administratifs et techniques de l'État » : 231 659 ETP ; part des centrales non publiée.

**F. Réduction envisageable.** **[HYPOTHÈSE]** Au-delà du PLF 2027 : 0 / 1 / 2 / 4 % du reliquat. Prudent à zéro, la référence absorbant déjà −812 ETP. Taux appliqués au reliquat du vivier : 0,00 % / 1,00 % / 2,00 % / 4,00 % (prudent / intermédiaire / ambitieux / radical). Répartition : non-remplacement 100 %, redéploiement 0 %, suppression indemnisée 0 %, transfert 0 %.

**G. Économies.** Résultats du moteur financier (`modele/modele.py`), en M€ 2026 constants, par écart à une référence qui remplace tous les départs. Le non-remplacement est valorisé au coût d'entrée hors pension, croissant de 1 % par an jusqu'au coût moyen ; les postes ne disparaissent qu'au rythme des départs à la retraite du vivier.

| Indicateur | Prudent | Intermédiaire | Ambitieux | Radical |
|---|---:|---:|---:|---:|
| ETP visés (cible) | 0 | 2 259 | 4 404 | 8 362 |
| Postes en moins en 2036 | 0 | 2 259 | 4 404 | 8 362 |
| ETP redéployés | 0 | 0 | 0 | 0 |
| Cible non réalisée en 2036 (ETP) | 0 | 0 | 0 | 0 |
| Économie nette 2036 (M€) | 0,0 | 106,2 | 207,0 | 391,6 |
| Cumul net 2027-2031 (M€) | 0,0 | 2,5 | 4,9 | −86,1 |
| Cumul net 2027-2036 (M€) | 0,0 | 522,9 | 1 019,5 | 1 801,0 |
| Cumul consolidé APU 2027-2036 (M€) | 0,0 | 270,2 | 526,9 | 912,8 |
| Investissement total (M€) | 0,0 | 199,0 | 388,0 | 736,7 |
| Coût récurrent à terme (M€/an) | 0,0 | 0,0 | 0,0 | 0,0 |

**H. Investissements nécessaires.** **[HYPOTHÈSE de convention]** Deux années d'économie brute.

**I. Conséquences sur le service.** Risque de perte de capacité de pilotage et de recours accru au conseil externe (59,9 M€ d'AE de conseil en stratégie et organisation en 2025).

**J. Contraintes.** Décrets d'organisation ; risque de transfert de charge vers les opérateurs.

**K. Calendrier.** 2028-2031.

**L. Niveau de confiance.** **Faible.** Base et gisement non mesurés.

**Indicateur de validation à 2-3 ans.** ETP des centrales à périmètre constant ; dépenses de conseil ; délais de publication des textes d'application.

**M. Sources et calculs.**

- [Note 10 — audit des propositions](../10_audit_propositions.md)
- [Note 01c — coûts](../01c_couts_entree_pensions.md)
- [Dossier de presse PLF 2027, PDF p. 58-59](https://presse.economie.gouv.fr/download?n=1076%20-%20DP%20-%20Budget%202027-pdf&id=184723)
- [NAO, Central government staff costs, 2015](https://www.nao.org.uk/wp-content/uploads/2015/06/Central-government-staff-costs.pdf)

Calculs : Taux en part du reliquat ; mouvements du PLF 2027 exclus (référence). Paramètres nationaux : [hypotheses.json](../../modele/hypotheses.json) ; ligne `R06` de [catalogue_reformes.csv](../../data/reformes/catalogue_reformes.csv) ; vivier dans [registre_viviers.csv](../../data/reformes/registre_viviers.csv). Reproduction : `python -I scripts/11_catalogue.py`.
