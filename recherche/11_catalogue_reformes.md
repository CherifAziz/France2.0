# 11 — Catalogue des réformes chiffrées

Catalogue arrêté au **30 octobre 2026**. Trente fiches de réforme suivent la structure A à M du cahier des charges, avec un indicateur de validation à deux ou trois ans. Chaque fait cité provient d'une note des lots 1 à 3 contre-vérifiée ; chaque taux de réduction est une **[HYPOTHÈSE]** rattachée à un précédent observé. Les économies sont calculées par le moteur financier sur la même base pour toutes les fiches. **Ces totaux sont préliminaires** : les analyses de sensibilité, le test formel des seuils et la contre-expertise relèvent des phases 4 et 5.

## 1. Résultats préliminaires par scénario

| Indicateur | Prudent | Intermédiaire | Ambitieux | Radical |
|---|---:|---:|---:|---:|
| Postes en moins en 2031 | 9 553 | 45 578 | 85 930 | 123 103 |
| Postes en moins en 2036 | 11 106 | 56 142 | 120 250 | 194 476 |
| Économie nette en 2036 (M€) | 618 | 2 517 | 5 280 | 8 430 |
| Économie consolidée APU en 2036 (M€) | 458 | 1 710 | 3 539 | 5 726 |
| Cumul net 2027-2031 (M€) | 448 | 533 | 1 162 | −1 564 |
| Cumul net 2027-2036 (M€) | 3 464 | 12 627 | 25 701 | 35 448 |
| Investissements 2027-2036 (M€) | 857 | 3 953 | 7 202 | 13 505 |

**Aucun scénario n'approche 500 000 postes.** Le scénario radical retire environ **194 476 postes en 2036**, pour **8,4 Md€** d'économie nette annuelle. Les sept viviers administratifs réunissent **1 151 911 ETP** ; même en retirant 35 % de chacun (plafond du scénario radical, au-delà de tout précédent observé), on obtiendrait **403 169 postes**. Atteindre 500 000 ou 800 000 postes supposerait donc de réduire aussi des métiers non administratifs (enseignants, soignants, forces de sécurité), ce que ni le plan audité ni ce catalogue ne proposent.

Les départs à la retraite limitent aussi le rythme : en scénario radical, 8 866 ETP de R11 restent non réalisés en 2036 faute de départs dans V_FPE_AUTRES ; en scénario radical, 13 501 ETP de R12 restent non réalisés en 2036 faute de départs dans V_FPE_AUTRES.

Le cumul net sur 2027-2031 est négatif dans le scénario radical (−1 564 M€) : les investissements précèdent les économies, qui n'apparaissent qu'au rythme des départs.

La masse des économies vient des mutualisations de fonctions support (communes, opérateurs, caisses, hôpitaux) et de la revue des opérateurs. L'IA pèse peu : aucune source ne montre de conversion du temps libéré en postes, et France Travail a réaffecté le sien.

## 2. Méthode

### 2.1 Viviers disjoints

