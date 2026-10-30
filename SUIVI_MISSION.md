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

## Avancement du deuxième lot

Les quatre volets fonctionnels 04a–04d sont documentés, avec une synthèse transversale et un deuxième dossier HTML. Il s'agit d'un premier diagnostic : les corrections complètes aux besoins et les potentiels nationaux demeurent non identifiés lorsque les sources ne permettent pas de les établir.

- **04a — Fiscalité et emploi** : 3 050 observations ISORA et 759 LMP, 23 pays demandés, sept fonctions fiscales et profils SPE rapprochés de comptes nationaux. 38 406 ETP fiscaux annuels ne sont pas les 93 789 agents de l'organisme en fin d'exercice. 132 comparaisons à quatre niveaux, six pistes de réforme, aucun écart brut converti en sureffectif.
- **04b — Éducation, police et justice** : ratios EAG par secteur et niveau, rémunérations et dépenses PPA, TALIS et métadonnées ; police à année commune2022 ; 360 observations CEPEJ. Les soutiens scolaires, enseignants, policiers et non-juges ne sont pas assimilés à des administratifs. La charge d'affaires et les délais sont explicités ; potentiel net non établi.
- **04c — Santé et protection sociale** : comptes DREES2026/année2025, 46 pays-années SHA, 1 851 lignes de régimes et 17 zones ESSPROS. HC7 inclut les assureurs privés et exclut les soutiens internes aux hôpitaux. Les OC privés représentent 52,09 % des frais de gestion de la santé2025. La décomposition par régime change le signe de l'écart France/Allemagne sur gouvernement/assurance sociale, sans prouver un gain causal. HCAAM conservé comme scénario historique, avec financement et transition.
- **04d — Territoires et supports** : 90 observations WOFI2020, DGCL2026, rapports Ravignon/Sénat et achats2025. Coordination valorisée, hypothèses support, gains achats et objectif immobilier restent distincts. Le cadre de foncière promulgué en août2026 entre dans la référence de réforme engagée. Les recouvrements et un raccordement RH non reconstitué sont documentés.
- **Reproduction et contrôle** : les cinq scripts analytiques reproduisent 36 CSV à l'identique. 63 contrôles indépendants relisent cellules, observations et passages primaires : 61 conformités sans correction et deux après correction (arrondi UK et rédaction RH). Les réserves d'unité/périmètre demeurent. 37 archives rapprochées de leurs empreintes ; 31 documents du cache sont restaurables par `scripts/restore_lot2_sources.py` (décomptes partiellement chevauchants). Les 104 fichiers bruts du lot sont identiques à leur index Git ; les attributs protègent aussi les empreintes des sorties assemblées.
- **Livrable** : `livrables/dossier_recherche_lot2.html`, six notes assemblées, graphique public/privé et manifeste des sources assemblées. Rendu bureau/mobile, 64 liens locaux, ancres et image vérifiés ; preuve associée à l'empreinte HTML dans `livrables/dossier_recherche_lot2.controle.json`. Les notes individuelles de contre-vérification sont aussi disponibles. Aucun rapport final ni scénario financier national n'est annoncé comme terminé.

## Avancement du troisième lot

Les six chantiers de recherche 05–10 sont documentés, contre-vérifiés et assemblés dans un troisième dossier. La session Codex a produit les notes et données le 28 octobre, puis s'est arrêtée sur une limite d'usage pendant l'assemblage ; la reprise du 30 octobre a sauvegardé ce travail, ajouté la contre-vérification 08–09, la synthèse et le dossier.

