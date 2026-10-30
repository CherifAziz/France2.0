"""Contre-vérification documentaire indépendante des volets06 et07.

Lecture directe des PDF et HTML primaires archivés ; aucun import, lecture ou
appel des scripts06/07. Les observations sont les mêmes sources statistiques,
pas une seconde observation indépendante de leurs phénomènes.
Écrit uniquement le CSV et la note de vérification demandés.
Usage : python -I scripts/00_verification_06_07_lot3.py
"""
from __future__ import annotations

import csv
import hashlib
import html
import json
import re
import sys
import unicodedata
from decimal import Decimal
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data/risques/verification_06_07_lot3.csv"
NOTE_PATH = ROOT / "recherche/00_verification_06_07_lot3.md"
COLS = ["id", "theme", "indicateur", "annee", "valeur_publiee", "valeur_source",
        "unite", "source_url", "source_localisation", "statut_controle", "note"]
SOURCE_PATHS = {
    "j26": "data/cache/06/operateurs_plf2026.pdf",
    "j27": "data/cache/06/operateurs_plf2027.pdf",
    "rgpp": "data/cache/06/rgpp_inspections2012.pdf",
    "rgpp_net": "data/raw/06/rgpp_net_an2012.html",
    "cnen": "data/raw/07/cnen_accueil.html",
    "cnen_rapport": "data/cache/07/cnen_rapport2023.html",
    "norme": "data/raw/07/norme_reponse2026.html",
    "loi": "data/raw/07/loi_simplification2026_senat.html",
    "dlnuf": "data/raw/07/dlnuf_reponse2019.html",
    "choc": "data/raw/07/choc_senat2017.html",
    "ue": "data/raw/07/ue_omnibus2026.html",
    "scm": "data/cache/07/ue_scm2025.pdf",
}


def normalized(text: str) -> str:
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", text)).strip().replace("’", "'")


def html_text(raw: bytes) -> str:
    # L'ancien HTML de l'AN déclare ISO-8859-1 ; les nouveaux sont UTF-8.
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        text = raw.decode("cp1252")
    text = re.sub(r"<(script|style)\b[^>]*>.*?</\1>", " ", text, flags=re.S | re.I)
    return normalized(html.unescape(re.sub(r"<[^>]*>", " ", text)))


def numeric_cells(page: str, label: str) -> list[int]:
    """Lit une ligne précise de tableau, sans fusionner ses colonnes."""
    matches = [line for line in page.splitlines()
               if normalized(line).startswith(label)]
    assert len(matches) == 1, (label, matches)
    # Les séparateurs de colonnes sont les espaces de mise en page ; les
    # espaces de milliers restent à l'intérieur d'une cellule.
    cells = re.split(r" {2,}", matches[0].strip())
    numbers = []
    for cell in cells:
        cell = re.sub(r"\s", "", cell)
        if re.fullmatch(r"-?\d+", cell):
            numbers.append(int(cell))
    assert numbers, (label, matches)
    return numbers


