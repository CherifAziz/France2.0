#!/usr/bin/env python3
"""Assemble les chapitres Markdown du rapport en un document unique (Markdown, HTML, DOCX, PDF).

Usage : python3 scripts/build_rapport.py [--pdf]
Entrées : rapport/[0-9][0-9]_*.md (ordre lexicographique), synthese/synthese.md
Sorties : livrables/rapport_complet.{md,html,docx,pdf}, livrables/synthese.{html,docx,pdf}
"""
import glob
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "livrables")
CSS = os.path.join(ROOT, "scripts", "rapport.css")


def pandoc(src, dst, title, extra=()):
    cmd = ["pandoc", src, "-o", dst, "--standalone", "--toc", "--toc-depth=2",
           "--metadata", f"title={title}", "--metadata", "lang=fr", "--resource-path", ROOT]
    if dst.endswith(".html"):
        cmd += ["--css", os.path.relpath(CSS, OUT), "--embed-resources"]
    cmd += list(extra)
    subprocess.run(cmd, check=True, cwd=ROOT)


def html_to_pdf(html, pdf):
    js = f"""
const {{ chromium }} = require('playwright');
(async () => {{
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://{html}', {{ waitUntil: 'networkidle' }});
  await p.pdf({{ path: '{pdf}', format: 'A4', printBackground: true,
    margin: {{ top: '18mm', bottom: '18mm', left: '16mm', right: '16mm' }},
    displayHeaderFooter: true, headerTemplate: '<span></span>',
    footerTemplate: '<div style="font-size:8px;width:100%;text-align:center;color:#666"><span class="pageNumber"></span> / <span class="totalPages"></span></div>' }});
  await b.close();
}})();"""
    subprocess.run(["node", "-e", js], check=True)


def main():
    os.makedirs(OUT, exist_ok=True)
    chapters = sorted(glob.glob(os.path.join(ROOT, "rapport", "[0-9][0-9]_*.md")))
    full = os.path.join(OUT, "rapport_complet.md")
    with open(full, "w", encoding="utf-8") as f:
        for c in chapters:
            f.write(open(c, encoding="utf-8").read().rstrip() + "\n\n")
    title = ("La France est-elle suradministrée ? Comparaison internationale, audit des effectifs publics "
             "et potentiel de transformation de l'État à l'ère de l'intelligence artificielle")
    pandoc(full, os.path.join(OUT, "rapport_complet.html"), title)
    pandoc(full, os.path.join(OUT, "rapport_complet.docx"), title)
    syn = os.path.join(ROOT, "synthese", "synthese.md")
    if os.path.exists(syn):
        pandoc(syn, os.path.join(OUT, "synthese.html"), "Synthèse — La France est-elle suradministrée ?")
        pandoc(syn, os.path.join(OUT, "synthese.docx"), "Synthèse — La France est-elle suradministrée ?")
    if "--pdf" in sys.argv:
        html_to_pdf(os.path.join(OUT, "rapport_complet.html"), os.path.join(OUT, "rapport_complet.pdf"))
        if os.path.exists(syn):
            html_to_pdf(os.path.join(OUT, "synthese.html"), os.path.join(OUT, "synthese.pdf"))
    print("ok", [os.path.basename(c) for c in chapters])


if __name__ == "__main__":
    main()
