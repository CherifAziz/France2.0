# Réforme R08 — Supprimer les procédures et obligations d'information sans usage

Vivier : **V_FPE_AUTRES** (Autres corps administratifs et techniques de la FPE (ministères et EPA, dont opérateurs)) · ordre d'application **21** · début **2028**, durée **5 ans** · confiance **faible**.

**A. Problème identifié.** **[FAIT]** Le Sénat recensait en 2015 environ **1 200 procédures** en silence vaut accord sur 3 600, avec **42 décrets d'exceptions** et des délais de deux à douze mois. La loi de simplification n° 2026-403 a été promulguée le **26 mai 2026** ; son application reste à suivre.

**B. Organisation actuelle.** Procédures définies par les textes ; aucun inventaire national des obligations d'information avec leur coût public.

**C. Comparaison internationale.** **[FAIT]** Les Pays-Bas ont réduit d'environ **20 %** la charge d'information des entreprises entre 2002 et 2007 (cible −25 %) avec le Standard Cost Model : un gain privé, pas une baisse d'effectifs publics mesurée.

**D. Réforme proposée.** Mesurer le coût public de chaque obligation (temps × volume) ; supprimer celles dont l'information n'est pas utilisée ; étendre le silence vaut accord à des autorisations à faible risque.

**E. Effectifs concernés.** Vivier « autres administratifs et techniques de l'État » : 231 659 ETP.

**F. Réduction envisageable.** **[HYPOTHÈSE]** 0 / 0,5 / 1,5 / 3 %. Les gains publiés sont surtout privés ; la part publique est inconnue. Taux appliqués au reliquat du vivier : 0,00 % / 0,50 % / 1,50 % / 3,00 % (prudent / intermédiaire / ambitieux / radical). Répartition : non-remplacement 100 %, redéploiement 0 %, suppression indemnisée 0 %, transfert 0 %.

**G. Économies.** Résultats du moteur financier (`modele/modele.py`), en M€ 2026 constants, par écart à une référence qui remplace tous les départs. Le non-remplacement est valorisé au coût d'entrée hors pension, croissant de 1 % par an jusqu'au coût moyen ; les postes ne disparaissent qu'au rythme des départs à la retraite du vivier.

| Indicateur | Prudent | Intermédiaire | Ambitieux | Radical |
|---|---:|---:|---:|---:|
| ETP visés (cible) | 0 | 1 107 | 3 172 | 5 840 |
| Postes en moins en 2036 | 0 | 1 107 | 3 172 | 5 840 |
| ETP redéployés | 0 | 0 | 0 | 0 |
| Cible non réalisée en 2036 (ETP) | 0 | 0 | 0 | 0 |
| Économie nette 2036 (M€) | 0,0 | 51,8 | 148,4 | 263,5 |
| Cumul net 2027-2031 (M€) | 0,0 | −18,5 | −53,1 | −514,5 |
| Cumul net 2027-2036 (M€) | 0,0 | 230,4 | 660,2 | 244,7 |
| Cumul consolidé APU 2027-2036 (M€) | 0,0 | 115,6 | 331,3 | −21,0 |
| Investissement total (M€) | 0,0 | 97,5 | 279,5 | 514,5 |
| Coût récurrent à terme (M€/an) | 0,0 | 0,0 | 0,0 | 0,0 |

**H. Investissements nécessaires.** **[HYPOTHÈSE de convention]** Deux années d'économie brute (mesure, réécriture des textes).

**I. Conséquences sur le service.** Moins de charges pour usagers et entreprises ; risque juridique si un contrôle utile est supprimé.

**J. Contraintes.** Modifications législatives et réglementaires ; droit de l'UE.

**K. Calendrier.** Inventaire 2027 ; suppressions par vagues 2028-2032.

**L. Niveau de confiance.** **Faible.** Gain public non mesuré.

**Indicateur de validation à 2-3 ans.** Nombre d'obligations supprimées pondéré par leur volume ; temps public mesuré avant et après.

**M. Sources et calculs.**

- [Note 07](../07_simplification_reglementaire.md)
- [Note 05](../05_reformes_etrangeres.md)

Calculs : Taux en part du reliquat. Paramètres nationaux : [hypotheses.json](../../modele/hypotheses.json) ; ligne `R08` de [catalogue_reformes.csv](../../data/reformes/catalogue_reformes.csv) ; vivier dans [registre_viviers.csv](../../data/reformes/registre_viviers.csv). Reproduction : `python -I scripts/11_catalogue.py`.
