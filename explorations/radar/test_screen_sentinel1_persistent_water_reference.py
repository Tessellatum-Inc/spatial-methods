"""Offline tests for the JRC persistent-water reference screen."""
import importlib.util
from pathlib import Path
import unittest

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "explorations" / "radar" / "screen_sentinel1_persistent_water_reference.py"
SPEC = importlib.util.spec_from_file_location("screen_sentinel1_persistent_water_reference", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class PersistentWaterReferenceTests(unittest.TestCase):
    def test_threshold_and_two_pixel_erosion(self):
        occurrence = np.zeros((9, 9), dtype=np.uint8)
        occurrence[2:7, 2:7] = 100
        valid = np.ones((9, 9), dtype=bool)
        candidate, core = MODULE.build_occurrence_masks(occurrence, valid, 95, 2)
        self.assertEqual(int(candidate.sum()), 25)
        self.assertEqual(int(core.sum()), 1)
        self.assertTrue(core[4, 4])

    def test_nodata_and_invalid_pixels_are_excluded(self):
        occurrence = np.full((5, 5), 100, dtype=np.uint8)
        occurrence[0, 0] = 255
        valid = np.ones((5, 5), dtype=bool)
        valid[1, 1] = False
        candidate, core = MODULE.build_occurrence_masks(occurrence, valid, 95, 0)
        self.assertFalse(candidate[0, 0])
        self.assertFalse(candidate[1, 1])
        self.assertEqual(int(candidate.sum()), 23)
        self.assertTrue(np.array_equal(candidate, core))

    def test_rejects_mismatched_shapes_and_bad_thresholds(self):
        with self.assertRaisesRegex(ValueError, "matching 2D"):
            MODULE.build_occurrence_masks(np.ones((2, 2)), np.ones((3, 3), dtype=bool))
        with self.assertRaisesRegex(ValueError, "between 1 and 100"):
            MODULE.build_occurrence_masks(np.ones((2, 2)), np.ones((2, 2), dtype=bool), 101)

    def test_erode_mask_rejects_negative_iterations(self):
        with self.assertRaisesRegex(ValueError, "cannot be negative"):
            MODULE.erode_mask(np.ones((3, 3), dtype=bool), -1)


if __name__ == "__main__":
    unittest.main()
