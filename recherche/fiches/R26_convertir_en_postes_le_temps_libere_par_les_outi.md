# Réforme R26 — Convertir en postes le temps libéré par les outils d'IA de France Travail

Vivier : **V_FT** (France Travail) · ordre d'application **40** · début **2028**, durée **5 ans** · confiance **faible**.

**A. Problème identifié.** **[FAIT]** France Travail estime **226 ETP** de temps gagné pour ChatFT, **300** pour Panoptes et **241** pour NEO, soit 767 au total. La mission précise que ces chiffrages **n'ont pas entraîné de diminution des ETP**.

**B. Organisation actuelle.** 51 000 agents ont adopté ChatFT fin 2025 sur 55 000 concernés. Investissement IA de 12,875 M€ en 2025, déjà engagé (donc hors coûts de cette fiche).

**C. Comparaison internationale.** **[FAIT]** Humlum–Vestergaard : pas d'effet moyen supérieur à 2 % sur les heures totales au Danemark à fin 2024 ; le temps libéré est absorbé par d'autres tâches.

**D. Réforme proposée.** Arbitrer explicitement l'usage du temps libéré : une part réduit les effectifs par non-remplacement, le reste améliore l'accompagnement.

**E. Effectifs concernés.** Vivier France Travail : 48 232 ETPT.

**F. Réduction envisageable.** **[HYPOTHÈSE]** 0 / 0,5 / 1,6 / 3 %. L'ambitieux convertit entièrement les 767 ETP estimés (1,59 % du vivier) ; le radical suppose un doublement. Taux appliqués au reliquat du vivier : 0,00 % / 0,50 % / 1,60 % / 3,00 % (prudent / intermédiaire / ambitieux / radical). Répartition : non-remplacement 100 %, redéploiement 0 %, suppression indemnisée 0 %, transfert 0 %.

**G. Économies.** Résultats du moteur financier (`modele/modele.py`), en M€ 2026 constants, par écart à une référence qui remplace tous les départs. Le non-remplacement est valorisé au coût d'entrée hors pension, croissant de 1 % par an jusqu'au coût moyen ; les postes ne disparaissent qu'au rythme des départs à la retraite du vivier.

| Indicateur | Prudent | Intermédiaire | Ambitieux | Radical |
|---|---:|---:|---:|---:|
| ETP visés (cible) | 0 | 239 | 756 | 1 404 |
| Postes en moins en 2036 | 0 | 239 | 756 | 1 404 |
| ETP redéployés | 0 | 0 | 0 | 0 |
| Cible non réalisée en 2036 (ETP) | 0 | 0 | 0 | 0 |
| Économie nette 2036 (M€) | 0,0 | 11,2 | 35,4 | 65,6 |
| Cumul net 2027-2031 (M€) | 0,0 | 17,0 | 54,0 | 100,2 |
| Cumul net 2027-2036 (M€) | 0,0 | 70,7 | 224,0 | 415,7 |
| Cumul consolidé APU 2027-2036 (M€) | 0,0 | 46,0 | 145,6 | 270,2 |
| Investissement total (M€) | 0,0 | 0,0 | 0,0 | 0,0 |
| Coût récurrent à terme (M€/an) | 0,0 | 0,0 | 0,0 | 0,0 |

**H. Investissements nécessaires.** Investissement déjà engagé, inclus dans la référence.

**I. Conséquences sur le service.** Réduire les postes plutôt qu'améliorer l'accompagnement peut dégrader le retour à l'emploi.

**J. Contraintes.** Choix politique entre service et économie.

**K. Calendrier.** 2028-2032.

**L. Niveau de confiance.** **Faible.** L'organisme a choisi de réaffecter le temps.

**Indicateur de validation à 2-3 ans.** ETP à volume de demandeurs constant ; taux de retour à l'emploi durable ; délais d'accompagnement.

**M. Sources et calculs.**

- [Note 08](../08_ia_france.md)
- [Note 09](../09_ia_preuves_internationales.md)
- [Rapport IGF–IGAS–IGA, avril 2026](https://igas.gouv.fr/sites/igas/files/2026-07/Rapport%20D%C3%A9ploiement%20IA%20(2026).pdf)

Calculs : 767 / 48 232 = 1,59 % ; taux ambitieux arrondi à 1,6 %. Paramètres nationaux : [hypotheses.json](../../modele/hypotheses.json) ; ligne `R26` de [catalogue_reformes.csv](../../data/reformes/catalogue_reformes.csv) ; vivier dans [registre_viviers.csv](../../data/reformes/registre_viviers.csv). Reproduction : `python -I scripts/11_catalogue.py`.
