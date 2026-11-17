import json
from pathlib import Path
import tempfile
import unittest

from check_ci_coverage import audit_coverage


class CICoverageTests(unittest.TestCase):
    def make_repo(self, base: Path):
        (base / ".github" / "workflows").mkdir(parents=True)
        (base / "scripts").mkdir()
        (base / "implementations" / "python" / "alpha").mkdir(parents=True)
        (base / "notebooks").mkdir()
        (base / ".github" / "workflows" / "python-tests.yml").write_text(
            "run: python scripts/run_python_package_tests.py\\n", encoding="utf-8"
        )
        (base / "scripts" / "execute_learning_notebooks.py").write_text(
            "NOTEBOOKS = [('lesson.ipynb', 120)]\\n", encoding="utf-8"
        )
        (base / "notebooks" / "lesson.ipynb").write_text("{}", encoding="utf-8")
        package = base / "implementations" / "python" / "alpha"
        (package / "README.md").write_text("# Alpha\\n", encoding="utf-8")
        (package / "test_alpha.py").write_text("def test_ok(): pass\\n", encoding="utf-8")
        (base / "scripts" / "python-ci-packages.json").write_text(
            json.dumps([{"directory": "implementations/python/alpha", "pythonpath": ""}]),
            encoding="utf-8",
        )

    def test_complete_manifest_passes(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_repo(root)
            errors, packages, notebooks = audit_coverage(root)
            self.assertEqual(errors, [])
            self.assertEqual((packages, notebooks), (1, 1))

    def test_unregistered_package_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_repo(root)
            (root / "implementations/python/beta").mkdir()
            errors, _, _ = audit_coverage(root)
            self.assertTrue(any("missing from CI" in error and "beta" in error for error in errors))

    def test_missing_readme_and_test_fail(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_repo(root)
            package = root / "implementations/python/alpha"
            (package / "README.md").unlink()
            (package / "test_alpha.py").unlink()
            errors, _, _ = audit_coverage(root)
            self.assertTrue(any("README is missing" in error for error in errors))
            self.assertTrue(any("no top-level test module" in error for error in errors))

    def test_invalid_import_path_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_repo(root)
            manifest = root / "scripts/python-ci-packages.json"
            manifest.write_text(json.dumps([{
                "directory": "implementations/python/alpha",
                "pythonpath": "../missing-package",
            }]), encoding="utf-8")
            errors, _, _ = audit_coverage(root)
            self.assertTrue(any("import path does not exist" in error for error in errors))

    def test_duplicate_manifest_entry_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_repo(root)
            manifest = root / "scripts/python-ci-packages.json"
            entry = {"directory": "implementations/python/alpha", "pythonpath": ""}
            manifest.write_text(json.dumps([entry, entry]), encoding="utf-8")
            errors, _, _ = audit_coverage(root)
            self.assertTrue(any("occur more than once" in error for error in errors))

    def test_missing_notebook_reference_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_repo(root)
            (root / "notebooks" / "extra.ipynb").write_text("{}", encoding="utf-8")
            errors, _, _ = audit_coverage(root)
            self.assertTrue(any("Learning notebooks missing from CI" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
