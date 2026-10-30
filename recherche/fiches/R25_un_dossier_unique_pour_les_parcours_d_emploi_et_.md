# Réforme R25 — Un dossier unique pour les parcours d'emploi et d'insertion

Vivier : **V_FT** (France Travail) · ordre d'application **20** · début **2028**, durée **5 ans** · confiance **faible**.

**A. Problème identifié.** **[FAIT]** Les dépenses françaises de catégorie 1 des politiques du marché du travail atteignent **6 899 M€ en 2023**, dont **5 187 M€** d'autres coûts non ventilés (75,2 %) : ce manque de ventilation empêche d'identifier les doublons.

**B. Organisation actuelle.** France Travail, missions locales, Cap emploi, départements (RSA) ; plafond de **48 232 ETPT** pour France Travail en 2027.

**C. Comparaison internationale.** **[FAIT]** Norvège : la fusion NAV a connu un démarrage défavorable et des progrès hétérogènes après deux ans, sans bilan net publié.

**D. Réforme proposée.** Dossier et diagnostic uniques partagés entre opérateurs du réseau pour l'emploi ; suppression des saisies multiples ; non-remplacement des postes de saisie.

**E. Effectifs concernés.** Vivier France Travail : **48 232 ETPT** (plafond PLF 2027) ; agents de droit privé.

**F. Réduction envisageable.** **[HYPOTHÈSE]** 0 / 1 / 2 / 3 %. Taux appliqués au reliquat du vivier : 0,00 % / 1,00 % / 2,00 % / 3,00 % (prudent / intermédiaire / ambitieux / radical). Répartition : non-remplacement 100 %, redéploiement 0 %, suppression indemnisée 0 %, transfert 0 %.

**G. Économies.** Résultats du moteur financier (`modele/modele.py`), en M€ 2026 constants, par écart à une référence qui remplace tous les départs. Le non-remplacement est valorisé au coût d'entrée hors pension, croissant de 1 % par an jusqu'au coût moyen ; les postes ne disparaissent qu'au rythme des départs à la retraite du vivier.

| Indicateur | Prudent | Intermédiaire | Ambitieux | Radical |
|---|---:|---:|---:|---:|
| ETP visés (cible) | 0 | 482 | 965 | 1 447 |
| Postes en moins en 2036 | 0 | 482 | 965 | 1 447 |
| ETP redéployés | 0 | 0 | 0 | 0 |
| Cible non réalisée en 2036 (ETP) | 0 | 0 | 0 | 0 |
| Économie nette 2036 (M€) | 0,0 | 22,6 | 45,1 | 67,7 |
| Cumul net 2027-2031 (M€) | 0,0 | −8,1 | −16,1 | −24,2 |
| Cumul net 2027-2036 (M€) | 0,0 | 100,4 | 200,7 | 301,1 |
| Cumul consolidé APU 2027-2036 (M€) | 0,0 | 50,4 | 100,7 | 151,1 |
| Investissement total (M€) | 0,0 | 42,5 | 85,0 | 127,5 |
| Coût récurrent à terme (M€/an) | 0,0 | 0,0 | 0,0 | 0,0 |

**H. Investissements nécessaires.** **[HYPOTHÈSE de convention]** Deux années d'économie brute.

**I. Conséquences sur le service.** Parcours plus fluides pour les demandeurs ; risque de transfert de charge vers les partenaires.

**J. Contraintes.** Partage de données entre organismes ; gouvernance du réseau.

**K. Calendrier.** 2028-2032.

**L. Niveau de confiance.** **Faible.** Coûts non ventilés.

**Indicateur de validation à 2-3 ans.** Temps de saisie par inscription ; délais d'entrée en parcours ; ETP par demandeur suivi.

**M. Sources et calculs.**

- [Note 04a](../04a_fiscalite_emploi.md)
- [Note 06](../06_doublons_structures.md)
- [Note 05](../05_reformes_etrangeres.md)
- [Jaune « Opérateurs de l'État », PLF 2027](https://www.budget.gouv.fr/documentation/file-download/34432)

Calculs : Taux en part du vivier de 48 232 ETPT. Paramètres nationaux : [hypotheses.json](../../modele/hypotheses.json) ; ligne `R25` de [catalogue_reformes.csv](../../data/reformes/catalogue_reformes.csv) ; vivier dans [registre_viviers.csv](../../data/reformes/registre_viviers.csv). Reproduction : `python -I scripts/11_catalogue.py`.
