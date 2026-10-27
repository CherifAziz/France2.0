"""Equipe 04 - extrait la liste des indicateurs ISORA (CL_ISORA_TAX) en CSV code,libelle.
Usage: python3 -I 04_isora_codelist.py cl.xml out.csv"""
import sys, re, csv
import xml.etree.ElementTree as ET
ns = {'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure',
      'com': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common'}
tree = ET.parse(sys.argv[1])
out = csv.writer(open(sys.argv[2], 'w', newline=''))
out.writerow(['codelist', 'code', 'name'])
for cl in tree.iter('{%s}Codelist' % ns['str']):
    cid = cl.get('id')
    if cid not in ('CL_ISORA_TAX', 'CL_JURISDICTION'):
        continue
    for c in cl.iter('{%s}Code' % ns['str']):
        n = c.find('com:Name', ns)
        out.writerow([cid, c.get('id'), (n.text or '').strip() if n is not None else ''])
