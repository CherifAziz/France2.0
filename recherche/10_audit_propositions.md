# Audit des propositions chiffrées et des références budgétaires

Recherche arrêtée au **28 octobre 2026**. Le volet principal examine les **24 annonces** du site budget2027.fr, avec une analyse approfondie des effectifs et de l'IA. Il distingue annonce, identité arithmétique, enveloppe de dépenses, scénario et économie nette réalisable. Cette note n'attribue pas d'intention aux auteurs et ne juge pas l'opportunité politique des prestations concernées.

## 1. Synthèse

1. **[FAIT sur une annonce]** Le site affiche un objectif de **140 Md€ par an**, avec 24 mesures. Une nouvelle lecture du 28 octobre retrouve exactement le corps HTML de l'instantané initial : **113 850 octets**, SHA-256 commençant par `3fa12a84`. Le téléchargement répété n'est pas une source indépendante. [Site politique][site].
2. **[FAIT de périmètre]** Le bandeau indique **Budget 2026** sur une URL **budget2027.fr**. La date de publication, les prix retenus et le premier exercice d'application ne sont pas explicités. Les liens inspectés renvoient à l'auteur, aux réseaux sociaux, au plan en image et aux libraires ; aucun lien documentaire par mesure n'a été trouvé. Même source.
3. **[ESTIMATION]** L'addition des bornes basses affichées donne **138,366 Md€**, celle des bornes hautes **145,366 Md€**, hors prix de cession d'actifs. Les attributs HTML du compteur retiennent les milieux des fourchettes et totalisent **141,866 Md€**. Ces additions ne valident ni l'indépendance des lignes ni une économie nette de 140 Md€. [Extraction des 24 montants][site] ; `10_sommes_annonces.csv`.
4. **[ESTIMATION]** Les **40 Md€ pour 800 000 postes** impliquent **50 000 € par poste et par an**. C'est un coût implicite calculé, pas un coût d'entrée publié avec son champ, ses pensions et ses cotisations. Les **5 Md€ d'IA** s'ajoutent dans la présentation, sans ventilation de leurs activités ni raccordement au vivier des 800 000. [Mesures 1–2][site].
5. **[ESTIMATION]** Les 800 000 représentent **34,78 %** des 2,3 millions de départs annoncés. Cette proportion ne prouve pas une part administrative ni une capacité de remplacement évitable. Le lot 1 a identifié **2,339789 millions d'occurrences de sorties civiles sur 2020–2024**, un autre objet que des départs définitifs administratifs futurs. [Note01b](01b_flux_retraites.md) et données DGAFP citées dans cette note.
6. **[HYPOTHÈSE illustrative]** Avec 160 000 postes évités chaque année et 50 000 € constants, une convention d'année pleine produit **8,16,24,32,40 Md€**, cumul 120 Md€. Une convention de mi-année produit **4,12,20,28,36 Md€**, cumul 100 Md€. Aucun de ces calendriers n'est une prévision française ; ils montrent pourquoi un montant à terme ne se répète pas automatiquement dès la première année.
7. **[NON TROUVÉ]** L'origine précise du vivier administratif de 800 000, sa répartition par métier/versant, les départs définitifs correspondants et le coût marginal de recrutement évité ne sont pas établis par le site. Le livre n'a pas été lu intégralement. La fiche éditeur confirme une publication le **2 septembre 2026** et 286 pages déclarées, pas son argumentation financière. [Fayard, JSON-LD][fayard].
8. **[FAIT / LIMITE]** Le rapport IGF–IGAS–IGA accessible est daté **avril 2026**, publié en juillet 2026 ; ses numéros de mission comportent 2025. Cela constitue une piste de confusion de millésime, pas l'identification démontrée de la référence «IGF-IGAS 2025» du site. Les **20 % d'exposition** ne sont pas un taux de productivité. [Volet08](08_ia_france.md), PDF p.24–25 du [rapport][igas].
9. **[FAIT sur une estimation externe]** Le même rapport cite pour trois outils France Travail des équivalents de temps de **226,300 et 241 ETP**, en précisant qu'ils n'ont pas été traduits en diminution des ETP. Leur somme de 767 ne constitue donc pas 767 postes supprimés. [Rapport, PDF p.236, annexeV p.41, note 162][igas] ; [volet08](08_ia_france.md).
10. **[FAIT]** Le jaune opérateurs annexé au PLF 2027 présente des **budgets initiaux 2026** : compte de résultat Ademe **1 603,575 M€**, dont **1 322,880 M€ d'interventions** ; Anah **3 651,541 M€**, dont **3 450,687 M€ d'interventions**. Ces budgets ne sont pas intégralement des frais administratifs. [Jaune, PDF p.226 et 246][operateurs].
11. **[FAIT]** Dans ces mêmes budgets initiaux, le personnel représente **104,788 M€ à l'Ademe** et **25,000 M€ à l'Anah**. Le fonctionnement hors personnel comprend d'autres activités et achats ; il ne constitue pas automatiquement du siège supprimable. Les montants politiques de 3,4 et 6 Md€ exigent un pont de champ/année/activité. Même source.
12. **[FAIT]** Le budget initial 2026 de France Travail affiche **6 889,234 M€ de charges**, dont **3 886,736 M€ de personnel** et **1 972,446 M€ d'interventions**. La proximité du montant politique de 4 Md€ avec la masse salariale ne démontre pas son origine. La rubrique internationale LMP placement de 2023 et le budget de l'organisme sont distincts. [Jaune, PDF p.458][operateurs] ; [note04a](04a_fiscalite_emploi.md).
13. **[FAIT de référence]** L'Observatoire de la laïcité figure encore dans la liste politique d'organismes à supprimer, alors que ses missions ont été reprises en **2021** par le Comité interministériel de la laïcité. Aucun gain additionnel n'est déduit de cette seule actualisation. [Présentation officielle du Comité][laicite] ; [volet06](06_doublons_structures.md).
14. **[FAIT de nature]** Le plan réunit suppressions d'institutions, baisses de prestations, arrêts d'interventions, recettes de tarification et une cession d'actifs. Un euro de l'une de ces catégories n'est pas un euro d'économie administrative. Le prix ponctuel de cession est explicitement ajouté à la ligne audiovisuelle par le site et n'est pas inclus dans notre somme récurrente. [Mesures 3–24][site].
15. **[HYPOTHÈSE à instruire]** Treize intersections de mesures sont enregistrées : effectifs/IA/institutions, critères RSA/fraude, aides urbaines/associations, énergie/Ademe, APD/contribution européenne, associations/presse. Ce sont des risques de recouvrement, pas treize montants de double compte prouvés. L'exclusion des soutiens énergétiques revendiquée à la ligne Ademe est reconnue mais doit être rapprochée comptablement.
16. **[FAIT de statut]** La loi de finances 2026 a été promulguée le **19 février 2026**, loi 2026-103. Elle ne doit pas être confondue avec le plan Bayrou de juillet 2025 ou les projets 2027. [Dossier législatif Sénat][lfi]. L'effort Bayrou de 43,8 Md€ est seulement **[EXTRAIT]** dans la source Matignon indexée ici : l'accès direct a répondu 403. [Compte rendu du 16 juillet 2025][bayrou].
17. **[FAIT sur un projet]** Le dossier gouvernemental du 1 er octobre 2026 distingue **54 Md€ d'effort total** et **43 Md€ de mesures dans PLF/PLFSS 2027**, avec montée en charge de mesures engagées. La différence calculée est 11 Md€. Ce n'est ni 54 Md€ de suppressions de personnel ni un résultat budgétaire déjà réalisé. [Dossier, PDF p.29–31][plf].
18. **[FAIT sur un projet]** Les schémas proposés sont **+8 025 ETP à l'État**, **−1 209 chez les opérateurs**, sous-total **+6 816**. Le total retraité, avec caisses sociales et hors formation initiale des enseignants et marche LPM, est **−1 076 ETP**. Les plafonds ETPT, les flux ETP, les sous-ensembles et les réalisations ne sont pas interchangeables. [Double page PDF 58–59, contrôlée visuellement][plf].
19. **[FAIT de comparaison]** Le tableau gouvernemental comprend **−812 ETP d'administration centrale** et **+404 ETP numériques réinternalisés**, déjà inclus dans ses flux. La formule générale du site selon laquelle aucun poste ne serait supprimé n'est pas une description complète de ce projet d'octobre 2026 ; sa date et son budget de référence restent à préciser. Même source.
20. **[FAIT sur des positions]** L'Institut Montaigne rappelle les objectifs 2017 de **120 000 emplois pour Macron** et **500 000 pour Fillon**, et son propre chiffrage historique de **3,17 Md€ à terme** pour le premier. Il s'agit de promesses et d'estimations datées, pas d'économies exécutées ni de coûts transposables à2027. [Bilan 2021, PDF p.4–5][montaigne] et [tableau 2017][montaigne 2017].

