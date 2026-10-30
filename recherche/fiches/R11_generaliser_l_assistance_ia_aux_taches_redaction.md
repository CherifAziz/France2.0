# Réforme R11 — Généraliser l'assistance IA aux tâches rédactionnelles de l'État

Vivier : **V_FPE_AUTRES** (Autres corps administratifs et techniques de la FPE (ministères et EPA, dont opérateurs)) · ordre d'application **40** · début **2028**, durée **6 ans** · confiance **faible**.

**A. Problème identifié.** **[FAIT]** L'évaluation DITP de L'Assistant mesure **2,5 minutes** gagnées sur un mail et **5,4 minutes** sur une synthèse, sur environ 30 agents volontaires, sans possibilité de généraliser. Le rapport IGF–IGAS–IGA classe 20 % des agents comme exposés, sans y voir une estimation de gains.

**B. Organisation actuelle.** L'Assistant généralisé à tous les agents de l'État depuis juin 2026 après un pilote auprès de 10 000 agents ; usages réels et économies non mesurés.

**C. Comparaison internationale.** **[FAIT]** Gains de tâche hétérogènes : −40 % de temps en rédaction (Noy–Zhang), −25,1 % pour des consultants (Dell'Acqua), +19 % de temps pour des développeurs expérimentés (METR). Au Danemark, les registres excluent un effet moyen supérieur à **2 %** sur les heures totales à fin 2024.

**D. Réforme proposée.** Mesurer les temps par tâche dans des services pilotes, réorganiser les postes dont une part importante est rédactionnelle, ne pas remplacer les départs dans les équipes où le temps libéré est démontré.

**E. Effectifs concernés.** Vivier « autres administratifs et techniques de l'État » : 231 659 ETP.

**F. Réduction envisageable.** **[HYPOTHÈSE]** 0 / 1 / 3 / 5 % du reliquat. Le scénario ambitieux dépasse l'effet maximal compatible avec les registres danois ; le radical suppose une génération d'outils plus efficace. Taux appliqués au reliquat du vivier : 0,00 % / 1,00 % / 3,00 % / 5,00 % (prudent / intermédiaire / ambitieux / radical). Répartition : non-remplacement 100 %, redéploiement 0 %, suppression indemnisée 0 %, transfert 0 %.

**G. Économies.** Résultats du moteur financier (`modele/modele.py`), en M€ 2026 constants, par écart à une référence qui remplace tous les départs. Le non-remplacement est valorisé au coût d'entrée hors pension, croissant de 1 % par an jusqu'au coût moyen ; les postes ne disparaissent qu'au rythme des départs à la retraite du vivier.

| Indicateur | Prudent | Intermédiaire | Ambitieux | Radical |
|---|---:|---:|---:|---:|
| ETP visés (cible) | 0 | 2 159 | 6 002 | 8 882 |
| Postes en moins en 2036 | 0 | 2 159 | 6 002 | 17 |
| ETP redéployés | 0 | 0 | 0 | 0 |
| Cible non réalisée en 2036 (ETP) | 0 | 0 | 0 | 8 866 |
| Économie nette 2036 (M€) | 0,0 | 98,0 | 270,1 | −2,1 |
| Cumul net 2027-2031 (M€) | 0,0 | 62,5 | −47,0 | −65,9 |
| Cumul net 2027-2036 (M€) | 0,0 | 511,7 | 875,2 | −77,3 |
| Cumul consolidé APU 2027-2036 (M€) | 0,0 | 305,4 | 541,7 | −77,4 |
| Investissement total (M€) | 0,0 | 61,9 | 61,9 | 61,9 |
| Coût récurrent à terme (M€/an) | 0,0 | 2,4 | 2,4 | 2,4 |

**H. Investissements nécessaires.** **[ESTIMATION par analogie]** 267 € par ETP d'investissement (France Travail 2025) et 10,5 € par ETP et par an de fonctionnement, probablement sous-estimé (licences, inférence).

**I. Conséquences sur le service.** Gains de qualité possibles (+0,95 et +1,28 point sur 20 dans l'essai DITP) ; risque d'erreurs non détectées et de dépendance technologique.

**J. Contraintes.** Souveraineté, sécurité des données, AI Act (règles annexe III au 2 décembre 2027).

**K. Calendrier.** Mesures 2027 ; non-remplacement 2028-2033.

**L. Niveau de confiance.** **Faible.** Aucune preuve de conversion du temps en postes ; France Travail n'a pas réduit ses ETP.

**Indicateur de validation à 2-3 ans.** Temps par tâche mesuré contre groupe témoin ; ETP des services pilotes à volume constant ; qualité des productions.

**M. Sources et calculs.**

- [Note 08](../08_ia_france.md)
- [Note 09](../09_ia_preuves_internationales.md)
- [DITP, évaluation de L'Assistant, PDF p. 16-17](https://www.modernisation.gouv.fr/files/2026-06/Synthese-evaluation-experimentation-Assistant-IA.pdf)
- [Humlum–Vestergaard, révision 2026](https://www.nber.org/system/files/working_papers/w33777/w33777.pdf)
- [Rapport IGF–IGAS–IGA, avril 2026](https://igas.gouv.fr/sites/igas/files/2026-07/Rapport%20D%C3%A9ploiement%20IA%20(2026).pdf)

Calculs : Investissement = 0,267 k€ × ETP du vivier, sur 3 ans ; fonctionnement = 0,0105 k€ × ETP du vivier par an. Paramètres nationaux : [hypotheses.json](../../modele/hypotheses.json) ; ligne `R11` de [catalogue_reformes.csv](../../data/reformes/catalogue_reformes.csv) ; vivier dans [registre_viviers.csv](../../data/reformes/registre_viviers.csv). Reproduction : `python -I scripts/11_catalogue.py`.
