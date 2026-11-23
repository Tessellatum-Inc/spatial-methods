import json
from pathlib import Path
import tempfile
import unittest

from lock_visual_review import REQUIRED_FIELDS
from visual_review import DECISION_FIELDS, image_stem, load_split


class VisualReviewTests(unittest.TestCase):
    def test_decision_template_matches_lock_utility_schema(self):
        self.assertEqual(DECISION_FIELDS, REQUIRED_FIELDS)

    def test_loads_control_checkpoint_and_excluded_roles(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "split.json"
            path.write_text(json.dumps({
                "selection": {
                    "control_points": ["209", "108"],
                    "checkpoint_points": ["101", "206"],
                    "excluded_low_observation_points": {"102": 4, "303": 3},
                }
            }), encoding="utf-8")
            roles = load_split(path)
            self.assertEqual(roles["209"], "control")
            self.assertEqual(roles["101"], "checkpoint")
            self.assertEqual(roles["102"], "excluded")
            self.assertEqual(len(roles), 6)

    def test_rejects_point_in_multiple_roles(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "split.json"
            path.write_text(json.dumps({
                "selection": {
                    "control_points": ["206"],
                    "checkpoint_points": ["206"],
                    "excluded_low_observation_points": {},
                }
            }), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "more than one split"):
                load_split(path)

    def test_rejects_excluded_point_also_in_control_or_checkpoint_set(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "split.json"
            path.write_text(json.dumps({
                "selection": {
                    "control_points": ["209"],
                    "checkpoint_points": [],
                    "excluded_low_observation_points": {"209": 3},
                }
            }), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "also appears in split"):
                load_split(path)

    def test_image_stem_adds_dataset_prefix_only_when_needed(self):
        self.assertEqual(image_stem("0101_0031"), "EB-02-00761_0101_0031")
        self.assertEqual(
            image_stem("EB-02-00761_0101_0031"),
            "EB-02-00761_0101_0031",
        )


if __name__ == "__main__":
    unittest.main()