| Vivier | Description | ETP de base | Taux de départ annuel | Source | Recouvrements |
|---|---|---:|---:|---|---|
| V_DGFIP | DGFiP, titulaires et contractuels en fonction 2025 | 94 468 | 2,61 % | DGFiP cahier statistique 2025 PDF p.46-47 (88 659 + 5 910 PP) ; conversion EQTP/PP FPE 2024 (IP2094 / DGAFP) ; départs : pensions civiles FPE 2025 / fonctionnaires FPE | Inclus dans les corps administratifs et techniques FPE ; retiré de V_FPE_AUTRES. Millésime 2025 contre 2024. |
| V_FPE_AUTRES | Autres corps administratifs et techniques de la FPE (ministères et EPA, dont opérateurs) | 231 659 | 2,61 % | DGAFP RA 2026 postes FPE figure 2 B11+B26+B37 (79 668 + 157 099 + 142 142) moins DGFiP et filière administrative scolaire | Fonctionnaires seulement (total de la figure = 1 501 736 fonctionnaires FPE, contrôle V5-04) : contractuels administratifs absents. Mêle personnels administratifs et techniques. La DGFiP et le scolaire soustraits incluent des contractuels : base légèrement sous-estimée. |
| V_MEN_ADM | Filière administrative de l'Éducation nationale | 50 849 | 2,61 % | DEPP, personnels non enseignants, tableau 3.1 L27 (ETP au 30/11/2025) | Retirée de V_FPE_AUTRES (52 432 PP). |
| V_FPT_ADM | Filière administrative de la fonction publique territoriale | 444 817 | 3,31 % | DGAFP RA 2026 postes FPT figure 1 filière S28 ; conversion EQTP/PP FPT 2024 ; départs : pensions CNRACL FPT 2025 / fonctionnaires FPT | Filière statutaire, pas mesure des tâches ; disjointe des autres viviers. |
| V_FPH_ADM | Filière administrative de la fonction publique hospitalière | 119 264 | 2,75 % | DGAFP RA 2026 postes FPH figure 1 filière T25 ; conversion EQTP/PP FPH 2024 ; départs : pensions CNRACL FPH 2025 / fonctionnaires FPH | Ne pas superposer aux postes SAE (110 089). |
| V_OPS | Organismes de protection sociale (droit privé, financement public prédominant) | 162 623 | 2,61 % | DGAFP RA 2026 effectifs, figure 3 (162 623 PP fin 2024), utilisées comme majorant des ETP ; taux de départ FPE faute de donnée propre | Hors fonction publique ; tous métiers des caisses, pas seulement les fonctions support. |
| V_FT | France Travail | 48 232 | 2,61 % | Jaune Opérateurs PLF 2027, plafond d'emplois 2027 (48 232 ETPT) ; taux de départ FPE faute de donnée propre | Agents de droit privé : absents des corps de fonctionnaires de V_FPE_AUTRES (contrôle V5-04), donc disjoints. |
| V_FONCT | Dépenses de fonctionnement sans effectif (achats, immobilier, instances) | 0 | 0,00 % | Sans effectif : les fiches y portent des économies de fonctionnement en M€ | Sans objet. |

Plafonds de réduction par vivier : **5 / 12 / 20 / 35 %** (prudent / intermédiaire / ambitieux / radical). Les trois premiers encadrent les contractions observées à l'étranger (Irlande −9,6 %, Portugal −12 %, Royaume-Uni −20,2 %, toutes suivies d'un rebond) ; le radical les dépasse et n'est pas démontré.

Le taux de départ retenu est celui des **départs à la retraite des fonctionnaires civils** (pensions 2025 / fonctionnaires fin 2024, par versant). C'est une borne prudente : les sorties de contractuels, plus nombreuses, sont souvent des fins de contrat remplacées et ne libèrent pas de postes.

### 2.2 Hypothèses nationales

| Paramètre | Valeur | Justification |
|---|---|---|
| Coût d'entrée / moyen hors pension, FPE | 44,05 / 48,99 k€ | [ESTIMATION] Moyenne des coûts HCAS d'entrée et globaux des PAP 2026 des programmes 156 et 218 par catégorie A/B/C, pondérée par les corps administratifs et techniques de la FPE fin 2024 (A 79 668, B 157 099, C 142 142). data/france/01c_couts_documentes.csv, data/france/02_metiers.csv. |
| Coût d'entrée / moyen hors pension, FPE_DGFIP | 40,55 / 45,41 k€ | [ESTIMATION] Coûts HCAS du seul PAP 2026 du programme 156 (DGFiP), même pondération A/B/C. |
| Coût d'entrée / moyen hors pension, FPT | 33,67 / 37,45 k€ | [HYPOTHÈSE] Coûts FPE multipliés par le rapport des salaires bruts moyens par EQTP FPT/FPE 2024 (2 857,75 / 3 738,28 = 0,7645). Aucun coût d'entrée territorial publié n'a été trouvé. |
| Coût d'entrée / moyen hors pension, FPH | 33,67 / 37,45 k€ | [HYPOTHÈSE] Même proxy que la FPT : le salaire moyen FPH inclut les médecins et surestimerait le coût des administratifs hospitaliers. |
| Coût d'entrée / moyen hors pension, HORS_FP | 44,05 / 48,99 k€ | [HYPOTHÈSE] Organismes de protection sociale et France Travail, agents de droit privé : aucun coût d'entrée publié trouvé ; proxy FPE. Confiance faible. |
| gvt_individuel_reel | 0,01 | [HYPOTHÈSE] Taux individuel réel national NON TROUVÉ (01c). 1 %/an, plafonné au coût moyen ; sensibilité 0-2 % en phase 5. |
| taux_conservation_consolide | 0,65 | [ESTIMATION] Part du coût hors pension conservée en lecture APU statique. Charges employeur hors pension : 13,7 à 17,6 % du coût d'entrée (PAP 156 : coût HCAS moins rémunération d'activité). Retenue pension 11,1 % (01c) et CSG-CRDS sur la rémunération reviennent aussi aux APU : environ 32 % au total, IR non chiffré. Retenu : 1 - 0,35. |
| facteur_transfert_cout | 1,00 | [HYPOTHÈSE] Une activité transférée au privé coûte autant que sa production publique : l'essai Behaghel-Crépon-Gurgand (2014) ne montre pas de supériorité de l'offre privée (note 04a). |
| fraction_economie_premiere_annee | 0,50 | Convention de mi-année, comme le calendrier illustratif de la note 10. |

