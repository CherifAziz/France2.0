# Contre-vérification indépendante — volets 06–07, lot 3

Contrôle arrêté au **28 octobre 2026**. **20 points décisifs** ont été examinés directement dans les PDF et HTML primaires archivés : **19 sont confirmés dans leur champ, dont quatre avec qualification ou réserve explicite ; un reste non vérifiable faute de document CNEN accessible**. Aucune nouvelle correction chiffrée des notes n'est demandée. Une inversion de signe dans le commentaire du jaune budgétaire, non reprise par 06, est consignée. Les réserves de période, unité, prévision et consolidation sont nécessaires au résultat.

## Méthode et indépendance

Le vérificateur n'a rédigé ni 06 ni 07. Il a lu les notes pour identifier les affirmations, puis les pages des documents primaires. **Aucun extracteur 06/07 n'a été lu, importé ou appelé ; aucun CSV produit par ces extracteurs ne sert de preuve.** Le script de contrôle lit les PDF avec pypdf, les octets HTML originaux et les métadonnées de téléchargement pour URL et SHA. Il recalcule séparément les différences, conversions k€→M€ et sommes de composantes. Les pages réellement consultées sont listées ci-dessous ; aucune lecture exhaustive des jaunes ou des rapports n'est revendiquée.

Cette indépendance concerne le **contrôle documentaire**, pas la production d'une nouvelle observation statistique. Les chiffres sont relus dans les mêmes sources primaires ; ils ne constituent pas une seconde série indépendante confirmant leurs phénomènes ou leur causalité.

Versions des notes contrôlées lors de cette reproduction :

- 06 : SHA256 `1de94827c327c50e24705eac48c8ddc513b60c097396fd88c3b458a81d036962`.
- 07 : SHA256 `9e16071b739813ea47b61845baa03a4832ad1c9fdc49490af60742a85e351ba5`.

## Résultats décisifs

Les 431 et 423 sont les nombres des périmètres proposés aux PLF 2026 et 2027. Le comparateur d'emplois 401389 est en revanche la **LFI 2026** : il ne faut pas reprendre les 401310 de la proposition initiale du jaune 2026. Le plafond 397282 et sa baisse 4107 ne sont pas des suppressions observées de personnes. Les 3248 d'abattements de vacance, le schéma-1209 ETP et son impact-998 ETPT ont des natures et unités différentes.

La baisse apparente de SCSP est 866902294€. Le seul reclassement de l'Agence du service civique enlève 460098952€ de cette différence, laissant 406803342€. Après toutes les mesures de périmètre, la différence vaut 417155884€. Les arrondis 866,902/406,803/417,156 M€ de 06 sont corrects. Ces trois différences ne sont ni cumulables ni des mesures causales de productivité.

**Anomalie primaire :** p.24, le jaune dit que les crédits d'intervention « diminuent en apparence de 28 M€ ». Ses CP passent pourtant de 16338579734€ à 16366164675€, soit **+27584941€**. Après le reclassementASC, la baisse de 432514011€ correspond bien aux 433 M€ annoncés à champ constant. La note 06 ne reprend pas le signe courant erroné. Le tableau et le calcul sont privilégiés, sans corriger silencieusement le commentaire primaire.

Les comptes Anah, Ademe et France Travail, publiés dans le jaune 2027, sont bien les **budgets initiaux 2026**. L'unité source est le millier d'euros. Les trois composantes principales de charges se somment aux totaux de la note. Les interventions, missions et emplois d'accompagnement empêchent de traiter tout le budget comme un coût de siège.

Le rapport parlementaire donne 808/264 M€ bruts/nets pour 2010 et 935/373 M€ pour 2011, après retour catégoriel. Le texte 373 et le calcul 935-562,6=372,4 diffèrent ;06 signale déjà ce point et ne corrige pas silencieusement la source. Le rapport des inspections présente 11,9 Md€ comme des gains attendus révisés, encore partiellement à confirmer, dans une présentation brute aux coûts induits mal suivis. Aucun net causal complet de la RGPP n'est ainsi reconstitué.

Les 26%→5% du CNEN sont une déclaration gouvernementale sur les saisines urgentes. Ils ne mesurent pas des normes supprimées ou des économies d'emploi. L'accueil et l'URL du rapport renvoient exactement la même maintenance de 654 octets : le coût récent net reste **non vérifiable dans ce lot**, et son absence de la base est justifiée. Ce constat d'accès ne prouve pas qu'aucun document n'existe ailleurs.

La page primaire du Sénat confirme l'adoption définitive en avril, la censure partielle en mai et la promulgation de la loi 2026-403 le 26 mai 2026. Elle n'établit pas l'application effective de chaque mesure ; le JORF intégral n'est pas revendiqué. Les 320 M€/an DLNUF sont au conditionnel pour l'État ; les 5 Md€/an du choc sont privés, potentiels et jugés invérifiables dans le document sénatorial.

