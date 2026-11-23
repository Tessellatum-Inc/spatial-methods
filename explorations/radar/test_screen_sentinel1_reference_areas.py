import unittest

import numpy as np

from screen_sentinel1_reference_areas import distribution, erode_binary


class ReferenceAreaScreenTests(unittest.TestCase):
    def test_erode_binary_removes_edges_and_preserves_interior(self):
        mask = np.zeros((9, 9), dtype=bool)
        mask[1:8, 1:8] = True
        result = erode_binary(mask, iterations=2)
        self.assertEqual(int(result.sum()), 9)
        self.assertTrue(result[3:6, 3:6].all())

    def test_erode_binary_empty_and_zero_iterations(self):
        mask = np.zeros((4, 4), dtype=bool)
        self.assertFalse(erode_binary(mask, iterations=1).any())
        np.testing.assert_array_equal(erode_binary(mask, iterations=0), mask)

    def test_erode_binary_rejects_invalid_input(self):
        with self.assertRaises(ValueError):
            erode_binary(np.ones(4), iterations=1)

    def test_distribution_reports_db_quantiles(self):
        result = distribution(np.array([0.1, 1.0, 10.0], dtype=np.float32))
        self.assertEqual(result["valid_pixels"], 3)
        self.assertAlmostEqual(result["median_db"], 0.0, places=9)


if __name__ == "__main__":
    unittest.main()