### 2.3 Conventions

- **Référence.** Les économies sont des écarts à une trajectoire qui remplace tous les départs. Les mouvements déjà votés ou engagés (schémas d'emplois du PLF 2027, foncière immobilière, investissements IA de France Travail) sont dans la référence et ne sont pas recomptés.
- **Ordre et non-cumul.** Dans chaque vivier, les réformes s'appliquent au reliquat, dans l'ordre structures (10-19), simplification (20-29), mutualisation (30-39), IA (40-49), règle transversale (50). Un même poste ne peut être compté deux fois.
- **Investissements.** Faute de coûts publiés, convention de **deux années d'économie brute** (sur le modèle du timbre électronique : 2,65 M€, retour en deux ans), **trois années** pour les projets à risque élevé (paie, suppression d'un échelon). Pour l'IA, analogie avec France Travail 2025 : 267 € par ETP d'investissement, 10,5 € par ETP et par an de fonctionnement.
- **Pas de licenciement.** Les réductions passent par le non-remplacement des départs ou le redéploiement ; aucune fiche ne recourt à la suppression indemnisée de postes de fonctionnaires.
- **Fiches à effet nul.** R03 (redéploiement), R23 (recettes seulement), R27 (externalisation non retenue) et R30 (non chiffrable) restent au catalogue pour documenter les choix.

## 3. Les trente fiches