Le portefeuille UE reste prospectif malgré le titre « achieved so far ». La page emploie aussi « will save », donne une cible 2029 et distingue des statuts de textes. Les 1,8 Md€ pour agriculteurs,210 M€ pour administrations et 324 M€ ponctuels sur 350 M€ d'investissements ont les périmètres correctement séparés dans 07. La méthode de coût standard confirme la différence obligations nouvelles/retirées ; elle ne transforme pas un temps valorisé en crédit budgétaire annulé.

## Tableau de contrôle

Le CSV fournit en plus les unités, périodes, URL exactes, localisations, objections et empreintes. Les champs de valeurs peuvent contenir plusieurs composantes du même point de contrôle ; ils ne sont pas un fichier de paramètres financiers.

| Identifiant | Point contrôlé | Résultat | Lecture de la source |
|---|---|---|---|
| V0607-01 | Nombre d'opérateurs et recomposition du périmètre | CONFIRME | 431 puis423 ; trois sorties, une entrée et trois regroupements |
| V0607-02 | Plafond légal et variation | CONFIRME | 401389→397282 ; différence4107 |
| V0607-03 | Abattement technique, schéma et impact annuel | CONFIRME | -3248 ETPT de vacance ; -1209 ETP de schéma ; -998 ETPT d'impact ; 79.084% par calcul |
| V0607-04 | Total rémunéré et hors plafond | CONFIRME | 482010→481336 ; hors plafond80621→84054 |
| V0607-05 | SCSP apparente et reclassement service civique | CONFIRME | 866902294€ -460098952€ =406803342€ |
| V0607-06 | SCSP à champ constant après tous transferts | CONFIRME_AVEC_ANOMALIE_SOURCE | 33519966787€ -33102810903€ = 417155884€ ; intervention courante+27584941€ |
| V0607-07 | Anah : année et composantes du compte de résultat | CONFIRME | 3651541 / 25000 / 175854 / 3450687 k€ ; chaque valeur divisée par1000 |
| V0607-08 | Ademe : année et composantes du compte de résultat | CONFIRME | 1603575 / 104788 / 175907 / 1322880 k€ ; chaque valeur divisée par1000 |
| V0607-09 | France Travail : année et composantes du compte de résultat | CONFIRME | 6889234 / 3886736 / 1030052 / 1972446 k€ ; chaque valeur divisée par1000 |
| V0607-10 | Économies titre2 brutes et nettes2010 | CONFIRME | 808 bruts /264 nets dans le même paragraphe |
| V0607-11 | Économies titre2 brutes et nettes2011 | CONFIRME_AVEC_RESERVE_SOURCE | 935 bruts /373 nets dans le texte ; 562,6 de mesures catégorielles au tableau |
| V0607-12 | Objectif révisé11,9 et portée du bilan | CONFIRME | 12,3→11,9Md€ ; gains bruts ; coûts induits rarement estimés ou suivis |
| V0607-13 | Saisines urgentes déclarées | CONFIRME_COMME_DECLARATION | 26% des textes à l'ordre du jour2022→5% en2025 |
| V0607-14 | Absence de chiffrage récent net vérifié | NON_VERIFIABLE_SOURCE_INACCESSIBLE | Accueil et URL du rapport renvoient la même maintenance de654 octets |
| V0607-15 | Loi entreprises : adoption et promulgation | CONFIRME | Sénat : adoption définitive après14/15 avril, décision21 mai et promulgation26 mai |
| V0607-16 | Potentiel annoncé et décrets déjà publiés | CONFIRME | Conditionnel permettrait ;320M€/an pour l'État ; mention JO20/01/2019 |
| V0607-17 | Nombre de mesures et potentiel privé | CONFIRME | 460 ;5 milliards potentiels chaque année ; coûts nouveaux non déduits |
| V0607-18 | Portefeuille de simplification et cible2029 | CONFIRME_AVEC_RESERVE_EXISTANTE | 12 propositions ; titre achieved so far mais texte will save ;37,5Md€ attendus2029 ;25%/35% |
| V0607-19 | Charges privées/publiques et ponctuel/récurrent | CONFIRME | Montants et one-off explicitement présents dans les deux rubriques |
| V0607-20 | Standard Cost Model : formule et périmètre | CONFIRME | ΣPN×QN-ΣPR×QR ; tarif et temps ; entreprises et fréquence ; distinction des activités habituelles |

## Corrections et limites

- **Chiffres et interprétations prioritaires :** pas de correction nouvelle demandée après ces lectures. Les écarts de périmètre et l'incertitude 2011 sont déjà documentés dans les notes.
- **Jaune, p.24 :** conserver la trace du signe erroné de variation courante des interventions, en distinguant cette anomalie primaire d'une erreur de la note 06.
- **CNEN :** conserver le manque et la distinction entre coûts de politique, coûts de formalité et économies administratives. La source de coût n'a pas été lue.
- **Droit :** le statut de promulgation est vérifié sur la source parlementaire primaire ; ce contrôle ne remplace pas la lecture du droit consolidé ou des décrets d'application.
- **Prévisions :** aucun montant PLF, portefeuille UE ou potentiel de simplification n'est requalifié en exécution ni en économie nette française.
- **Présentation :** Le lien initial vers 04 d a été corrigé au moment de cette reproduction.

