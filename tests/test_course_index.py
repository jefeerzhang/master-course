from html.parser import HTMLParser
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "index.html"
CSS = ROOT / "assets" / "course-index.css"
FIRST_PRINCIPLES_PAGE = ROOT / "第一性原理" / "index.html"


class IndexParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.heading_stack = []
        self.headings = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if tag in {"h1", "h2", "h3"}:
            self.heading_stack.append([tag, []])

    def handle_data(self, data):
        if self.heading_stack:
            self.heading_stack[-1][1].append(data)

    def handle_endtag(self, tag):
        if self.heading_stack and self.heading_stack[-1][0] == tag:
            heading_tag, chunks = self.heading_stack.pop()
            self.headings.append((heading_tag, "".join(chunks).strip()))


def parse_index():
    parser = IndexParser()
    parser.feed(PAGE.read_text(encoding="utf-8"))
    return parser


def class_tokens(attrs):
    return attrs.get("class", "").split()


class CourseIndexTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.parser = parse_index()

    def test_page_matches_the_academic_site_contract(self):
        self.assertTrue(CSS.exists())
        self.assertIn('href="assets/course-index.css"', self.html)
        self.assertIn('<link rel="canonical" href="https://jefeerzhang.github.io/master-course/">', self.html)
        self.assertNotIn("fonts.googleapis.com", self.html)
        self.assertEqual(
            [text for tag, text in self.parser.headings if tag == "h1"],
            ["硕士课程"],
        )
        for tag in ("nav", "main", "footer"):
            self.assertEqual(sum(1 for current, _ in self.parser.tags if current == tag), 1)

    def test_all_three_course_destinations_are_preserved(self):
        links = {
            attrs.get("href")
            for tag, attrs in self.parser.tags
            if tag == "a"
        }
        self.assertTrue(
            {"第一性原理/", "research-methods/", "yuan-yunfen-writing/"}.issubset(links)
        )
        cards = [
            attrs
            for tag, attrs in self.parser.tags
            if tag == "article" and "course-card" in class_tokens(attrs)
        ]
        self.assertEqual(len(cards), 3)

    def test_course_cards_use_existing_visual_assets(self):
        expected = {
            "yuan-yunfen-writing/md2_skeleton.png": (900, 900),
            "research-methods/md1_path.png": (900, 900),
            "第一性原理/第一性原理配图/01_概念三层分解.jpeg": (756, 806),
        }
        images = {
            attrs.get("src"): (int(attrs.get("width")), int(attrs.get("height")))
            for tag, attrs in self.parser.tags
            if tag == "img"
        }
        self.assertEqual(images, expected)
        for source in expected:
            self.assertTrue((ROOT / source).exists(), source)

    def test_styles_are_responsive_and_accessible(self):
        css = CSS.read_text(encoding="utf-8")
        for contract in (
            ":focus-visible",
            "@media (max-width: 760px)",
            "@media (prefers-reduced-motion: reduce)",
            "grid-template-columns: repeat(12",
            "--accent: #245642",
        ):
            self.assertIn(contract, css)


class FirstPrinciplesNavigationTests(unittest.TestCase):
    def test_page_links_back_to_the_course_index(self):
        html = FIRST_PRINCIPLES_PAGE.read_text(encoding="utf-8")
        parser = IndexParser()
        parser.feed(html)
        matches = [
            attrs
            for tag, attrs in parser.tags
            if tag == "a" and "course-back-link" in class_tokens(attrs)
        ]
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].get("href"), "../index.html")
        self.assertIn("返回硕士课程", html)
        for contract in (
            ".course-back-link:focus-visible",
            "@media screen and (max-width: 500px)",
            "@media (prefers-reduced-motion: reduce)",
        ):
            self.assertIn(contract, html)


if __name__ == "__main__":
    unittest.main()
