#!/usr/bin/env python3
"""Archive une source et sa preuve d'accès. Les téléchargements ne sont jamais exécutés.

python scripts/fetch.py URL nom --out-dir data/cache/01
PDF : pdftotext -layout si disponible, sinon pypdf (repères de pages explicites).
HTML : html2text si disponible, sinon HTMLParser de la bibliothèque standard.
Les replis sont enregistrés dans le manifeste, jamais dissimulés.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

import requests

# Dépendances facultatives installées localement, sans modifier le Python de la machine.
LOCAL_DEPS = Path(__file__).resolve().parents[1] / ".cache" / "python_deps"
if LOCAL_DEPS.is_dir():
    sys.path.append(str(LOCAL_DEPS))


class ReadableHTML(HTMLParser):
    """Repli sans dépendance : texte et destinations des liens, sans script/style."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.hidden = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript"):
            self.hidden += 1
        if not self.hidden:
            if tag in ("p", "div", "br", "tr", "li", "h1", "h2", "h3", "h4"):
                self.parts.append("\n")
            if tag == "a":
                dest = dict(attrs).get("href")
                if dest:
                    self.parts.append(f" [{dest}] ")

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript") and self.hidden:
            self.hidden -= 1

    def handle_data(self, data):
        if not self.hidden:
            self.parts.append(data)

    def get_text(self):
        return re.sub(r"\n[ \t]*\n[ \t]*\n+", "\n\n", "".join(self.parts))


def convert_html(html):
    try:
        import html2text
    except ImportError:
        parser = ReadableHTML()
        parser.feed(html)
        return parser.get_text(), "html.parser (repli, html2text absent)"
    converter = html2text.HTML2Text()
    converter.body_width = 0
    converter.ignore_links = False
    return converter.handle(html), "html2text"


def guess_extension(content, content_type, url):
    if content.startswith(b"%PDF-"):
        return ".pdf"
    if content.startswith(b"PK\x03\x04"):
        return ".xlsx" if urlsplit(url).path.lower().endswith(".xlsx") else ".zip"
    if "html" in content_type or content.lstrip().lower().startswith((b"<!doctype html", b"<html")):
        return ".html"
    if "json" in content_type:
        return ".json"
    if "csv" in content_type:
        return ".csv"
    if "xml" in content_type:
        return ".xml"
    if "text/plain" in content_type:
        return ".txt"
    suffix = Path(urlsplit(url).path).suffix.lower()
    return suffix if suffix in (".txt", ".csv", ".json", ".xml", ".xlsx", ".ods", ".zip") else ".bin"


def fetch(url, name, out_dir, timeout=45, max_mb=100):
    if urlsplit(url).scheme not in ("http", "https"):
        raise ValueError("Seules les URL HTTP(S) sont acceptées")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", name) or ".." in name:
        raise ValueError("Nom court invalide (lettres ASCII, chiffres, tirets et underscores)")
    directory = Path(out_dir)
    directory.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc)
    meta = {"source_url": url, "date_consultation": now.date().isoformat(), "retrieved_at_utc": now.isoformat()}
    try:
        with requests.get(url, timeout=timeout, stream=True,
                          headers={"User-Agent": "France2.0-recherche/1.0 (audit documentaire)"}) as response:
            meta.update(http_status=response.status_code, final_url=response.url,
                        content_type=response.headers.get("Content-Type", ""),
                        last_modified=response.headers.get("Last-Modified"), etag=response.headers.get("ETag"))
            chunks, size = [], 0
            for chunk in response.iter_content(chunk_size=65536):
                size += len(chunk)
                if size > max_mb * 1024 * 1024:
                    raise ValueError(f"Source supérieure à la limite de {max_mb} Mio")
                chunks.append(chunk)
            content = b"".join(chunks)
            meta["encoding"] = response.encoding
        ext = guess_extension(content, meta["content_type"], meta["final_url"])
        raw = directory / (name + ext)
        # Ne pas modifier silencieusement un instantané déjà cité.
        if raw.exists() and raw.read_bytes() != content:
            raise FileExistsError(f"Instantané différent déjà présent : {raw}. Choisir un autre nom.")
        raw.write_bytes(content)
        meta.update(raw_path=str(raw), bytes=len(content), sha256=hashlib.sha256(content).hexdigest())
        meta["acces"] = "integral" if 200 <= meta["http_status"] < 300 else "inaccessible"
        if ext == ".html" and len(content) < 4096 and b"_Incapsula_Resource" in content:
            meta.update(acces="inaccessible", erreur="Défi Incapsula : HTTP 200 ne donne pas accès au document demandé")
        if ext == ".pdf" and meta["acces"] == "integral":
            from pypdf import PdfReader
            reader = PdfReader(raw)
            meta["pages"] = len(reader.pages)
            converter = shutil.which("pdftotext")
            if converter:
                plain = subprocess.run([converter, "-layout", "-enc", "UTF-8", str(raw), "-"],
                                       check=True, capture_output=True).stdout.decode("utf-8")
                plain = "\n".join(f"[PAGE {i}]\n{p}" for i, p in enumerate(plain.split("\f"), 1) if p.strip())
                meta["conversion"] = "pdftotext -layout"
            else:
                plain = "\n".join(f"[PAGE {i}]\n{p.extract_text(extraction_mode='layout')}" for i, p in enumerate(reader.pages, 1))
                meta["conversion"] = "pypdf layout (repli, pdftotext absent)"
            raw.with_suffix(".txt").write_text(plain, encoding="utf-8")
        elif ext in (".html", ".json", ".csv", ".xml", ".txt"):
            # requests annonce souvent ISO-8859-1 par défaut pour le HTML UTF-8.
            try:
                plain = content.decode("utf-8-sig")
            except UnicodeDecodeError:
                plain = content.decode(meta.get("encoding") or "windows-1252", errors="replace")
            if ext == ".html":
                plain, meta["conversion"] = convert_html(plain)
            else:
                meta["conversion"] = "décodage texte"
            raw.with_suffix(".txt").write_text(plain, encoding="utf-8")
    except Exception as exc:
        meta.update(acces="inaccessible", erreur=f"{type(exc).__name__}: {exc}")
    target = directory / f"{name}.meta.json"
    if target.exists() and meta["acces"] == "inaccessible":
        # Garder la preuve de la précédente lecture réussie lors d'un échec de réaccès.
        target = directory / f"{name}.attempt-{uuid.uuid4().hex[:12]}.meta.json"
    target.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return meta


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url")
    parser.add_argument("nom")
    parser.add_argument("--out-dir", default="data/cache/sources")
    parser.add_argument("--timeout", type=int, default=45)
    parser.add_argument("--max-mb", type=int, default=100)
    args = parser.parse_args()
    result = fetch(args.url, args.nom, args.out_dir, args.timeout, args.max_mb)
    print(json.dumps(result, ensure_ascii=True))
    return 0 if result["acces"] == "integral" else 1


if __name__ == "__main__":
    raise SystemExit(main())