## 2. Lecture des 24 lignes

Tous les montants ci-dessous sont des **[FAIT] sur l'annonce politique**, en Md€ annuels annoncés, sans économie nette validée. Les bornes reproduisent les nombres affichés, pas un intervalle de confiance. Les descriptions sont des paraphrases d'audit ; le texte source et les montants exacts sont conservés dans l'archive et le CSV.

| ID | Objet annoncé | Montant | Qualification et vérification nécessaire |
|---|---|---:|---|
| 01 | Recrutements évités sur cinq ans | 40 | Départs, métiers, ETP et coût d'entrée évité à documenter ; montant à terme et calendrier |
| 02 | Productivité par IA | 5 | Référence exacte, tâches, adoption, contrôle, conversion en dépenses et recouvrement avec 01 |
| 03 | Nationalité et aides non contributives | 15–20 | Prestations ; droits et catégories de bénéficiaires, périmètre et réactions comportementales |
| 04 | RSA limité dans la durée | 4,8 | Prestations ; appliquer après 03, calendrier des cohortes et effets d'emploi |
| 05 | Fraudes et exclusions d'aides | 2–3 | Distinguer montants détectés, droits évités, recouvrement effectif et coûts de contrôle |
| 06 | Soutiens énergétiques interrompus | 8 | Interventions et contrats ; engagements, contentieux et prix de marché |
| 07 | Dispositifs de politique urbaine arrêtés | 8 | Définir l'ensemble interministériel/local ; aides associatives et missions reprises |
| 08 | Anah fermée | 6 | Intervention majoritaire ; fermeture et suppression des aides sont deux décisions différentes |
| 09 | Ademe fermée | 3,4 | Périmètre hors 06 annoncé ; réconciliation par fonds, contrats et missions |
| 10 | Activité de placement de France Travail retirée | 4 | Organisme, placement, assurance et accompagnement ; coûts publics/privés et résultat d'emploi |
| 11 | ARS supprimées | 1 | Personnels et missions à reprendre ; le statut de l'organisme ne détermine pas le coût évitable |
| 12 | Autres organismes supprimés | 1 | Liste et coûts incomplets ; certaines références institutionnelles déjà modifiées |
| 13 | CESE et conseils régionaux correspondants | 0,066 | Financements État/régions, agents, indemnités et transition à consolider |
| 14 | Aide au développement et AFD arrêtées | 14 | APD statistique, dons, prêts, remboursements et charges de l'organisme distincts |
| 15 | Contribution européenne réduite | 14 | Année de référence, obligations et renégociation ; articulation avec l'APD multilatérale |
| 16 | Frais d'études pour étudiants étrangers | 4 | Recette de tarification ; situation initiale, exemptions, volumes et coût marginal |
| 17 | AME supprimée | 1,3 | Dépense du dispositif et coût net de soins reportés vers d'autres financeurs |
| 18 | Visas plus chers | 0,7 | Recette ; volumes, tarifs, exemptions, réaction de la demande et frais consulaires |
| 19 | Hébergement d'urgence restreint | 0,7 | Dépenses marginales, missions alternatives et cadre juridique à examiner |
| 20 | Aide juridictionnelle restreinte | 0,1 | Dossiers concernés, exceptions, accès à la justice et modifications du droit |
| 21 | Audiovisuel privatisé | 4 + actifs | Économie récurrente distincte du produit de cession ; passifs et obligations maintenues |
| 22 | Aides associatives réduites | 1–2 | Critère de sélection absent ; service délégué, bénéficiaires et autres mesures |
| 23 | Soutiens à la presse arrêtés | 0,2 | Aides directes, dispositifs fiscaux et bénéficiaires déjà visés par 22 |
| 24 | Financements syndicaux arrêtés | 0,1 | Subventions, fonds paritaires et décharges de personnel distincts |

