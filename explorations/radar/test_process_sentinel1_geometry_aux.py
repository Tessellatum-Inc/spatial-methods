"""Offline tests for local incidence angle processing."""
import importlib.util
from pathlib import Path
import unittest

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
PATH = ROOT / "explorations" / "radar" / "process_sentinel1_geometry_aux.py"
SPEC = importlib.util.spec_from_file_location("process_sentinel1_geometry_aux", PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class LocalIncidenceAngleTests(unittest.TestCase):
    def test_payload_requests_angle_and_mask_on_fixed_grid(self):
        feature = {"properties": {"datetime": "2026-11-14T03:11:11Z"}}
        payload = MODULE.build_angle_payload(feature)
        self.assertEqual(payload["output"]["width"], 2048)
        self.assertEqual(payload["output"]["height"], 1536)
        self.assertIn("localIncidenceAngle", payload["evalscript"])
        self.assertIn("dataMask", payload["evalscript"])
        self.assertTrue(payload["input"]["data"][0]["processing"]["orthorectify"])

    def test_summarizes_valid_angles(self):
        angles = np.array([[30, 31], [32, 33]], dtype=np.float32)
        valid = np.array([[1, 1], [1, 0]], dtype=bool)
        report = MODULE.summarize_angle(angles, valid)
        self.assertEqual(report["valid_pixels"], 3)
        self.assertEqual(report["median_degrees"], 31.0)

    def test_rejects_no_valid_pixels(self):
        with self.assertRaisesRegex(ValueError, "No valid"):
            MODULE.summarize_angle(np.zeros((2, 2)), np.zeros((2, 2), dtype=bool))

    def test_rejects_angles_outside_documented_range(self):
        with self.assertRaisesRegex(ValueError, "0–180"):
            MODULE.summarize_angle(np.array([[181.0]]), np.array([[True]]))

    def test_rejects_grid_shape_mismatch(self):
        with self.assertRaisesRegex(ValueError, "matching 2D"):
            MODULE.summarize_angle(np.zeros((2, 2)), np.ones((2, 3), dtype=bool))


if __name__ == "__main__":
    unittest.main()
