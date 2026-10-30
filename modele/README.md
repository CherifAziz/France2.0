# Moteur financier : conventions et utilisation

Le moteur est un calculateur de scénarios, **pas une estimation nationale calibrée**.
Les fichiers `hypotheses.json`, `registre_viviers.csv` et `catalogue_reformes.csv`
doivent résulter des chantiers documentaires. Aucun montant de test ne doit les alimenter.

```powershell
python -m unittest discover -s tests -p test_modele.py -v
python modele/modele.py --hyp modele/hypotheses.json --out modele/resultats
```

Les chemins des deux CSV sont ceux de `hypotheses.json`, relatifs à la racine du
projet ou absolus. Les entrées numériques obligatoires manquantes provoquent une
erreur ; elles ne sont pas remplacées par zéro. Les quatre scénarios sont validés
avant toute écriture. Une absence de réforme produit des fichiers avec en-têtes
et des résultats nuls, sans prétendre établir le potentiel national.

## Unités et trajectoire de référence

Les effectifs sont des ETP continus. Les coûts individuels sont en **k€ par ETP
et par an**, les investissements, coûts récurrents, recettes et résultats en **M€**.
Le passage k€ vers M€ est une division par 1 000. Tous les montants doivent être
exprimés dans les mêmes euros constants, à préciser dans les hypothèses nationales.
Le moteur n'intègre aucune inflation nominale.

Les économies sont des écarts à une référence conservant les postes et activités
visés, avec remplacement des départs. Elles ne prouvent pas une baisse des dépenses
totales par rapport à l'année actuelle. Cette baisse exige une trajectoire de
référence globale, les nouveaux besoins et les autres recrutements, non modélisés ici.

## Cibles et départs

Pour un vivier initial `B`, les réformes sont ordonnées par `ordre`, obligatoirement
distinct. Leurs cibles sont affectées successivement :

`cible_i = min(taux_i × (B − somme des cibles précédentes), plafond × B − somme des cibles précédentes)`.

Une cible encore non réalisée reste réservée à cette réforme. Elle ne peut pas
être recyclée dans une seconde cible sans modifier explicitement le catalogue.
Cette convention évite de compter deux fois un poste si une réforme manque de
départs. Les viviers eux-mêmes doivent être documentés comme disjoints : le moteur
ne peut détecter qu'une même personne figure dans deux sources statistiques.

La réalisation est simulée **année par année**. Pour chaque année :

1. Calcul du stock restant au début de l'année, après les mouvements réellement
   exécutés les années précédentes, y compris redéploiements et transferts hors vivier.
2. Enveloppe commune de départs = `taux_departs_annuel × stock restant`.
3. Allocation du non-remplacement à toutes les réformes selon leur priorité, dans
   cette seule enveloppe annuelle. Les demandes non satisfaites sont reportées.
4. Application des autres mouvements prévus cette année. Ces mouvements portent
   sur les fractions distinctes affectées lors du calcul des cibles.

Un objectif pour 2035 ne diminue donc pas le stock présent en 2027. Le taux annuel
doit représenter des départs effectivement mobilisables du vivier, pas un turnover
brut comprenant des mobilités internes ou des contrats automatiquement renouvelés.
Le caractère constant et homogène de ce taux est une hypothèse à tester.

Une réforme antérieure à `annee_debut` est refusée : il faudrait un état initial
des cohortes et des postes déjà retirés, absent du schéma actuel. Une réforme
postérieure à l'horizon ne produit aucune économie anticipée. Sa cible non exécutée
est indiquée dans `etp_cible_non_realisee`.

## Valorisation des mouvements

Le non-remplacement est valorisé au **coût d'entrée hors pension**. Chaque cohorte
évolue avec `gvt_individuel_reel`, plafonnée au coût moyen hors pension :

`coût_NR(n) = min(coût_moyen, coût_entrée × (1 + GVT_réel)^n)`.

Le GVT doit être positif ou nul dans cette version. Les suppressions indemnisées
et les transferts retirent des postes existants ; ils sont valorisés au coût moyen
hors pension. C'est une convention, à remplacer par un coût des postes réellement
visés si le catalogue le documente. Les indemnités sont un coût ponctuel :
`ETP supprimés dans l'année × indemnité_k€ / 1 000`.

Un coût récurrent suit par défaut le calendrier de déploiement. Avec `cout_recurrent_proportionnel = 1`, il suit la réduction effectivement réalisée, comme une rétrocession d'une part de l'économie aux agents restants : sans poste supprimé, pas de rétrocession.

Un redéploiement conserve la paie publique : il n'apporte aucune économie salariale
dans ce modèle. Une éventuelle embauche évitée ailleurs doit être démontrée et
introduite séparément sans double comptage.

`fraction_economie_premiere_annee` règle le temps écoulé entre le mouvement et la
fin d'année. La valeur 1 signifie une année pleine, 0,5 une demi-année. Cette
fraction affecte l'économie salariale des nouvelles cohortes, le coût de reprise
des nouveaux transferts et la montée des économies de fonctionnement associées.
Les années suivantes portent sur le stock entier. Par compatibilité, l'absence
du paramètre retient 1 et émet une alerte. **Une année pleine n'est pas un constat
empirique** : le calendrier national doit la justifier.

## Deux lectures financières et transferts

`eco_brute_meur` = paie évitée à l'origine + fonctionnement évité, avant coûts de
transformation. Les transferts sont affichés séparément, et non déduits du brut.

`eco_nette_meur` représente le budget **normalisé hors pensions** de l'employeur à l'origine, après la part des
coûts de reprise qu'il finance, investissements, indemnités, charges récurrentes
et effet signé des recettes. Les redéploiements sont conservés dans le périmètre
de cet employeur pour cette convention budgétaire.

