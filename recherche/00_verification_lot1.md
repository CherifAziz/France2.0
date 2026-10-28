# Contre-vérification indépendante du premier lot statistique

Date : **28 octobre 2026**. Périmètre : notes **01, 01b, 02 et 03** et leurs
principales extractions. Le vérificateur n'a pas rédigé ces quatre notes ; ses
travaux antérieurs portent sur le moteur et le volet 01c, exclus de cet échantillon.

**Résultat : 100 vérifications numériques, 98 confirmées et deux corrections de
statut de preuve réalisées. Aucun écart numérique résiduel dans l'échantillon.**
Les deux sommes concernées étaient arithmétiquement correctes ; leur étiquette
« fait publié » était trop forte. Cette conclusion ne valide pas des économies
nationales ni des suppressions de postes à service comparable.

## 1. Échantillon et méthode

La demande minimale de quarante chiffres est dépassée avec un échantillon de
cent affirmations :

- **42** sur les stocks, champs, statuts, employeurs, budgets, salaires et heures
  de la note 01 ;
- **29** sur les flux, mobilités, retraites, âges et calculs conditionnels de la
  note 01b ;
- **16** sur les filières, enseignants, salariés hospitaliers et la reconstruction
  de groupes à dominante opérationnelle de la note 02 ;
- **13** sur les effectifs et ratios OCDE actuels ainsi que trois cellules du
  StatLink du Panorama 2025 de la note 03.

Les valeurs ont été relues dans les **XLSX primaires**, avec leur feuille et leur
cellule, et dans les réponses **CSV SDMX brutes de l'OCDE**. Les colonnes d'unités,
années, champs et notes de lecture ont été examinées. Les CSV analytiques produits
par les auteurs ne servent pas de preuve de leur propre transcription. Aucun
script d'extraction des auteurs n'est importé pour recalculer les résultats.

Le contrôle réapplique les conversions de milliers de personnes en personnes et
les multiplicateurs `10^UNIT_MULT` de l'OCDE. Les calculs indépendants incluent
des différences, sommes, ratios, le stock décroissant sous taux constant et la
déduction de l'intersection enseignants/militaires. Les deux monnaies sont
rapprochées avant les calculs D1/PIB. La tolérance de chaque ligne correspond à
l'arrondi réellement affiché ; elle ne représente pas une marge d'erreur statistique.

Le registre `data/risques/verification_40_chiffres_lot1.csv` conserve pour chaque
affirmation son identifiant, valeur citée, valeur relue ou recalculée, unité,
année, champ, source, cellule ou sélection SDMX, empreinte de source, écart,
tolérance, statut initial/retenu, résultat et objection éventuelle.

## 2. Corrections réalisées après signalement

### Mouvements interversants : 31 942

**Constat.** La synthèse 01b n°5 étiquetait initialement ce total `[FAIT]`, alors
que le tableau le présentait déjà comme `[ESTIMATION]`. Le classeur primaire
`ra_2026_vue_flux_de_personnels_entrees_sorties.xlsx`, feuille `Encadré 1`, publie
séparément les composantes H11, H16 et H21, exprimées en milliers.

**Vérification.** Leur somme convertie donne bien 31 942 personnes. Il s'agit de
mobilités internes entre versants, pas de sorties nationales de la fonction publique.

**Correction.** Le responsable du lot a remplacé le statut de la synthèse par
`[ESTIMATION]` et explicité la somme. Ligne de contrôle : `FLUX_INTERVERSANTS`,
résultat `STATUT_CORRIGE`.

### Fonctionnaires civils ayant une nouvelle pension : 108 796

**Constat.** La synthèse 01b n°10 présentait ce nombre comme `[FAIT]`, tout en
précisant qu'il était calculé. Dans le classeur primaire
`ra_2026_vue_flux_de_personnels_retraites.xlsx`, feuille `Figure 1`, les cellules
E5/E10/E13 correspondent respectivement aux fonctionnaires civils SRE, FPT et FPH
CNRACL, mais cette figure ne publie pas leur somme comme total autonome.

**Vérification.** `39 146 + 46 897 + 22 753 = 108 796` est exact. L'unité est la
pension de droit direct attribuée en 2025, pas l'ETP devenu vacant.

**Correction.** Le responsable du lot a remplacé le statut par `[ESTIMATION]`
pour la somme, en conservant `[FAIT]` pour les trois composantes publiées. Ligne
de contrôle : `PENSIONS_FONCT_CIVILS`, résultat `STATUT_CORRIGE`.

Ces modifications ont été coordonnées ; le vérificateur n'a pas modifié les
notes des autres auteurs.

## 3. Constats substantiels confirmés

### Les différences de champs et de versions sont réelles

Les valeurs DGAFP de **5 848 291 personnes hors contrats aidés fin 2024** et
Insee IP2094 de **5 850 900 personnes sur le même champ nominal** sont toutes
deux présentes dans leurs fichiers primaires. Leur divergence n'est pas une
erreur de transcription du premier lot. Le registre conserve les deux versions.
Le rapprochement de leurs variations aboutit bien à l'écart résiduel calculé de
**1 236 personnes** ; sa cause ne se déduit pas de cette seule identité arithmétique.

Les **5 781 800 EQTP annuels** de l'IP2094 se rapportent à tout poste actif dans
l'année, selon A16 de la figure 1. Ils ne constituent pas le dénominateur d'une
différence avec les personnes présentes au 31 décembre.

Les **370,012 Md€ de D1 des APU en 2025**, les **156,241675 Md€ de titre 2 du
budget général** et les **49,219294 Md€ de la ligne CAS** ont été vérifiés dans
leurs cellules originales et unités. L'écart de champ est correctement indiqué
dans la note 01. La soustraction HCAS est un calcul, pas une ventilation de toutes
les pensions ni un coût marginal d'entrée.

