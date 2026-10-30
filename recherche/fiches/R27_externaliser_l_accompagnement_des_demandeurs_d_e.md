# Réforme R27 — Externaliser l'accompagnement des demandeurs d'emploi (non retenue)

Vivier : **V_FT** (France Travail) · ordre d'application **50** · début **2029**, durée **5 ans** · confiance **faible**.

**A. Problème identifié.** **[FAIT sur une annonce]** Le plan audité en note 10 annonce **4 Md€** d'économie par le retrait de l'activité de placement de France Travail, sans ventilation. Le budget initial 2026 de France Travail affiche **3 886,736 M€ de personnel** sur 6 889,234 M€ de charges.

**B. Organisation actuelle.** Accompagnement assuré par France Travail et des opérateurs privés de placement sous contrat.

**C. Comparaison internationale.** **[FAIT]** L'essai randomisé français de Behaghel, Crépon et Gurgand (2014) ne montre pas de supériorité de l'offre privée ; l'effet par bénéficiaire est plus fort pour l'offre publique.

**D. Réforme proposée.** Non retenue : le transfert d'activité vers le privé ne produit pas d'économie démontrée à service égal.

**E. Effectifs concernés.** Vivier France Travail : 48 232 ETPT.

**F. Réduction envisageable.** **Aucune réduction retenue** dans les quatre scénarios. Un transfert au privé à coût égal (facteur 1,0) ne crée aucune économie nette. Taux appliqués au reliquat du vivier : 0,00 % / 0,00 % / 0,00 % / 0,00 % (prudent / intermédiaire / ambitieux / radical). Répartition : non-remplacement 100 %, redéploiement 0 %, suppression indemnisée 0 %, transfert 0 %.

**G. Économies.** Résultats du moteur financier (`modele/modele.py`), en M€ 2026 constants, par écart à une référence qui remplace tous les départs. Le non-remplacement est valorisé au coût d'entrée hors pension, croissant de 1 % par an jusqu'au coût moyen ; les postes ne disparaissent qu'au rythme des départs à la retraite du vivier.

| Indicateur | Prudent | Intermédiaire | Ambitieux | Radical |
|---|---:|---:|---:|---:|
| ETP visés (cible) | 0 | 0 | 0 | 0 |
| Postes en moins en 2036 | 0 | 0 | 0 | 0 |
| ETP redéployés | 0 | 0 | 0 | 0 |
| Cible non réalisée en 2036 (ETP) | 0 | 0 | 0 | 0 |
| Économie nette 2036 (M€) | 0,0 | 0,0 | 0,0 | 0,0 |
| Cumul net 2027-2031 (M€) | 0,0 | 0,0 | 0,0 | 0,0 |
| Cumul net 2027-2036 (M€) | 0,0 | 0,0 | 0,0 | 0,0 |
| Cumul consolidé APU 2027-2036 (M€) | 0,0 | 0,0 | 0,0 | 0,0 |
| Investissement total (M€) | 0,0 | 0,0 | 0,0 | 0,0 |
| Coût récurrent à terme (M€/an) | 0,0 | 0,0 | 0,0 | 0,0 |

**H. Investissements nécessaires.** Sans objet.

**I. Conséquences sur le service.** Risque de sélection des publics les plus proches de l'emploi par les prestataires.

**J. Contraintes.** Marchés publics ; continuité du service public de l'emploi.

**K. Calendrier.** Sans objet.

**L. Niveau de confiance.** **Faible** pour l'économie annoncée ; fiche conservée pour documenter l'écart avec la proposition politique.

**Indicateur de validation à 2-3 ans.** Si une expérimentation est menée : coût par retour à l'emploi durable comparé à un groupe témoin.

**M. Sources et calculs.**

- [Note 04a](../04a_fiscalite_emploi.md)
- [Note 10](../10_audit_propositions.md)
- [Site budget2027.fr, instantané du 28/10/2026](https://www.budget2027.fr/)
- [Jaune « Opérateurs de l'État », PLF 2027](https://www.budget.gouv.fr/documentation/file-download/34432)

Calculs : Taux nul ; facteur de coût de transfert 1,0 (hypotheses.json). Paramètres nationaux : [hypotheses.json](../../modele/hypotheses.json) ; ligne `R27` de [catalogue_reformes.csv](../../data/reformes/catalogue_reformes.csv) ; vivier dans [registre_viviers.csv](../../data/reformes/registre_viviers.csv). Reproduction : `python -I scripts/11_catalogue.py`.