Ce résultat n'est pas l'intégralité des décaissements évités dans le budget propre
de l'employeur à taux de cotisation fixés. Une contribution CNRACL évitée est une
économie locale et une perte de recette de la caisse ; ces deux écritures doivent
être suivies séparément pour le solde APU. Le CAS relève d'un autre mécanisme
institutionnel, interne à l'État. Enfin, les coûts **HCAS** des PAP ne sont pas
nécessairement hors toutes retraites (CNAV, Ircantec, RAFP) et ne doivent pas être
importés sans rapprochement. Voir `recherche/01c_couts_entree_pensions.md`.

`eco_consolidee_apu_meur` est une **approximation statique hors pension** : la paie
évitée est multipliée par `taux_conservation_consolide`, qui retranche les recettes
publiques perdues sur l'emploi initial. Le moteur ne calcule ni taux de prélèvements
individuels ni retour à l'emploi. L'hypothèse de conservation doit être sourcée et
soumise à sensibilité. Ce résultat n'est pas un compte national complet.

Dès que `part_transfert > 0`, le champ `type_transfert` doit valoir :

- `prive` : l'employeur finance la totalité du coût de reprise, calculé comme
  `ETP transférés × coût moyen d'origine × facteur_transfert_cout`. Le coût de la
  prestation est aussi déduit dans la lecture APU. Les éventuelles recettes nouvelles
  provenant des emplois privés ne sont pas supposées automatiquement ; elles
  peuvent être documentées dans `effet_recettes_meur_<scenario>`.
- `public` : il faut renseigner `etp_destination_par_etp_transfere`,
  `taux_conservation_transfert` et `part_cout_transfert_charge_source`. La première
  valeur détermine les recrutements publics nécessaires ailleurs. La deuxième
  convertit le coût de destination en coût consolidé. La troisième détermine la
  fraction de ce coût financée par l'employeur d'origine. Un transfert public à
  coût et effectifs identiques ne réduit ni les emplois ni le coût consolidé APU.

Le facteur de coût de transfert représente **le coût total de reprise par ETP
d'origine**, et non le salaire individuel à destination. Il inclut donc déjà le
ratio d'effectifs, les prestations et la productivité supposée. Le multiplier une
seconde fois par le ratio d'effectifs serait un double comptage.

`etp_postes_en_moins` et `postes_en_moins_5ans/10ans` concernent l'origine.
Utiliser les colonnes `etp_postes_apu_en_moins` / `postes_apu_en_moins_5ans/10ans`
pour le total public net après recrutements publics de destination. Les créations
privées ne sont pas estimées ; une réduction du nombre de postes publics par
externalisation ne démontre aucune économie économique à service identique.

Les pensions sont exclues des coûts individuels d'entrée et moyens. Aucune économie
sur les pensions déjà liquidées, aucun droit futur, aucune modification de taux
employeur et aucune compensation entre régimes ne sont calculés. Ce sont des
trajectoires distinctes, à chiffrer ailleurs avant toute conclusion nationale.

## Coûts, calendrier et cumuls

Les investissements commencent par défaut à l'année de mise en œuvre et s'étalent
sur `invest_duree_ans` (défaut : un an). Une date plus précoce se renseigne avec
`annee_invest_debut`. Les coûts antérieurs à l'horizon figurent dans
`invest_avant_horizon_meur`. Les cumuls ordinaires couvrent strictement l'horizon ;
les cumuls `incl_invest_avant` déduisent aussi ces coûts initiaux. Rien n'est effacé
parce qu'un déploiement commence en 2027.

Les charges récurrentes suivent la montée calendaire prévue, même si les départs
manquent. Quand une réforme cible des effectifs, ses économies de fonctionnement
et son effet de recettes suivent la fraction effectivement réalisée, pondérée par
la première année. Une ligne à taux nul peut représenter une réforme purement
financière ; elle suit le calendrier et exige quand même les quatre montants
explicites par scénario, y compris les zéros. Les coûts et recettes signés sont
conservés même en l'absence de réduction d'effectif.

Un horizon de moins de cinq ou dix ans laisse vides les cumuls correspondants.
Le résultat annuel final ne s'appelle plus « régime permanent » : un stock peut
encore évoluer, le GVT continuer et des investissements rester nécessaires.

## Contrôle synthétique calculable à la main

**[HYPOTHÈSE DE TEST, aucune portée nationale]** Vivier de 100 ETP, cible de 20 ETP,
départs mobilisables de 10 % par an, coût d'entrée de 40 k€, coût moyen de 50 k€,
GVT nul, année pleine, aucun autre mouvement ni coût. Les non-remplacements sont
10 en 2027, 9 en 2028 et 1 en 2029. Les économies annuelles sont 0,40 M€, 0,76 M€,
puis 0,80 M€. Le cumul 2027-2031 est 3,56 M€ et celui de 2027-2036 est 7,56 M€.
Ces égalités sont vérifiées dans `tests/test_modele.py`.

## Limites avant chiffrage national

La validité mathématique du moteur ne valide pas les viviers, taux de réduction,
coûts, calendriers, gains IA ou qualité du service. Les réactions macroéconomiques,
droits sociaux de transition, effets sur le chômage, capacités d'absorption du privé,
disponibilité des compétences, recrutements nouveaux hors transfert, interactions
fiscales détaillées et pensions demandent une analyse distincte. Le coût des autres
recrutements peut être saisi comme charge récurrente, mais leur nombre n'a pas encore
de colonne autonome hors transferts publics.