Source de chaque annonce : [budget2027.fr][site], `li.mesure` numéro 1–24, lecture du 28 octobre 2026. Les conditions juridiques indiquées sont des **points à instruire**, pas un avis juridique définitif validant ou interdisant les réformes. Aucun total d'économies «certaines» n'est fabriqué à partir des cases manquantes.

## 3. Effectifs : passer du slogan au calcul contrôlable

### 3.1 Définir le vivier avant de compter les départs

Le mot administratif peut désigner une profession, une filière, une institution ou une tâche. Les lots 01–04 ont montré que ces axes ne se recouvrent pas : assistance judiciaire, vie scolaire et fonctions d'un payeur de santé ne deviennent pas des supports inutiles par leur nom. Le plan doit donc fournir des **viviers disjoints par métier et activité**, avec un passage personnes physiques/ETP et une affiliation institutionnelle FP/APU explicite.

Les 2,3 millions de départs ne sont accompagnés sur le site ni d'une série, ni d'une définition, ni d'une projection par vivier. La somme historique de sorties civiles du lot 01b est proche numériquement mais comprend des occurrences et motifs qui ne constituent pas tous des sorties définitives de l'administration. Elle ne démontre pas l'origine du chiffre politique. On ne peut lui affecter une part administrative fixe de 34,78 % pour créer une disponibilité de 800 000 postes.

