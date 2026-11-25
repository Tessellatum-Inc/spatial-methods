import unittest
import numpy as np

from explorations.radar.simulate_matched_strata_equal_block_contrast import (
    equal_stratum_block_contrast,
    equal_eligible_block_mean,
    draw_pixel_noise,
)


class MatchedStrataEstimandTests(unittest.TestCase):
    def test_pixel_noise_is_reproducible_and_finite(self):
        first = draw_pixel_noise(np.random.default_rng(17), 100, 1.2)
        second = draw_pixel_noise(np.random.default_rng(17), 100, 1.2)
        np.testing.assert_array_equal(first, second)
        self.assertTrue(np.isfinite(first).all())

    def test_pixel_noise_rejects_invalid_parameters(self):
        with self.assertRaises(ValueError):
            draw_pixel_noise(np.random.default_rng(1), 10, 1.0, degrees_freedom=2)

    def test_strata_are_equally_weighted_not_pixel_weighted(self):
        # The second stratum may contain many more pixels; the block estimand
        # is the arithmetic mean of its within-stratum contrasts.
        self.assertEqual(equal_stratum_block_contrast([1.0, 9.0]), 5.0)

    def test_blocks_are_equally_weighted(self):
        # A block with many more underlying pixels receives no extra weight.
        self.assertEqual(equal_eligible_block_mean([2.0, 10.0]), 6.0)

    def test_empty_or_nonfinite_strata_are_rejected(self):
        with self.assertRaises(ValueError):
            equal_stratum_block_contrast([])
        with self.assertRaises(ValueError):
            equal_stratum_block_contrast([1.0, np.nan])

    def test_empty_or_nonfinite_block_population_is_rejected(self):
        with self.assertRaises(ValueError):
            equal_eligible_block_mean([])
        with self.assertRaises(ValueError):
            equal_eligible_block_mean([1.0, np.inf])


if __name__ == "__main__":
    unittest.main()
