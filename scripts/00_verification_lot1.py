#!/usr/bin/env python3
"""Contre-vérification du lot 1 à partir des XLSX et réponses d'API primaires.

Ne réutilise aucune fonction d'extraction des chantiers 01/01b/02/03.
Les valeurs citées sont un échantillon explicite des notes et jeux de données.
Le contrôle porte sur la transcription et les calculs, pas sur une seconde enquête.
"""
import csv
import hashlib
import json
from pathlib import Path
import re

from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[1]
DG = "https://www.fonction-publique.gouv.fr/files/files/publications/vue-rapport-annuel/2026/"
FP = "data/raw/01/dgafp_ra2026/"
BOOKS = {
    "e": (FP+"ra_2026_vue_emploi_effectifs.xlsx", DG+"ra_2026_effectifs.zip"),
    "comp": (FP+"RA_2026_effectifs_donnees_comp_FP.xlsx", DG+"ra_2026_effectifs.zip"),
    "p": (FP+"ra_2026_vue_emploi_caracteristiques_postes.xlsx", DG+"ra_2026_postes.zip"),
    "i": ("data/raw/01/insee_IP2094_donnees.xlsx", "https://www.insee.fr/fr/statistiques/fichier/8732435/IP2094.xlsx"),
    "d": ("data/raw/01/insee_2381404_depenses_apu_2025.xlsx", "https://www.insee.fr/fr/statistiques/fichier/2381404/econ-fin-pub-dep-adm-pub-secteur.xlsx"),
    "t": (FP+"ra_2026_remu_niveaux_donnees_comp_depenses.xlsx", DG+"ra_2026_remu_niveaux.zip"),
    "s": (FP+"ra_2026_remu_niveaux_donnees_comp.xlsx", DG+"ra_2026_remu_niveaux.zip"),
    "h": (FP+"ra_2026_vue_temps_organisation_temps_travail.xlsx", DG+"ra_2026_tps_organisation_tps_travail.zip"),
    "f": (FP+"ra_2026_vue_flux_de_personnels_entrees_sorties.xlsx", DG+"ra_2026_entrants-sortants.zip"),
    "fc": (FP+"ra_2026_entrees_sorties_donnees_comp.xlsx", DG+"ra_2026_entrants-sortants.zip"),
    "r": (FP+"ra_2026_vue_flux_de_personnels_retraites.xlsx", DG+"ra_2026_retraite.zip"),
    "a": (FP+"ra_2026_50plus.xlsx", "https://www.fonction-publique.gouv.fr/toutes-les-publications/les-agents-de-50-ans-ou-plus-dans-la-fonction-publique-en-2024"),
    "fpt": (FP+"ra2026_caracteristiques_postes_donnees_comp_FPT.xlsx", DG+"ra_2026_postes.zip"),
    "fph": (FP+"ra2026_caracteristiques_postes_donnees_comp_FPH.xlsx", DG+"ra_2026_postes.zip"),
    "fpe": (FP+"ra2026_caracteristiques_postes_donnees_comp_FPE.xlsx", DG+"ra_2026_postes.zip"),
    "fp": (FP+"ra2026_caracteristiques_postes_donnees_comp_FP.xlsx", DG+"ra_2026_postes.zip"),
    "efpe": (FP+"RA_2026_effectifs_donnees_comp_FPE.xlsx", DG+"ra_2026_effectifs.zip"),
    "depp": ("data/raw/02/depp_ch2_2025_2026.xlsx", "https://www.education.gouv.fr/sites/default/files/document/chapitre-2-les-enseignants-520474.xlsx"),
    "drees": ("data/raw/02/drees_es2026_f07.xlsx", "https://www.drees.solidarites-sante.gouv.fr/sites/default/files/2026-07/ES%202026%20-%20Fiche%2007%20-%20Les%20%C3%A9volutions%20des%20effectifs%20salari%C3%A9s%20du%20secteur%20hospitalier.xlsx"),
    "gag": ("data/raw/03/03_oecd_gag2025_fig13_1.xlsx", "https://stat.link/8htodn"),
}
OPEN = {}
ROWS = []


