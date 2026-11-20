import json
import tempfile
import unittest
from pathlib import Path

from validate_knowledge_catalog import validate_catalog


class KnowledgeCatalogTests(unittest.TestCase):
    def build_fixture(self, root: Path) -> None:
        catalog = root / "catalog"
        (catalog / "schemas").mkdir(parents=True)
        (root / "content").mkdir()
        (root / "content" / "sample.md").write_text("# Sample\n", encoding="utf-8")
        (catalog / "master-subject-index.md").write_text("| SM-FND-001 | Mathematics |\n", encoding="utf-8")
        (catalog / "schemas" / "knowledge-record.schema.json").write_text(
            json.dumps({"$schema": "https://json-schema.org/draft/2020-12/schema", "type": "object"}),
            encoding="utf-8",
        )
        record = {
            "record_id": "SM-KB-000001",
            "title": "Sample record",
            "kind": "foundation",
            "canonical_path": "content/sample.md",
            "subject_ids": ["SM-FND-001"],
            "summary": "A sufficiently detailed sample record summary.",
            "status": "curated",
            "relationships": [],
            "evidence_refs": ["content/sample.md"],
        }
        (catalog / "knowledge-records.jsonl").write_text(json.dumps(record) + "\n", encoding="utf-8")
        (catalog / "knowledge-graph-reference-positioning-measurement.csv").write_text(
            "source_id,relationship,target_id,evidence_path,relationship_basis,qualification\n",
            encoding="utf-8",
        )

    def test_minimal_valid_catalogue_passes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.build_fixture(root)
            self.assertEqual(validate_catalog(root), [])

    def test_review_kind_is_supported(self):\n        with tempfile.TemporaryDirectory() as directory:\n            root = Path(directory)\n            self.build_fixture(root)\n            record_path = root / "catalog" / "knowledge-records.jsonl"\n            record = json.loads(record_path.read_text(encoding="utf-8"))\n            record["kind"] = "review"\n            record_path.write_text(json.dumps(record) + "\\n", encoding="utf-8")\n            self.assertEqual(validate_catalog(root), [])\n\n    def test_unknown_subject_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.build_fixture(root)
            record_path = root / "catalog" / "knowledge-records.jsonl"
            record = json.loads(record_path.read_text(encoding="utf-8"))
            record["subject_ids"] = ["SM-FND-999"]
            record_path.write_text(json.dumps(record) + "\n", encoding="utf-8")
            self.assertTrue(any("unknown subject_id" in error for error in validate_catalog(root)))

    def test_missing_canonical_file_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.build_fixture(root)
            record_path = root / "catalog" / "knowledge-records.jsonl"
            record = json.loads(record_path.read_text(encoding="utf-8"))
            record["canonical_path"] = "content/missing.md"
            record_path.write_text(json.dumps(record) + "\n", encoding="utf-8")
            self.assertTrue(any("canonical file does not exist" in error for error in validate_catalog(root)))

    def test_duplicate_record_id_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.build_fixture(root)
            record_path = root / "catalog" / "knowledge-records.jsonl"
            line = record_path.read_text(encoding="utf-8")
            record_path.write_text(line + line, encoding="utf-8")
            self.assertTrue(any("Duplicate record_id" in error for error in validate_catalog(root)))


if __name__ == "__main__":
    unittest.main()