| Fiche | Vivier | Confiance | Postes en moins 2036 (P / I / A / R) | Économie nette 2036, M€ (P / I / A / R) |
|---|---|---|---|---|
| [R01 — Automatiser les contrôles de forme et supprimer les ressaisies fiscales](fiches/R01_automatiser_les_controles_de_forme_et_supprimer_.md) | V_DGFIP | moyen | 520 / 1 039 / 2 078 / 3 117 | 23 / 45 / 90 / 136 |
| [R02 — Mutualiser les fonctions RH et informatiques de la DGFiP](fiches/R02_mutualiser_les_fonctions_rh_et_informatiques_de_.md) | V_DGFIP | faible | 94 / 439 / 647 / 859 | 4 / 19 / 28 / 37 |
| [R03 — Utiliser l'IA pour cibler le contrôle fiscal, à effectifs redéployés](fiches/R03_utiliser_l_ia_pour_cibler_le_controle_fiscal_a_e.md) | V_DGFIP | faible | 0 / 0 / 0 / 0 | 0 / −1 / −1 / −1 |
| [R04 — Revoir les missions des opérateurs et regrouper ceux qui se recouvrent](fiches/R04_revoir_les_missions_des_operateurs_et_regrouper_.md) | V_FPE_AUTRES | moyen | 927 / 2 780 / 5 560 / 11 120 | 44 / 131 / 263 / 525 |
| [R05 — Allouer les effectifs de l'État territorial selon des besoins mesurés](fiches/R05_allouer_les_effectifs_de_l_etat_territorial_selo.md) | V_FPE_AUTRES | faible | 0 / 2 282 / 4 494 / 8 710 | 0 / 107 / 210 / 407 |
| [R06 — Resserrer les administrations centrales au-delà du PLF 2027](fiches/R06_resserrer_les_administrations_centrales_au_dela_.md) | V_FPE_AUTRES | faible | 0 / 2 259 / 4 404 / 8 362 | 0 / 106 / 207 / 392 |
| [R07 — Réutiliser les données détenues et ne plus redemander les pièces](fiches/R07_reutiliser_les_donnees_detenues_et_ne_plus_redem.md) | V_FPE_AUTRES | moyen | 1 153 / 2 236 / 4 316 / 6 021 | 54 / 106 / 204 / 278 |
| [R08 — Supprimer les procédures et obligations d'information sans usage](fiches/R08_supprimer_les_procedures_et_obligations_d_inform.md) | V_FPE_AUTRES | faible | 0 / 1 107 / 3 172 / 5 840 | 0 / 52 / 148 / 263 |
| [R09 — Créer des services partagés de gestion pour les opérateurs](fiches/R09_creer_des_services_partages_de_gestion_pour_les_.md) | V_FPE_AUTRES | faible | 1 147 / 3 304 / 6 250 / 7 553 | 54 / 155 / 292 / 312 |
| [R10 — Industrialiser la gestion RH et la paie interministérielles](fiches/R10_industrialiser_la_gestion_rh_et_la_paie_intermin.md) | V_FPE_AUTRES | faible | 0 / 1 085 / 2 021 / 3 625 | 0 / 50 / 92 / 80 |
| [R11 — Généraliser l'assistance IA aux tâches rédactionnelles de l'État](fiches/R11_generaliser_l_assistance_ia_aux_taches_redaction.md) | V_FPE_AUTRES | faible | 0 / 2 159 / 6 002 / 17 | 0 / 98 / 270 / −2 |
| [R12 — Ne remplacer qu'un départ sur deux dans les fonctions administratives restantes de l'État](fiches/R12_ne_remplacer_qu_un_depart_sur_deux_dans_les_fonc.md) | V_FPE_AUTRES | faible | 0 / 0 / 5 822 / 0 | 0 / 0 / 133 / 0 |
| [R13 — Mutualiser et automatiser la gestion administrative des personnels de l'Éducation nationale](fiches/R13_mutualiser_et_automatiser_la_gestion_administrat.md) | V_MEN_ADM | faible | 0 / 1 525 / 3 051 / 5 085 | 0 / 71 / 143 / 238 |
| [R14 — Désigner un chef de file unique par politique cofinancée entre collectivités](fiches/R14_designer_un_chef_de_file_unique_par_politique_co.md) | V_FPT_ADM | faible | 0 / 4 448 / 8 896 / 17 793 | 0 / 159 / 318 / 636 |
| [R15 — Supprimer un échelon d'administration territoriale (transformation radicale)](fiches/R15_supprimer_un_echelon_d_administration_territoria.md) | V_FPT_ADM | faible | 0 / 0 / 0 / 17 081 | 0 / 0 / 0 / 596 |
| [R16 — Évaluer a posteriori et alléger les normes imposées aux collectivités](fiches/R16_evaluer_a_posteriori_et_alleger_les_normes_impos.md) | V_FPT_ADM | faible | 0 / 2 202 / 4 359 / 8 113 | 0 / 79 / 156 / 290 |
| [R17 — Mutualiser les fonctions support entre communes et intercommunalités](fiches/R17_mutualiser_les_fonctions_support_entre_communes_.md) | V_FPT_ADM | moyen | 4 448 / 13 145 / 21 578 / 31 805 | 160 / 472 / 775 / 1 142 |
| [R18 — Automatiser l'instruction des actes et la gestion RH des collectivités](fiches/R18_automatiser_l_instruction_des_actes_et_la_gestio.md) | V_FPT_ADM | faible | 0 / 4 250 / 12 299 / 18 288 | 0 / 147 / 433 / 639 |
| [R19 — Mutualiser les fonctions administratives au sein des groupements hospitaliers](fiches/R19_mutualiser_les_fonctions_administratives_au_sein.md) | V_FPH_ADM | faible | 1 193 / 3 578 / 5 963 / 9 541 | 43 / 128 / 213 / 341 |
| [R20 — Automatiser le codage, la facturation et le secrétariat hospitaliers](fiches/R20_automatiser_le_codage_la_facturation_et_le_secre.md) | V_FPH_ADM | faible | 0 / 1 157 / 3 399 / 5 486 | 0 / 40 / 120 / 194 |
| [R21 — Simplifier le double circuit de remboursement assurance maladie et complémentaires](fiches/R21_simplifier_le_double_circuit_de_remboursement_as.md) | V_OPS | faible | 0 / 1 626 / 3 252 / 6 505 | 0 / 76 / 152 / 304 |
| [R22 — Mutualiser les fonctions support des caisses de Sécurité sociale](fiches/R22_mutualiser_les_fonctions_support_des_caisses_de_.md) | V_OPS | faible | 1 626 / 3 220 / 6 375 / 9 367 | 76 / 151 / 298 / 438 |
| [R23 — Réduire les indus et payer à bon droit](fiches/R23_reduire_les_indus_et_payer_a_bon_droit.md) | V_OPS | moyen | 0 / 0 / 0 / 0 | 100 / 100 / 100 / 100 |
| [R24 — Automatiser le traitement des dossiers de prestations](fiches/R24_automatiser_le_traitement_des_dossiers_de_presta.md) | V_OPS | faible | 0 / 1 578 / 4 590 / 7 338 | 0 / 72 / 212 / 338 |
| [R25 — Un dossier unique pour les parcours d'emploi et d'insertion](fiches/R25_un_dossier_unique_pour_les_parcours_d_emploi_et_.md) | V_FT | faible | 0 / 482 / 965 / 1 447 | 0 / 23 / 45 / 68 |
| [R26 — Convertir en postes le temps libéré par les outils d'IA de France Travail](fiches/R26_convertir_en_postes_le_temps_libere_par_les_outi.md) | V_FT | faible | 0 / 239 / 756 / 1 404 | 0 / 11 / 35 / 66 |
| [R27 — Externaliser l'accompagnement des demandeurs d'emploi (non retenue)](fiches/R27_externaliser_l_accompagnement_des_demandeurs_d_e.md) | V_FT | faible | 0 / 0 / 0 / 0 | 0 / 0 / 0 / 0 |
| [R28 — Professionnaliser et mutualiser davantage les achats publics](fiches/R28_professionnaliser_et_mutualiser_davantage_les_ac.md) | V_FONCT | moyen | 0 / 0 / 0 / 0 | 61 / 122 / 244 / 365 |
| [R29 — Réduire les surfaces de bureaux au-delà de la foncière de l'État](fiches/R29_reduire_les_surfaces_de_bureaux_au_dela_de_la_fo.md) | V_FONCT | faible | 0 / 0 / 0 / 0 | 0 / 0 / 100 / 250 |
| [R30 — Réexaminer périodiquement les commissions et instances consultatives](fiches/R30_reexaminer_periodiquement_les_commissions_et_ins.md) | V_FONCT | faible | 0 / 0 / 0 / 0 | 0 / 0 / 0 / 0 |

## 4. Limites

- Les taux de réduction sont des hypothèses : aucune fiche ne repose sur une mesure française de postes effectivement supprimés après réforme.
- Les coûts territoriaux, hospitaliers et des organismes de droit privé sont des proxys du coût de l'État ; les investissements suivent une convention, pas des devis.
- Les viviers sont des filières ou des corps statutaires, pas des mesures de tâches ; le vivier de l'État mêle personnels administratifs et techniques.
- Les effets sur les pensions futures, la sous-traitance et les indicateurs de service sont qualitatifs dans les fiches ; ils seront quantifiés quand les données le permettront.
- La phase 5 testera la sensibilité au coût par ETP, au taux de départ, au GVT, à la conversion du temps libéré par l'IA et au taux de conservation APU.

## 5. Reproduction

```powershell
python -I scripts/11_catalogue.py
```

Le script écrit `data/reformes/registre_viviers.csv`, `data/reformes/catalogue_reformes.csv`, les fiches de `recherche/fiches/` et ce document, puis exécute `modele/modele.py` dont les résultats sont dans `modele/resultats/`. Le contenu rédigé des fiches est dans `scripts/11_fiches_etat.py` et `scripts/11_fiches_local_social.py`.
