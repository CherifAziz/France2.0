#!/usr/bin/env python3
"""Archive les corps HTTP primaires du lot05, compresses sans perte.

python scripts/05_collecte_sources.py [ID ...] [--refresh]
Les PDF sont dans le cache ignore. Les manifestes et URL permettent de
restaurer le cache. Aucun telechargement n'est execute. Requests et pypdf.
"""
from __future__ import annotations
import argparse, csv, gzip, hashlib, json, re, sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from html.parser import HTMLParser
from io import BytesIO
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
LOCAL_DEPS=ROOT/'.cache/python_deps'
if LOCAL_DEPS.is_dir(): sys.path.append(str(LOCAL_DEPS))
import requests
from pypdf import PdfReader
RAW=ROOT/'data/raw/05'
CACHE=ROOT/'data/cache/05'
CAT=ROOT/'sources/05_catalogue_sources.json'

class HTMLText(HTMLParser):
    def __init__(self): super().__init__(convert_charrefs=True); self.parts=[]; self.hidden=0
    def handle_starttag(self,tag,attrs):
        if tag in ['script','style','noscript']: self.hidden+=1
        if not self.hidden and tag in ['p','div','br','li','tr','h1','h2','h3','h4']: self.parts.append('\n')
    def handle_endtag(self,tag):
        if tag in ['script','style','noscript'] and self.hidden: self.hidden-=1
    def handle_data(self,data):
        if not self.hidden: self.parts.append(data)
    def text(self): return re.sub(r'\n[ \t]*\n+', '\n\n',''.join(self.parts))

def archive(source,refresh=False):
    sid=source['id']; meta_path=RAW/(sid+'.meta.json')
    if meta_path.exists() and not refresh:
        old=json.loads(meta_path.read_text(encoding='utf-8'))
        body_path=ROOT/old.get('local_path','missing')
        if body_path.is_file() and old.get('http_status')==200: return old
    meta=dict(source)
    meta.update(date_consultation=datetime.now(timezone.utc).date().isoformat(),retrieved_at_utc=datetime.now(timezone.utc).isoformat())
    try:
        r=requests.get(source['url'],timeout=(12,45),headers={'User-Agent':'France2.0 independent documentary audit','Accept-Encoding':'identity'})
        body=r.content
        allowed_headers={'content-type','content-length','content-encoding','etag','last-modified','date','content-disposition'}
        safe_headers={k:v for k,v in r.headers.items() if k.lower() in allowed_headers}
        meta.update(http_status=r.status_code,final_url=r.url,content_type=r.headers.get('Content-Type',''),response_headers=safe_headers,body_bytes=len(body),sha256_body=hashlib.sha256(body).hexdigest())
        pdf=body.startswith(b'%PDF-')
        ext='.pdf' if pdf else '.csv' if 'csv' in meta['content_type'] or (',' in body[:100].decode('utf-8',errors='ignore') and 'html' not in meta['content_type']) else '.html'
        dest=CACHE/(sid+ext) if pdf else RAW/(sid+ext+'.gz')
        archived=body if pdf else gzip.compress(body,mtime=0)
        dest.write_bytes(archived)
        meta.update(local_path=dest.relative_to(ROOT).as_posix(),sha256_stored=hashlib.sha256(archived).hexdigest(),archive_format='identity PDF' if pdf else 'gzip lossless response.content, accept-encoding identity')
        if pdf:
            reader=PdfReader(BytesIO(body)); texts=[p.extract_text() or '' for p in reader.pages]
            txt='\n\n'.join(f'=== PDF PAGE {i} ===\n{s}' for i,s in enumerate(texts,1))
            meta['pages_pdf']=len(texts)
        else:
            if ext=='.html':
                parser=HTMLText(); parser.feed(body.decode(r.encoding or 'utf-8',errors='replace')); txt=parser.text()
            else: txt=body.decode('utf-8-sig',errors='replace')
        textpath=(CACHE if pdf else RAW)/(sid+'.txt')
        textpath.write_text(txt,encoding='utf-8',newline='\n')
        meta['text_path']=textpath.relative_to(ROOT).as_posix()
        meta['conversion']='pypdf with physical page markers' if pdf else 'HTMLParser standard library' if ext=='.html' else 'utf-8'
        expected_pdf='.pdf' in source['url'].split('?')[0].lower()
        meta['expected_pdf']=expected_pdf
        meta['acces']='integral' if r.status_code==200 and len(txt)>200 and (not expected_pdf or pdf) else 'inaccessible'
        if expected_pdf and not pdf: meta['error']='PDF attendu ; reponse non PDF archivee comme corps HTTP, non utilisable comme rapport.'
    except Exception as exc:
        meta['error']=f'{type(exc).__name__}: {exc}'; meta['acces']='inaccessible'
    meta_path.write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
    return meta

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('ids',nargs='*'); ap.add_argument('--refresh',action='store_true'); args=ap.parse_args()
    RAW.mkdir(parents=True,exist_ok=True); CACHE.mkdir(parents=True,exist_ok=True)
    catalog=json.loads(CAT.read_text(encoding='utf-8'))
    selected=[s for s in catalog if not args.ids or s['id'] in args.ids]
    with ThreadPoolExecutor(max_workers=6) as pool:
        fs={pool.submit(archive,s,args.refresh):s['id'] for s in selected}
        for f in as_completed(fs):
            m=f.result(); print(m['id'],m.get('http_status','ERROR'),m.get('body_bytes',''),m.get('acces'),m.get('error',''),flush=True)
    manifests=[json.loads(p.read_text(encoding='utf-8')) for p in sorted(RAW.glob('*.meta.json'))]
    (ROOT/'sources/05_manifestes.json').write_text(json.dumps(manifests,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
    cols=['id','titre','institution','date_publication','url','date_consultation','acces','sha256_16','notes']
    with (ROOT/'sources/registre_05.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=cols,lineterminator='\n');w.writeheader()
        by_id={s['id']:s for s in catalog}
        for m in manifests:
            row={k:m.get(k,'') for k in cols}; row['sha256_16']=m.get('sha256_body','')[:16]
            row['notes']=f"Cas {m['cas']}; HTTP {m.get('http_status','')}; {m.get('local_path','')}; corpsSHA256={m.get('sha256_body','')}; stockageSHA256={m.get('sha256_stored','')}; {m.get('error','')}"
            source=by_id.get(m['id'],{})
            if m.get('acces')!='integral' and source.get('preuve_web_local'):
                proof=ROOT/source['preuve_web_local']
                assert proof.is_file(),proof
                row['acces']=source.get('acces_web','partiel')
                row['sha256_16']=hashlib.sha256(proof.read_bytes()).hexdigest()[:16]
                row['notes']+=' ; '+source.get('note_web','')+' ; SHA16=preuve connectée '+source['preuve_web_local']
            w.writerow(row)

if __name__=='__main__':main()
