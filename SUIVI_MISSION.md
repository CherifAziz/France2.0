# Suivi de mission

Date de reprise : **28 octobre 2026**, fuseau du commanditaire Africa/Lagos. Branche imposée : `claude/focused-wozniak-l2w1o4`, dépôt `CherifAziz/France2.0`.

## Objectif conservé

Poursuivre le cahier des charges de `PROMPT_CODEX.md` jusqu'à un rapport indépendant et reproductible sur l'administration française, ses coûts et son potentiel de transformation. Le travail est livré par étapes substantielles. Les notes présentes ne sont pas un rapport final et aucun total national d'économies n'est encore établi.

## État à la fin du premier lot de reprise

- **Infrastructure** : `scripts/fetch.py` rétabli, archivage brut/texte/manifeste, préservation des instantanés, contrôle des erreurs HTTP et défis Incapsula. Accès Insee, DGAFP, Eurostat et OCDE vérifiés ; timeout sur une page Cour. Agent Reach/conda/mcporter absents du PATH : moteur de recherche connecté et sources directes utilisés.
- **Moteur financier** : simulation corrigée, départs partagés dans le temps, cibles disjointes, transferts publics/privés séparés, coûts et cumuls documentés. **23 tests financiers et cinq tests d'archivage passent**. Aucun paramètre national calibré ajouté.
- **01 — Emploi France** : extraction des stocks, statuts, rattachements, série rétropolée, champs hors FP, D1/titre 2, salaires et temps. Dix contrôles arithmétiques réussis ; 19 XLSX hérités sont identiques aux distributions officielles retéléchargées. L'écart de version Insee/DGAFP reste documenté, sans explication causale inventée.
- **01b — Départs et retraites** : note et neuf CSV produits, contrôle SRE effectué. Les 2,339789 millions de sorties civiles 2020–2024 sont des occurrences, pas un vivier administratif de postes supprimables.
- **01c — Coûts** : note de lecture primaire PAP 156/218 et pensions produite, 80 indicateurs et 16 sources, dont cinq paramètres nationaux explicitement manquants. Les coûts HCAS ne doivent pas être injectés automatiquement comme coûts hors toutes pensions.
- **02 — Métiers** : extraction de 221 lignes et note produites, avec champs SIASP/DEPP/SAE séparés ; panier de groupes à dominante opérationnelle, dédupliqué des 19 enseignants militaires, estimé à 2 400 090 PP. Ce n'est pas une partition des tâches ni la preuve d'un total de terrain strict. Couverture des métiers manquants consignée et PDF DGFiP restaurable par --download.
- **03 — International** : première base harmonisée produite pour 44 pays et agrégats séparés : 3 859 lignes dont 3 553 valeurs et 306 absences explicites. Pays/années/versions et multiplicateurs explicités ; 224 rapprochements financiers sans écart supérieur à 0,15 point de PIB. Sept divergences d'emploi S13 entre tables restent documentées. Corrections de besoins et qualité de service encore à construire.
- **04 — Fonctions** : contrôle préparatoire des 15 CSV hérités terminé ; trois observations Eurostat vérifiées, 218 valeurs ISORA rapprochées. Analyse fonctionnelle et correction des écarts à réaliser.
- **05 à 10** : recherches de fond à poursuivre après les bases. Le rapport IGF–IGAS–IGA 2026 (PDF de 709 pages) et le site budget2027.fr ont été téléchargés dans `data/cache/08/` et `data/cache/10/`. Téléchargement ne signifie pas lecture ni validation de leurs affirmations. Le livre n'a pas été lu.
- **Phases 3–6** : catalogue d'au moins 25 fiches A–M, registre national de viviers, paramètres et classeur financier, quatre scénarios, seuils, sensibilités, contre-expertise, rapport en 17 parties, synthèse et exports restent à produire.
- **Contre-vérification du lot** : 100 chiffres relus directement dans les sources primaires, sans utiliser les fonctions d'extraction des auteurs : 98 confirmés, deux statuts FAIT reclassés ESTIMATION (sommes calculées), aucun écart numérique résiduel dans cet échantillon. Les 100 contrôles ne clôturent pas la contre-expertise des futures économies.
- **Livrable consultable** : `livrables/dossier_recherche_lot1.html`, assemblage des notes et données avec manifeste ; rendu local, liens, images et absence de débordement horizontal vérifiés. Aucun rapport final PDF/DOCX ni classeur national n'est annoncé comme terminé.

## Points décisifs à ne pas perdre

1. Base française détaillée : DGAFP RA2026, fin 2024, hors contrats aidés, 5 848 291 PP. L'IP2094 conserve une autre version, et son EQTP annuel est un autre concept.
2. La somme des sorties civiles sur cinq ans ne démontre ni départs définitifs à vie, ni unité ETP, ni métier administratif, ni origine exacte de l'affirmation politique.
3. Ne pas additionner pensions et sorties ; ni gendarmes et militaires sans déduplication ; ni médecins/enseignants privés déjà compris et stock total FP.
4. Distinguer trois lectures financières : budget employeur complet, coût normalisé hors retraite, APU consolidées. Les pensions déjà dues demeurent ; la cotisation de l'employeur peut cependant cesser à taux fixé.
5. Les chiffres PAP sont par programme/catégorie, les salaires SIASP des moins de 30 ans ne sont pas des coûts d'entrée, et le D1 moyen n'est pas un coût marginal.
6. Les jeux internationaux sont multidimensionnels : HC7 et total santé, régimes HF imbriqués, unités et multiplicateurs, moyennes/erreurs standard TALIS, dépenses/ratios EAG. Aucun cumul naïf.
7. Une différence internationale brute n'est pas une mesure de sureffectif. L'externalisation doit être intégrée au diagnostic économique.

## Prochaine séquence

Reprendre le chantier 04 fonction par fonction à partir des données contrôlées. Compléter les variables manquantes du chantier 03 (NACE/ISCO, PPA, heures, démographie, modes public/privé et résultats de service) avant de corriger les écarts bruts. Les chantiers 05–10 doivent documenter les réformes avant la calibration des scénarios. Répéter une contre-vérification d'au moins 40 chiffres décisifs lors de la phase 5, cette fois sur les réformes et économies finales.

## Sauvegarde

Un premier commit technique a été créé et poussé : `3c13606`. Le push avait d'abord été refusé par la revue automatique faute de destination vérifiée. La lecture du compte et du dépôt par le connecteur GitHub a confirmé que l'utilisateur connecté est le propriétaire `CherifAziz`, avec droits admin/push ; le même push, réévalué avec cette preuve, a ensuite réussi. Ne jamais forcer ni pousser sur une autre branche. Les prochains commits doivent séparer les chantiers et exclure le cache lourd.

Les sauvegardes suivantes sont poussées : `2f1247a` (France, flux et coûts), `d4ff1cb` (métiers), `3938915` (international et contrôle préparatoire), `07e9339` (préservation des octets des archives). Les 54 nouveaux fichiers bruts des dossiers 02, 03 et 04_controle ont été rapprochés octet pour octet de l'index Git sans divergence. Les règles `.gitattributes` préservent ces empreintes lors des futurs clonages ; aucun fichier brut hérité 01/04 n'a été modifié.
