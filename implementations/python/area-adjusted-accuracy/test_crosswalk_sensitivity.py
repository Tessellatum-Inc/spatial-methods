import tempfile
import unittest
from pathlib import Path

from crosswalk_sensitivity import (
    broad_vegetation_groups,
    load_observations,
    run_sensitivity,
    strict_crosswalk,
    wetland_to_grassland,
)


class CrosswalkSensitivityTests(unittest.TestCase):
    def setUp(self):
        self.rows = [
            {"sampling_stratum": "tree", "map_class": "tree", "reference_class": "tree"},
            {"sampling_stratum": "tree", "map_class": "herbaceous_wetland", "reference_class": "grassland"},
            {"sampling_stratum": "grassland", "map_class": "grassland", "reference_class": "grassland"},
            {"sampling_stratum": "grassland", "map_class": "tree", "reference_class": "tree"},
        ]
        self.weights = {"tree": 0.7, "grassland": 0.3}
        self.populations = {"tree": 70, "grassland": 30}

    def test_transform_definitions(self):
        self.assertEqual(strict_crosswalk("herbaceous_wetland"), "herbaceous_wetland")
        self.assertEqual(wetland_to_grassland("herbaceous_wetland"), "grassland")
        self.assertEqual(broad_vegetation_groups("mangrove"), "woody_cover")
        self.assertEqual(broad_vegetation_groups("shrubland"), "open_vegetation")

    def test_scenarios_preserve_sample_and_change_legend_explicitly(self):
        result = run_sensitivity(self.rows, self.weights, self.populations)
        self.assertEqual(result["sample_size"], 4)
        self.assertEqual([x["scenario_id"] for x in result["scenarios"]], [
            "strict_8_class", "wetland_as_grassland", "broad_vegetation_groups"
        ])
        strict, recoded, broad = result["scenarios"]
        self.assertAlmostEqual(
            strict["worldcover_overall_accuracy"]["estimate"], 0.65
        )
        self.assertAlmostEqual(
            recoded["worldcover_overall_accuracy"]["estimate"], 1.0
        )
        self.assertAlmostEqual(
            broad["worldcover_overall_accuracy"]["estimate"], 1.0
        )
        self.assertAlmostEqual(
            strict["worldcover_minus_original_accuracy_difference"]["estimate"], 0.15
        )

    def test_requires_all_weighted_strata(self):
        with self.assertRaises(ValueError):
            run_sensitivity(self.rows[:2], self.weights)

    def test_csv_loader_requires_expected_columns_and_rows(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.csv"
            path.write_text("sample_id,map_class\\na,tree\\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                load_observations(path)


if __name__ == "__main__":
    unittest.main()
