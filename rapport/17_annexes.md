# 17. Annexes statistiques et calculs reproductibles

Toutes les données, scripts et contrôles de la mission sont versionnés dans le dépôt. Les documents lourds (PDF de rapports) sont conservés hors Git dans `data/cache/` ; leurs URL et empreintes figurent dans les registres, et les scripts `restore_lot*_sources.py` les restaurent.

## 17.1 Livrables complémentaires

| Livrable | Fichier |
|---|---|
| Base comparative internationale structurée (3 859 lignes, 44 pays) | `data/international/03_base_comparative.csv`, dictionnaire `03_dictionnaire_variables.csv` ; feuille « Base comparative » de `livrables/tableaux_livrables.xlsx` |
| Tableau exhaustif des réformes et de leurs économies | `data/reformes/catalogue_reformes.csv`, `modele/resultats/reformes_*.csv` ; feuille « Reformes » de `livrables/tableaux_livrables.xlsx` |
| Modèle financier modifiable | `modele/modele_financier.xlsx` (formules, hypothèses en cellules jaunes) et moteur `modele/modele.py` |
| Matrice des risques et incertitudes | `data/reformes/14_matrice_risques.csv` ; feuille « Matrice des risques » |
| Synthèse de 10 pages | `livrables/synthese.html`, `.docx`, `.pdf` |
| Bibliographie fusionnée | `livrables/bibliographie.csv` |

## 17.2 Notes de recherche détaillées

| Note | Objet |
|---|---|
| [00_audit_modele.md](../recherche/00_audit_modele.md) | Vérification indépendante du moteur financier |
| [00_AVENANT_METHODOLOGIQUE.md](../recherche/00_AVENANT_METHODOLOGIQUE.md) | Avenant méthodologique de la reprise du 28 octobre 2026 |
| [00_PROTOCOLE.md](../recherche/00_PROTOCOLE.md) | Protocole de recherche commun à toutes les équipes de la mission |
| [00_synthese_lot3.md](../recherche/00_synthese_lot3.md) | Ce que les réformes ont réellement produit |
| [00_verification_04a_lot2.md](../recherche/00_verification_04a_lot2.md) | Contre-vérification indépendante du lot 04a — fiscalité et service public de l'emploi |
| [00_verification_04b_lot2.md](../recherche/00_verification_04b_lot2.md) | Contre-vérification indépendante 04b — lot 2 |
| [00_verification_04d_lot2.md](../recherche/00_verification_04d_lot2.md) | Contre-vérification du volet 04d — territoires et fonctions support |
| [00_verification_06_07_lot3.md](../recherche/00_verification_06_07_lot3.md) | Contre-vérification indépendante — volets 06–07, lot 3 |
| [00_verification_08_09_lot3.md](../recherche/00_verification_08_09_lot3.md) | Contre-vérification indépendante des chantiers 08 et 09 — lot 3 |
| [00_verification_10_lot3.md](../recherche/00_verification_10_lot3.md) | Contre-vérification indépendante du chantier 10 — lot 3 |
| [00_verification_lot1.md](../recherche/00_verification_lot1.md) | Contre-vérification indépendante du premier lot statistique |
| [00_verification_lot2.md](../recherche/00_verification_lot2.md) | Contre-vérification du deuxième lot |
| [00_verification_lot3.md](../recherche/00_verification_lot3.md) | Contre-vérification du troisième lot |
| [01_emploi_public_france.md](../recherche/01_emploi_public_france.md) | 01 — Cartographie de l'emploi public français : stocks, champs et coûts |
| [01b_flux_retraites.md](../recherche/01b_flux_retraites.md) | 01b — Entrées, sorties, retraites et capacité de non-remplacement |
| [01c_couts_entree_pensions.md](../recherche/01c_couts_entree_pensions.md) | Chantier 01c — Coût du recrutement évité, pensions et dépenses de conseil |
| [02_metiers_classification.md](../recherche/02_metiers_classification.md) | 02 — Métiers, fonctions et reconstruction des effectifs de terrain |
| [03_comparaison_harmonisee.md](../recherche/03_comparaison_harmonisee.md) | Base comparative internationale : collecte harmonisée initiale |
| [04_controle_preliminaire.md](../recherche/04_controle_preliminaire.md) | Contrôle préparatoire des données internationales héritées |
| [04_synthese_fonctions.md](../recherche/04_synthese_fonctions.md) | Comparer les fonctions avant de chiffrer les réformes |
| [04a_fiscalite_emploi.md](../recherche/04a_fiscalite_emploi.md) | Administration fiscale et services publics de l'emploi |
| [04b_education_securite_justice.md](../recherche/04b_education_securite_justice.md) | Enseignement, police et justice : écarts observés et corrections encore manquantes |
| [04c_sante_protection_sociale.md](../recherche/04c_sante_protection_sociale.md) | 04c — Coûts de gestion de la santé et de la protection sociale |
| [04d_territoires_fonctions_support.md](../recherche/04d_territoires_fonctions_support.md) | Organisation territoriale, agences et fonctions support |
| [05_reformes_etrangeres.md](../recherche/05_reformes_etrangeres.md) | Réformes étrangères : résultats observés, coûts, périmètres et conditions de transposition |
| [06_doublons_structures.md](../recherche/06_doublons_structures.md) | Doublons, structures et précédents français |
| [07_simplification_reglementaire.md](../recherche/07_simplification_reglementaire.md) | Simplification réglementaire : obligations, coûts et résultats |
| [08_ia_france.md](../recherche/08_ia_france.md) | 08 — IA en France : déploiements, mesures et conversion en économies |
| [09_ia_preuves_internationales.md](../recherche/09_ia_preuves_internationales.md) | 09 — IA : preuves internationales, temps de terrain et paramètres par tâche |
| [10_audit_propositions.md](../recherche/10_audit_propositions.md) | Audit des propositions chiffrées et des références budgétaires |
| [11_catalogue_reformes.md](../recherche/11_catalogue_reformes.md) | 11 — Catalogue des réformes chiffrées |
| [12_scenarios_seuils.md](../recherche/12_scenarios_seuils.md) | 12 — Scénarios, seuils et sensibilités |
| [13_contre_expertise.md](../recherche/13_contre_expertise.md) | 13 — Contre-expertise du catalogue et des scénarios |

