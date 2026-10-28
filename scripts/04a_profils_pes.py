#!/usr/bin/env python3
"""Relit des profils SPE et leurs contrôles nationaux, sans convertir staff en ETP.

Python 3 + pypdf. Sources restaurables avec les URL du registre04a et fetch.py.
Ces observations complètent les comptes LMP ; elles ne s'y additionnent pas.
"""
import csv
import json
import re
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
# Dépendances locales facultatives lorsque le script est exécuté avec -I.
if (ROOT/'.cache/python_deps').is_dir():
    sys.path.append(str(ROOT/'.cache/python_deps'))
from pypdf import PdfReader

RAW=ROOT/'data/raw/04a'
CACHE=ROOT/'data/cache/04a'
OUT=ROOT/'data/international'


def source(name,cache=False):
    return json.loads(((CACHE if cache else RAW)/(name+'.meta.json')).read_text(encoding='utf-8'))


def main():
    rows=[]
    def add(country,indicator,value,unit,year,scope,meta,location,status='[FAIT]',note=''):
        rows.append(dict(pays_iso3=country,indicateur=indicator,valeur='' if value is None else value,unite=unit,annee=year,champ=scope,
                         source_url=meta['source_url'],source_localisation=meta['raw_path']+' ; '+location,statut=status,note=note))
    meta=source('world_public_employment_services_2026',True)
    reader=PdfReader(CACHE/'world_public_employment_services_2026.pdf')
    for country,page in [('AUS',309),('FRA',365),('DEU',371),('NLD',401)]:
        text=reader.pages[page-1].extract_text() or ''
        # Texte simple : l'extraction layout déplace certaines colonnes.
        patterns={
            'staff':r'\bStaff\s+([\d,]+|No data)',
            'bureaux':r'\bOffices\s+([\d,]+|No data)',
            'ratio_public_demandeurs_par_staff':r'Seekers per Staff Member\s+([\d,]+|No data)',
            'chomeurs_ilo_milliers':r'Unemployment\s+(\d{4})\s*\(ILO modelled estimate, in thousands\)\s+([\d,.]+|No data)',
            'population_active_potentielle_ilo_milliers':r'Potential Labor Force\s+(\d{4})\s*\(ILO, in thousands\)\s+([\d,.]+|No data)',
        }
        found={}
        for indicator,pattern in patterns.items():
            match=re.search(pattern,text)
            if not match:raise ValueError(f'Champ introuvable {country}/{indicator} à la page{page}')
            year=int(match.group(1)) if 'milliers' in indicator else 2024
            raw=match.group(2) if 'milliers' in indicator else match.group(1)
            value=None if raw=='No data' else float(raw.replace(',',''))
            found[indicator]=(value,year)
            unit='milliers de personnes' if 'milliers' in indicator else 'staff, unité non explicitée dans le profil' if indicator=='staff' else 'bureaux' if indicator=='bureaux' else 'personnes par staff selon la publication'
            add(country,indicator,value,unit,year,'Organisme répondant enquête World of PES2024, pas ensemble harmonisé des acteurs',meta,f'PDF p.{page}, imprimé p.{page-21}',
                '[NON TROUVÉ]' if value is None else '[FAIT]', 'Les prestataires et fonctions assurantielles ne sont pas harmonisés ; ratio publié non assimilable au portefeuille d’un conseiller')
        staff=found['staff'][0]
        unemployed,uy=found['chomeurs_ilo_milliers']
        potential,py=found['population_active_potentielle_ilo_milliers']
        if staff and unemployed is not None and potential is not None and uy==py:
            calculated=(unemployed+potential)*1000/staff
            add(country,'ratio_recalcule_bases_affichees',round(calculated,6),'personnes par staff',uy,'Somme des deux effectifsILO affichés / staff publié',meta,f'PDF p.{page}',
                '[ESTIMATION]', 'Ne réplique pas nécessairement le ratio publié : vintages/champs du calcul original non reconstitués')
    national=[
        ('NLD','uwv2024_comptes',r'2024\|\s*5\.207\|\s*4\.418\|\s*4\.566\|\s*1\.375\|\s*430\|\s*961\|\s*530\|\s*2\.120\|\s*5\|\s*19\.612',2024,
         [('uwv_total_annuel',19612,'ETP annuels moyens','EnsembleUWV'),('uwv_werkbedrijf_annuel',5207,'ETP annuels moyens','Werkbedrijf, brancheemploi'),('uwv_medico_social_annuel',4418,'ETP annuels moyens','Évaluations sociales/médicales'),('uwv_versement_annuel',4566,'ETP annuels moyens','Versement de prestations')], 'Table Gemiddeld aantal fte’s'),
        ('NLD','uwv2024_personnel',r'Totaal\|\s*22\.267\|\s*21\.960',2024,
         [('uwv_total_fin_annee_personnes',22267,'personnes en fin d’année','EnsembleUWV'),('uwv_total_fin_annee_etp',19714,'ETP fin d’année','EnsembleUWV'),('uwv_externes',680,'personnes externes fin d’année','Travailleurs externes'),('uwv_flexibles',421,'personnes fin d’année','Flexkrachten')], 'Tables Aantal medewerkers et Personeelsverloop'),
    ]
    for country,name,pattern,year,observations,location in national:
        text=(RAW/(name+'.txt')).read_text(encoding='utf-8')
        if not re.search(pattern,text):raise ValueError(f'Table nationale modifiée : {name}')
        for indicator,value,unit,scope in observations:
            # Contrôle présence des valeurs, les champs exacts sont localisés par les titres de table.
            if format(value,',').replace(',','.') not in text:raise ValueError(f'Valeur absente : {name}/{value}')
            add(country,indicator,value,unit,year,scope,source(name),location)
    for year,name,expected,observations in [
        (2024,'ba2024_rapport','101.300',[('ba_total_decembre',101300,'TotalBA, arrondi'),('ba_assurance_chomage_services',55300,'Assurance-chômage et services minimumsocial'),('ba_minimum_social',39400,'Grundsicherung'),('ba_prestations_familiales',6500,'Familienkasse')]),
        (2025,'ba2025_rapport','102.896,10',[('ba_total_quatrieme_trimestre',102896.1,'TotalBA'),('ba_assurance_chomage_services',56705.5,'Assurance-chômage et services minimumsocial'),('ba_minimum_social',39278.5,'Grundsicherung'),('ba_prestations_familiales',6912,'Familienkasse')]),
    ]:
        text=(RAW/(name+'.txt')).read_text(encoding='utf-8')
        if expected not in text:raise ValueError(f'TotalBA non retrouvé : {year}')
        for indicator,value,scope in observations:
            add('DEU',indicator,value,'ETP à la date de référence',year,scope,source(name),'Personal der Bundesagentur für Arbeit, tableMitarbeitendenkapazität',note='Périmètre comprenant indemnisation, minimumsocial et allocations familiales ; pas conseillers de placement seuls')
    ftmeta=source('france_travail_2024',True)
    reader=PdfReader(CACHE/'france_travail_2024.pdf')
    pages=[]
    for i,page in enumerate(reader.pages,1):
        text=(page.extract_text() or '').replace('\u00a0',' ').replace('\u202f',' ')
        if re.search(r'55\s*000',text) and ('collaborateurs' in text or 'COLLABORATEURS' in text):pages.append(i)
    if not pages:raise ValueError('Ordre de grandeur55000 collaborateurs non retrouvé')
    add('FRA','france_travail_collaborateurs_arrondi',55000,'collaborateurs, valeur arrondie publiée',2024,'FranceTravail',ftmeta,'PDF pages '+','.join(map(str,pages)),note='Ne fournit pas une unitéETP ni le périmètre de tous les acteurs du réseau pour l’emploi')
    path=OUT/'04a_pes_profils_nationaux.csv'
    with path.open('w',encoding='utf-8',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    print(json.dumps({'observations_profils_et_comptes':len(rows),'pages_france_travail_55000':pages},ensure_ascii=True))


if __name__=='__main__':main()