Les volumes évoqués de «métiers essentiels» ou de «professionnels de terrain» exigent eux aussi une déclaration primaire précise et une règle de partition. La reconstruction indépendante du lot 02 ne valide pas un chiffre politique par proximité. Le texte intégral du livre et l'origine des formulations exactes restent à examiner ; rien ne permet de présenter les personnels omis d'une liste comme un reliquat intégralement supprimable.

### 3.2 Coût implicite et coût évité

L'identité `40 Md€ / 800 000 = 50 000 €` est arithmétiquement exacte. Elle ne prouve pas que 50 000 € soit le coût d'un recrutement administratif évité. Le coût moyen d'un agent en place et le coût du partant peuvent être plus élevés que celui d'un nouvel entrant. Le montant dépend du métier, de la catégorie, du statut, de la quotité, des primes, des charges, des pensions et de la trajectoire de carrière.

Il faut publier séparément le budget employeur complet, une normalisation hors financements de retraite et l'effet consolidé APU. Une cotisation qui cesse peut diminuer la dépense de l'employeur et les recettes d'un régime public simultanément. Les pensions déjà liquidées restent dues. Les coûts PAP 156/218 documentés au lot 01c ne constituent pas une moyenne nationale, et «hors CAS» ne signifie pas automatiquement hors toutes pensions.

La formule annuelle contrôlable doit donc traiter les **postes effectivement non pourvus pendant l'année**, leur coût d'entrée contrefactuel, le GVT correspondant et les coûts récurrents de remplacement ou de service commun. Redéployer conserve un emploi ; externaliser conserve une dépense à déduire ; transférer entre APU demande une consolidation.

### 3.3 Le calendrier modifie le cumul

L'illustration du CSV `10_calendrier_800000_illustration.csv` suppose 800 000 recrutements évités sur cinq ans, également répartis. Elle valorise volontairement ces postes à50 000 €, pour isoler le seul effet de calendrier. L'intervalle 100–120 Md€ de cumuls qui en découle n'est **ni une estimation nationale ni un intervalle de confiance**. Il manque la validation des départs, du vivier, du coût et des transitions ; le GVT et les effets macroéconomiques ne sont pas calculés ici.

Cette illustration suffit à montrer qu'un objectif annuel en régime permanent ne doit pas être multiplié mécaniquement par cinq. La première année peut être partielle ; une réduction entrée en vigueur en fin d'année ne produit pas douze mois d'économie. Le modèle du projet possède déjà ces mécanismes, mais aucun paramètre national nouveau n'y est introduit par ce contre-calcul.

![Illustration du calendrier des recrutements évités, sans calibration nationale](../figures/10_calendrier_illustratif.png)

## 4. IA : temps, effectifs et additionnalité

La source précise des 5 Md€ n'est pas identifiée avec certitude dans le site. L'existence de numéros de mission 2025 dans le rapport daté 2026 est une piste, pas une preuve que l'auteur visait ce document. Les recherches et la lecture primaire sont détaillées au [volet08](08_ia_france.md).

Le raisonnement doit séparer la part d'activités exposées, les tâches effectivement outillées, le taux d'usage, le temps gagné net des reprises et contrôles, la qualité obtenue, le redéploiement et les postes entiers qu'on peut réellement ne pas pourvoir. Le rapport français présente plusieurs équivalents de temps qui n'ont pas entraîné de diminution d'effectif ; les études internationales n'autorisent pas davantage un taux national uniforme. Voir les [preuves09](09_ia_preuves_internationales.md).