## 17.3 Contrôles et contre-vérifications

| Contrôle | Chiffres | Résultat | Fichier |
|---|---:|---|---|
| Lot 1 (emploi, départs, coûts, métiers, base internationale) | 100 | 98 confirmés, 2 reclassés en estimation | `data/risques/verification_40_chiffres_lot1.csv` |
| Lot 2 (comparaisons par fonction) | 63 | 61 conformes, 2 après correction | `data/risques/verification_chiffres_lot2.csv` |
| Lot 3 (réformes étrangères, structures, simplification, IA, propositions) | 98 | aucun chiffre contredit ; 3 corrections de forme | `data/risques/verification_chiffres_lot3.csv` |
| Phase 5 (catalogue, hypothèses, scénarios) | 47 | aucun écart ; 2 réserves | `data/risques/verification_phase5.csv` |

## 17.4 Reproduction complète

```powershell
python -I scripts/11_catalogue.py          # catalogue, viviers, moteur, fiches
python -I scripts/12_sensibilites.py       # sensibilités et seuils
python -I scripts/12_classeur.py           # classeur Excel
python -I scripts/00_verification_phase5.py
python -I scripts/13_equipe_b.py
python -I scripts/14_livrables.py          # matrice, bibliographie, figures, chapitres générés
python scripts/build_rapport.py --pdf      # rapport et synthèse (Markdown, python-docx, Playwright)
python -I -m unittest discover -s tests -p "test_modele.py"
```

## 17.5 Dictionnaire des principales variables du modèle

| Variable | Définition | Unité |
|---|---|---|
| `etp_base` | Effectif initial du vivier | ETP |
| `taux_departs_annuel` | Départs mobilisables par an, rapportés au stock restant | fraction |
| `plafond_reduction_{scénario}` | Part maximale du vivier réductible | fraction |
| `taux_{scénario}` | Part du reliquat du vivier visée par une réforme | fraction |
| `part_non_remplacement`, `part_redeploiement`… | Répartition des mouvements | fraction, somme = 1 |
| `invest_meur_{scénario}` | Investissement total de la réforme | M€ 2026 |
| `cout_recurrent_meur_{scénario}` | Coût annuel supplémentaire à terme | M€/an |
| `eco_fonct_meur_{scénario}`, `effet_recettes_meur_{scénario}` | Économie de fonctionnement, recettes | M€/an |
| `cout_entree_hors_pension`, `cout_moyen_hors_pension` | Coût employeur annuel hors pension | k€/ETP |
| `gvt_individuel_reel`, `taux_conservation_consolide` | Progression du coût d'une cohorte ; part conservée en lecture APU | fraction |