def value(alias, sheet, cell):
    if alias not in OPEN:
        OPEN[alias] = load_workbook(ROOT / BOOKS[alias][0], data_only=True, read_only=False)
    val = OPEN[alias][sheet][cell].value
    if not isinstance(val, (float, int)):
        raise ValueError(f"Cellule non numérique {alias}/{sheet}!{cell} : {val!r}")
    return float(val)


def hash16(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()[:16]


def append(ident, claim, cited, actual, unit, year, scope, doc, loc, urls, hashes,
           *, status="[FAIT]", tolerance=1e-6, method="Lecture directe d'une cellule primaire et conversion explicite d'unité", objection="", corrected=False):
    delta = actual - cited
    result = "CONFIRME" if abs(delta) <= tolerance else "ECART_A_CORRIGER"
    if corrected and result == "CONFIRME":
        result = "STATUT_CORRIGE"
    ROWS.append({
        "id": ident, "affirmation": claim, "valeur_citee": cited, "valeur_verifiee": round(actual, 10),
        "unite": unit, "annee": year, "champ": scope, "document_verifie": doc,
        "source_url": urls, "source_localisation": loc, "source_sha256_16": hashes,
        "ecart": round(delta, 10), "tolerance_affichage": tolerance,
        "statut_initial": "[FAIT]" if corrected else status, "statut_retenu": status,
        "resultat": result, "methode": method,
        "objection_correction": objection or "Unité, champ et période confirmés ; aucune déduction de sureffectif validée par ce contrôle.",
        "date_verification": "2026-10-28",
    })


def cell(ident, claim, alias, sheet, address, expected, unit, year, scope, *, multiplier=1, doc="recherche/01_emploi_public_france.md", tolerance=1e-6, note=""):
    actual = value(alias, sheet, address) * multiplier
    path, url = BOOKS[alias]
    append(ident, claim, expected, actual, unit, year, scope, doc, f"{path} / {sheet}!{address} ; multiplicateur={multiplier}", url, hash16(path), tolerance=tolerance, objection=note)


def calc(ident, claim, refs, operation, expected, unit, year, scope, *, doc="recherche/01b_flux_retraites.md", method="", tolerance=1e-6, status="[ESTIMATION]", note="", corrected=False):
    vals = [value(*ref) for ref in refs]
    paths = list(dict.fromkeys(BOOKS[alias][0] for alias, _, _ in refs))
    urls = list(dict.fromkeys(BOOKS[alias][1] for alias, _, _ in refs))
    loc = "; ".join(f"{BOOKS[a][0]} / {s}!{c}={v}" for (a, s, c), v in zip(refs, vals))
    append(ident, claim, expected, operation(vals), unit, year, scope, doc, loc, " ; ".join(urls),
           " ; ".join(hash16(p) for p in paths), status=status, tolerance=tolerance,
           method=method, objection=note, corrected=corrected)


def domestic():
    stock = "France hors Mayotte, emplois principaux au 31/12, hors contrats aidés"
    for suffix, row, name, expected in (("TOTAL",9,"FP",5848291),("FPE",6,"FPE",2581870),("FPT",7,"FPT",2017830),("FPH",8,"FPH",1248591)):
        cell("STOCK_"+suffix, "DGAFP : effectif "+name, "e", "Figure 2", f"C{row}", expected, "PP", 2024, stock, multiplier=1000)
    for suffix, sheet, address, expected, unit, scope in (
        ("AIDES","Figure 6","S23",25797,"PP","Contrats aidés des trois versants"),
        ("AVEC_AIDES","Figure 4","P18",5874088,"PP","Trois versants, contrats aidés inclus"),
        ("2023_HCA","Figure 4","O22",5811255,"PP","Trois versants, hors contrats aidés"),
        ("S13","Figure 2","L28",6531025,"PP","Salariés principaux S13 au 31/12, contrats aidés inclus"),
        ("PUBLIC_HORS_FP","Figure 3","U20",188011,"PP","Organismes publics hors FP, marchands et non marchands"),
        ("PROTECTION_SOCIALE","Figure 3","U22",162623,"PP","Organismes privés de protection sociale, financement public prédominant"),
        ("ENTREPRISES_PUB","Figure 3","U28",512501,"PP","Entreprises publiques marchandes, hors champ FP"),
    ):
        cell("STOCK_"+suffix, "DGAFP : "+scope, "comp", sheet, address, expected, unit, 2023 if suffix.startswith("2023") else 2024, scope+" ; France hors Mayotte", multiplier=1000)
    for suffix, address, expected, unit, scope in (
        ("PP_AVEC_AIDES","D9",5876700,"PP","Postes principaux au 31/12, contrats aidés inclus"),
        ("PP_HCA","E9",5850900,"PP","Postes principaux au 31/12, hors contrats aidés"),
        ("EQTP_AVEC_AIDES","D14",5804200,"EQTP annuels","Tout poste actif dans l'année, contrats aidés inclus"),
        ("EQTP_HCA","E14",5781800,"EQTP annuels","Tout poste actif dans l'année, hors contrats aidés"),
    ):
        cell("INSEE_"+suffix, "IP2094 : "+scope, "i", "Figure 1", address, expected, unit, 2024, scope+" ; France hors Mayotte", multiplier=1000, note="Cellules A15/A16 : stock au 31 décembre et tout poste actif dans l'année sont deux concepts distincts.")
    for row, name, expected in ((19,"fonctionnaires",3745836),(20,"contractuels",1407727),(21,"militaires FPE",312854),(22,"autres catégories",381874)):
        cell("STATUT_"+str(row), "Effectif des "+name, "p", "Figure 1", f"D{row}", expected, "PP", 2024, stock+" ; "+name, multiplier=1000)
    for suffix,sheet,address,label,expected in (
        ("MINISTERES","Figure 4","C36","Ministères FPE",2058555),("EPA","Figure 4","C37","EPA FPE",523315),
        ("EDUCATION","Figure 4","C6","Rattachement Éducation/ESR, ministères et EPA",1501101),
        ("COMMUNES","Figure 6","C6","Organismes communaux",1146464),("INTERCO","Figure 6","C9","Organismes intercommunaux",401402),
        ("HOPITAUX","Figure 7","C6","Hôpitaux",1118560),("EHPAD","Figure 7","C9","Ehpad non hospitaliers",92510),
        ("MEDICOSOCIAL","Figure 7","C10","Autres établissements médico-sociaux",37521),
    ):
        cell("EMPLOYEUR_"+suffix, label, "e",sheet,address,expected,"PP",2024,stock+" ; "+label,multiplier=1000)
    for ident,address,label,expected in (
        ("D1_S13","F8","D1 APU",370.012),("D1_APUC","B8","D1 APUC",184.8776),
        ("D1_APUL","D8","D1 APUL",96.9526),("D1_ASSO","E8","D1 ASSO",88.1818),
        ("P2_S13","F7","P2 APU",163.4965),
    ):
        cell(ident,label,"d","Figure 1",address,expected,"Md€ courants",2025,"France, comptes nationaux base 2020, données provisoires")
    cell("BUDGET_T2","Titre 2 exécuté","t","Figure 2","T35",156.241675,"Md€ courants",2025,"Budget général de l'État",tolerance=0.0000005)
    cell("BUDGET_CAS","Contributions d'équilibre au CAS, ligne dédiée","t","Figure 2","T14",49.219294,"Md€ courants",2025,"Budget général de l'État",tolerance=0.0000005)
    calc("BUDGET_HCAS","Titre 2 moins ligne contributions CAS",[("t","Figure 2","T35"),("t","Figure 2","T14")],lambda x:x[0]-x[1],107.022381,"Md€ courants",2025,"Budget général État, normalisation HCAS",doc="recherche/01_emploi_public_france.md",method="T35 − T14 ; ne retire pas toutes les cotisations retraite",tolerance=0.0000005)
    for address,name,expected in (("B11","FPE",3738.28),("B28","FPT",2857.75),("B45","FPH",3559.79)):
        cell("SALAIRE_"+name,"Salaire brut mensuel moyen "+name,"s","Figure 1",address,expected,"€/mois par EQTP mensualisé",2024,"Civils hors contrats aidés ; exclusions de la source, France hors Mayotte",tolerance=0.005,note="Hors militaires, assistants maternels/familiaux, apprentis, internes/externes. Salaire, pas coût employeur ni coût d'entrée.")
    for address,name,expected in (("F6","FP",1623.116),("G6","prive",1680.234)):
        cell("HEURES_"+name,"Durée annuelle effective déclarée "+name,"h","Figure 1",address,expected,"heures/an",2025,"Enquête emploi ; temps complet, logement ordinaire, hors enseignants/apprentis/contrats aidés ; France hors Mayotte",tolerance=0.0005)
    calc("VARIATION_FP","Hausse DGAFP hors contrats aidés",[("comp","Figure 4","P22"),("comp","Figure 4","O22")],lambda x:(x[0]-x[1])*1000,37036,"PP",2024,stock,doc="recherche/01_emploi_public_france.md",method="(P22 − O22) × 1 000")
    calc("ECART_VARIATIONS","Écart de variations DGAFP/Insee sur champ HCA",[("comp","Figure 4","P22"),("comp","Figure 4","O22"),("i","Figure 1","E9"),("i","Figure 1","C9")],lambda x:(x[0]-x[1]-x[2]+x[3])*1000,1236,"PP",2024,"Versions différentes et même champ nominal hors contrats aidés",doc="recherche/01_emploi_public_france.md",method="[(P22−O22)−(E9−C9)] × 1 000 ; pas d'explication causale inférée")


def flows():
    doc="recherche/01b_flux_retraites.md"
    civil="France hors Mayotte, FP civile, postes principaux entre deux 31 décembre, hors contrats aidés"
    for ident,sheet,address,claim,expected in (
        ("ENTRANTS","Fig. 1","D8","Entrants FP civile",517134),
        ("SORTANTS","Fig. 1","H8","Sortants FP civile",481598),
        ("SORT_FONCT","Fig. 1","H22","Sortants fonctionnaires",174655),
        ("SORT_CONTR","Fig. 1","H26","Sortants contractuels",261179),
        ("SORT_AUTRES","Fig. 1","H30","Sortants autres statuts",45764),
        ("SORT_FPE","Fig. 2","H9","Sortants FPE",169983),
        ("SORT_FPT","Fig. 2","H14","Sortants FPT",201530),
        ("SORT_FPH","Fig. 2","H19","Sortants FPH",110085),
        ("COURTS","Fig. 4","C5","Postes commencés et finis dans l'année",332144),
        ("COURTS_CONTR","Fig. 4","C10","Postes contractuels courts, figure 4",307069),
        ("COURTS_CONTR_AUTRE","Fig. 5","K6","Postes contractuels courts, figure 5",307134),
    ):
        unit="postes occupés" if ident.startswith("COURTS") else "PP"
        cell("FLUX_"+ident,claim,"f",sheet,address,expected,unit,2024,civil,multiplier=1000,doc=doc,note="Comparer les deux 31 décembre ne prouve pas une sortie définitive. Les postes courts sont un autre concept ; écart de 65 entre figures signalé dans la note.")
    calc("FLUX_INTERVERSANTS","Total des mouvements interversants",[("f","Encadré 1",c) for c in ("H11","H16","H21")],lambda x:sum(x)*1000,31942,"PP",2024,"Mobilités internes, sans réduction du total FP",method="(H11 + H16 + H21) × 1 000",corrected=True,note="Synthèse n°5 initialement [FAIT] ; somme calculée, [ESTIMATION] corrigé par le parent le 28/10/2026. Tableau déjà correctement étiqueté.")
    calc("FLUX_CUMUL_5ANS","Occurrences annuelles de sortie 2020-2024",[("fc","Figure 2",c) for c in ("K5","M5","O5","Q5","S5")],lambda x:sum(x)*1000,2339789,"occurrences annuelles", "2020-2024",civil,method="Somme de cinq cellules annuelles × 1 000 ; personnes non dédupliquées entre années")
    calc("FLUX_CONSTANT","Cinq fois le flux de sorties 2024",[("f","Fig. 1","H8")],lambda x:x[0]*5000,2407990,"occurrences hypothétiques","2027-2031",civil,method="H8 × 1 000 × 5 ; flux et stock supposés constants",status="[HYPOTHÈSE]",note="Test mécanique et non prévision officielle ni départs administratifs définitivement mobilisables.")
    calc("FLUX_PART_CONTR","Part des contractuels dans les sorties",[("f","Fig. 1","H26"),("f","Fig. 1","H8")],lambda x:x[0]/x[1]*100,54.23,"%",2024,civil,method="H26/H8 × 100",tolerance=0.005)
    pension="Nouvelles pensions de droit direct, SRE hors La Poste/Orange ; condition d'activité publique récente pour Ircantec"
    for suffix,address,label,expected in (("ENSEMBLE","E17","Ensemble",144033),("CIVILES","E16","Hors militaires",133342),("FPE","E5","FPE fonctionnaires civils",39146),("FPT","E10","FPT fonctionnaires CNRACL",46897),("FPH","E13","FPH fonctionnaires CNRACL",22753),("MILITAIRES","E6","Militaires",10691)):
        cell("PENSIONS_"+suffix,"Pensions2025 : "+label,"r","Figure 1",address,expected,"pensions",2025,pension,multiplier=1000,doc=doc)
    cell("PENSIONS_CONTR","Pensions de contractuels encore récemment employés","r","Figure encadré 4 contractuels","C9",19187,"pensions",2025,pension,multiplier=1000,doc=doc)
    calc("PENSIONS_FONCT_CIVILS","Total calculé des pensions des fonctionnaires civils",[("r","Figure 1",c) for c in ("E5","E10","E13")],lambda x:sum(x)*1000,108796,"pensions",2025,"Somme SRE civils + CNRACL FPT + CNRACL FPH",method="(E5 + E10 + E13) × 1 000",corrected=True,note="Synthèse n°10 initialement [FAIT] ; somme absente comme total de cette figure, [ESTIMATION] corrigé par le parent le 28/10/2026.")
    calc("PENSIONS_5ANS","Cinq fois le flux de pensions civiles2025",[("r","Figure 1","E16")],lambda x:x[0]*5000,666710,"pensions hypothétiques","2027-2031",pension,method="E16 × 1 000 × 5",status="[HYPOTHÈSE]",note="Pas une projection démographique ; les métiers protégés ne sont pas déduits.")
    calc("PENSIONS_SEUIL800","Seuil800000 rapporté au test constant de pensions civiles",[("r","Figure 1","E16")],lambda x:800000/(x[0]*5000)*100,120.0,"%","2027-2031",pension,method="800 000 / (E16 × 1 000 × 5) × 100",tolerance=0.05,note="Ratio sur une hypothèse, pas preuve d'impossibilité de toutes les réformes.")
    for suffix,sheet,label,expected in (("AGENTS50","Figure 1","Agents de50ans ou plus",2215506),("FONCT50","Figure 4","Fonctionnaires de50ans ou plus",1695233),("FONCT60","Figure 7","Fonctionnaires de60ans ou plus",379024)):
        cell("AGE_"+suffix,label,"a",sheet,"C9",expected,"PP",2024,"Stock au31/12, hors contrats aidés et Mayotte ; pas flux de départ",multiplier=1000,doc=doc)
    refs=[("f","Encadré 1",f"K{r}") for r in (11,16,21)]+[("f","Fig. 2",f"H{r}") for r in (9,14,19)]
    calc("FLUX_STOCK_DECROISSANT","Sorties civiles sur cinqans, aucun recrutement et taux constants",refs,lambda x:sum(b*1000*(1-(1-fl/b)**5) for b,fl in zip(x[:3],x[3:])),2018805,"PP hypothétiques","2027-2031",civil,method="Somme_v stock_v × [1 − (1 − sorties2024_v/stock2024_v)^5] ; stock2027 supposé égal2024",tolerance=0.5,note="[ESTIMATION] conditionnelle à des hypothèses explicites ; le tableau de la note est étiqueté [HYPOTHÈSE]. Ne mesure pas un scénario de maintien du service.")


def jobs():
    doc="recherche/02_metiers_classification.md et data/france/02_metiers.csv"
    scope="Emplois principaux au31/12/2024, hors Mayotte et contrats aidés ; filière statutaire, pas mesure des tâches"
    for ident,alias,sheet,address,name,expected in (
        ("FPT_ADMIN","fpt","Figure 1 filiere","S28","Filière administrative FPT",453224),
        ("FPT_TECH","fpt","Figure 1 filiere","S37","Filière technique FPT",872787),
        ("FPT_SECOURS","fpt","Figure 1 filiere","S31","Filière incendie-secours FPT",44546),
        ("FPH_ADMIN","fph","Figure 1 filiere","T25","Filière administrative FPH non médicale",121829),
        ("FPH_SOINS","fph","Figure 1 filiere","T28","Filière soignante FPH non médicale",766961),
    ):
        cell("METIER_"+ident,name,alias,sheet,address,expected,"PP",2024,scope,multiplier=1000,doc=doc)
    for suffix,address,label,expected,unit in (("PUBLIC_PP","D18","Enseignants scolaires publics",747404,"PP"),("PUBLIC_ETP","L18","Enseignants scolaires publics",719542,"ETP au30/11"),("PRIVE_PP","D33","Enseignants scolaires privés sous contrat",141411,"PP")):
        cell("DEPP_"+suffix,label,"depp","2.1",address,expected,unit,2025,"30 novembre2025 ; France, hors Mayotte pour le privé ; corps enseignants rémunérés par Éducation nationale",doc=doc,note="Champ et date vérifiés en A46/A47 ; public avec Mayotte, privé hors Mayotte. Ne pas additionner au stock SIASP2024.")
    for suffix,address,label,expected in (("INFIRMIERS","H10","Infirmiers salariés du secteur hospitalier public",267414),("AIDESSOIGNANTS","H11","Aides-soignants salariés du secteur hospitalier public",227505),("ADMIN","H14","Filière administrative du secteur hospitalier public",115516)):
        cell("DREES_"+suffix,label,"drees","ES205_F07_Tableau1",address,expected,"PP",2024,"Salariés présents au31/12, contrats aidés inclus ; France hors Saint-Martin/Saint-Barthélemy, SSA inclus ; hors stagiaires/externes/apprentis",doc=doc,note="Champ relu en B33 ; différent de SIASP-FPH incluant établissements médico-sociaux. Conserver les deux définitions.")
    cell("ENSEIGNANTS_FPE","Enseignants FPE tous ministères et EPA","efpe","Figure 2","P14",972918,"PP",2024,scope+" ; privé sous contrat et élèves enseignants inclus",multiplier=1000,doc=doc)
    calc("MEDECINS_FPH","Médecins et internes FPH par différence",[("fp","Figure 4 catégorie","Q41"),("fph","Figure 1 filiere","T31")],lambda x:(x[0]-x[1])*1000,144604,"PP",2024,scope,doc=doc,method="(Total FPH − personnels non médicaux) × 1 000",note="Différence Siasp ; ne pas confondre avec postes médicaux SAE.")
    calc("POLICE_4_CORPS","Quatre groupes de corps policiers identifiés",[("fpe","Figure 2 catégorie",c) for c in ("B14","B21","B32","B33")],lambda x:sum(x)*1000,116786,"PP",2024,"Fonctionnaires FPE, quatre groupes PCS ; pas toute la police nationale",doc=doc,method="Somme de quatre cellules PCS × 1 000")
    calc("INTERSECTION_MIL_ENS","Enseignants également militaires",[("fpe","Figure 2 statut","D18"),("fpe","Figure 2 statut","D19")],lambda x:(x[0]-x[1])*1000,19,"PP",2024,scope,doc=doc,method="(Militaires totaux − militaires hors enseignants) × 1 000")
    refs=[("efpe","Figure 2","P14"),("fpe","Figure 2 statut","D18")]+[("fpe","Figure 2 catégorie",c) for c in ("B14","B21","B32","B33")]+[("fph","Figure 1 filiere","T28"),("fp","Figure 4 catégorie","Q41"),("fph","Figure 1 filiere","T31")]+[("fpe","Figure 2 catégorie",c) for c in ("B25","B34","B38","B22","B27")]+[("fpt","Figure 1 filiere","S31"),("fpe","Figure 2 statut","D18"),("fpe","Figure 2 statut","D19")]
    calc("PANIER_TERRAIN","Panier de groupes à dominante opérationnelle de la note02",refs,lambda x:(sum(x[:8])-x[8]+sum(x[9:15])-x[15]+x[16])*1000,2400090,"PP",2024,"Panier SIASP fin2024, hors Mayotte/contrats aidés ; corps et filières, pas relevé de tâches",doc=doc,method="Enseignants + militaires + quatre PCS police + filière soignante + différence médicale + greffiers + surveillance/encadrement pénitentiaire + incendie-secours − enseignants militaires",note="Arithmétique et intersection vérifiées. Le classement opérationnel reste hypothétique ; panier non exhaustif et non équivalent à2,4M d'ETP supprimables ou de tâches de terrain exclusives.")


def oecd(file, country, year, transaction=None):
    path=ROOT/"data/raw/03"/file
    with path.open(encoding="utf-8-sig",newline="") as f:
        rows=[{k.split(":",1)[0]:v for k,v in r.items()} for r in csv.DictReader(f)]
    selected=[]
    for row in rows:
        code=lambda key:row.get(key,"").split(":",1)[0].strip()
        if code("REF_AREA")==country and code("TIME_PERIOD")==str(year) and (transaction is None or code("TRANSACTION")==transaction):
            selected.append(row)
    if len(selected)!=1:
        raise ValueError(f"Filtre OCDE ambigu : {file}/{country}/{year}/{transaction} => {len(selected)}")
    row=selected[0]
    mult=int(row["UNIT_MULT"].split(":",1)[0])
    val=float(row["OBS_VALUE"])*10**mult
    meta=json.loads(path.with_suffix(path.suffix+".meta.json").read_text(encoding="utf-8"))
    return val,row,meta["url"],str(path.relative_to(ROOT)),mult


def international():
    doc="recherche/03_comparaison_harmonisee.md"
    for suffix,file,transaction,expected in (("EMP_GOV","03_oecd_emp_gov.csv","EMP",6336000),("EMP_TOTAL","03_oecd_emp_total.csv","EMP",30376000),("POP","03_oecd_population.csv","POP",68553000)):
        val,row,url,path,mult=oecd(file,"FRA",2023,transaction)
        append("OCDE_FRA_"+suffix,"France2023 : "+transaction+" / "+suffix,expected,val,"personnes",2023,"Comptes nationaux annuels ; emploi intérieur et population annuelle, pas PP au31/12 SIASP",doc,f"{path} ; REF_AREA=FRA ; TIME_PERIOD=2023 ; TRANSACTION={transaction} ; OBS_VALUE={row['OBS_VALUE']} ; UNIT_MULT={mult}",url,hash16(path),objection="Dimensions et multiplicateur relus dans le CSV primaire ; comparaison annuelle S13/S1.")
    for country,expected in (("FRA",20.859),("DEU",11.802),("ITA",13.529),("ESP",15.765)):
        gov,rg,ug,pg,mg=oecd("03_oecd_emp_gov.csv",country,2023,"EMP")
        total,rt,ut,pt,mt=oecd("03_oecd_emp_total.csv",country,2023,"EMP")
        append("OCDE_RATIO_"+country,"Emploi S13 / emploi intérieur "+country,expected,100*gov/total,"% emploi intérieur",2023,"Personnes, S13/S1, année commune2023",doc,f"{pg} et {pt} ; pays={country},2023 ; valeurs converties={gov}/{total}",ug+" ; "+ut,hash16(pg)+" ; "+hash16(pt),status="[ESTIMATION]",tolerance=0.0005,method="100 × OBS_VALUE_S13 ×10^UNIT_MULT_S13 / (OBS_VALUE_S1 ×10^UNIT_MULT_S1)",objection="Écart brut, pas mesure d'emplois administratifs ni preuve de sureffectif.")
    for country,expected in (("FRA",12.222),("DEU",8.013)):
        d1,rd,ud,pd,md=oecd("03_oecd_fiscal.csv",country,2023,"D1")
        gdp,rg,ug,pg,mg=oecd("03_oecd_pib.csv",country,2023,"B1GQ")
        if rd["CURRENCY"].split(":",1)[0]!=rg["CURRENCY"].split(":",1)[0]:
            raise ValueError("Monnaies non concordantes")
        append("OCDE_D1_"+country,"D1 / PIB "+country,expected,100*d1/gdp,"% PIB",2023,"S13, dépenses courantes en même monnaie nationale que le PIB",doc,f"{pd} D1 et {pg} B1GQ ; {country},2023 ; montants convertis={d1}/{gdp}",ud+" ; "+ug,hash16(pd)+" ; "+hash16(pg),status="[ESTIMATION]",tolerance=0.0005,method="100 × D1/PIB après conversion des deux multiplicateurs",objection="D1 n'est pas un coût d'entrée ; monnaie et prix courants relus.")
    gov,_,ug,pg,_=oecd("03_oecd_emp_gov.csv","FRA",2023,"EMP")
    pop,_,up,pp,_=oecd("03_oecd_population.csv","FRA",2023,"POP")
    append("OCDE_FRA_1000","Emploi S13 français pour1000habitants",92.425,1000*gov/pop,"personnes pour1000habitants",2023,"Emploi intérieur S13 / population annuelle",doc,f"{pg} et {pp} ; FRA2023",ug+" ; "+up,hash16(pg)+" ; "+hash16(pp),status="[ESTIMATION]",tolerance=0.0005,method="1 000 × emploi S13 / population annuelle",objection="Sensibilité au concept intérieur et aux frontaliers ; pas d'ETP ni correction des besoins.")
    for country,address,expected,scope in (("FRA","C39",20.740,"France, emploi S13/intérieur, publication2025"),("USA","C57",14.560,"États-Unis, source ILOSTAT selon A22"),("JPN","C67",4.938,"Japon, fonds de sécurité sociale exclus selon A26")):
        cell("STATLINK_"+country,"Part emploi public publiée Panorama2025 : "+country,"gag","g13-1",address,expected,"% emploi intérieur",2023,scope,doc=doc,tolerance=0.0005,note="Millésime de publication2025 distinct de l'API actuelle ; année réelle et exclusions relues en A22:A26.")


def main():
    domestic(); flows(); jobs(); international()
    out=ROOT/"data/risques/verification_40_chiffres_lot1.csv"
    out.parent.mkdir(parents=True,exist_ok=True)
    with out.open("w",encoding="utf-8",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=list(ROWS[0]))
        writer.writeheader(); writer.writerows(ROWS)
    for wb in OPEN.values():
        wb.close()
    counts={key:sum(row["resultat"]==key for row in ROWS) for key in sorted({row["resultat"] for row in ROWS})}
    print(json.dumps({"verifications":len(ROWS),"resultats":counts},ensure_ascii=True))
    if any(row["resultat"]=="ECART_A_CORRIGER" for row in ROWS):
        for row in ROWS:
            if row["resultat"]=="ECART_A_CORRIGER":
                print(json.dumps({k:row[k] for k in ("id","valeur_citee","valeur_verifiee","source_localisation")},ensure_ascii=True))
        return 1
    return 0


if __name__=="__main__":
    raise SystemExit(main())
