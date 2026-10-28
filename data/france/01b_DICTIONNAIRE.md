# Dictionnaire — données 01b

Script producteur : `scripts/01b_flux_retraites.py`. Séparateur virgule, UTF-8. Les valeurs de classeur en milliers sont multipliées par 1 000 puis arrondies à l'unité disponible. Les nombres en pourcentage restent dans l'unité « pourcent » (8,7 et non 0,087). Les taux calculés dans les projections sont des fractions (0,087 et non 8,7).

## Variables communes aux données extraites

- `indicateur` : mesure publiée ou calculée, explicitement nommée.
- `groupe` : ensemble, versant, statut ou caisse. Les totaux et leurs composantes ne doivent pas être additionnés.
- `dimension` : type de ventilation. Dans `01b_flux_annuels.csv`, les lignes total, versant, statut et sexe sont quatre présentations du même ensemble. On ne les somme pas entre dimensions.
- `valeur` : valeur numérique dans l'unité indiquée.
- `unite` : `personnes_physiques`, `postes_occupes`, `pensions` ou `pourcent` selon le fichier. Une pension ne représente pas un ETP et les PP ne sont pas des EQTP.
- `annee` : année d'observation. Le rapport édité en 2026 ne transforme pas ses observations 2024/2025 en observations 2026.
- `statut` : `FAIT`, `ESTIMATION` ou `HYPOTHÈSE`, au sens du protocole.
- `source_url` : URL exacte de l'archive officielle ou fiche primaire.
- `source_localisation` : fichier, onglet et cellule, ou section du tableau HTML.
- `note` : périmètre, précaution d'agrégation ou hypothèse.

## Fichiers

- `01b_flux_annuels.csv` : entrées/sorties civiles 2016-2024, soit 162 lignes = 9 ans × 9 groupes × 2 flux. Comparaisons aux 31 décembre ; pas de déduplication interannuelle des personnes. Source complément, figure 2.
- `01b_flux_2024_versant_statut.csv` : 48 lignes = 3 versants × 4 statuts (dont ensemble) × 4 indicateurs. Les taux publiés utilisent la moyenne des stocks fin 2023 et fin 2024.
- `01b_mobilites_2024.csv` : 18 lignes, stocks 2023/2024 et quatre flux par versant. Mouvements interversants sans effet national. L'identité stock-flux peut conserver un écart de suivi documenté.
- `01b_retraites_annuelles.csv` : séries 2000-2025, six groupes. Ircantec absent avant 2008, jamais remplacé par zéro.
- `01b_retraites_2025.csv` : 11 composantes des pensions et deux totaux emboîtés. Les lignes `FP_total` et `FP_hors_militaires` ne sont pas des composantes supplémentaires.
- `01b_ages_2024.csv` : 24 lignes = 3 mesures d'âge × 4 versants/ensemble × 2 mesures (niveau et pourcentage). Une même personne peut appartenir à plusieurs mesures : 60 ans ou plus est inclus dans 50 ans ou plus.
- `01b_projection_2027_2031.csv` : 15 lignes de **tests mécaniques**, et non prévisions ; 3 versants × 5 ans. `stock_debut_suppose_pp`, `flux_sortie_suppose_pp` et `sorties_cumulees_pp` sont des PP. `taux_sortie_applique` est `sorties2024/stockfin2024`, fraction calculée qui diffère du taux publié. Le stock initial 2027 est supposé égal à fin 2024 ; aucun recrutement. Les stocks/sorties sont calculés sans arrondi intermédiaire puis exportés à six décimales.
- `01b_tests_seuils_departs.csv` : 30 lignes = 6 bases × 5 seuils. `volume_sur_5ans` est une somme historique ou une simulation selon `base`. `seuil_pp` est le seuil testé dans l'unité de cette base, sans conversion en ETP. `part_du_volume_necessaire = seuil_pp/volume_sur_5ans`. Une valeur inférieure à 1 ne valide pas la réforme. Le libellé d'unité mixte oblige à lire `base` : les bases pensions portent sur des pensions, les autres sur des occurrences de sortie en PP.
- `01b_sre_controle_pensions.csv` : extraction des deux tableaux primaires SRE. `sous_categorie` distingue motif ou domaine administratif selon `source_localisation`. FPE civile comprend ici La Poste et Orange. Les tableaux motif et domaine présentent deux fois les mêmes agrégats : ne pas les sommer.
- `01b_controles.json` : contrôles de rapprochement, paramètres de simulation, écarts conservés et limite d'indépendance des sources.

## Reproduction des sources

Les XLSX bruts sont déjà versionnés dans `data/raw/01/dgafp_ra2026/`. Les empreintes dans `sources/registre_01b.csv` portent sur ces **XLSX**, pas sur les ZIP des URL. Le contrôle SRE nécessite le cache HTML téléchargé par la commande reproduite dans `recherche/01b_flux_retraites.md` ; ce cache n'est pas supposé versionné. Aucun document téléchargé n'est exécuté.
