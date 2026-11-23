import json
import unittest
from unittest.mock import patch

import fiji_case_study


CONFUSION_COUNTS = [
    [84, 6, 3, 0, 0, 1, 1, 5],
    [0, 90, 0, 0, 0, 1, 2, 7],
    [11, 4, 53, 1, 3, 15, 2, 11],
    [4, 0, 26, 44, 4, 9, 5, 8],
    [0, 0, 0, 1, 55, 18, 17, 9],
    [0, 0, 3, 2, 6, 70, 15, 4],
    [0, 0, 1, 0, 1, 19, 55, 24],
    [0, 1, 0, 0, 0, 2, 12, 119],
]


def fixture_geojson():
    features = []
    sequence = 0
    for stratum, row in enumerate(CONFUSION_COUNTS, start=1):
        for reference_class, count in enumerate(row, start=1):
            for _ in range(count):
                sequence += 1
                features.append({
                    "type": "Feature",
                    "properties": {"strata": stratum, "ref_class": reference_class},
                    "geometry": {"type": "Point", "coordinates": [float(sequence), 0.0]},
                })
    return json.dumps({"type": "FeatureCollection", "features": features}).encode("utf-8")


class FijiCaseStudyTests(unittest.TestCase):
    def test_fixture_reproduces_audited_case_results(self):
        data = fixture_geojson()
        expected_sha = fiji_case_study.git_blob_sha1(data)
        with patch.object(fiji_case_study, "EXPECTED_GIT_BLOB_SHA1", expected_sha):
            report = fiji_case_study.analyse(data, "test_fixture")

        self.assertEqual(report["dataset"]["feature_count"], 834)
        self.assertEqual(report["dataset"]["unique_point_coordinates"], 834)
        self.assertEqual(report["dataset"]["sample_allocation_observed"]["tree"], 134)
        self.assertIn("133", report["dataset"]["allocation_documentation_discrepancy"])
        self.assertAlmostEqual(report["raw_count_summary"]["overall_accuracy"], 570 / 834)
        self.assertAlmostEqual(
            report["design_adjusted_estimates"]["overall_accuracy"]["estimate"],
            0.8250512585270284,
        )
        self.assertIsNotNone(
            report["design_adjusted_estimates"]["finite_population_correction_by_mapped_class"]
        )

    def test_rejects_dataset_blob_that_does_not_match_pinned_identity(self):
        data = fixture_geojson()
        with patch.object(fiji_case_study, "EXPECTED_GIT_BLOB_SHA1", "0" * 40):
            with self.assertRaises(ValueError):
                fiji_case_study.analyse(data, "test_fixture")

    def test_rejects_unknown_class_codes(self):
        collection = json.loads(fixture_geojson())
        collection["features"][0]["properties"]["strata"] = 99
        data = json.dumps(collection).encode("utf-8")
        with patch.object(
            fiji_case_study, "EXPECTED_GIT_BLOB_SHA1", fiji_case_study.git_blob_sha1(data)
        ):
            with self.assertRaises(ValueError):
                fiji_case_study.analyse(data, "test_fixture")

    def test_rejects_nonpoint_geometry(self):
        collection = json.loads(fixture_geojson())
        collection["features"][0]["geometry"]["type"] = "Polygon"
        data = json.dumps(collection).encode("utf-8")
        with patch.object(
            fiji_case_study, "EXPECTED_GIT_BLOB_SHA1", fiji_case_study.git_blob_sha1(data)
        ):
            with self.assertRaises(ValueError):
                fiji_case_study.analyse(data, "test_fixture")


if __name__ == "__main__":
    unittest.main()