Si l'IA contribue à réaliser le non-remplacement de 800 000 postes, ses mêmes heures ne donnent pas automatiquement 5 Md€ supplémentaires. Si elle porte sur d'autres tâches ou produit des économies d'achat, il faut montrer ce champ distinct et ses coûts. La matrice enregistre ce risque, **sans considérer le double compte comme démontré en l'absence de ventilation**.

## 5. Agences, prestations et recettes

### 5.1 Une institution fermée ne supprime pas automatiquement ses dépenses

Les fiches Ademe, Anah et France Travail du jaune 2027 sont particulièrement utiles parce qu'elles présentent les comptes de résultat de leurs **budgets initiaux 2026**, en milliers d'euros. Les lignes de personnel, fonctionnement, interventions et produits sont distinctes ; les autorisations et paiements budgétaires forment un autre tableau et ne s'ajoutent pas au compte de résultat.

À l'Anah, les 3,451 Md€ d'interventions constituent l'essentiel des 3,652 Md€ de charges du budget initial. Fermer l'organisme tout en maintenant ses aides transfère l'instruction et le paiement ; arrêter les aides modifie une politique publique. Ces deux décisions ont des effets différents sur bénéficiaires, contrats, travaux, recettes et financement. Aucun des deux effets nets ne se déduit d'une multiplication des 25 M€ de personnel par un taux de support arbitraire.

À l'Ademe, les 1,323 Md€ d'interventions ne sont pas des frais de siège. La ligne du site exclut explicitement les renouvelables déjà comptées ailleurs : cette intention de déduplication est reconnue, mais il manque un tableau par fonds et année qui réconcilie 3,4 Md€ avec les budgets et engagements concernés. Une différence avec le budget initial 2026 ne réfute pas à elle seule tout champ plus large ; elle réclame une explication de ce champ.

France Travail combine fonctions de service, accompagnement, droits, prestations, partenariats et achats. Les 4 Md€ du site ne peuvent être affectés par simple proximité à ses 3,887 Md€ de personnel. Le périmètre et les dates du LMP placement, du budget de l'organisme et de ses moyens humains sont différents. La suppression d'une mission doit préciser ce que deviennent l'accès au service, l'orientation, les prestataires, les allocataires et les personnels.

Les ARS et autres agences demandent le même examen. L'existence d'une mission de régulation ou de contrôle ne prouve pas son organisation optimale ; sa suppression juridique ne prouve pas non plus que les obligations cessent. Enfin, un changement déjà réalisé, comme la reprise des missions de l'Observatoire de la laïcité en 2021, ne peut être reconstitué comme une économie entièrement nouvelle.

### 5.2 Nature des autres annonces

L'audit ne considère pas les lignes de prestations comme des «administratifs». Elles demandent des populations et droits précis, des comportements, une transition et des effets distributifs. Une même personne peut être touchée par plusieurs règles : la seconde économie se calcule sur les droits restant servis après la première, pas sur la base initiale inchangée.

Les tarifs de visa ou d'études produisent des recettes conditionnelles, avec exemptions, volumes et effets de demande. Une suppression de subvention peut nécessiter de racheter un service jusque-là délégué. Un produit de cession ne se répète pas chaque année. L'APD statistique incorpore des instruments et conventions distincts des dépenses propres de l'AFD ; les prêts, remboursements, garanties et dons ne sont pas tous des décaissements budgétaires annulables de même montant. Ces différences imposent une réconciliation, sans autoriser un total alternatif inventé.

## 6. Comparer les plans sur la même référence

Le plan Bayrou de juillet 2025 était une annonce pour 2026 ; la loi 2026 adoptée a suivi une autre séquence. Le projet gouvernemental 2027 étudié est encore un **projet**, publié en octobre 2026. Les 54 Md€ sont un effort de redressement par rapport à une référence, avec des mesures nouvelles et des effets déjà engagés ; ils ne sont pas 54 Md€ de baisse nominale de masse salariale. Des dépenses prioritaires continuent d'augmenter.

Le tableau d'emplois 2027 montre pourquoi «aucun poste supprimé» et «l'emploi total augmente» ne sont pas équivalents. Les hausses dans certaines missions coexistent avec des baisses dans d'autres. Le sous-total+6 816 ETP comprend notamment la formation initiale des enseignants et la marche LPM ; le total retraité avec caisses sociales est−1 076. Les−812 de centrale et+404 numériques sont des sous-ensembles déjà compris, et les plafonds 2 032 750/397 282 ETPT ne sont pas des flux de recrutement. Ces propositions ne démontrent aucun résultat d'exécution 2027.

