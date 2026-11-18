import unittest

from check_internal_links import github_heading_slug, heading_anchors, resolve_heading_anchor, resolve_target


class InternalLinkAnchorTests(unittest.TestCase):
    def test_github_heading_slug_punctuation_and_case(self):
        self.assertEqual(github_heading_slug("My **Spatial** Analysis (2026)!"), "my-spatial-analysis-2026")

    def test_duplicate_headings_receive_numeric_suffixes(self):
        text = """# Methods
## Methods
## Methods
"""
        self.assertEqual(heading_anchors(text), {"methods", "methods-1", "methods-2"})

    def test_explicit_html_anchor_is_recognized(self):
        self.assertIn("custom-target", heading_anchors('<a id="custom-target"></a>'))

    def test_fenced_code_is_not_a_heading(self):
        fence = chr(96) * 3
        text = "# Actual\\n" + fence + "md\\n# Not a heading\\n" + fence + "\\n"
        self.assertEqual(heading_anchors(text), {"actual"})

    def test_same_page_fragment_resolves_to_source(self):
        import tempfile
        from pathlib import Path
        import check_internal_links as checker

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            file_path = root / "guide.md"
            file_path.write_text("""# Heading
""", encoding="utf-8")
            old_root = checker.ROOT
            checker.ROOT = root
            try:
                target, anchor = resolve_heading_anchor("guide.md", "#heading")
                self.assertEqual(target, file_path.resolve())
                self.assertEqual(anchor, "heading")
                self.assertEqual(resolve_target("guide.md", "#heading"), file_path.resolve())
            finally:
                checker.ROOT = old_root


if __name__ == "__main__":
    unittest.main()
