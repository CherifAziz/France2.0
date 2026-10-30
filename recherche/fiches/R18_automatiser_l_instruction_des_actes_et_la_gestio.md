# Réforme R18 — Automatiser l'instruction des actes et la gestion RH des collectivités

Vivier : **V_FPT_ADM** (Filière administrative de la fonction publique territoriale) · ordre d'application **40** · début **2028**, durée **6 ans** · confiance **faible**.

**A. Problème identifié.** **[FAIT sur un retour d'expérience]** Au centre de gestion de Haute-Savoie, la préanalyse par IA de **30 000 à 40 000 arrêtés par an** aurait libéré **20 % du temps de l'équipe**, réinvesti dans le conseil aux collectivités.

**B. Organisation actuelle.** Contrôle de légalité, actes RH et instruction des dossiers répartis entre collectivités, centres de gestion et préfectures.

**C. Comparaison internationale.** **[FAIT]** Le rapport IA relève des gains de 20 à 30 % sur des activités courtes à la CNAV ; au Danemark, les registres ne montrent pas d'effet moyen supérieur à 2 % sur les heures totales.

**D. Réforme proposée.** Diffuser les outils de préanalyse dans les centres de gestion et les grandes collectivités ; réorganiser les équipes ; non-remplacement des départs là où le temps libéré est mesuré.

**E. Effectifs concernés.** Vivier filière administrative FPT : 444 817 ETP.

**F. Réduction envisageable.** **[HYPOTHÈSE]** 0 / 1 / 3 / 5 % du reliquat ; le précédent de Haute-Savoie a réinvesti le temps, sans réduction d'effectif. Taux appliqués au reliquat du vivier : 0,00 % / 1,00 % / 3,00 % / 5,00 % (prudent / intermédiaire / ambitieux / radical). Répartition : non-remplacement 100 %, redéploiement 0 %, suppression indemnisée 0 %, transfert 0 %.

**G. Économies.** Résultats du moteur financier (`modele/modele.py`), en M€ 2026 constants, par écart à une référence qui remplace tous les départs. Le non-remplacement est valorisé au coût d'entrée hors pension, croissant de 1 % par an jusqu'au coût moyen ; les postes ne disparaissent qu'au rythme des départs à la retraite du vivier.

| Indicateur | Prudent | Intermédiaire | Ambitieux | Radical |
|---|---:|---:|---:|---:|
| ETP visés (cible) | 0 | 4 250 | 12 299 | 18 288 |
| Postes en moins en 2036 | 0 | 4 250 | 12 299 | 18 288 |
| ETP redéployés | 0 | 0 | 0 | 0 |
| Cible non réalisée en 2036 (ETP) | 0 | 0 | 0 | 0 |
| Économie nette 2036 (M€) | 0,0 | 146,5 | 432,8 | 638,7 |
| Cumul net 2027-2031 (M€) | 0,0 | 66,7 | 432,6 | 514,8 |
| Cumul net 2027-2036 (M€) | 0,0 | 737,7 | 2 417,1 | 2 944,1 |
| Cumul consolidé APU 2027-2036 (M€) | 0,0 | 427,3 | 1 518,9 | 1 861,5 |
| Investissement total (M€) | 0,0 | 118,8 | 118,8 | 118,8 |
| Coût récurrent à terme (M€/an) | 0,0 | 4,7 | 4,7 | 4,7 |

**H. Investissements nécessaires.** **[ESTIMATION par analogie]** 267 € par ETP d'investissement et 10,5 € par ETP et par an (France Travail 2025).

**I. Conséquences sur le service.** Délais d'instruction réduits ; risque d'erreurs de légalité non détectées.

**J. Contraintes.** Responsabilité juridique des actes ; RGPD ; marchés publics d'outils.

**K. Calendrier.** 2028-2033.

**L. Niveau de confiance.** **Faible.** Un retour d'expérience local, sans baisse d'effectif.

**Indicateur de validation à 2-3 ans.** Temps d'instruction par acte ; erreurs relevées au contrôle de légalité ; ETP des équipes concernées.

**M. Sources et calculs.**

- [Note 08](../08_ia_france.md)
- [Note 09](../09_ia_preuves_internationales.md)
- [Rapport IGF–IGAS–IGA, avril 2026](https://igas.gouv.fr/sites/igas/files/2026-07/Rapport%20D%C3%A9ploiement%20IA%20(2026).pdf)

Calculs : Investissement = 0,267 k€ × ETP du vivier, sur 3 ans ; fonctionnement = 0,0105 k€ × ETP par an. Paramètres nationaux : [hypotheses.json](../../modele/hypotheses.json) ; ligne `R18` de [catalogue_reformes.csv](../../data/reformes/catalogue_reformes.csv) ; vivier dans [registre_viviers.csv](../../data/reformes/registre_viviers.csv). Reproduction : `python -I scripts/11_catalogue.py`.
