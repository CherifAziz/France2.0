# Réforme R12 — Ne remplacer qu'un départ sur deux dans les fonctions administratives restantes de l'État

Vivier : **V_FPE_AUTRES** (Autres corps administratifs et techniques de la FPE (ministères et EPA, dont opérateurs)) · ordre d'application **50** · début **2029**, durée **5 ans** · confiance **faible**.

**A. Problème identifié.** **[FAIT]** La RGPP (2007-2012) appliquait une règle de non-remplacement d'un départ sur deux. Pour le titre 2, l'économie passe de **808 M€ bruts à 264 M€ nets en 2010**, et de **935 M€ à 373 M€ en 2011**, après retour catégoriel aux agents.

**B. Organisation actuelle.** Règle transversale appliquée après les réformes ciblées, sur le reliquat du vivier.

**C. Comparaison internationale.** **[FAIT]** Irlande : −9,60 % d'emploi public entre 2008 et 2014 par moratoire, puis rebond à 317 495 en 2017. Italie : quotas de remplacement de 25 % des dépenses des sortants en 2016-2018, revenus à 100 % en 2019.

**D. Réforme proposée.** Règle de non-remplacement partiel, appliquée seulement aux postes administratifs non couverts par les fiches précédentes, avec rétrocession de 50 % de l'économie aux agents restants comme sous la RGPP.

**E. Effectifs concernés.** Vivier « autres administratifs et techniques de l'État », reliquat après R04 à R11.

**F. Réduction envisageable.** **[HYPOTHÈSE]** 0 / 0 / 3 / 8 % du reliquat. Cette règle descendante n'est pas une réforme démontrée : elle sert à tester le scénario radical. Taux appliqués au reliquat du vivier : 0,00 % / 0,00 % / 3,00 % / 8,00 % (prudent / intermédiaire / ambitieux / radical). Répartition : non-remplacement 100 %, redéploiement 0 %, suppression indemnisée 0 %, transfert 0 %.

**G. Économies.** Résultats du moteur financier (`modele/modele.py`), en M€ 2026 constants, par écart à une référence qui remplace tous les départs. Le non-remplacement est valorisé au coût d'entrée hors pension, croissant de 1 % par an jusqu'au coût moyen ; les postes ne disparaissent qu'au rythme des départs à la retraite du vivier.

| Indicateur | Prudent | Intermédiaire | Ambitieux | Radical |
|---|---:|---:|---:|---:|
| ETP visés (cible) | 0 | 0 | 5 822 | 13 501 |
| Postes en moins en 2036 | 0 | 0 | 5 822 | 0 |
| ETP redéployés | 0 | 0 | 0 | 0 |
| Cible non réalisée en 2036 (ETP) | 0 | 0 | 0 | 13 501 |
| Économie nette 2036 (M€) | 0,0 | 0,0 | 132,7 | 0,0 |
| Cumul net 2027-2031 (M€) | 0,0 | 0,0 | 0,0 | 0,0 |
| Cumul net 2027-2036 (M€) | 0,0 | 0,0 | 294,7 | 0,0 |
| Cumul consolidé APU 2027-2036 (M€) | 0,0 | 0,0 | 90,7 | 0,0 |
| Investissement total (M€) | 0,0 | 0,0 | 0,0 | 0,0 |
| Coût récurrent à terme (M€/an) | 0,0 | 0,0 | 128,2 | 297,4 |

**H. Investissements nécessaires.** Pas d'investissement. **Coût récurrent** : rétrocession de 50 % de l'économie brute, sur le modèle de la RGPP.

**I. Conséquences sur le service.** Risque élevé de dégradation non ciblée du service et de recours à des contractuels ou prestataires, comme après 2012-2020 dans l'État territorial.

**J. Contraintes.** Acceptabilité sociale ; mécanique déjà éprouvée et abandonnée.

**K. Calendrier.** 2029-2033, après les réformes ciblées.

**L. Niveau de confiance.** **Faible.** Les précédents montrent des économies nettes partielles et des rebonds.

**Indicateur de validation à 2-3 ans.** Effectifs et dépenses de personnel nettes de rétrocession ; recours aux contractuels et prestataires ; délais des services.

**M. Sources et calculs.**

- [Note 06](../06_doublons_structures.md)
- [Note 05](../05_reformes_etrangeres.md)
- [Note 10](../10_audit_propositions.md)

Calculs : Coût récurrent = 0,5 × ETP visés × 44,05 k€ / 1 000 (rétrocession RGPP de 50 %). Paramètres nationaux : [hypotheses.json](../../modele/hypotheses.json) ; ligne `R12` de [catalogue_reformes.csv](../../data/reformes/catalogue_reformes.csv) ; vivier dans [registre_viviers.csv](../../data/reformes/registre_viviers.csv). Reproduction : `python -I scripts/11_catalogue.py`.
