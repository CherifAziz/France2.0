# Vérification indépendante du moteur financier

Date : 28 octobre 2026. Périmètre : code et calculs synthétiques uniquement.
**Statut : moteur vérifié sur cas analytiques, paramètres nationaux non calibrés.**

## 1. Résultats de la contre-vérification

**[FAIT — lecture du code initial]** L'ébauche traitait entièrement la première
réforme jusqu'en 2036 avant de passer à la deuxième. La capacité de départs de
2027 de cette deuxième réforme était calculée en retranchant des suppressions
futures déjà connues du programme. La variable `res_y` ne servait pas à corriger
cette anticipation. Le moteur simule maintenant les années successivement et
partage une enveloppe unique de départs par vivier et année.

**[FAIT — lecture du code initial]** Une cible insuffisamment réalisée rendait
disponible son reliquat à la réforme suivante. L'objectif reporté de la première
réforme et la cible de la seconde pouvaient alors viser les mêmes postes. Les
cibles sont maintenant attribuées au reliquat prévu, distinctes même en cas de
retard ; la réalisation effective détermine seule le stock de départs.

**[FAIT — lecture du code initial]** La contribution des transferts n'était pas
reprise dans `eco_consolidee_apu_meur`, et les postes transférés étaient tous
comptés en moins au total public. Le moteur impose la destination public/privé,
calcule les coûts de reprise dans les deux lectures et distingue les postes de
l'origine de la réduction nette APU après créations publiques à destination.

**[FAIT — lecture du code initial]** Les investissements commençaient implicitement
l'année précédant la réforme. Pour une réforme de 2027, une partie des coûts
disparaissait du cumul 2027-2036. Le défaut est remplacé par un début à la mise en
œuvre et une date explicite facultative. Les coûts antérieurs restent affichés
séparément, avec des cumuls incluant leur décaissement.

**[FAIT — lecture du code initial]** Les parts invalides étaient normalisées,
y compris une somme nulle qui provoquait une division par zéro. Elles sont
désormais refusées. Les taux hors [0 ; 1], durées non entières, montants manquants,
valeurs non finies, identifiants ou priorités dupliqués sont également refusés.

**[FAIT — lecture du code initial]** Une réforme sans taux de réduction et sans
économie de fonctionnement était ignorée, même avec investissement, coût
récurrent ou perte de recettes. Les lignes de coûts seules sont maintenant conservées.

**[FAIT — lecture du code initial]** Un scénario sans réforme ne disposait pas
d'un schéma annuel stable et un horizon court provoquait un accès à une cinquième
année inexistante. Les colonnes sont explicites, les scénarios vides s'exportent
et les cumuls à cinq/dix ans restent vides lorsque la durée est insuffisante.

**[CONVENTION]** Le coût d'entrée s'applique au non-remplacement. La suppression
indemnisée d'un poste existant utilise le coût moyen hors pension. Aucun paramètre
de coût national n'a été introduit. La fraction d'année et les limites de la
lecture consolidée sont détaillées dans `modele/README.md`.

## 2. Vérifications reproductibles

Commande : `python -m unittest discover -s tests -p test_modele.py -v`.

Résultat de l'exécution du 28 octobre 2026 : **23 tests réussis**.

Les tests couvrent les cumuls 5/10 ans calculés à la main, deux réformes d'un
même vivier, réforme future prioritaire, objectif non réalisable sans double
comptage, plafond, transfert privé, transfert public identique ou avec productivité,
redéploiement, indemnités, GVT plafonné, demi-année, investissement en 2027 et avant
horizon, calendrier au-delà de 2036, coûts seuls, recettes négatives, données
invalides, scénario vide, horizon court et export des quatre scénarios.

Un contrôle supplémentaire compare le stock restant avec la formule analytique
`B × (1 − taux_départs)^n` lorsque tous les départs sont non remplacés. Les cas
incluent un taux nul et un taux de 100 %, sur un, trois et dix ans.

**[ESTIMATION — calcul synthétique]** Pour 100 ETP, 20 postes ciblés, 10 % de départs,
40 k€ de coût d'entrée et GVT nul : 10, 9 puis 1 non-remplacements ; économies
0,40, 0,76 puis 0,80 M€ annuels ; cumuls 3,56 M€ sur cinq ans et 7,56 M€ sur dix ans.
Ces nombres sont des contrôles du programme, sans portée empirique nationale.

## 3. Limites et suites obligatoires

Cette vérification ne constitue ni une validation des données statistiques ni
une contre-expertise indépendante du montant national futur. Il reste à sourcer
les coûts d'entrée/sortie, départs mobilisables par vivier, conversion des gains
en postes et indicateurs de service. La disjonction de deux viviers portant des
identifiants différents exige une vérification documentaire ; le programme ne
possède pas les identités individuelles des agents.

Les effets de pensions, prélèvements individuels et retour à l'emploi ne sont
pas calculés. L'effet consolidé utilise des taux explicites et doit être présenté
comme une simulation statique hors pension. Les postes transférés au privé
n'établissent pas une économie de coût total ; les coûts des prestations restent
déduits. Le coût des autres recrutements peut être intégré en charge, mais leurs
effectifs hors transferts publics demandent une extension du schéma.

Le montant de la dernière année ne doit pas être décrit comme un régime permanent
tant que la réalisation, le GVT et les coûts n'ont pas cessé d'évoluer. Les cibles
non réalisées et coûts antérieurs à l'horizon doivent accompagner tout résultat.

## 4. Fichiers de preuve

- `modele/modele.py` : moteur corrigé, validation des données et exports.
- `tests/test_modele.py` : cas synthétiques analytiques et tests des exports.
- `modele/README.md` : définitions, formules, schéma des transferts et limites.

Le document initial de comparaison est accessible dans le commit `a6ce753` du
dépôt. Aucune source externe n'est nécessaire aux constats de code ci-dessus.
Les données nationales devront conserver leur propre registre de sources.
