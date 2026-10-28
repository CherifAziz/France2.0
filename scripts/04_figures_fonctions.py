#!/usr/bin/env python3
"""Figure descriptive du lot 2, issue directement du classeur DREES 2026."""
import os
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT/".cache/python_deps"))
os.environ.setdefault("MPLCONFIGDIR",str(ROOT/".cache/matplotlib"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from openpyxl import load_workbook


def main():
    book=load_workbook(ROOT/"data/raw/04c/drees_cns2026_part3.xlsx",read_only=True,data_only=True)
    tab=book["F28 - Tab 1"]
    columns=list("CDEFGH")
    years=[str(tab[f"{c}4"].value) for c in columns]
    plt.rcParams.update({"font.family":"DejaVu Sans","font.size":11,"svg.hashsalt":"france2-04"})
    fig,ax=plt.subplots(figsize=(11,6.4),layout="constrained")
    bottom=[0.]*len(columns)
    for row,label,color in [(5,"Sécurité sociale","#326783"),(10,"Administrations centrales","#9fc3d2"),(6,"Complémentaires privées","#c57842")]:
        values=[tab[f"{c}{row}"].value/1000 for c in columns]
        ax.bar(range(len(columns)),values,bottom=bottom,label=label,color=color,width=.58)
        bottom=[x+y for x,y in zip(bottom,values)]
    for i,total in enumerate(bottom):
        ax.text(i,total+.2,f"{total:.2f}".replace(".",","),ha="center",fontsize=11)
    ax.set_xticks(range(len(columns)),years)
    ax.set_ylim(0,20.5)
    ax.set_ylabel("Milliards d’euros courants")
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x,_:f"{x:.1f}".replace(".",",")))
    ax.set_title("Les frais de gestion de la santé couvrent des acteurs publics et privés",loc="left",fontsize=15,pad=30)
    ax.text(0,1.02,"2025 : 17,62 Md€, dont 9,18 Md€ pour les complémentaires privées (52,1 %)",transform=ax.transAxes,color="#495a65",fontsize=11)
    ax.spines[["top","right"]].set_visible(False)
    ax.yaxis.grid(True,color="#e7ecef")
    ax.set_axisbelow(True)
    ax.legend(loc="upper left",frameon=False,ncols=3,fontsize=10)
    fig.text(.01,-.045,"Source : DREES, Comptes de la santé 2026, données 2025, fiche 28, tableau 1. Années sélectionnées, espacements non proportionnels au temps.\nIl s’agit de dépenses de gestion du système de santé, pas d’effectifs administratifs ni d’économies réalisables.",fontsize=9,color="#495a65")
    out=ROOT/"figures";out.mkdir(exist_ok=True)
    for suffix in ["png","svg"]:
        extra={"metadata":{"Date":None}} if suffix=="svg" else {}
        fig.savefig(out/f"04_gestion_sante_public_prive.{suffix}",dpi=160,bbox_inches="tight",facecolor="white",**extra)
    plt.close(fig);book.close()
    print("Figure santé produite (PNG et SVG)")


if __name__=="__main__":
    main()
