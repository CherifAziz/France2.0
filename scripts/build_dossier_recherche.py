#!/usr/bin/env python3
"""Assemble un lot de notes, sans le présenter comme un rapport final.

La conversion de chaque note est indépendante : leurs références Markdown de
même nom ne peuvent pas être mélangées entre sources. Pas de dépendance Pandoc.
"""
import argparse
import hashlib
import html
import json
import re
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
deps=ROOT/".cache/python_deps"
if deps.is_dir():
    sys.path.append(str(deps))
try:
    import markdown
except ImportError as exc:
    raise SystemExit("Installer Markdown (requirements-recherche.txt), puis relancer ce script") from exc

NOTES=[
    ("01","Stocks et dépenses","01_emploi_public_france.md"),
    ("01b","Départs et retraites","01b_flux_retraites.md"),
    ("01c","Coûts et pensions","01c_couts_entree_pensions.md"),
    ("02","Métiers","02_metiers_classification.md"),
    ("03","Base internationale","03_comparaison_harmonisee.md"),
    ("04","Contrôle des données héritées","04_controle_preliminaire.md"),
    ("verification","Vérification de 100 chiffres","00_verification_lot1.md"),
    ("modele","Moteur financier","00_audit_modele.md"),
    ("methode","Précisions de méthode","00_AVENANT_METHODOLOGIQUE.md"),
]
NOTES_LOT2=[
    ("04s","Résultats et conséquences","04_synthese_fonctions.md"),
    ("04a","Fiscalité et emploi","04a_fiscalite_emploi.md"),
    ("04b","Éducation, sécurité et justice","04b_education_securite_justice.md"),
    ("04c","Santé et protection sociale","04c_sante_protection_sociale.md"),
    ("04d","Territoires et fonctions support","04d_territoires_fonctions_support.md"),
    ("verification2","Contre-vérification du lot","00_verification_lot2.md"),
]
CSS="""
:root { color-scheme:light; --ink:#17232b; --muted:#53616b; --accent:#245574; --line:#dce2e6; }
* { box-sizing:border-box; }
html { scroll-behavior:smooth; }
body { margin:0; color:var(--ink); background:#fff; font:16px/1.65 system-ui,Segoe UI,sans-serif; }
header { max-width:1200px; margin:0 auto; padding:44px 28px 26px; }
header h1 { font-size:30px; line-height:1.25; margin:12px 0; letter-spacing:-.5px; }
header p { max-width:850px; margin:10px 0; }
.date { color:var(--muted); font-size:14px; }
nav { position:sticky; top:0; background:#fff; z-index:2; border-block:1px solid var(--line); padding:12px 28px; }
nav div { max-width:1144px; margin:auto; display:flex; flex-wrap:wrap; gap:8px 20px; }
nav a { font-size:14px; }
a { color:var(--accent); text-underline-offset:3px; overflow-wrap:anywhere; }
main { max-width:1200px; padding:0 28px 60px; margin:auto; }
section { margin:45px 0 65px; scroll-margin-top:110px; }
section + section { border-top:1px solid var(--line); padding-top:30px; }
h1,h2,h3,h4 { line-height:1.35; color:var(--ink); }
section h1 { font-size:25px; margin:0 0 24px; }
h2 { margin-top:34px; font-size:21px; }
h3 { margin-top:27px; font-size:18px; }
p,li { max-width:960px; }
li { margin:9px 0; }
pre,code { background:#f2f5f6; font-family:Consolas,monospace; font-size:.88em; }
code { padding:1px 4px; overflow-wrap:anywhere; }
pre { padding:16px; overflow:auto; }
pre code { padding:0; }
.table-wrap { overflow-x:auto; margin:24px 0; }
table { width:100%; border-collapse:collapse; font-size:13px; line-height:1.45; }
th { text-align:left; background:#eef2f4; white-space:normal; }
td,th { border-bottom:1px solid var(--line); padding:10px 9px; vertical-align:top; min-width:65px; }
td:first-child { min-width:130px; }
td a { overflow-wrap:anywhere; }
img { display:block; max-width:100%; height:auto; margin:25px 0; }
.note-source { font-size:13px; color:var(--muted); margin-top:-12px; }
.files { columns:2; column-gap:35px; font-size:14px; }
.files li { break-inside:avoid; }
footer { color:var(--muted); border-top:1px solid var(--line); padding:20px 28px; font-size:13px; }
@media(max-width:700px) { header,main { padding-inline:16px; } nav { position:static; padding-inline:16px; } header h1 { font-size:26px; } .files { columns:1; } }
@media print { nav { position:static; } body { font:10pt/1.5 Georgia,serif; } header h1 { font-size:24pt; } section { margin:22px 0; } table { font-size:8pt; } .table-wrap { overflow:visible; } pre { white-space:pre-wrap; } a { color:inherit; } }
"""


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lot",type=int,choices=[1,2],default=1)
    args=parser.parse_args()
    notes=NOTES if args.lot==1 else NOTES_LOT2
    out=ROOT/"livrables"
    out.mkdir(exist_ok=True)
    rendered=[]
    provenance=[]
    for key,label,filename in notes:
        path=ROOT/"recherche"/filename
        if not path.is_file():
            raise SystemExit(f"Note attendue absente : {path}")
        text=path.read_text(encoding="utf-8")
        body=markdown.markdown(text,extensions=["tables","fenced_code","toc"])
        body=re.sub(r'id="([^\"]+)"',lambda m:f'id="{key}-{m.group(1)}"',body)
        body=re.sub(r'href="#([^\"]+)"',lambda m:f'href="#{key}-{m.group(1)}"',body)
        body=body.replace("<table>",'<div class="table-wrap"><table>').replace("</table>","</table></div>")
        # Relocaliser les liens relatifs des notes, sans modifier leurs sources.
        body=re.sub(r'href="(?!https?://|#|/)([^\"]+\.md(?:#[^\"]*)?)"',r'href="../recherche/\1"',body)
        rendered.append(f'<section id="n{key}">{body}<p class="note-source"><a href="../recherche/{filename}">Source Markdown de cette note</a></p></section>')
        provenance.append({"fichier":path.relative_to(ROOT).as_posix(),"sha256":hashlib.sha256(path.read_bytes()).hexdigest()})
    files=sorted(p for d in ["data/france","data/international","data/risques","sources"] for p in (ROOT/d).glob("*") if p.suffix in (".csv",".json",".md"))
    if args.lot==2:
        files=[p for p in files if re.match(r"04[a-d]_|04_manifestes_cache\.|registre_04[a-d]\.",p.name) or (p.parent==ROOT/"data/risques" and "lot2" in p.name)]
    downloads="\n".join(f'<li><a href="../{p.relative_to(ROOT).as_posix()}">{html.escape(p.relative_to(ROOT).as_posix())}</a></li>' for p in files)
    nav="\n".join(f'<a href="#n{k}">{html.escape(l)}</a>' for k,l,_ in notes)+"<a href=\"#fichiers\">Données et registres</a>"
    title="Emploi public et comparaison internationale" if args.lot==1 else "Comparer les fonctions, définir les réformes"
    intro=("Premier dossier de données, de sources et de méthodes. Il réunit la cartographie française, les départs, les coûts documentés, les métiers et les premières séries harmonisées." if args.lot==1 else
           "Deuxième dossier de recherche : fiscalité, service public de l'emploi, éducation, sécurité, justice, santé, protection sociale et fonctions support. Il distingue écarts bruts, corrections de périmètre, besoins et potentiel réformable.")
    previous="" if args.lot==1 else '<p><a href="dossier_recherche_lot1.html">Consulter le premier dossier : cartographie française et bases internationales</a></p>'
    content='''<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>'''+title+''' — dossier de recherche</title><style>'''+CSS+'''</style></head>
<body><header><div class="date">Mission La France est-elle suradministrée · Recherche arrêtée au 28 octobre 2026</div>
<h1>'''+title+'''</h1>
<p>'''+intro+'''</p>
<p><strong>Le diagnostic national et le plan chiffré restent à construire.</strong> Les écarts bruts présentés ne démontrent pas des sureffectifs. Les données manquantes et les hypothèses sont signalées dans chaque note.</p>
<p><a href="../SUIVI_MISSION.md">État de la mission et prochaines étapes</a></p>'''+previous+'''</header>
<nav aria-label="Sommaire"><div>'''+nav+'''</div></nav><main>'''+"\n".join(rendered)+f'''
<section id="fichiers"><h1>Données et registres de sources</h1>
<p>Les tableaux conservent leurs unités, champs, années et localisations. Les PDF volumineux restent dans le cache local ; leurs URL et empreintes figurent dans les registres.</p>
<ul class="files">{downloads}</ul></section></main>
<footer>Assemblage reproductible : scripts/build_dossier_recherche.py. Le manifeste associé donne les empreintes des notes assemblées. Ce dossier intermédiaire ne remplace pas le rapport final prévu par le cahier des charges.</footer>
</body></html>'''
    target=out/f"dossier_recherche_lot{args.lot}.html"
    target.write_text(content,encoding="utf-8")
    manifest={"date":"2026-10-28","lot":args.lot,"notes":provenance,"sha256_html":hashlib.sha256(target.read_bytes()).hexdigest()}
    if args.lot==2:
        manifest["donnees_liees"]=[{"fichier":p.relative_to(ROOT).as_posix(),"sha256":hashlib.sha256(p.read_bytes()).hexdigest()} for p in files]
        images=set(re.findall(r'<img[^>]+src="([^\"]+)"',"\n".join(rendered)))
        manifest["images"]=[{"fichier":(out/ref).resolve().relative_to(ROOT).as_posix(),"sha256":hashlib.sha256((out/ref).read_bytes()).hexdigest()} for ref in sorted(images) if not re.match(r"https?:",ref)]
    target.with_suffix(".manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"{len(notes)} notes assemblées, {len(files)} fichiers liés, {target.stat().st_size} octets")


if __name__=="__main__":
    main()