def main() -> None:
    metadata, primary, readers, pages = {}, {}, {}, {}
    for key, rel in SOURCE_PATHS.items():
        path = ROOT / rel
        raw = path.read_bytes()
        m = json.loads(path.with_suffix(".meta.json").read_text(encoding="utf-8"))
        actual_hash = hashlib.sha256(raw).hexdigest()
        if m.get("sha256"):
            assert actual_hash == m["sha256"], rel
        metadata[key] = {"path": rel, "url": m["source_url"], "sha256": actual_hash}
        primary[key] = raw
        if path.suffix == ".pdf":
            readers[key] = PdfReader(path)

    def pdf(key: str, number: int) -> str:
        if (key, number) not in pages:
            pages[key, number] = readers[key].pages[number - 1].extract_text(extraction_mode="layout")
        return pages[key, number]

    texts = {k: html_text(v) for k, v in primary.items() if k not in readers}
    rows = []

    def add(n: int, theme: str, indicator: str, year: str, claim: str, source: str,
            unit: str, keys: list[str], loc: str, note: str, status: str = "CONFIRME") -> None:
        trace = "; ".join(f"{metadata[k]['path']} SHA256:{metadata[k]['sha256'][:16]}" for k in keys)
        rows.append(dict(id=f"V0607-{n:02d}", theme=theme, indicateur=indicator, annee=year,
                         valeur_publiee=claim, valeur_source=source, unite=unit,
                         source_url=" ; ".join(metadata[k]["url"] for k in keys),
                         source_localisation=loc, statut_controle=status, note=note + " Trace : " + trace))

    # Opérateurs : populations, autorisations et consommations restent séparées.
    assert "431 opérateurs" in normalized(pdf("j26", 12))
    assert "423 opérateurs" in normalized(pdf("j27", 12))
    p15 = normalized(pdf("j27", 15))
    assert all(s in p15 for s in ["sortie de trois entités", "une entrée", "cinq Instituts", "polaire", "intercontemporain"])
    assert 431 - 3 + 1 - 4 - 1 - 1 == 423
    add(1, "06_operateurs", "Nombre d'opérateurs et recomposition du périmètre", "PLF2026/PLF2027",
        "431 puis423 ; contrôle431-3+1-4-1-1=423", "431 puis423 ; trois sorties, une entrée et trois regroupements",
        "organismes du périmètre proposé", ["j26", "j27"], "Jaunes2026 et2027 PDF p.12 ; jaune2027 p.15",
        "Le calcul de passage est une ESTIMATION de contrôle ; les effectifs de listes sont publiés. Une fusion ou une reprise de mission ne prouve pas une économie nette.")

    p26, p27 = pdf("j27", 26), pdf("j27", 27)
    old_ceiling = numeric_cells(p26, "Emplois sous plafond en LFI 2026")[0]
    new_ceiling = numeric_cells(p27, "Emplois sous plafond en PLF 2027")[0]
    assert (old_ceiling, new_ceiling) == (401389, 397282)
    add(2, "06_emplois", "Plafond légal et variation", "LFI2026/PLF2027",
        "401389→397282 ; baisse4107", f"{old_ceiling}→{new_ceiling} ; différence{old_ceiling-new_ceiling}",
        "ETPT autorisés", ["j27"], "PDF p.26-27, tableau d'évolution et texte",
        "Le comparateur est la LFI2026. Le jaune du PLF2026 p.12 proposait401310 : il ne faut pas substituer ce projet à la LFI. Pas des départs effectivement observés.")

    abattement = numeric_cells(p27, "Abattements techniques")[0]
    flow = numeric_cells(p27, "Schéma d'emplois 2027 en ETP")[0]
    impact = numeric_cells(p26, "Impact du schéma d'emplois 2027")[0]
    assert (abattement, flow, impact) == (-3248, -1209, -998)
    assert "vacance structurelle" in normalized(p27)
    proportion = Decimal(3248) / Decimal(4107) * 100
    add(3, "06_emplois", "Abattement technique, schéma et impact annuel", "PLF2027",
        "-3248 de vacance ; schéma-1209 ; impact-998 ; environ79% de la baisse du plafond",
        f"{abattement} ETPT de vacance ; {flow} ETP de schéma ; {impact} ETPT d'impact ; {proportion:.3f}% par calcul",
        "ETPT et ETP distincts", ["j27"], "PDF p.26-27, tableau et paragraphe sur la vacance",
        "79% est un calcul descriptif, pas un fait publié de suppression d'emplois. Les autorisations vacantes sont distinctes des sorties de personnes.")

    totals = numeric_cells(p27, "Total des emplois rémunérés par les opérateurs")
    outside = numeric_cells(p27, "Emplois rémunérés par l'opérateur hors plafond")
    assert totals == [482010, 481336] and outside == [80621, 84054]
    assert old_ceiling + outside[0] == totals[0] and new_ceiling + outside[1] == totals[1]
    add(4, "06_emplois", "Total rémunéré et hors plafond", "LFI2026/PLF2027",
        "482010→481336 ; hors plafond80621→84054 ; baisse totale674",
        f"{totals[0]}→{totals[1]} ; hors plafond{outside[0]}→{outside[1]}", "ETPT prévisionnels", ["j27"],
        "PDF p.27, tableau en ETPT", "Les apprentis et contrats aidés sont des dont ; les ajouter de nouveau serait un double comptage.")

    scsp = numeric_cells(pdf("j27", 24), "Subvention pour charges de service public")
    assert scsp == [33969713197, 33969713197, 33102810903, 33102810903]
    raw_drop = scsp[1] - scsp[3]
    assert "460098952" in re.sub(r"\s", "", p26)
    asc = 460098952
    after_asc = raw_drop - asc
    assert (raw_drop, after_asc) == (866902294, 406803342)
    add(5, "06_financement", "SCSP apparente et reclassement service civique", "LFI2026/PLF2027",
        "866,902M€ apparents ; reclassement460,099M€ ; solde406,803M€",
        "866902294€ -460098952€ =406803342€", "euros puis M€ arrondis", ["j27"],
        "PDF p.24, tableau CP et explication-867/-407 ; p.26 reclassementASC",
        "Calcul de contrôle de montants budgétaires. Le reclassement du titre3 au titre6 ne supprime pas la mission ni sa dépense. Pas une productivité mesurée.")

    constant = numeric_cells(p26, "Subvention pour charge de")
    assert constant[:4] == [33969713197, -449746410, 33519966787, 33102810903]
    constant_drop = constant[2] - constant[3]
    assert constant_drop == 417155884
    transfers = numeric_cells(pdf("j27", 24), "Transferts (intervention)")
    constant_transfers = numeric_cells(p26, "Crédits de transferts")
    assert transfers == [16055823687, 16338579734, 20210091561, 16366164675]
    assert constant_transfers[:4] == [16338579734, 460098952, 16798678686, 16366164675]
    assert transfers[3] - transfers[1] == 27584941
    assert constant_transfers[2] - constant_transfers[3] == 432514011
    assert "diminuent en apparence de 28 M" in normalized(pdf("j27", 24))
    add(6, "06_financement", "SCSP à champ constant après tous transferts", "PLF2027/LFI2026 reformatée",
        "417,156M€ de baisse", f"33519966787€ -33102810903€ = {constant_drop}€ ; intervention courante+27584941€",
        "euros puis M€ arrondis", ["j27"], "PDF p.24 (variation courante) et p.25-26 (périmètre et tableau à champ constant)",
        "Le retraitement complet diffère du seul reclassementASC ; montants non cumulables. Anomalie du jaune p.24, non reprise par06 : le texte dit une baisse apparente des interventions de28M€, alors que le tableau donne une hausse de27,584941M€. AprèsASC, la baisse de432,514011M€ est cohérente.",
        "CONFIRME_AVEC_ANOMALIE_SOURCE")

    assert "Budget initiaux 2026" in normalized(pdf("j27", 221))
    for n, actor, page, expected in [
        (7, "Anah", 246, (3651541, 25000, 175854, 3450687)),
        (8, "Ademe", 226, (1603575, 104788, 175907, 1322880)),
        (9, "France Travail", 458, (6889234, 3886736, 1030052, 1972446)),
    ]:
        text = pdf("j27", page)
        assert "en milliers d'euros" in normalized(text)
        actual = (numeric_cells(text, "Total des charges")[0],
                  numeric_cells(text, "Personnel")[0],
                  numeric_cells(text, "Fonctionnement autre que les charges de personnel")[0],
                  numeric_cells(text, "Intervention (le cas échéant)")[0])
        assert actual == expected and actual[0] == sum(actual[1:])
        converted = tuple(Decimal(v) / 1000 for v in actual)
        add(n, "06_budgets_operateurs", actor + " : année et composantes du compte de résultat", "BI2026",
            " / ".join(str(v) for v in converted) + " M€ (total/personnel/fonctionnement/intervention)",
            " / ".join(str(v) for v in actual) + " k€ ; chaque valeur divisée par1000",
            "k€ source ; M€ dans la note", ["j27"], f"PDF p.221 (champ2026) et p.{page}, compte de résultat",
            "Le document est annexé au PLF2027 mais cette fiche est un BI2026. Les interventions financent des missions ; le total n'est pas un coût de siège. Opérations d'ordre et CAS sont des dont.")

    net = texts["rgpp_net"]
    pattern = (r"atteignaient respectivement (\d+) millions d'euros en 2010, contre (\d+) millions d'euros en économies brutes, "
               r"et (\d+) millions d'euros en 2011, contre (\d+) millions d'euros en économies brutes")
    match = re.search(pattern, net)
    assert match and tuple(map(int, match.groups())) == (264, 808, 373, 935)
    add(10, "06_RGPP", "Économies titre2 brutes et nettes2010", "2010, rapport AN2012",
        "808 bruts /264 nets", "808 bruts /264 nets dans le même paragraphe", "M€", ["rgpp_net"],
        "II.A.5, paragraphe précédant II.B, renvoi aux lois de règlement2010/2011",
        "Net publié après retour catégoriel, pas net complet consolidé de toute la RGPP. La note garde correctement ce champ partiel.")
    assert "562,6" in net
    add(11, "06_RGPP", "Économies titre2 brutes et nettes2011", "2011, rapport AN2012",
        "935 bruts /373 nets ; tableau de retour562,6", "935 bruts /373 nets dans le texte ; 562,6 de mesures catégorielles au tableau",
        "M€", ["rgpp_net"], "II.A.5 et II.B.1, tableau2011, ligne Total",
        "935-562,6=372,4M€, alors que le texte publie373M€. La divergence de présentation est déjà explicitée dans06 ; pas de correction silencieuse ni net au centime reconstitué.",
        "CONFIRME_AVEC_RESERVE_SOURCE")

    p49, p52 = normalized(pdf("rgpp", 49)), normalized(pdf("rgpp", 52))
    assert "Tableau n°4" in normalized(pdf("rgpp", 50))
    assert "Actualisation des économies" in normalized(pdf("rgpp", 51))
    assert all(s in p49 for s in ["La présentation des gains est énoncée en brut", "coûts induits", "suivi"])
    assert all(s in p52 for s in ["12,3 Mds", "11,9 Mds", "devraient", "restent à confirmer"])
    add(12, "06_RGPP", "Objectif révisé11,9 et portée du bilan", "prévisions2009-2012, rapport2012",
        "12,3 attendus révisés11,9 ;2012 encore à confirmer", "12,3→11,9Md€ ; gains bruts ; coûts induits rarement estimés ou suivis",
        "Md€ de gains attendus par rapport à la référence", ["rgpp"], "PDF p.49-52, imprimées40-43 ; tableaux4 et6",
        "La valeur de11,9 est un fait de prévision externe, pas un net causal entièrement observé. La note ne somme pas les colonnes annuelles du tableau4.")

    normative = texts["norme"]
    assert re.search(r"26%.*?2022.*?5% en 2025", normative)
    add(13, "07_CNEN", "Saisines urgentes déclarées", "2022/2025, réponse01/10/2026",
        "26%→5%", "26% des textes à l'ordre du jour2022→5% en2025", "% de textes, déclaration gouvernementale", ["norme"],
        "Réponse à la QE08930, paragraphe engagementsCNEN",
        "Mesure de procédure et non coût des normes ou économie d'ETP. Le rapport de dénominateurs n'a pas pu être contrôlé séparément ; la réserve existante est maintenue.",
        "CONFIRME_COMME_DECLARATION")

    assert "maintenance" in texts["cnen"].lower() and "maintenance" in texts["cnen_rapport"].lower()
    assert len(primary["cnen"]) == 654 and primary["cnen"] == primary["cnen_rapport"]
    add(14, "07_CNEN", "Absence de chiffrage récent net vérifié", "accès28/10/2026",
        "NON TROUVÉ ; aucun coût net récent retenu", "Accueil et URL du rapport renvoient la même maintenance de654 octets",
        "absence de preuve du coût dans ce lot", ["cnen", "cnen_rapport"], "Réponses HTML originales, titre et corps",
        "Le statut de manque est justifié par ces accès. Cela ne démontre pas qu'aucun bilan n'existe ailleurs. Aucun coût de politique ou de norme n'est transformé en économie administrative.",
        "NON_VERIFIABLE_SOURCE_INACCESSIBLE")

    law = texts["loi"]
    assert "Loi n° 2026-403 du 26 mai 2026" in law
    assert all(s in law for s in ["définitivement adopté", "15 avril", "21 mai 2026", "promulgué"])
    add(15, "07_droit", "Loi entreprises : adoption et promulgation", "2026",
        "Loi2026-403 promulguée26/05/2026 ; adoption avril, censure partielle mai",
        "Sénat : adoption définitive après14/15 avril, décision21 mai et promulgation26 mai",
        "dates et statut législatif", ["loi"], "La loi en clair, titre et chronologie",
        "Contrôle du statut via la page primaire du Sénat, pas lecture intégrale du JORF bloqué. La promulgation ne prouve pas l'application de chaque mesure ou décret.")

    once = texts["dlnuf"]
    assert "permettrait de générer des économies estimées à 320 millions d'euros par an pour l'Etat" in once
    assert "20 janvier 2019" in once
    add(16, "07_DLNUF", "Potentiel annoncé et décrets déjà publiés", "réponse07/05/2019",
        "320M€/an potentiels pour l'État ; décrets janvier2019", "Conditionnel permettrait ;320M€/an pour l'État ; mention JO20/01/2019",
        "M€/an de cible publique externe", ["dlnuf"], "QE10191, réponse gouvernementale, premier et deuxième paragraphes",
        "L'hypothèse externe est correctement séparée d'un gain exécuté. Une généralisation future doit être comparée au déploiement déjà engagé.")

    shock = texts["choc"]
    assert all(s in shock for s in ["460 mesures", "5 milliards", "pour les entreprises chaque année", "aucunement vérifiable"])
    add(17, "07_choc", "Nombre de mesures et potentiel privé", "2017",
        "Environ460 mesures ;5Md€/an potentiels entreprises, non vérifiables", "460 ;5 milliards potentiels chaque année ; coûts nouveaux non déduits",
        "mesures et Md€/an privés annoncés", ["choc"], "Trois questions Lamure/Cadic, première réponse",
        "Le Sénat décrit une annonce gouvernementale contestée ; ce montant n'est ni un gain public français ni un résultat ex post vérifié.")

    eu = texts["ue"]
    assert all(s in eu for s in ["€17 billion", "will save", "€37.5 billion", "by 2029", "at least 35%", "at least 25%", "12 omnibus proposals"])
    add(18, "07_UE", "Portefeuille de simplification et cible2029", "page28/10/2026 ; horizon2029",
        "12 omnibus ;17Md€ annoncés ;37,5Md€ cible ;25% général/35% PME",
        "12 propositions ; titre achieved so far mais texte will save ;37,5Md€ attendus2029 ;25%/35%",
        "propositions et annonces de charge administrative UE", ["ue"], "What savings can we expect? et Simplification in action",
        "La note a déjà neutralisé l'ambiguïté du titre : absence de bilan encaissé. Pour37,5, le contexte vise la charge annuelle mais aucune somme exécutée française n'est démontrée.",
        "CONFIRME_AVEC_RESERVE_EXISTANTE")

    assert all(s in eu for s in ["€1.8 billion in savings for farmers", "€210 million in savings for administrations", "€350 million", "€324 million in one-off"])
    add(19, "07_UE", "Charges privées/publiques et ponctuel/récurrent", "portefeuille annoncé2026",
        "PAC1,8Md€ agriculteurs/210M€ administrations ; investissements324M€ ponctuels sur350M€",
        "Montants et one-off explicitement présents dans les deux rubriques",
        "M€ et Md€ attendus, périmètre UE", ["ue"], "Rubriques Common agricultural policy et Investments",
        "Les210M€ ne sont pas une économie française identifiée. La composante324M€ interdit d'annualiser intégralement les350M€. Aucune addition à une enveloppe nationale.")

    p528, p529 = normalized(pdf("scm", 528)), normalized(pdf("scm", 529))
    assert all(s in p528 for s in ["Tariff x Time", "Number of businesses x Frequency", "new obligations", "removed obligations"])
    assert all(s in p529 for s in ["businesses, citizens or public administrations", "new or eliminating existing administrative obligations"])
    add(20, "07_methode", "Standard Cost Model : formule et périmètre", "toolbox décembre2025",
        "Nouveaux coûts moins coûts retirés ; prix=tarif×temps ; quantité=population×fréquence",
        "ΣPN×QN-ΣPR×QR ; tarif et temps ; entreprises et fréquence ; distinction des activités habituelles",
        "coûts administratifs par obligation", ["scm"], "Outil58, PDF p.528-529, imprimées527-528, encadrés2-3 et étape préparatoire",
        "La méthode s'applique selon le groupe cible et exige un inventaire. Valorisation d'une charge et dépense budgétaire évitée restent distinctes ; pas de coefficient national d'ETP.")

    assert len(rows) == 20 and len({r["id"] for r in rows}) == 20
    with CSV_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLS)
        writer.writeheader()
        writer.writerows(rows)

    claims = {
        "06": ROOT / "recherche/06_doublons_structures.md",
        "07": ROOT / "recherche/07_simplification_reglementaire.md",
    }
    claim_hashes = {key: hashlib.sha256(path.read_bytes()).hexdigest() for key, path in claims.items()}
    broken_link = "04 d_territoires_fonctions_support.md" in claims["06"].read_text(encoding="utf-8")
    summary_lines = []
    for r in rows:
        summary_lines.append(f"| {r['id']} | {r['indicateur']} | {r['statut_controle']} | {r['valeur_source']} |")
    source_lines = []
    for key, m in metadata.items():
        selected = sorted(n for k, n in pages if k == key)
        location = "PDF p." + ",".join(map(str, selected)) if selected else "HTML original, paragraphes indiqués dans le CSV"
        source_lines.append(f"- `{key}` : [{m['path']}]({m['url']}) ; SHA256 `{m['sha256']}` ; {location}.")
    presentation = ("Le premier paragraphe de06 cible `04 d_territoires_fonctions_support.md`, alors que le fichier est `04d_territoires_fonctions_support.md`. Défaut de lien signalé au parent ; aucune modification de la note auditée."
                    if broken_link else "Le lien initial vers04d a été corrigé au moment de cette reproduction.")
    note = f"""# Contre-vérification indépendante — volets06–07, lot3

Contrôle arrêté au **28 octobre2026**. **20 points décisifs** ont été examinés directement dans les PDF et HTML primaires archivés : **19 sont confirmés dans leur champ, dont quatre avec qualification ou réserve explicite ; un reste non vérifiable faute de document CNEN accessible**. Aucune nouvelle correction chiffrée des notes n'est demandée. Une inversion de signe dans le commentaire du jaune budgétaire, non reprise par06, est consignée. Les réserves de période, unité, prévision et consolidation sont nécessaires au résultat.

## Méthode et indépendance

Le vérificateur n'a rédigé ni06 ni07. Il a lu les notes pour identifier les affirmations, puis les pages des documents primaires. **Aucun extracteur06/07 n'a été lu, importé ou appelé ; aucun CSV produit par ces extracteurs ne sert de preuve.** Le script de contrôle lit les PDF avec pypdf, les octets HTML originaux et les métadonnées de téléchargement pour URL et SHA. Il recalcule séparément les différences, conversions k€→M€ et sommes de composantes. Les pages réellement consultées sont listées ci-dessous ; aucune lecture exhaustive des jaunes ou des rapports n'est revendiquée.

Cette indépendance concerne le **contrôle documentaire**, pas la production d'une nouvelle observation statistique. Les chiffres sont relus dans les mêmes sources primaires ; ils ne constituent pas une seconde série indépendante confirmant leurs phénomènes ou leur causalité.

Versions des notes contrôlées lors de cette reproduction :

- 06 : SHA256 `{claim_hashes['06']}`.
- 07 : SHA256 `{claim_hashes['07']}`.

## Résultats décisifs

Les431 et423 sont les nombres des périmètres proposés aux PLF2026 et2027. Le comparateur d'emplois401389 est en revanche la **LFI2026** : il ne faut pas reprendre les401310 de la proposition initiale du jaune2026. Le plafond397282 et sa baisse4107 ne sont pas des suppressions observées de personnes. Les3248 d'abattements de vacance, le schéma-1209ETP et son impact-998ETPT ont des natures et unités différentes.

La baisse apparente de SCSP est866902294€. Le seul reclassement de l'Agence du service civique enlève460098952€ de cette différence, laissant406803342€. Après toutes les mesures de périmètre, la différence vaut417155884€. Les arrondis866,902/406,803/417,156M€ de06 sont corrects. Ces trois différences ne sont ni cumulables ni des mesures causales de productivité.

**Anomalie primaire :** p.24, le jaune dit que les crédits d'intervention « diminuent en apparence de28M€ ». Ses CP passent pourtant de16338579734€ à16366164675€, soit **+27584941€**. Après le reclassementASC, la baisse de432514011€ correspond bien aux433M€ annoncés à champ constant. La note06 ne reprend pas le signe courant erroné. Le tableau et le calcul sont privilégiés, sans corriger silencieusement le commentaire primaire.

Les comptes Anah, Ademe et France Travail, publiés dans le jaune2027, sont bien les **budgets initiaux2026**. L'unité source est le millier d'euros. Les trois composantes principales de charges se somment aux totaux de la note. Les interventions, missions et emplois d'accompagnement empêchent de traiter tout le budget comme un coût de siège.

Le rapport parlementaire donne808/264M€ bruts/nets pour2010 et935/373M€ pour2011, après retour catégoriel. Le texte373 et le calcul935-562,6=372,4 diffèrent ;06 signale déjà ce point et ne corrige pas silencieusement la source. Le rapport des inspections présente11,9Md€ comme des gains attendus révisés, encore partiellement à confirmer, dans une présentation brute aux coûts induits mal suivis. Aucun net causal complet de la RGPP n'est ainsi reconstitué.

Les26%→5% du CNEN sont une déclaration gouvernementale sur les saisines urgentes. Ils ne mesurent pas des normes supprimées ou des économies d'emploi. L'accueil et l'URL du rapport renvoient exactement la même maintenance de654 octets : le coût récent net reste **non vérifiable dans ce lot**, et son absence de la base est justifiée. Ce constat d'accès ne prouve pas qu'aucun document n'existe ailleurs.

La page primaire du Sénat confirme l'adoption définitive en avril, la censure partielle en mai et la promulgation de la loi2026-403 le26mai2026. Elle n'établit pas l'application effective de chaque mesure ; le JORF intégral n'est pas revendiqué. Les320M€/an DLNUF sont au conditionnel pour l'État ; les5Md€/an du choc sont privés, potentiels et jugés invérifiables dans le document sénatorial.

Le portefeuille UE reste prospectif malgré le titre « achieved so far ». La page emploie aussi « will save », donne une cible2029 et distingue des statuts de textes. Les1,8Md€ pour agriculteurs,210M€ pour administrations et324M€ ponctuels sur350M€ d'investissements ont les périmètres correctement séparés dans07. La méthode de coût standard confirme la différence obligations nouvelles/retirées ; elle ne transforme pas un temps valorisé en crédit budgétaire annulé.

## Tableau de contrôle

Le CSV fournit en plus les unités, périodes, URL exactes, localisations, objections et empreintes. Les champs de valeurs peuvent contenir plusieurs composantes du même point de contrôle ; ils ne sont pas un fichier de paramètres financiers.

| Identifiant | Point contrôlé | Résultat | Lecture de la source |
|---|---|---|---|
{chr(10).join(summary_lines)}

## Corrections et limites

- **Chiffres et interprétations prioritaires :** pas de correction nouvelle demandée après ces lectures. Les écarts de périmètre et l'incertitude2011 sont déjà documentés dans les notes.
- **Jaune, p.24 :** conserver la trace du signe erroné de variation courante des interventions, en distinguant cette anomalie primaire d'une erreur de la note06.
- **CNEN :** conserver le manque et la distinction entre coûts de politique, coûts de formalité et économies administratives. La source de coût n'a pas été lue.
- **Droit :** le statut de promulgation est vérifié sur la source parlementaire primaire ; ce contrôle ne remplace pas la lecture du droit consolidé ou des décrets d'application.
- **Prévisions :** aucun montant PLF, portefeuille UE ou potentiel de simplification n'est requalifié en exécution ni en économie nette française.
- **Présentation :** {presentation}

Les contrôles automatiques sécurisent la transcription et les calculs ; ils ne démontrent pas à eux seuls l'interprétation de la source. Le présent rapport explicite les principales qualifications lues.

## Sources effectivement rouvertes et reproduction

{chr(10).join(source_lines)}

Commande : `python -I scripts/00_verification_06_07_lot3.py`.

Sorties : `data/risques/verification_06_07_lot3.csv` et `recherche/00_verification_06_07_lot3.md`. Aucun téléchargement supplémentaire, normalisation des réponses primaires, modification de06/07, commit ou push n'est effectué. La note est écrite en UTF-8 avec fins de ligneLF ; le CSV conserve le format exact émis par le script.
"""
    # Espaces de présentation dans les seuls paragraphes humains. Préserver les
    # chemins, empreintes, identifiants et URL de la table de preuves.
    cleaned = []
    for line in note.splitlines():
        if "`" not in line and not line.startswith("|") and "http" not in line:
            line = re.sub(r"(?<=[A-Za-zÀ-ÿ])(?=\d)|(?<=\d)(?=[A-Za-zÀ-ÿ])", " ", line)
            line = re.sub(r"^-0([67]) :", r"- 0\1 :", line)
        cleaned.append(line)
    NOTE_PATH.write_text("\n".join(cleaned) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"points": len(rows), "confirmes_avec_qualifications": 19,
                      "non_verifiable_CNEN": 1, "sources_primaires": len(metadata),
                      "pages_pdf_lues": len(pages), "correction_chiffree_nouvelle": False}, ensure_ascii=False))


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main()
