from html.parser import HTMLParser
from pathlib import Path
import unittest

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "yuan-yunfen-writing" / "index.html"
PDF = ROOT / "yuan-yunfen-writing" / "sample-thesis.pdf"


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.links.append(dict(attrs))


class YuanThesisDownloadTests(unittest.TestCase):
    def test_pdf_is_valid_and_complete(self):
        self.assertTrue(PDF.exists())
        self.assertEqual(PDF.read_bytes()[:5], b"%PDF-")
        reader = PdfReader(PDF)
        self.assertFalse(reader.is_encrypted)
        self.assertEqual(len(reader.pages), 94)

    def test_page_exposes_a_download_link(self):
        html = PAGE.read_text(encoding="utf-8")
        parser = LinkParser()
        parser.feed(html)
        matches = [link for link in parser.links if link.get("href") == "sample-thesis.pdf"]
        self.assertEqual(len(matches), 1)
        self.assertIn("download", matches[0])
        self.assertEqual(matches[0].get("class"), "download-link")
        self.assertIn("下载论文 PDF", html)
        self.assertIn("数字乡村建设背景下雅安市名山区农村集体“三资”管理问题及对策研究", html)


if __name__ == "__main__":
    unittest.main()