Les contrôles automatiques sécurisent la transcription et les calculs ; ils ne démontrent pas à eux seuls l'interprétation de la source. Le présent rapport explicite les principales qualifications lues.

## Sources effectivement rouvertes et reproduction

- `j26` : [data/cache/06/operateurs_plf2026.pdf](https://www.budget.gouv.fr/documentation/file-download/31510) ; SHA256 `c408d289e3a8a324f0954a772b1e5efb9439baf2f489ff99d06f0b7f33a0447b` ; PDF p.12.
- `j27` : [data/cache/06/operateurs_plf2027.pdf](https://www.budget.gouv.fr/documentation/file-download/34432) ; SHA256 `474aee86b0a60d931651883e02a0b69ed4d0c3c8de4c68ca01b8fddd6ed793d3` ; PDF p.12,15,24,26,27,221,226,246,458.
- `rgpp` : [data/cache/06/rgpp_inspections2012.pdf](https://www.vie-publique.fr/files/rapport/pdf/124000520.pdf) ; SHA256 `11d8795aaf1967e523792fd43f678c67c3d6a4a738b88a947517b5c976c30b0e` ; PDF p.49,50,51,52.
- `rgpp_net` : [data/raw/06/rgpp_net_an2012.html](https://www.assemblee-nationale.fr/14/budget/plf2013/b0251-tIII-a28.asp) ; SHA256 `508ca1a1c84d157be03c2a9068b9b84a441d54fcb581a659faa9cbff82da5a8c` ; HTML original, paragraphes indiqués dans le CSV.
- `cnen` : [data/raw/07/cnen_accueil.html](https://www.cnen.dgcl.interieur.gouv.fr/) ; SHA256 `007be15585aff1960999a8653305e8aa29a3f08a02341ee0f9e42fb9a8f2e35a` ; HTML original, paragraphes indiqués dans le CSV.
- `cnen_rapport` : [data/cache/07/cnen_rapport2023.html](https://www.cnen.dgcl.interieur.gouv.fr/inlinedocs/2cc5e11123c95830ee392a3d114ae908/cnen-rpa-2023.pdf) ; SHA256 `007be15585aff1960999a8653305e8aa29a3f08a02341ee0f9e42fb9a8f2e35a` ; HTML original, paragraphes indiqués dans le CSV.
- `norme` : [data/raw/07/norme_reponse2026.html](https://www.senat.fr/questions/base/2026/qSEQ260508930.html) ; SHA256 `44bfaa0999b0551a6367b93e3d2547dd7c2909a68a999913b86a279557f5b2bb` ; HTML original, paragraphes indiqués dans le CSV.
- `loi` : [data/raw/07/loi_simplification2026_senat.html](https://www.senat.fr/travaux-parlementaires/textes-legislatifs/la-loi-en-clair/projet-de-loi-de-simplification-de-la-vie-economique.html) ; SHA256 `150a65da5393c1f771ee44bee309518c7b4588951425078d8057b875f12289d5` ; HTML original, paragraphes indiqués dans le CSV.
- `dlnuf` : [data/raw/07/dlnuf_reponse2019.html](https://questions.assemblee-nationale.fr/q15/15-10191QE.htm) ; SHA256 `eecb5f92ea849f57244269ae35a6395bca2f77e17abe56a1c7dffeed16ab7329` ; HTML original, paragraphes indiqués dans le CSV.
- `choc` : [data/raw/07/choc_senat2017.html](https://www.senat.fr/salle-de-presse/201702/trois-questions-a-elisabeth-lamure-et-olivier-cadic-auteurs-du-rapport-simplifier-efficacement-pour-liberer-les-entreprises.html) ; SHA256 `b85c6f0a55d4c39db8f5dd9985818994c6af7e08bb13f37062e9589aef2026b6` ; HTML original, paragraphes indiqués dans le CSV.
- `ue` : [data/raw/07/ue_omnibus2026.html](https://commission.europa.eu/topics/competitiveness/simplification_en) ; SHA256 `d1caec0ad48977ab2a8e0fae4d9479a9f51876fee9fa1f007e4f589979b593df` ; HTML original, paragraphes indiqués dans le CSV.
- `scm` : [data/cache/07/ue_scm2025.pdf](https://commission.europa.eu/document/download/9c8d2189-8abd-4f29-84e9-abc843cc68e0_en?filename=BR%20toolbox%20-%20December%202025.pdf) ; SHA256 `ced7548997fd3d6a3043c426422a218c874e468dc7c1438aa3057d0a488407bd` ; PDF p.528,529.

Commande : `python -I scripts/00_verification_06_07_lot3.py`.

Sorties : `data/risques/verification_06_07_lot3.csv` et `recherche/00_verification_06_07_lot3.md`. Aucun téléchargement supplémentaire, normalisation des réponses primaires, modification de06/07, commit ou push n'est effectué. La note est écrite en UTF-8 avec fins de ligneLF ; le CSV conserve le format exact émis par le script.
