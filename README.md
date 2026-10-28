# La France est-elle suradministrée

Mission d'audit documentaire et de modélisation reprise le **28 octobre 2026** à partir de `PROMPT_CODEX.md`. La priorité est de distinguer effectifs publics, fonctions administratives et économies effectivement réalisables à service comparable.

Le dépôt contient désormais des extractions vérifiées et un moteur testé. **Il ne contient pas encore le rapport final ni un chiffrage national calibré.** L'état précis des chantiers et la prochaine action sont consignés dans [SUIVI_MISSION.md](SUIVI_MISSION.md).

## Lire les premiers résultats

Le [dossier de recherche consultable](livrables/dossier_recherche_lot1.html) assemble les notes, tableaux et graphiques, avec les liens vers les données et sources.

- [Stocks, champs, dépenses et rapprochement Insee/DGAFP](recherche/01_emploi_public_france.md).
- [Sorties, retraites, tests des départs sur cinq ans](recherche/01b_flux_retraites.md).
- [Coûts d'entrée documentés et périmètre des pensions](recherche/01c_couts_entree_pensions.md).
- [Métiers, filières et limites des chiffres de terrain](recherche/02_metiers_classification.md).
- [Première base internationale harmonisée](recherche/03_comparaison_harmonisee.md).
- [Contrôle préparatoire des quinze fichiers internationaux hérités](recherche/04_controle_preliminaire.md).
- [Audit du moteur financier](recherche/00_audit_modele.md) et [conventions de calcul](modele/README.md).
- [Protocole de preuve](recherche/00_PROTOCOLE.md) et [précisions méthodologiques de la reprise](recherche/00_AVENANT_METHODOLOGIQUE.md).
- [Contre-vérification de 100 chiffres](recherche/00_verification_lot1.md).

Chaque CSV d'indicateurs conserve l'année, le champ, l'unité, l'URL et la localisation dans la source. Les PDF lourds et pages de recherche sont conservés dans `data/cache/`, ignoré par Git ; leurs URL et empreintes restent dans les registres de `sources/`. Les petites pages de métadonnées officielles utilisées dans le contrôle international sont versionnées avec les autres bruts.

Les règles `.gitattributes` conservent les octets des sources brutes et leurs empreintes. Ne pas nettoyer leurs espaces ou changer leurs fins de ligne pour satisfaire un contrôle de style : ces archives servent de preuves.

## Reproduire les extractions

Python 3.12 a été utilisé. Les dépendances nécessaires sont dans `requirements-recherche.txt`. Pour une installation isolée :

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements-recherche.txt
```

Puis, avec ce Python ou celui disposant des dépendances :

```powershell
python -I scripts/01_cartographie.py
python -I scripts/01b_flux_retraites.py
python -I scripts/01_provenance.py
python -I scripts/01_figures.py
python -I scripts/02_metiers.py
python -I scripts/03_collecte_harmonisee.py
python -I scripts/04_audit_raw.py
python -I scripts/00_verification_lot1.py
python -I scripts/build_dossier_recherche.py
python -m unittest discover -s tests -v
```

`01_cartographie.py` et `01b_flux_retraites.py` relisent les bruts fournis et ne nécessitent pas Internet. `01_provenance.py` relit les archives primaires présentes dans le cache ; les requêtes permettant de les restaurer figurent dans `sources/01_manifest_telechargements.json`. Exemple :

```powershell
python scripts/fetch.py 'https://www.insee.fr/fr/statistiques/fichier/8732435/IP2094.xlsx' insee_ip2094_verification --out-dir data/cache/01
```

Le volet 01c et les deux lignes DGFiP du volet 02 utilisent des documents lourds ignorés par Git. Sur un clone neuf, exécuter `python -I scripts/01c_extrait_couts.py --fetch` et `python -I scripts/02_metiers.py --download` avant la vérification complète. L'absence du PDF DGFiP est signalée dans les contrôles et ne donne pas un zéro d'effectif. Les autres sources des chantiers 02/03/04 sont conservées dans les dossiers bruts correspondants.

Les paramètres nationaux du modèle seront construits après les réformes documentées. Les tests utilisent exclusivement des cas synthétiques calculables à la main. Le script historique `scripts/build_rapport.py` reste réservé à l'assemblage des futurs chapitres `rapport/NN_*.md` ; il nécessite Pandoc et, pour sa sortie PDF, Playwright/Chromium.
