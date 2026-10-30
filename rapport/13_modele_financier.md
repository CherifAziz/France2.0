# 13. Modèle financier à 5 et 10 ans

Moteur : `modele/modele.py` (24 tests unitaires) ; classeur modifiable : `modele/modele_financier.xlsx` ; hypothèses : `modele/hypotheses.json`.

## 13.1 Principes de calcul

- **Référence.** Les économies sont des écarts à une trajectoire qui remplace tous les départs, en euros 2026 constants. Elles ne prouvent pas une baisse des dépenses par rapport au niveau actuel.
- **Rythme.** Chaque année, le non-remplacement ne peut dépasser les départs à la retraite du vivier, calculés sur le stock restant. Une cible non réalisable est reportée, puis signalée.
- **Valorisation.** Un poste non remplacé économise le **coût d'entrée hors pension**, qui croît de 1 % par an jusqu'au coût moyen. Convention de mi-année : la première année compte pour moitié.
- **Coûts.** Investissements selon une convention de deux années d'économie brute (trois pour les projets à risque), coûts récurrents des outils d'IA, rétrocession de 50 % pour la règle de non-remplacement partiel (R12), proportionnelle aux postes réellement supprimés.
- **Deux lectures.** Économie pour l'employeur, et économie consolidée des administrations publiques, qui conserve 65 % de la masse salariale évitée : cotisations, CSG et retenues reviennent aux APU.

## 13.2 Hypothèses nationales

| Paramètre | Valeur | Source |
|---|---|---|
| Coût d'entrée / moyen hors pension, État | 44,05 / 48,99 k€ | PAP 2026, programmes 156 et 218, pondérés A/B/C |
| idem, DGFiP | 40,55 / 45,41 k€ | PAP 2026, programme 156 |
| idem, territoriale et hospitalière | 33,67 / 37,45 k€ | Proxy : coût État × 0,7645 (rapport des salaires bruts) |
| idem, organismes de droit privé | 44,05 / 48,99 k€ | Proxy État, faute de donnée |
| Départs mobilisables | 2,61 % (État), 3,31 % (FPT), 2,75 % (FPH) | Pensions 2025 / fonctionnaires fin 2024 |
| GVT individuel réel | 1 % par an | Hypothèse, testée de 0 à 2 % |
| Conservation APU | 0,65 | Estimation à partir des charges hors pension (17,6 % du coût d'entrée) et des prélèvements sur salaire |

## 13.3 Résultats à 5 et 10 ans

| M€ 2026 constants | Prudent | Intermédiaire | Ambitieux | Radical |
|---|---:|---:|---:|---:|
| Économie brute en 2031 | 398 | 1 712 | 3 280 | 4 697 |
| Économie nette en 2031 | 498 | 1 805 | 3 372 | 3 927 |
| **Économie nette annuelle en 2036** | **618** | **2 517** | **5 280** | **8 430** |
| Économie consolidée APU en 2036 | 458 | 1 710 | 3 539 | 5 726 |
| Cumul net 2027-2031 | 448 | 533 | 1 162 | −1 564 |
| **Cumul net 2027-2036** | **3 464** | **12 627** | **25 701** | **35 448** |
| Cumul consolidé APU 2027-2036 | 2 385 | 7 403 | 15 179 | 20 012 |
| Investissements 2027-2036 | 857 | 3 953 | 7 202 | 13 505 |

**Lecture.** Les économies montent lentement : elles suivent les départs à la retraite et les investissements les précèdent, si bien que le cumul sur cinq ans est faible, voire négatif dans le scénario radical. L'économie nette de 2031 inclut 100 M€ de recettes (réduction des indus, fiche R23), qui ne sont pas une baisse de dépense. En lecture consolidée, l'économie est environ un tiers plus faible.

## 13.4 Effets non chiffrés

- **Pensions futures.** Moins de recrutements signifie moins de droits futurs, mais l'effet n'apparaît qu'au-delà de 25 ans ; il est hors horizon.
- **Sous-traitance.** Aucune fiche ne transfère d'activité au privé ; le risque de substitution par des prestataires est traité comme un risque (chapitre 14), non comme une économie.
- **Recettes.** Seule la réduction des indus (100 M€/an) est chiffrée ; l'effet d'un meilleur ciblage du contrôle fiscal ne l'est pas.

## 13.5 Le classeur modifiable

Le classeur `modele/modele_financier.xlsx` reprend les 30 réformes en formules, avec les hypothèses en cellules jaunes et quatre multiplicateurs de sensibilité (taux, départs, coûts, investissements). Il calcule un régime permanent : recalculé, il reproduit exactement les postes du moteur dans trois scénarios (1,3 % d'écart en radical) et l'économie nette à 0,7-2,4 % près. Le moteur annuel reste la référence.
