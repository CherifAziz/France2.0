# Dictionnaire des données du chantier 01

Date : 28 octobre 2026. Extraction : `python -I scripts/01_cartographie.py`.

## Tables

- `01_effectifs_versions.csv` : 48 observations. PP instantanées et EQTP annuels Insee 2023/2024 ; deux versions DGAFP/Insee et champs contrats aidés compris/exclus. Les unités ne s'additionnent pas.
- `01_effectifs_statuts.csv` : 18 observations, PP fin 2024, statuts par versant et total FP. Chaque statut est déjà inclus dans le total de son versant.
- `01_effectifs_employeurs.csv` : 50 observations de rattachement institutionnel, PP fin 2024. Les lignes « dont » sont incluses dans leurs sous-totaux.
- `01_effectifs_serie_2011_2024.csv` : 56 observations de la série rétropolée DGAFP, trois versants et total, hors contrats aidés. Les décimales historiques reflètent le retraitement, pas une précision à la fraction de personne.
- `01_effectifs_hors_fp.csv` : 21 observations de périmètre institutionnel, y compris totaux. S13, FP, entreprises marchandes et organismes financés publiquement se recouvrent partiellement. Ne pas sommer toutes les lignes.
- `01_depenses_personnel.csv` : 57 observations, Md€ courants 2024/2025. D1 et titre 2 sont des concepts différents. Les catégories, sous-catégories et totaux du titre 2 sont imbriqués. Les dépenses ne sont pas des effectifs.
- `01_salaires_temps.csv` : 14 observations. Salaires bruts par EQTP mensualisé en 2024 et heures annuelles effectives déclarées en 2025, avec champs spécifiques. Le salaire des moins de 30 ans n'est pas un coût d'entrée.
- `01_controles.csv` : dix contrôles arithmétiques, exprimés dans l'unité des cellules originales (milliers de personnes ou Md€). Tolérance de 0,01 dans cette unité. Les écarts effectifs sont exportés, pas effacés.
- `01_manifest_fichiers.csv` : SHA-256 complet des neuf fichiers utilisés par l'extracteur, URL et date de publication.
- `01_controle_provenance.csv` : comparaison binaire SHA-256 de 19 fichiers hérités avec leurs distributions officielles archivées ; contrôle d'intégrité, pas contrôle indépendant des statistiques.

Les CSV `01b_*` ont leur propre [dictionnaire](01b_DICTIONNAIRE.md).

## Colonnes communes des tables d'indicateurs

| Colonne | Définition |
|---|---|
| `id` | Identifiant technique stable de l'observation |
| `indicateur` | Concept mesuré, en français |
| `versant` | FPE/FPT/FPH/FP ou secteur institutionnel explicite |
| `categorie` | Statut, type d'employeur ou champ contrats aidés |
| `annee` | Année de référence statistique, différente du millésime de publication |
| `valeur` | Nombre converti dans l'unité de la colonne `unite` |
| `unite` | PP, EQTP annuels, MdEUR courants, EUR mensuels par EQTP ou heures annuelles |
| `champ` | Territoire, date/volume, exclusions et population couverte |
| `niveau` | `detail`, `detail_inclus`, `sous_total` ou `total` ; empêche une somme naïve |
| `version` | Publication dont est issu le nombre |
| `source_url` | Adresse de la source primaire ; pour un ZIP, fichier membre précisé dans la localisation |
| `source_localisation` | Fichier XLSX, feuille et cellule exacte |
| `date_publication` | Date de publication de la source |
| `statut` | `[FAIT]` pour les valeurs numériques publiées, transcrites et converties d'unité |
| `fichier_brut` | Chemin du fichier original conservé dans Git |
| `valeur_brute` | Nombre exact avant conversion, tel que lu dans la cellule |
| `multiplicateur` | Facteur de conversion, par exemple 1000 pour milliers de personnes vers personnes |
| `notes` | Risques de double comptage et limites de lecture |

L'arrondi purement numérique d'une conversion ne transforme pas un fait publié en estimation économique. Une variation, un ratio construit ou une projection sont identifiés séparément comme estimation ou hypothèse dans les notes de recherche. Les données manquantes ne sont jamais imputées à zéro.
