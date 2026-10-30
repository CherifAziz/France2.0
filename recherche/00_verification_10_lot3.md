# Contre-vérification indépendante du chantier 10 — lot 3

Contrôle arrêté au **28 octobre 2026**, sur la note finale présente dans le dépôt. Le code auteur du volet 10 n’a été ni lu, ni importé, ni exécuté. Les 24 montants sont reparsés dans l’HTML primaire gzip ; les PDF et le JSON-LD éditeur sont relus directement.

**Résultat : 20 points contrôlés, 0 écart de chiffre ou de localisation détecté.** Les statuts et réserves de chaque ligne figurent dans `data/risques/verification_10_lot3.csv`.

**Archives nécessaires toutes présentes.**

## Résultats décisifs

- **V10-01 — CONFIRME** : 24 montants, unité et bornes de chaque ligne. Source : HTML li.mesure 1-24 ; conversion 66 M€ en 0,066 Md€.
- **V10-02 — CONFIRME** : Borne basse des 24 montants. Source : Somme des bornes basses lues dans les spans de montant.
- **V10-03 — CONFIRME** : Borne haute des 24 montants. Source : Somme des bornes hautes lues dans les spans de montant.
- **V10-04 — CONFIRME** : Attributs numériques du compteur. Source : 24 attributs data-valeur, lus sans script auteur.
- **V10-05 — CONFIRME** : Bandeau Budget 2026 sur URL 2027. Source : Bandeau span, distinct du titre HTML 140 milliards.
- **V10-06 — CALCUL_CONFIRME** : Coût implicite par poste à terme. Source : Mesure 1 : 40 Md€ et 800000 départs non remplacés.
- **V10-07 — CALCUL_CONFIRME** : Part de 800000 dans 2,3 millions. Source : Mesure 1, quotient des deux nombres.
- **V10-08 — CALCUL_CONFIRME_HYPOTHESE** : Séquences et cumuls des deux conventions illustratives. Source : Contre-calcul indépendant 160000 postes/an× 50000 € ; conventions année pleine/mi-année.
- **V10-09 — CONFIRME_COHERENCE_06** : Anah: charges/intervention/personnel du compte de résultat. Source : PDF p. 246 ; en milliers d’euros ; lecture directe.
- **V10-10 — CONFIRME_COHERENCE_06** : Ademe: charges/intervention/personnel du compte de résultat. Source : PDF p. 226 ; en milliers d’euros ; lecture directe.
- **V10-11 — CONFIRME_COHERENCE_06** : France Travail: charges/intervention/personnel du compte de résultat. Source : PDF p. 458 ; en milliers d’euros ; lecture directe.
- **V10-12 — CONFIRME_PROJET** : Effort 54, mesures 43, différence 11. Source : PDF p. 29, imprimée 10 ; premier paragraphe.
- **V10-13 — CONFIRME_PROJET** : Schémas État/opérateurs et sous-total. Source : PDF 59, sous-total ; libellés/notes sur PDF 58.
- **V10-14 — CONFIRME_PROJET** : Total retraité avec caisses sociales. Source : PDF 59 TOTAL GENERAL ; exceptions PDF 30-31 ; 6816−4742−2150−1000.
- **V10-15 — CONFIRME_PROJET** : Administration centrale, tableau et arrondi de texte. Source : PDF 59 colonne dont Administration centrale ; texte PDF 30−800.
- **V10-16 — CONFIRME_PROJET** : Numérique réinternalisé, tableau et arrondi. Source : PDF 59 colonne dont Emplois numériques réinternalisés ; PDF 31 plus 400.
- **V10-17 — CONFIRME_PROJET** : Plafonds État et opérateurs. Source : PDF 59 colonnes plafonds ; note 2 PDF 58/59.
- **V10-18 — CONFIRME** : Taille, empreinte et copies du corps HTML. Source : Gzip versionné décompressé sans transformation ; copies cache si présentes.
- **V10-19 — CONFIRME** : Publication, pagination déclarée et ISBN. Source : JSON-LD @graph, Book principal ; décodage UTF-8.
- **V10-20 — LIMITE_CONFIRMEE** : Limite du feuilletage archivé. Source : HTML archivé du lecteur, sans exécution de JavaScript.

Les bornes de 138,366/145,366 Md€ et les attributs 141,866 Md€ sont des additions exactes d’annonces. Le quotient 50000 €/poste/an et les cumuls illustratifs 100/120 Md€ sont confirmés comme calculs conditionnels, sans validation du vivier, du coût marginal ni de l’additionnalité.

Les budgets Anah/Ademe/France Travail sont les **BI 2026** du jaune PLF 2027, en milliers d’euros au tableau source. Les trois lignes sont un **contrôle de cohérence avec le même original réemployé dans 06**, pas trois nouvelles observations statistiques indépendantes. Personnel de mission, interventions et frais de siège ne sont pas assimilés.

Le tableau d’emplois est une double page : PDF 58 porte les libellés, PDF 59 les colonnes numériques. Les objets PDF restituent des éléments hors cadre sur les deux pages ; un rendu visuel avec Poppler a été inspecté séparément pour éviter un double compte. Le script retient une seule ligne de sous-total, puis vérifie 6816−4742−2150−1000=−1076. Les sous-ensembles−812/+404 et plafonds 2032750/397282 ETPT restent distincts du flux net.

La fiche Fayard confirme les métadonnées du livre, non son contenu. Le lecteur archivé ne reçoit qu’une coquille HTML avec ressources JavaScript externes ; aucun texte intégral n’est considéré comme lu. Aucun montant de cession non publié n’est ajouté aux économies annuelles.

## Réserves conservées

- Date/exercice de la page politique non explicités ; bandeau Budget 2026 sur URL 2027.
- Annonces, objectifs, effets en régime permanent et exécution budgétaire restent distincts.
- Départs définitifs par métier, coût d’entrée, pensions, transition et doubles comptes ne sont pas validés par cette contre-lecture.
- Le budget d’un organisme et la masse salariale de ses agents de mission ne donnent pas ses frais administratifs supprimables.
- Aucune correction de la note 10 n’est appliquée directement ; tout écart éventuel doit être traité par son auteur.

## Reproduction

```powershell
python -I scripts/00_verification_10_lot3.py
```

Dépendances déjà disponibles : beautifulsoup4 et pypdf. Seuls les deux livrables de contrôle sont réécrits ; les bruts primaires restent inchangés. Un cache absent produit un statut explicite avec la commande exacte utilisant le collecteur commun `scripts/fetch.py`. La note est écrite en UTF-8, fins de ligne LF.

Sources : [page politique](https://www.budget2027.fr/), [jaune opérateurs](https://www.budget.gouv.fr/documentation/file-download/34432), [dossier PLF 2027](https://presse.economie.gouv.fr/download?n=1076%20-%20DP%20-%20Budget%202027-pdf&id=184723), [éditeur](https://www.fayard.fr/livre/le-casse-du-siecle-9782213733135/), [lecteur](https://www.liseuse-hachette.fr/ean/9782213732329).
