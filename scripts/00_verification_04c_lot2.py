#!/usr/bin/env python3
"""Contre-lecture 04c sans importer les fonctions d'extraction de l'auteur."""
import csv
import json
from decimal import Decimal
from pathlib import Path

from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[1]
ROWS = []


def csv_rows(path):
    with (ROOT / path).open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def check(name, year, claimed, source, unit, url, location, note=""):
    ok = abs(Decimal(str(claimed)) - Decimal(str(source))) < Decimal("0.00001")
    ROWS.append(dict(id=f"04C-{len(ROWS)+1:02d}", theme="Santé et protection sociale", indicateur=name,
                     annee=year, valeur_publiee=claimed, valeur_source=source, unite=unit, source_url=url,
                     source_localisation=location, statut_controle="CONFIRME" if ok else "ECART", note=note))


def main():
    costs = csv_rows("data/international/04c_france_couts.csv")
    raw = ROOT / "data/raw/04c/drees_cns2026_part3.xlsx"
    book = load_workbook(raw, read_only=True, data_only=True)
    tab = book["F28 - Tab 1"]
    url = json.loads(raw.with_suffix(".meta.json").read_text(encoding="utf-8"))["source_url"]
    for n in [5,6,7,8,9,10,11,12,13]:
        label, value = tab[f"B{n}"].value, tab[f"H{n}"].value
        selected = [r for r in costs if r["indicateur"] == label and r["annee"] == "2025"]
        assert len(selected) == 1, label
        check(label,2025,selected[0]["valeur"],value,"M EUR courants",url,f"F28 - Tab 1!H{n}","Édition CNS2026, donnée2025; sous-totaux non additifs")
    share = Decimal(str(tab["H6"].value)) / Decimal(str(tab["H13"].value)) * 100
    check("Part OC privée dans la gestion totale",2025,tab["J6"].value,share,"%",url,"F28 - Tab 1!J6 et H6/H13","Part de dépenses de gestion, pas part d'emplois publics")
    check("Identité gestion totale",2025,tab["H13"].value,sum(Decimal(str(tab[f"H{i}"].value)) for i in [5,6,10]),"M EUR courants",url,"F28 - Tab 1!H5+H6+H10","Seuls les trois postes disjoints sont sommés")
    book.close()

    source_path = ROOT / "data/raw/04c/oecd_sha_current_schemes.csv"
    rawrows = csv_rows(str(source_path.relative_to(ROOT)))
    long = csv_rows("data/international/04c_sha_regimes.csv")
    shaurl = json.loads(source_path.with_suffix(".meta.json").read_text(encoding="utf-8"))["source_url"]
    code = lambda r,k: r[k].split(":",1)[0]
    for regime in ["_T","HF1","HF11","HF121","HF122","HF21"]:
        filtered = [r for r in rawrows if code(r,"REF_AREA: Reference area")=="FRA" and r["TIME_PERIOD: Time period"]=="2023"
                    and code(r,"FUNCTION: Health function")=="HC7" and code(r,"FINANCING_SCHEME: Financing scheme")==regime
                    and code(r,"UNIT_MEASURE: Unit of measure")=="XDC" and code(r,"PRICE_BASE: Price base")=="V"]
        target = [r for r in long if r["pays"]=="FRA" and r["annee"]=="2023" and r["fonction"]=="HC7"
                  and r["regime"]==regime and r["unite"]=="XDC" and r["prix"]=="V"]
        assert len(filtered)==len(target)==1,regime
        r = filtered[0]
        check("HC7 " + regime,2023,target[0]["valeur"],r["OBS_VALUE"],"M EUR courants",shaurl,f"FRA;2023;HC7;{regime};XDC;V",
              f"Multiplicateur {code(r,'UNIT_MULT: Unit multiplier')}; HF1 ne signifie pas secteur S13")
    target = ROOT / "data/risques/verification_04c_lot2.csv"
    with target.open("w",encoding="utf-8",newline="") as stream:
        writer=csv.DictWriter(stream,fieldnames=list(ROWS[0])); writer.writeheader(); writer.writerows(ROWS)
    failed = [r for r in ROWS if r["statut_controle"]!="CONFIRME"]
    print(f"04c : {len(ROWS)} contre-lectures, {len(failed)} écarts")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