### Les limites des sorties et pensions ne doivent pas être effacées

Le total de **2 339 789 occurrences annuelles de sortie sur 2020-2024** est
arithmétiquement confirmé. Il n'identifie ni autant de personnes uniques ni
autant de postes administratifs pérennes. Les postes commencés et finis pendant
l'année restent une autre unité que les personnes comparées entre deux fins d'année.

L'écart de **65 postes courts contractuels** entre deux figures DGAFP est lui
aussi présent dans le primaire : **307 069** dans `Fig. 4!C10` et **307 134** dans
`Fig. 5!K6`. Ce contrôle confirme l'anomalie documentaire signalée par la note ;
il ne la résout pas et ne justifie aucune correction arbitraire des sorties.

Le test sans aucun recrutement et à taux constant donne bien environ
**2 018 805 sorties civiles sur cinq ans**, en partant du stock 2024 supposé
inchangé jusqu'au début du test. La formule est correcte, mais les hypothèses
n'en font pas une prévision 2027-2031 ni un scénario de qualité comparable.

### La reconstruction de 2,4 millions est un panier de groupes

Le panier de la note 02 atteint bien **2 400 090 personnes**, après lecture
des cellules de chaque composante et déduction des **19 enseignants militaires**.
La sélection de quatre groupes policiers donne **116 786** et la différence
entre total FPH et personnels non médicaux donne **144 604 médecins et internes**,
selon la nomenclature SIASP utilisée. Les sommes et l'intersection sont exactes.

Ce résultat ne valide pas une mesure individuelle des tâches de terrain. Les
corps et filières incluent de la gestion et du soutien, et d'autres métiers
opérationnels restent hors du panier. La note conserve cette limite et ne
calcule pas un reliquat d'agents inutiles.

Les chiffres DEPP ont été vérifiés au **30 novembre 2025** ; le champ comprend
Mayotte pour le public et l'exclut pour le privé, conformément à la cellule A46.
Les chiffres de salariés hospitaliers DREES se rapportent au **31 décembre 2024**,
avec contrats aidés et un champ distinct de la FPH complète. Ces séries ne doivent
pas être additionnées sans harmonisation aux stocks SIASP.

### Les deux millésimes OCDE ne sont pas interchangeables

L'API OCDE actuelle fournit pour la France en 2023 les effectifs convertis
**6 336 000 S13**, **30 376 000 emplois intérieurs** et **68 553 000 habitants**.
Les ratios recalculés reproduisent **20,859 %** et **92,425 pour mille** aux
arrondis annoncés. Les comparaisons Allemagne/Italie/Espagne et D1/PIB vérifiées
concordent avec les réponses brutes.

Le StatLink du Panorama 2025 contient bien **20,740 %** pour la France, et non
le ratio de la collecte actuelle. Il contient également **14,560 % pour les
États-Unis** et **4,938 % pour le Japon** aux arrondis cités. La note japonaise
excluant les fonds de sécurité sociale a été relue en A26, et les années réelles
dérogatoires du tableau figurent en A25. Le premier lot distingue correctement
les millésimes et n'interprète pas leur écart comme une évolution entre deux années.

## 4. Objections qui restent ouvertes après ce contrôle

1. **Transcription exacte ne signifie pas comparabilité complète.** Les unités,
   champs, dates et conventions territoriales doivent encore être harmonisés
   pour passer du fichier statistique au diagnostic par fonction.
2. **Un statut de corps n'est pas une part de temps administratif.** Les classes
   fonctionnelles dominantes de la note 02 restent des hypothèses séparées des
   effectifs observés. Le classement D ne peut pas être obtenu par différence.
3. **Des sorties observées ne sont pas des vacances supprimables.** Motifs,
   quotités, retours, compétences et obligations de service restent nécessaires
   pour alimenter les viviers et les hypothèses du modèle.
4. **Les écarts internationaux restent bruts.** Les résultats de service,
   besoins, délégations au privé, temps de travail et responsabilités doivent
   être intégrés avant toute conclusion de sureffectif.
5. **Aucune économie nationale n'est validée ici.** Les coûts d'entrée, pensions,
   recettes perdues, dépenses de transition et gains réellement convertibles
   nécessitent leurs propres preuves et contre-expertises.

## 5. Portée de l'indépendance et reproduction

Il s'agit d'une **contre-vérification de transcription, de champ et de calcul par
un autre agent**, et non d'une seconde observation statistique indépendante.
DGAFP et Insee exploitent notamment SIASP ; les deux diffuseurs OCDE/Eurostat
peuvent reprendre les mêmes comptes nationaux ; les régimes de retraite
alimentent aussi les publications de synthèse. L'accord de plusieurs tableaux
ne permet donc pas d'affirmer que leurs erreurs statistiques sont indépendantes.

La sélection est explicite, ciblée sur les chiffres structurants et non aléatoire.
L'absence d'écart dans cent vérifications ne garantit pas l'absence d'erreur dans
chaque cellule des bases complètes. Les coûts 01c, les réformes futures et les
résultats nationaux du modèle n'ont pas été validés indépendamment par ce lot.
Le document ne clôt pas la phase de contre-expertise du rapport final.

```powershell
python -I scripts/00_verification_lot1.py
```

Résultat de l'exécution du 28 octobre 2026 :
`100 vérifications ; CONFIRME=98 ; STATUT_CORRIGE=2 ; ECART_A_CORRIGER=0`.

Les URL exactes et empreintes de tous les fichiers primaires utilisés sont
dans le CSV. Les lectures et calculs se reproduisent hors réseau à partir des
instantanés du dépôt. Aucun fichier primaire ni note d'un autre auteur n'a été
modifié par ce script.
