# Réforme R01 — Automatiser les contrôles de forme et supprimer les ressaisies fiscales

Vivier : **V_DGFIP** (DGFiP, titulaires et contractuels en fonction 2025) · ordre d'application **20** · début **2027**, durée **5 ans** · confiance **moyen**.

**A. Problème identifié.** **[FAIT]** ISORA déclare pour la France **10 356 ETP** dans la fonction « usagers, déclarations et paiements » en 2023, sur 38 406 ETP fiscaux. La déclaration électronique couvre déjà **96,0 %** des déclarations d'impôt sur les sociétés et **86,8 %** des déclarations de revenus. Le gisement restant porte donc sur les contrôles de forme, les rapprochements et les ressaisies, pas sur la dématérialisation elle-même.

**B. Organisation actuelle.** **[FAIT]** La DGFiP compte **88 659 titulaires et 5 910 contractuels** en 2025 (effectifs en fonction). Sa série d'emplois passe de **107 202 ETPT en 2015 à 91 064 en 2025**, soit **[ESTIMATION]** −15,05 % ; la Cour ne permet pas d'attribuer cette baisse au seul numérique. Les services de publicité foncière ont perdu 218 ETP entre fin 2021 et fin 2023, avec un délai de publication tombé de 134 à 24,6 jours.

**C. Comparaison internationale.** **[FAIT]** L'administration fiscale canadienne déclare avoir automatisé plus de **40 processus**, pour plus de **187 000 heures** cumulées libérées : une capacité, pas des postes supprimés (OCDE, Tax Administration 2025). Le ratio d'ETP fiscaux pour 1 000 habitants est de 0,562 en France contre 1,328 en Allemagne et 0,857 au Royaume-Uni : la France n'est pas suradministrée sur cet indicateur brut.

**D. Réforme proposée.** Cartographier les flux de la fonction « usagers et déclarations » par acte ; supprimer les pièces et données déjà détenues ; automatiser les contrôles de cohérence et les rapprochements avec vérification humaine sur exception ; ne pas remplacer les départs des postes de saisie et de contrôle de forme ainsi libérés.

**E. Effectifs concernés.** Vivier DGFiP : **94 468 ETP** (94 569 personnes physiques 2025 × 0,9989). Périmètre visé : les 10 356 ETP de la fonction usagers/déclarations/paiements.

**F. Réduction envisageable.** **[HYPOTHÈSE]** Réduction de **5 / 10 / 20 / 30 %** de la fonction visée (prudent, intermédiaire, ambitieux, radical), soit 0,55 % à 3,3 % du vivier, par non-remplacement. Repère : la DGFiP a réduit ses ETPT de 15 % en dix ans à périmètre non constant ; le scénario radical suppose que la tendance passée se prolonge sur ce seul segment. Taux appliqués au reliquat du vivier : 0,55 % / 1,10 % / 2,20 % / 3,30 % (prudent / intermédiaire / ambitieux / radical). Répartition : non-remplacement 100 %, redéploiement 0 %, suppression indemnisée 0 %, transfert 0 %.

**G. Économies.** Résultats du moteur financier (`modele/modele.py`), en M€ 2026 constants, par écart à une référence qui remplace tous les départs. Le non-remplacement est valorisé au coût d'entrée hors pension, croissant de 1 % par an jusqu'au coût moyen ; les postes ne disparaissent qu'au rythme des départs à la retraite du vivier.

| Indicateur | Prudent | Intermédiaire | Ambitieux | Radical |
|---|---:|---:|---:|---:|
| ETP visés (cible) | 520 | 1 039 | 2 078 | 3 117 |
| Postes en moins en 2036 | 520 | 1 039 | 2 078 | 3 117 |
| ETP redéployés | 0 | 0 | 0 | 0 |
| Cible non réalisée en 2036 (ETP) | 0 | 0 | 0 | 0 |
| Économie nette 2036 (M€) | 22,6 | 45,2 | 90,4 | 135,5 |
| Cumul net 2027-2031 (M€) | 11,4 | 22,8 | 45,5 | 68,3 |
| Cumul net 2027-2036 (M€) | 122,1 | 244,2 | 488,5 | 732,7 |
| Cumul consolidé APU 2027-2036 (M€) | 64,6 | 129,3 | 258,5 | 387,8 |
| Investissement total (M€) | 42,1 | 84,3 | 168,5 | 252,8 |
| Coût récurrent à terme (M€/an) | 0,0 | 0,0 | 0,0 | 0,0 |

**H. Investissements nécessaires.** **[HYPOTHÈSE de convention]** Investissement égal à deux années d'économie brute, sur le modèle du timbre électronique (2,65 M€, retour sur investissement en deux ans, selon la Cour). Coûts de licences et de maintenance non documentés.

**I. Conséquences sur le service.** Délais de traitement et taux d'erreur peuvent s'améliorer ; risque de rejets automatiques injustifiés et de report de charge sur l'accueil, en particulier pour les usagers en difficulté numérique (7 % des 16-74 ans en illectronisme en 2025).

**J. Contraintes.** Garantie d'intervention humaine pour les décisions individuelles (RGPD art. 22, CRPA) ; fiabilité des données tierces ; dialogue social sur les mobilités internes.

**K. Calendrier.** Court terme : cartographie et pilotes (2027). Moyen terme : généralisation sur cinq ans. Long terme : réexamen des pièces exigées par les textes.

**L. Niveau de confiance.** **Moyen.** Le problème et le précédent sont documentés ; le taux de conversion du temps libéré en postes ne l'est pas.

**Indicateur de validation à 2-3 ans.** ETP de la fonction usagers/déclarations dans ISORA ; délai et taux d'erreur par acte ; nombre de réclamations ; part des dossiers traités sans intervention, publiés chaque année à périmètre constant.

**M. Sources et calculs.**

- [Note 04a — fiscalité et emploi](../04a_fiscalite_emploi.md)
- [Note 06 — structures et précédents](../06_doublons_structures.md)
- [DGFiP, rapport d'activité 2025, cahier statistique, PDF p. 46-47](https://www.economie.gouv.fr/files/files/directions_services/dgfip/Rapport/2025/ra_2025_cahierstat.pdf)
- [PAP 2026 programme 156, p. 50](https://www.assemblee-nationale.fr/dyn/contenu/visualisation/1087984/file/PAP2026_BG_Gestion_finances_publiques_GA.pdf#page=50)

Calculs : taux_vivier = 10 356 × {0,05 ; 0,10 ; 0,20 ; 0,30} / 94 468. Coût d'entrée DGFiP 40,55 k€ (PAP 156, pondéré A/B/C). Paramètres nationaux : [hypotheses.json](../../modele/hypotheses.json) ; ligne `R01` de [catalogue_reformes.csv](../../data/reformes/catalogue_reformes.csv) ; vivier dans [registre_viviers.csv](../../data/reformes/registre_viviers.csv). Reproduction : `python -I scripts/11_catalogue.py`.
