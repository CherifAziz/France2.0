#!/usr/bin/env python3
"""Contrôle descriptif des extractions héritées, sans modifier les bruts.

Usage : python -I scripts/04_audit_raw.py --date 2026-10-28
Ne certifie ni la complétude des API ni la comparabilité des statistiques.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET_ISO3 = set("FRA DEU ITA ESP PRT BEL NLD CHE AUT GBR IRL SWE DNK NOR FIN POL EST CAN USA AUS NZL JPN KOR".split())
TARGET_EURO = set("FR DE IT ES PT BE NL CH AT UK IE SE DK NO FI PL EE EU27_2020".split())
API_CHECKS = {
    "gov_10a_main": {"geo": "FR", "sector": "S13", "unit": "PC_GDP", "na_item": "D1PAY", "time": "2024"},
    "crim_just_job": {"geo": "FR", "isco08": "OC5412", "sex": "T", "unit": "NR", "time": "2022"},
    "spr_exp_type": {"geo": "FR", "spdeps": "ADM", "unit": "PC_GDP", "time": "2023"},
}
METADATA_URLS = {
    "gov_10a_main": "https://ec.europa.eu/eurostat/cache/metadata/en/gov_10a_main_esms.htm",
    "crim_just_job": "https://ec.europa.eu/eurostat/cache/metadata/en/crim_sims.htm",
    "spr_exp_type": "https://ec.europa.eu/eurostat/cache/metadata/en/spr_esms.htm",
}


def code(value):
    return (value or "").split(":", 1)[0].strip()


def j(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def numeric(value):
    try:
        return math.isfinite(float(value))
    except (ValueError, TypeError):
        return False


def source_for(name, rows):
    if name.startswith("eurostat_"):
        dataset = name.removeprefix("eurostat_").removesuffix(".csv")
        return "Eurostat", "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/" + dataset
    if name.startswith("isora_"):
        return "FMI / ISORA", "https://api.imf.org/external/sdmx/2.1/data/ISORA,ISORA_LATEST_DATA_PUB,5.0.0/"
    flow = next((r.get("DATAFLOW", "") for r in rows if r.get("DATAFLOW")), "")
    match = re.fullmatch(r"([^:]+):(.+)\(([^)]+)\)", flow)
    if match:
        agency, dataset, version = match.groups()
        return "OCDE", f"https://sdmx.oecd.org/public/rest/data/{agency},{dataset},{version}/"
    return "", ""


def audit_file(path, consultation_date):
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    decoded = raw.decode("utf-8-sig")
    if not raw or re.match(r"\s*(<!doctype|<html|<\?xml)", decoded, re.I):
        raise ValueError(f"{path.name}: fichier vide ou réponse HTML/XML")
    reader = csv.DictReader(decoded.splitlines(keepends=True))
    headers = reader.fieldnames or []
    rows = list(reader)
    if not rows or not headers:
        raise ValueError(f"{path.name}: absence de tableau")
    hmap = {h.split(":", 1)[0]: h for h in headers}
    year_col = next((hmap[x] for x in ("TIME_PERIOD", "time", "year") if x in hmap), None)
    geo_col = next((hmap[x] for x in ("REF_AREA", "geo", "JURISDICTION", "jurisdiction") if x in hmap), None)
    value_col = next((hmap[x] for x in ("OBS_VALUE", "value") if x in hmap), None)
    if path.name == "isora_codelist.csv":
        dimensions = ["codelist", "code"]
    elif path.name == "isora_selection_long.csv":
        dimensions = ["jurisdiction", "indicator", "year"]
    elif path.name == "isora_FRA_all_indicators.csv":
        dimensions = ["JURISDICTION", "INDICATOR", "FREQUENCY", "TIME_PERIOD"]
    elif path.name.startswith("eurostat_"):
        dimensions = headers[:headers.index("time") + 1]
    else:
        dimensions = headers[1:headers.index(year_col) + 1]
    bad_rows = sum(None in r or any(v is None for v in r.values()) for r in rows)
    exact = Counter(tuple(j(r.get(h, "")) for h in headers) + (j(r.get(None, [])),) for r in rows)
    keys = defaultdict(list)
    for r in rows:
        keys[tuple(code(r.get(d, "")) for d in dimensions)].append(r)
    duplicates = sum(len(items)-1 for items in keys.values())
    conflicting = sum(len({r.get(value_col, "") for r in items}) > 1 for items in keys.values()) if value_col else 0
    years = sorted({r[year_col] for r in rows if r.get(year_col)}) if year_col else []
    countries = sorted({code(r.get(geo_col, "")) for r in rows if r.get(geo_col)}) if geo_col else []
    per_country = {}
    if geo_col and year_col:
        for country in countries:
            selected = [r for r in rows if code(r.get(geo_col)) == country]
            known = sorted({r[year_col] for r in selected if r.get(year_col)})
            per_country[country] = {"n": len(selected), "annees": known}
    unit_dimensions = {}
    for c in ("unit", "UNIT_MEASURE", "UNIT_MULT", "SCALE", "scale", "CURRENCY", "PRICE_BASE", "BASE_PER", "STATISTICAL_OPERATION"):
        if c in hmap:
            unit_dimensions[c] = sorted({r.get(hmap[c], "") for r in rows})
    categorical = Counter(r.get(value_col, "") for r in rows if value_col and not numeric(r.get(value_col)))
    flags = {}
    for c in ("flag", "OBS_STATUS", "OBS_STATUS2", "OBS_STATUS3", "OBS_STATUS4", "OBS_STATUS_2", "OBS_STATUS_3", "CONF_STATUS"):
        if c in hmap:
            flags[c] = dict(Counter(r.get(hmap[c], "") for r in rows))
    institution, source_url = source_for(path.name, rows)
    absent = sorted((TARGET_EURO if path.name.startswith("eurostat_") else TARGET_ISO3) - set(countries)) if geo_col and path.name != "isora_FRA_all_indicators.csv" else []
    warnings = []
    if bad_rows:
        warnings.append("lignes de largeur incohérente")
    if duplicates:
        warnings.append("clés d'observation répétées")
    if year_col and any(not r.get(year_col) for r in rows):
        warnings.append("périodes vides à exclure avant analyse")
    if categorical:
        warnings.append("valeurs non numériques ou manquantes à qualifier")
    if absent:
        warnings.append("pays du groupe cible absents")
    if "6: Millions" in unit_dimensions.get("UNIT_MULT", []):
        warnings.append("multiplicateur 10^6 présent")
    if "3" in unit_dimensions.get("SCALE", []) or "3" in unit_dimensions.get("scale", []):
        warnings.append("échelle ISORA 3 présente, dictionnaire requis")
    if unit_dimensions.get("UNIT_MULT") == [""]:
        warnings.append("UNIT_MULT vide, vérifier métadonnées d'unité")
    if any(code(v) == "SE" for v in unit_dimensions.get("STATISTICAL_OPERATION", [])):
        warnings.append("moyennes et erreurs standard dans le même fichier")
    if path.name.startswith("oecd_") or path.name.startswith("eurostat_"):
        warnings.append("URL de requête originale et horodatage absents")
    result = dict(
        fichier=str(path.relative_to(ROOT)).replace("\\", "/"), octets=len(raw), sha256=digest,
        lignes=len(rows), colonnes=len(headers), lignes_malformees=bad_rows,
        doublons_exacts=sum(n-1 for n in exact.values()), doublons_cles=duplicates,
        cles_valeurs_contradictoires=conflicting, cles_observation=j(dimensions),
        repartition_dimensions=j({d: dict(Counter(code(r.get(d, "")) for r in rows)) for d in dimensions}),
        annees=j(years), lignes_sans_annee=sum(not r.get(year_col) for r in rows) if year_col else "",
        pays=j(countries), pays_cibles_absents=j(absent), couverture_par_pays=j(per_country),
        dimensions_unites=j(unit_dimensions), valeurs_non_numeriques=j(dict(categorical)),
        statuts_observations=j(flags), alertes=" ; ".join(warnings),
        source_url=source_url, source_localisation=str(path.relative_to(ROOT)).replace("\\", "/") + "; CSV intégral",
        annee="-".join((years[0], years[-1])) if years else "", statut="[FAIT]",
    )
    registry = dict(
        id="04C_"+path.stem, titre="Extraction héritée : "+path.name, institution=institution,
        date_publication="", url=source_url, date_consultation=consultation_date,
        acces="integral", sha256_16=digest[:16],
        notes="Fichier local lu intégralement. URL canonique du jeu reconstruite, sans attester la requête de téléchargement originale ni la lecture de ses métadonnées complètes. Date de publication non consignée.",
    )
    dates = sorted({r.get("PUBLICATION_DATE", "") for r in rows} - {""})
    if len(dates) == 1:
        registry["date_publication"] = dates[0].split("T")[0]
        registry["notes"] = registry["notes"].replace("Date de publication non consignée.", "Date PUBLICATION_DATE intégrée au CSV, sans vérification indépendante de cette date.")
    return result, registry


def verify_api(consultation_date, refresh=False):
    """Trois contrôles ponctuels. Les instantanés ne remplacent pas les bruts hérités."""
    folder = ROOT / "data/raw/04_controle"
    results, registry = [], []
    for dataset, filters in API_CHECKS.items():
        path = folder / (dataset + "_FR_temoin.json")
        url = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/" + dataset + "?" + urllib.parse.urlencode({"lang": "en", **filters})
        if refresh:
            request = urllib.request.Request(url, headers={"User-Agent": "France20-research-audit/1.0"})
            with urllib.request.urlopen(request, timeout=30) as response:
                raw = response.read()
            data = json.loads(raw)
            if data.get("class") != "dataset" or not data.get("value"):
                raise ValueError(f"{dataset}: aucune observation témoin reçue")
            folder.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
        if not path.exists():
            continue
        raw = path.read_bytes()
        data = json.loads(raw)
        values = data.get("value", {})
        if isinstance(values, dict):
            values = list(values.values())
        with (ROOT / "data/raw/04" / ("eurostat_" + dataset + ".csv")).open(encoding="utf-8-sig", newline="") as stream:
            candidates = [r for r in csv.DictReader(stream) if all(r.get(k) == v for k, v in filters.items())]
        old = float(candidates[0]["value"]) if len(candidates) == 1 else None
        current = float(values[0]) if len(values) == 1 else None
        match = old is not None and current is not None and math.isclose(old, current, rel_tol=1e-12, abs_tol=1e-12)
        results.append(dict(jeu=dataset, filtres=j(filters), valeur_locale=old, valeur_api=current,
                            correspondance=match, mise_a_jour_api=data.get("updated", ""),
                            source_url=url, source_localisation=str(path.relative_to(ROOT)).replace("\\", "/"),
                            annee=filters["time"], statut="[FAIT]"))
        registry.append(dict(id="04C_API_"+dataset, titre="Contrôle ponctuel API Eurostat : "+dataset,
                             institution="Eurostat", date_publication="", url=url,
                             date_consultation=consultation_date, acces="integral",
                             sha256_16=hashlib.sha256(raw).hexdigest()[:16],
                             notes="Réponse JSON-stat intégrale archivée dans "+str(path.relative_to(ROOT)).replace("\\", "/")+" ; horodatage API : "+data.get("updated", "")))
    return results, registry


def metadata_registry(consultation_date, refresh=False):
    folder = ROOT / "data/raw/04_controle"
    registry = []
    for dataset, url in METADATA_URLS.items():
        path = folder / (dataset + "_metadonnees.html")
        if refresh:
            request = urllib.request.Request(url, headers={"User-Agent": "France20-research-audit/1.0"})
            with urllib.request.urlopen(request, timeout=30) as response:
                raw = response.read()
            folder.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
        if path.exists():
            registry.append(dict(id="04C_META_"+dataset, titre="Métadonnées Eurostat : "+dataset,
                                 institution="Eurostat", date_publication="", url=url,
                                 date_consultation=consultation_date, acces="partiel",
                                 sha256_16=hashlib.sha256(path.read_bytes()).hexdigest()[:16],
                                 notes="Page intégralement archivée ; consultation ciblée des sections 3 et 15, pas validation de toutes les notes nationales. Fichier : "+str(path.relative_to(ROOT)).replace("\\", "/")))
    return registry


def reconcile_isora():
    with (ROOT / "data/raw/04/isora_FRA_all_indicators.csv").open(encoding="utf-8-sig", newline="") as stream:
        index = {(r["INDICATOR"], r["TIME_PERIOD"]): r for r in csv.DictReader(stream)}
    rows = []
    with (ROOT / "data/raw/04/isora_selection_long.csv").open(encoding="utf-8-sig", newline="") as stream:
        for item in csv.DictReader(stream):
            if item["jurisdiction"] != "FRA" or not item["year"]:
                continue
            other = index.get((item["indicator"], item["year"]))
            rows.append(dict(indicateur=item["indicator"], annee=item["year"], valeur_selection=item["value"],
                             valeur_fra_integral=other["OBS_VALUE"] if other else "",
                             meme_valeur=other is not None and other["OBS_VALUE"] == item["value"],
                             meme_echelle=other is not None and other["SCALE"] == item["scale"],
                             source_url="https://api.imf.org/external/sdmx/2.1/data/ISORA,ISORA_LATEST_DATA_PUB,5.0.0/",
                             source_localisation="data/raw/04/isora_selection_long.csv ; data/raw/04/isora_FRA_all_indicators.csv",
                             statut="[FAIT]"))
    write_csv(ROOT / "data/international/04_rapprochement_isora_fra.csv", rows)
    return rows


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", default="2026-10-28", help="Date de consultation ISO, fixée pour la reproductibilité")
    parser.add_argument("--refresh-api", action="store_true", help="Rafraîchir trois observations témoins via Eurostat, sinon relire les instantanés locaux")
    args = parser.parse_args()
    audited, registry = [], []
    for path in sorted((ROOT / "data/raw/04").glob("*.csv")):
        result, source = audit_file(path, args.date)
        audited.append(result)
        registry.append(source)
    if not audited:
        raise SystemExit("Aucun CSV à contrôler")
    write_csv(ROOT / "data/international/04_controle_fichiers.csv", audited)
    checks, api_registry = verify_api(args.date, args.refresh_api)
    registry.extend(api_registry)
    registry.extend(metadata_registry(args.date, args.refresh_api))
    isora_checks = reconcile_isora()
    if checks:
        write_csv(ROOT / "data/international/04_verification_api.csv", checks)
    write_csv(ROOT / "sources/registre_04_controle.csv", registry)
    for row in audited:
        print(f"{Path(row['fichier']).name}: {row['lignes']} lignes, {row['doublons_cles']} clés répétées, {row['lignes_malformees']} lignes malformées")
    print(f"Contrôle local : {len(audited)} fichiers, {sum(r['lignes'] for r in audited)} lignes")
    for check in checks:
        print(f"API {check['jeu']}: local={check['valeur_locale']}, API={check['valeur_api']}, égalité={check['correspondance']}")
    print(f"ISORA France : {len(isora_checks)} observations rapprochées ; {sum(not r['meme_valeur'] or not r['meme_echelle'] for r in isora_checks)} écarts")


if __name__ == "__main__":
    main()