Les promesses historiques Fillon/Macron peuvent éclairer ambition, calendrier et difficultés de mise en œuvre. Le chiffrage Montaigne 2017 de 3,17 Md€ pour 120 000 postes est une estimation de son auteur, rappelée dans son bilan 2021. Ni sa division par 120 000 ni le quotient politique actuel de 50 000 € ne créent une norme de coût marginal comparable : champs, années et retraites diffèrent, et la méthode historique détaillée n'a pas été retrouvée sur le lien cible qui reçoit aujourd'hui un autre article.

Les travaux Cour/RGPP/MAP/DGFiP sont traités au [volet06](06_doublons_structures.md). Les revues Fipeco, IFRAP, OFCE, CAE, IPP, Terra Nova, Fondation Jean-Jaurès et CAP 22 doivent être complétées par des lectures datées avant qu'une synthèse comparative exhaustive puisse être annoncée. Une position de think tank ne remplace pas les comptes et évaluations primaires ; l'IFRAP est notamment identifiée comme source de position dans le [volet08](08_ia_france.md).

## 7. Limites et reproduction

- **Livre.** La fiche Fayard et son JSON-LD ont été lus enUTF 8 dans l'HTML original. Le lien de feuilletage renvoie à une coquille de lecteur ; l'ouverture connectée a échoué et aucun extrait textuel du livre n'a été lu. Le texte intégral, le détail des populations protégées et la concordance livre/site demeurent non vérifiés.
- **Sources bloquées.** Matignon et Légifrance ont renvoyé 403 ; l'accueil HCFP a expiré. Les longs textes obtenus dans les résultats de recherche sont conservés comme **[EXTRAIT]**, sans promotion en lecture primaire. Le conteneur de recherche et les tentatives directes sont séparés. Les appréciations HCFP ne deviennent pas ici des paramètres calibrés.
- **Années.** La page politique ne fixe pas clairement son exercice ; le jaunePLF 2027 présente notamment des budgets initiaux 2026 ; LMP 2023 est une classification internationale, pas un budget 2026 de France Travail. Les différences de montant ne sont pas expliquées causalement sans pont documentaire.
- **Chiffrage net.** Aucune ligne ne fournit ici un coût national complet de transition ni une économie APU consolidée validée. Les cases correspondantes sont vides, jamais mises à zéro. Les intersections sont des hypothèses à examiner, sans déduction arbitraire de montants.
- **Lecture et contrôles.** Les PDF volumineux restent au cache. Les transcriptions manuelles sont signalées et leurs ancres/SHA vérifiés. Le tableau d'emplois est une double page 58–59 dont la conversion texte répète des colonnes hors zone visible ; il a été relu visuellement pour éviter un double comptage.

```powershell
python -I scripts/10_audit_propositions.py
```

Le script reconstruit les 24 annonces numériques depuis l'HTML archivé sans perte, les six totaux, dix lignes de calendrier illustratif, treize intersections et 27 indicateurs primaires. Les douze observations d'opérateurs relisent directement les pages du jaune, sans appeler l'extracteur du volet 06. Les registres de sources et manifestes donnent les URL, dates, empreintes et lectures ciblées. Cette exécution vérifie une transcription et des identités ; elle ne valide pas les économies annoncées.

[site]: https://www.budget2027.fr/
[fayard]: https://www.fayard.fr/livre/le-casse-du-siecle-9782213733135/
[igas]: https://igas.gouv.fr/sites/igas/files/2026-07/Rapport%20D%C3%A9ploiement%20IA%20(2026).pdf
[operateurs]: https://www.budget.gouv.fr/documentation/file-download/34432
[laicite]: https://www.laicite.gouv.fr/nous-connaitre
[lfi]: https://www.senat.fr/dossier-legislatif/pjlf2026.html
[bayrou]: https://www.info.gouv.fr/conseil-des-ministres/compte-rendu-du-conseil-des-ministres-du-16-07-2025
[plf]: https://presse.economie.gouv.fr/download?n=1076%20-%20DP%20-%20Budget%202027-pdf&id=184723
[montaigne]: https://www.institutmontaigne.org/ressources/pdfs/publications/quinquennat-macron-le-gd-decryptage-action-fonction-publique.pdf
[montaigne2017]: https://www.institutmontaigne.org/presidentielle-2017/themes/administration-et-institutions/
