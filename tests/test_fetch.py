"""Contrôles de conservation des preuves, sans accès réseau."""
import hashlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

spec=importlib.util.spec_from_file_location("fetch_source",Path(__file__).resolve().parents[1]/"scripts/fetch.py")
fetch=importlib.util.module_from_spec(spec)
spec.loader.exec_module(fetch)


def response(content,code=200,mime="text/html; charset=utf-8"):
    r=fetch.requests.Response()
    r.status_code=code
    r.url="https://example.test/source"
    r.headers["Content-Type"]=mime
    r.raw=io.BytesIO(content)
    r.encoding="utf-8"
    return r


class FetchEvidenceTests(unittest.TestCase):
    def test_archive_and_digest_match_original_bytes(self):
        original=b"<html><body><h1>Source</h1><p>42 agents</p></body></html>"
        with tempfile.TemporaryDirectory() as d,patch.object(fetch.requests,"get",return_value=response(original)):
            m=fetch.fetch("https://example.test/source","preuve",d)
            self.assertEqual(m["acces"],"integral")
            self.assertEqual(m["sha256"],hashlib.sha256(original).hexdigest())
            self.assertEqual((Path(d)/"preuve.html").read_bytes(),original)
            self.assertIn("42 agents",(Path(d)/"preuve.txt").read_text(encoding="utf-8"))

    def test_changed_download_preserves_original_file_and_manifest(self):
        with tempfile.TemporaryDirectory() as d:
            with patch.object(fetch.requests,"get",return_value=response(b"<html>Version A</html>")):
                fetch.fetch("https://example.test/source","preuve",d)
            old=(Path(d)/"preuve.meta.json").read_bytes()
            with patch.object(fetch.requests,"get",return_value=response(b"<html>Version B</html>")):
                m=fetch.fetch("https://example.test/source","preuve",d)
            self.assertEqual(m["acces"],"inaccessible")
            self.assertEqual((Path(d)/"preuve.html").read_bytes(),b"<html>Version A</html>")
            self.assertEqual((Path(d)/"preuve.meta.json").read_bytes(),old)
            self.assertEqual(len(list(Path(d).glob("*.attempt-*.meta.json"))),1)

    def test_http_200_incapsula_is_not_document_access(self):
        body=b'<html><script src="/_Incapsula_Resource?challenge"></script><body></body></html>'
        with tempfile.TemporaryDirectory() as d,patch.object(fetch.requests,"get",return_value=response(body)):
            self.assertEqual(fetch.fetch("https://example.test/source","preuve",d)["acces"],"inaccessible")

    def test_error_status_remains_failure_even_with_readable_body(self):
        with tempfile.TemporaryDirectory() as d,patch.object(fetch.requests,"get",return_value=response(b"not found",404,"text/plain")):
            m=fetch.fetch("https://example.test/source","preuve",d)
            self.assertEqual(m["acces"],"inaccessible")
            self.assertEqual(Path(m["raw_path"]).suffix,".txt")

    def test_rejects_non_http_and_path_traversal(self):
        for url,name in [("file:///C:/secret","preuve"),("https://example.test/source","../preuve")]:
            with self.assertRaises(ValueError):
                fetch.fetch(url,name,"unused")


if __name__=="__main__":
    unittest.main()
