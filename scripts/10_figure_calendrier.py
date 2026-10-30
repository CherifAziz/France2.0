#!/usr/bin/env python3
"""Illustration du calendrier implicite ; aucun paramètre national validé."""
import csv
import os
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT/".cache/python_deps"));os.environ.setdefault("MPLCONFIGDIR",str(ROOT/".cache/matplotlib"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def main():
 rows=list(csv.DictReader((ROOT/"data/reformes/10_calendrier_800000_illustration.csv").open(encoding="utf-8",newline="")))
 plt.rcParams.update({"font.family":"DejaVu Sans","font.size":11,"svg.hashsalt":"france2-lot3"})
 fig,ax=plt.subplots(figsize=(10.5,6),layout="constrained")
 for convention,color,legend in [("année pleine","#326783","Année pleine : cumul de 120 Md€"),("départs répartis à mi-année","#c57842","Mi-année : cumul de 100 Md€")]:
  data=[r for r in rows if r["convention"]==convention];x=[int(r["annee"]) for r in data];y=[float(r["economie_brute_illustrative_MdEUR"]) for r in data]
  ax.plot(x,y,marker="o",color=color,label=legend,linewidth=2.3)
  for year,value in zip(x,y):ax.annotate(f"{value:.0f}",(year,value),xytext=(0,10 if convention=="année pleine" else -18),textcoords="offset points",ha="center",color=color)
 ax.set_xticks(x);ax.set_ylim(0,46);ax.set_ylabel("Md€ bruts annuels illustratifs")
 ax.set_title("Un objectif à terme ne produit pas le même montant dès la première année",loc="left",fontsize=14,pad=30)
 ax.text(0,1.02,"Hypothèses : 160 000 recrutements évités par an × 50 000 € implicites ; aucune validation du vivier",transform=ax.transAxes,fontsize=10,color="#53616b")
 ax.spines[["top","right"]].set_visible(False);ax.yaxis.grid(True,color="#e7ecef");ax.set_axisbelow(True);ax.legend(loc="upper left",frameon=False)
 fig.text(.01,-.06,"Source : contre-calcul de l’annonce 40 Md€ / 800 000 postes, budget2027.fr, 28 octobre 2026. Première année 2027 choisie pour l’exemple.\nExercice arithmétique : départs, coûts d’entrée, pensions, GVT, transitions et effets APU non calibrés. Ce graphique n’est pas une prévision.",fontsize=9,color="#53616b")
 out=ROOT/"figures";out.mkdir(exist_ok=True)
 fig.savefig(out/"10_calendrier_illustratif.png",dpi=160,bbox_inches="tight",facecolor="white")
 fig.savefig(out/"10_calendrier_illustratif.svg",bbox_inches="tight",facecolor="white",metadata={"Date":None})
 plt.close(fig);print("Illustration de calendrier produite, PNG/SVG")


if __name__=="__main__":main()
