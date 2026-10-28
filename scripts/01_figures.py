#!/usr/bin/env python3
"""Figures statistiques issues exclusivement des CSV du chantier 01."""
import csv
import os
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
deps=ROOT/".cache/python_deps"
if deps.is_dir():
    sys.path.append(str(deps))
os.environ["MPLCONFIGDIR"]=str(ROOT/".cache/matplotlib")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

OUT=ROOT/"figures"
OUT.mkdir(exist_ok=True)
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":10,"axes.spines.top":False,"axes.spines.right":False})


def rows(name):
    with (ROOT/"data/france"/name).open(encoding="utf-8",newline="") as f:
        return list(csv.DictReader(f))


def main():
    base=[r for r in rows("01_effectifs_versions.csv") if r["id"].startswith("DGAFP_2024_") and r["categorie"]=="hors contrats aidés" and r["versant"]!="FP"]
    values={r["versant"]:float(r["valeur"]) for r in base}
    fig,ax=plt.subplots(figsize=(9,4.6),layout="constrained")
    labels=["État (FPE)","Territoriale (FPT)","Hospitalière (FPH)"]
    vals=[values[v]/1e6 for v in ("FPE","FPT","FPH")]
    ax.barh(labels[::-1],vals[::-1],color="#245574",height=.58)
    ax.set(xlim=(0,3.1),xlabel="Effectifs au 31 décembre (millions de personnes physiques)",ylabel="Versant",
           title="Emploi dans la fonction publique française fin 2024")
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x,p:f"{x:.1f}".replace(".",",")))
    for y,v in enumerate(vals[::-1]):
        ax.text(v+.04,y,f"{v:.3f} M".replace(".",","),va="center")
    fig.get_layout_engine().set(rect=(0,.14,1,.84))
    fig.text(.03,.035,"Source : DGAFP, RA 2026, vue effectifs, figure 2. France hors Mayotte, hors contrats aidés.\nCes effectifs couvrent tous les métiers ; ils ne mesurent pas les seuls emplois administratifs.",fontsize=8,color="#444444")
    fig.savefig(OUT/"01_effectifs_versants.png",dpi=170)
    plt.close(fig)

    data=rows("01_effectifs_serie_2011_2024.csv")
    fig,ax=plt.subplots(figsize=(9,4.8),layout="constrained")
    for versant,color,style in [("FPE","#245574","-"),("FPT","#96632F","-"),("FPH","#487A69","-"),("FP","#202830","--")]:
        s=sorted((r for r in data if r["versant"]==versant),key=lambda r:int(r["annee"]))
        years=[int(r["annee"]) for r in s]
        values=[float(r["valeur"])/float(s[0]["valeur"])*100 for r in s]
        ax.plot(years,values,label="Ensemble FP" if versant=="FP" else versant,color=color,linestyle=style,linewidth=2)
    ax.set(xlabel="Année",ylabel="Effectifs physiques, indice 100 en 2011",title="Évolution des effectifs publics : série rétropolée DGAFP")
    ax.set_xticks([2011,2014,2017,2020,2024])
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x,p:f"{x:.0f}"))
    ax.grid(axis="y",alpha=.18)
    ax.legend(frameon=False,loc="upper left")
    fig.get_layout_engine().set(rect=(0,.14,1,.84))
    fig.text(.03,.035,"Source : DGAFP, RA 2026, complément effectifs FP, figure 5. 2011–2024.\nFrance hors Mayotte, hors contrats aidés. Retraitement publié ; ne pas raccorder aux anciens niveaux non rétropolés.",fontsize=8,color="#444444")
    fig.savefig(OUT/"01_effectifs_serie.png",dpi=170)
    plt.close(fig)
    print("Deux figures exportées dans figures/01_effectifs_*.png")


if __name__=="__main__":
    main()
