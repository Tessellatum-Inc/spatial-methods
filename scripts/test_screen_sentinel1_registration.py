"""Tests for Sentinel-1 global phase-correlation screening."""
from __future__ import annotations
import importlib.util
from pathlib import Path
import unittest
import numpy as np

SCRIPT = Path(__file__).resolve().parents[1] / "explorations/radar/screen_sentinel1_registration.py"
SPEC = importlib.util.spec_from_file_location("screen_sentinel1_registration", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class PhaseCorrelationTests(unittest.TestCase):
    def test_identical_images_have_near_zero_shift(self):
        rng = np.random.default_rng(42)
        image = rng.normal(size=(128,128)).astype(np.float32)
        result = MODULE.phase_correlation(image, image, np.ones(image.shape, dtype=bool))
        self.assertLess(result["shift_magnitude_pixels"], 0.01)

    def test_translation_is_recovered(self):
        rng = np.random.default_rng(7)
        noise = rng.normal(size=(128,128)).astype(np.float32)
        image = (noise + np.roll(noise,1,0) + np.roll(noise,-1,0) + np.roll(noise,1,1) + np.roll(noise,-1,1)) / 5.0
        moving = np.roll(np.roll(image, 2, axis=0), -3, axis=1)
        result = MODULE.phase_correlation(image, moving, np.ones(image.shape, dtype=bool))
        shift = result["estimated_shift_pixels"]
        self.assertAlmostEqual(abs(shift["x"]), 3.0, delta=0.1)
        self.assertAlmostEqual(abs(shift["y"]), 2.0, delta=0.1)

    def test_rejects_mismatched_shapes(self):
        with self.assertRaises(ValueError):
            MODULE.phase_correlation(np.zeros((32,32)), np.zeros((32,31)), np.ones((32,32),bool))

    def test_rejects_insufficient_common_pixels(self):
        valid = np.zeros((32,32), dtype=bool)
        with self.assertRaises(ValueError):
            MODULE.phase_correlation(np.zeros((32,32)), np.zeros((32,32)), valid)


if __name__ == "__main__":
    unittest.main()
