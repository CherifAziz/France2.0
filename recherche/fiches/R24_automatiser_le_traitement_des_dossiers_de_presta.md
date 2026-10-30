# Réforme R24 — Automatiser le traitement des dossiers de prestations

Vivier : **V_OPS** (Organismes de protection sociale (droit privé, financement public prédominant)) · ordre d'application **40** · début **2028**, durée **6 ans** · confiance **faible**.

**A. Problème identifié.** **[FAIT sur des gains déclarés]** À la CNAV, l'usage de Copilot Chat donne un gain de temps estimé de **20 à 30 %** sur des activités courtes à faible valeur métier pour environ 9 000 adoptants. La CNAM estime **5 %** de productivité sur 100 développeurs en test.

**B. Organisation actuelle.** Instruction des droits (retraite, famille, maladie) dans les caisses ; outils de détection CNAF déjà déployés.

**C. Comparaison internationale.** **[FAIT]** Essai DBT britannique : gains déclarés de 0,8 heure par tâche de synthèse, mais −0,6 heure en planification ; aucune preuve d'une productivité globale accrue.

**D. Réforme proposée.** Pré-instruction automatisée des dossiers simples, contrôle humain sur exceptions ; non-remplacement des départs là où le temps libéré est mesuré.

**E. Effectifs concernés.** Vivier organismes de protection sociale : 162 623 personnes.

**F. Réduction envisageable.** **[HYPOTHÈSE]** 0 / 1 / 3 / 5 % du reliquat. Taux appliqués au reliquat du vivier : 0,00 % / 1,00 % / 3,00 % / 5,00 % (prudent / intermédiaire / ambitieux / radical). Répartition : non-remplacement 100 %, redéploiement 0 %, suppression indemnisée 0 %, transfert 0 %.

**G. Économies.** Résultats du moteur financier (`modele/modele.py`), en M€ 2026 constants, par écart à une référence qui remplace tous les départs. Le non-remplacement est valorisé au coût d'entrée hors pension, croissant de 1 % par an jusqu'au coût moyen ; les postes ne disparaissent qu'au rythme des départs à la retraite du vivier.

| Indicateur | Prudent | Intermédiaire | Ambitieux | Radical |
|---|---:|---:|---:|---:|
| ETP visés (cible) | 0 | 1 578 | 4 590 | 7 338 |
| Postes en moins en 2036 | 0 | 1 578 | 4 590 | 7 338 |
| ETP redéployés | 0 | 0 | 0 | 0 |
| Cible non réalisée en 2036 (ETP) | 0 | 0 | 0 | 0 |
| Économie nette 2036 (M€) | 0,0 | 71,7 | 211,9 | 337,7 |
| Cumul net 2027-2031 (M€) | 0,0 | 47,6 | 226,7 | 299,7 |
| Cumul net 2027-2036 (M€) | 0,0 | 376,2 | 1 198,4 | 1 738,1 |
| Cumul consolidé APU 2027-2036 (M€) | 0,0 | 225,4 | 759,9 | 1 110,7 |
| Investissement total (M€) | 0,0 | 43,4 | 43,4 | 43,4 |
| Coût récurrent à terme (M€/an) | 0,0 | 1,7 | 1,7 | 1,7 |

**H. Investissements nécessaires.** **[ESTIMATION par analogie]** 267 € par ETP d'investissement et 10,5 € par ETP et par an.

**I. Conséquences sur le service.** Délais de liquidation réduits ; risque de refus automatisés contestés (RGPD art. 22).

**J. Contraintes.** Décisions individuelles automatisées encadrées ; qualité des données.

**K. Calendrier.** 2028-2033.

**L. Niveau de confiance.** **Faible.** Gains déclarés, sur des tâches courtes.

**Indicateur de validation à 2-3 ans.** Délais de liquidation ; taux d'erreurs et de recours ; ETP d'instruction par dossier.

**M. Sources et calculs.**

- [Note 08](../08_ia_france.md)
- [Note 09](../09_ia_preuves_internationales.md)
- [Rapport IGF–IGAS–IGA, avril 2026](https://igas.gouv.fr/sites/igas/files/2026-07/Rapport%20D%C3%A9ploiement%20IA%20(2026).pdf)

Calculs : Investissement = 0,267 k€ × ETP du vivier, sur 3 ans. Paramètres nationaux : [hypotheses.json](../../modele/hypotheses.json) ; ligne `R24` de [catalogue_reformes.csv](../../data/reformes/catalogue_reformes.csv) ; vivier dans [registre_viviers.csv](../../data/reformes/registre_viviers.csv). Reproduction : `python -I scripts/11_catalogue.py`.