- **05 — Réformes étrangères** : 27 résultats datés sur 17 pays. Les réductions d'effectifs rebondissent ou se déplacent (Royaume-Uni −20,17 % puis +36,20 % ; Irlande ; Canada avec 8 000 transferts) ; les économies vérifiées restent très inférieures aux annonces (Digital Post 19,67 % du potentiel ; DOGE non certifié par le GAO). Phénix et les allocations néerlandaises chiffrent le coût des échecs.
- **06 — Structures et précédents** : 423 opérateurs et 72,572 Md€ de concours, majoritairement des missions ; −4 107 ETPT de plafond, dont 79 % d'abattements de vacance ; budgets initiaux 2026 Anah/Ademe/France Travail ; RGPP nette partielle ; DGFiP et SPF sans attribution causale au numérique.
- **07 — Simplification** : gains chiffrés surtout privés (entreprises, usagers) ; DLNUF au conditionnel ; loi 2026-403 promulguée ; aucun coût récent net des normes des collectivités (CNEN inaccessible).
- **08 — IA en France** : rapport IGF–IGAS–IGA d'avril 2026 lu par passages localisés ; exposition de 20 % des agents, qui n'est pas un gain ; 226/300/241 équivalents ETP France Travail sans baisse d'effectifs ; référence « IGF-IGAS 2025 » non identifiée.
- **09 — Preuves internationales** : 43 constats issus de 27 sources ou tentatives d'accès, gains par tâche hétérogènes (Noy −40 %, Dell'Acqua −25,1 %, METR +19 %), effets nuls sur les heures totales au Danemark ; paramètres conservés par tâche, sans conversion nationale.
- **10 — Audit des propositions** : 24 mesures pour 138,366–145,366 Md€ d'annonces de natures différentes ; 50 000 €/poste implicites ; 800 000 = 34,78 % des départs annoncés ; cumul illustratif 100–120 Md€ sur cinq ans ; PLF 2027 retraité à −1 076 ETP.
- **Contre-vérification** : **98 contrôles indépendants** (05 : 20 ; 06–07 : 20 ; 08–09 : 38 ; 10 : 20). Aucun chiffre contredit par sa source ; trois corrections de forme reportées en 08/09 ; une anomalie de signe dans le jaune opérateurs documentée ; trois limites d'accès (CNEN, texte opposable AI Act, livre). 78 corps HTTP du cache rapprochés de leur empreinte via `sources/lot3_manifestes_cache.json`.
- **Livrable** : `livrables/dossier_recherche_lot3.html`, synthèse transversale `00_synthese_lot3.md`, six notes, contre-vérification et 92 fichiers liés. Rendu bureau/mobile, 110 liens locaux, ancres et figure vérifiés ; preuve dans `livrables/dossier_recherche_lot3.controle.json`. Les dossiers des lots 1 et 2 sont inchangés ; celui du lot 2 se reconstruit octet pour octet.

## Prochaine séquence

Les recherches 05–10 sont terminées. Phase suivante : le catalogue de **25 fiches A–M**, à partir des pistes de 04a–04d et des règles établies en 05–10 (référence explicite, gain net, temps ≠ poste, coût d'entrée, non-cumul des annonces, pilotes à 24–36 mois).

Compléter les variables encore manquantes du chantier03 (NACE/ISCO, heures, démographie, délégations, missions et résultats de service). Les PPA santé/éducation et plusieurs corrections public/privé sont maintenant documentées, mais ne constituent pas un ajustement complet aux besoins. Construire ensuite le registre disjoint des viviers/départs/coûts, les quatre scénarios et les sensibilités. Répéter une contre-vérification d'au moins40 chiffres décisifs lors de la phase5, cette fois sur les réformes et économies finales.

## Sauvegarde

Un premier commit technique a été créé et poussé : `3c13606`. Le push avait d'abord été refusé par la revue automatique faute de destination vérifiée. La lecture du compte et du dépôt par le connecteur GitHub a confirmé que l'utilisateur connecté est le propriétaire `CherifAziz`, avec droits admin/push ; le même push, réévalué avec cette preuve, a ensuite réussi. Ne jamais forcer ni pousser sur une autre branche. Les prochains commits doivent séparer les chantiers et exclure le cache lourd.

Les sauvegardes suivantes sont poussées : `2f1247a` (France, flux et coûts), `d4ff1cb` (métiers), `3938915` (international et contrôle préparatoire), `07e9339` (préservation des octets des archives). Les 54 nouveaux fichiers bruts des dossiers 02, 03 et 04_controle ont été rapprochés octet pour octet de l'index Git sans divergence. Les règles `.gitattributes` préservent ces empreintes lors des futurs clonages ; aucun fichier brut hérité 01/04 n'a été modifié.

Le travail du lot 3 laissé non commité par Codex a été sauvegardé le 30 octobre en sept commits poussés, un par chantier (`f675405` à `f0cf23d`). Les 304 fichiers bruts et données du lot sont identiques à leur index Git. Seul `sources/08_10_prefetch_non_analyse.json`, commité au lot 1 avant les règles d'attributs du lot 3, diffère de l'index par ses fins de ligne ; il est exclu du dossier 3.

Pour régénérer les dossiers : le paquet `markdown` du dossier `.cache/python_deps` créé par Codex n'est pas lisible depuis toutes les sessions Windows. Installer `Markdown==3.11.2` (version exacte du cache) ailleurs et le fournir par `PYTHONPATH`, sans `-I`, reproduit le dossier du lot 2 à l'octet près.
