# Dictionnaire — métiers et classification fonctionnelle

Producteur : `scripts/02_metiers.py`. CSV UTF-8, séparateur virgule. Aucune modification des classeurs bruts. Les classes fonctionnelles sont celles de l'audit, pas les catégories statutaires françaises.

## 02_metiers.csv

- `id` : identifiant stable du groupe et, pour DEPP, de son unité.
- `metier_ou_groupe` : libellé explicite de profession, corps, filière ou agrégat. Certains groupes sont composites.
- `valeur` : nombre numérique publié ou calculé. Les milliers DGAFP sont convertis en unités. Les ETP sont conservés selon leur précision publiée.
- `unite` : `PP` (personnes physiques), `postes_SAE` (non dédupliqués entre établissements), `ETP_au_30_novembre` (DEPP), `ETP_moyen_annuel_remunere` (SAE), ou `pourcent_de_personnes` (DEPP missions). Ne jamais sommer les unités.
- `annee`, `date_observation` : année et date de référence. Pour l'ETP moyen annuel, la date indique le millésime, pas une photographie au 31 décembre.
- `versant_ou_secteur` : versant, institution ou secteur juridique de la source. « Hospitalier public » SAE n'est pas synonyme de la FPH entière Siasp.
- `classe_fonctionnelle_dominante` : `A` mission directement opérationnelle, `B` soutien nécessaire, `C` administration/gestion. Les valeurs multiples indiquent une absence de ventilation et non un partage égal. `non_attribuee` signifie que l'affectation n'est pas établie.
- `statut_classification` : `HYPOTHÈSE` pour toute affectation de la mission dominante, même lorsque l'effectif est un fait publié. `NON TROUVÉ` si aucune classe n'est attribuée.
- `drapeau_D_revue` : `non_evalue` dans cette phase. D devra viser des activités précisément auditées ; aucun reliquat statistique n'est classé inutile.
- `dimension_source` : profession/filière, PCS/catégorie hiérarchique, mission principale, institution/statut ou discipline/section. Deux dimensions ne mesurent pas nécessairement la même fonction.
- `groupe_disjonction` : ensemble dans lequel une addition limitée peut avoir un sens. Ce champ ne constitue pas un registre national de viviers déjà dédupliqué.
- `additif_dans_groupe` : `non` pour les agrégats ou contrôles répétés ; `oui` pour des composantes du groupe. Cela **n'autorise pas** à additionner les lignes de groupes différents, les unités différentes ou les parents et enfants.
- `parent_id` : identifiant de la ligne du groupe englobant, lorsqu'il est représenté. Les parents référencés sont contrôlés comme existants et distincts de leur enfant. Le graphe n'est pas une partition nationale exhaustive.
- `couverture` : champ géographique et statutaire, exclusions, date conceptuelle.
- `statut` : `FAIT` pour un nombre lu dans une source ; `ESTIMATION` pour une somme ou différence ; ne préjuge pas de la classification fonctionnelle.
- `source_url`, `source_localisation` : URL exacte et fichier/onglet/cellule ou page PDF. Les archives DGAFP regroupent plusieurs classeurs ; les empreintes du registre portent sur les XLSX.
- `note` : chevauchements, limites et règles particulières.

La table comprend des parents et enfants, deux unités pour DEPP et plusieurs sources de santé. **Son total général n'a aucun sens statistique.** Pour une analyse nationale, filtrer d'abord par source, champ, date, unité et composantes disjointes, puis contrôler chaque intersection.

## 02_panier_siasp_2024.csv

Contributions à un panier de groupes à dominante opérationnelle, homogène en date/unité/géographie Siasp. `valeur_pp` peut être négative pour une déduction de chevauchement. Les identifiants `source_ids` renvoient à la table principale. Les 19 enseignants militaires sont déduits une fois. Le résultat 2 400 090 n'est pas une classification en tâches A et ne valide pas un total de « terrain » strict.

## 02_positions_2_2m.csv

Les six chiffres d'une recension attribuant un périmètre à Sarah Knafo, conservés à titre de position à vérifier. `statut=HYPOTHÈSE`, année statistique non précisée, unité non harmonisée. L'article a été lu ; le livre n'a pas été lu. **Ce fichier n'est pas une source de calibration statistique** et ne s'additionne pas aux données de la table principale. Sa somme 2 191 000 explique seulement l'arrondi de la position rapportée.

## 02_controles.json

Ratios calculés, nombre de lignes produites et contrôles d'agrégation. `panier_terrain_strict_etabli=false` doit rester visible : le contrôle arithmétique du panier ne valide pas son interprétation comme temps de terrain ou emplois intégralement opérationnels. Le bloc `source_DGFiP` indique la présence du PDF, le nombre de lignes produites et la commande exacte de restauration. Une absence ne disparaît pas dans un total silencieux.

## 02_couverture_metiers.csv

Suivi des quinze familles prioritaires : identifiants des données disponibles, portée de la mesure et lacunes explicites. Ce fichier est un index de couverture et ne porte pas de chiffres supplémentaires. `NON TROUVÉ` pour la gendarmerie signifie absence de décompte isolé des tâches demandé ; ses agents sont déjà inclus dans le total militaire, ce n'est pas une valeur zéro.

## Sources et régénération

Les huit XLSX DEPP/DREES sont dans `data/raw/02/`, accompagnés des manifestes HTTP avec URL, date, statut et SHA-256 complet. Les cinq fichiers DGAFP requis sont dans `data/raw/01/dgafp_ra2026/`. Le cache documentaire conserve notamment le PDF DGFiP et les recensions. `--download` restaure aussi le PDF DGFiP. Sans ce PDF et sans l'option de téléchargement, le script régénère la base métier principale, omet les deux lignes documentaires correspondantes et signale leur absence dans les contrôles avec la commande de restauration. Le registre `sources/registre_02.csv` distingue une lecture via outil web d'un téléchargement direct refusé par HTTP 403.

Commande : `python -I scripts/02_metiers.py --download`. Requiert `openpyxl`, et `pypdf` pour les deux totaux DGFiP si le PDF est présent. Les fichiers téléchargés ne sont jamais exécutés.
