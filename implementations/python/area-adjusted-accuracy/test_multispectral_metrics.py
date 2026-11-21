import unittest

import numpy as np

from multispectral_metrics import (
    apply_valid_mask, index_stack, mndwi, ndvi, ndbi, ndre,
    ndwi_mcfeeters, safe_normalized_difference, scl_valid_mask,
    summarize_window,
)


class SpectralIndexTests(unittest.TestCase):
    def test_ndvi_known_values(self):
        result = ndvi(np.array([0.8, 0.2]), np.array([0.2, 0.2]))
        np.testing.assert_allclose(result, [0.6, 0.0])

    def test_all_named_indices(self):
        self.assertAlmostEqual(float(ndwi_mcfeeters([0.6], [0.2])[0]), 0.5)
        self.assertAlmostEqual(float(mndwi([0.6], [0.2])[0]), 0.5)
        self.assertAlmostEqual(float(ndbi([0.6], [0.2])[0]), 0.5)
        self.assertAlmostEqual(float(ndre([0.6], [0.2])[0]), 0.5)

    def test_zero_denominator_and_nonfinite_inputs_become_nan(self):
        result = safe_normalized_difference([0.0, np.nan, 0.3], [0.0, 0.2, np.inf])
        self.assertTrue(np.isnan(result).all())

    def test_scl_mask_excludes_cloud_shadow_cloud_cirrus_and_nodata(self):
        classes = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
        expected = np.array([False, False, True, False, True, True, True,
                             False, False, False, False, False])
        np.testing.assert_array_equal(scl_valid_mask(classes), expected)

    def test_mask_applied_to_index(self):
        result = apply_valid_mask(ndvi([0.8, 0.8], [0.2, 0.2]), [True, False])
        self.assertTrue(np.isfinite(result[0]))
        self.assertTrue(np.isnan(result[1]))

    def test_index_stack_only_returns_indices_with_required_bands(self):
        bands = {"B08": [0.8], "B04": [0.2], "B03": [0.4]}
        result = index_stack(bands)
        self.assertEqual(set(result), {"NDVI", "NDWI"})
        self.assertAlmostEqual(float(result["NDVI"][0]), 0.6)

    def test_window_summary_ignores_nodata_and_masked_pixels(self):
        result = summarize_window([[1, 2], [3, np.nan]], [[True, True], [False, True]])
        self.assertEqual(result["pixel_count"], 4)
        self.assertEqual(result["valid_pixel_count"], 2)
        self.assertEqual(result["valid_fraction"], 0.5)
        self.assertEqual(result["median"], 1.5)

    def test_empty_window_summary_is_explicit(self):
        result = summarize_window([[np.nan, np.nan]])
        self.assertEqual(result["valid_pixel_count"], 0)
        self.assertTrue(np.isnan(result["mean"]))


if __name__ == "__main__":
    unittest.main()
