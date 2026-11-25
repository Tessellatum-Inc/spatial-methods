import unittest
import numpy as np
from explorations.radar.simulate_tree_built_label_error import (
    apply_label_confusion, class_mae_contrast, equal_mean, one_realization,
    paired_factorial_interaction
)


class LabelErrorTests(unittest.TestCase):
    def test_zero_confusion_preserves_labels(self):
        labels = np.array(["T", "B", "T", "B"])
        out = apply_label_confusion(labels, np.random.default_rng(3), 0, 0)
        np.testing.assert_array_equal(out, labels)

    def test_confusion_is_reproducible(self):
        labels = np.array(["T"] * 500 + ["B"] * 500)
        a = apply_label_confusion(labels, np.random.default_rng(8), .2, .1)
        b = apply_label_confusion(labels, np.random.default_rng(8), .2, .1)
        np.testing.assert_array_equal(a, b)

    def test_ambiguity_increases_flip_probability(self):
        labels = np.array(["T"] * 5000)
        ambiguity = np.concatenate([np.zeros(2500), np.ones(2500)])
        observed = apply_label_confusion(
            labels, np.random.default_rng(31), .1, .1,
            ambiguity=ambiguity, ambiguity_multiplier=3.0)
        low_flip = np.mean(observed[:2500] == "B")
        high_flip = np.mean(observed[2500:] == "B")
        self.assertGreater(high_flip, low_flip + .15)

    def test_ambiguity_shape_and_range_are_validated(self):
        with self.assertRaises(ValueError):
            apply_label_confusion(["T", "B"], np.random.default_rng(1),
                                  .1, .1, ambiguity=[0.2])
        with self.assertRaises(ValueError):
            apply_label_confusion(["T"], np.random.default_rng(1),
                                  .1, .1, ambiguity=[1.2])

    def test_confusion_rejects_invalid_probabilities(self):
        with self.assertRaises(ValueError):
            apply_label_confusion(["T"], np.random.default_rng(1), 1.1, 0)

    def test_class_mae_contrast_uses_labels_not_pixel_weights_between_strata(self):
        self.assertAlmostEqual(class_mae_contrast(
            ["T", "T", "B", "B"], [2, 4, 1, 1], min_class_pixels=2), 2.0)

    def test_missing_class_support_returns_none(self):
        self.assertIsNone(class_mae_contrast(["T", "T"], [1, 2]))

    def test_equal_mean_rejects_empty_and_nonfinite(self):
        with self.assertRaises(ValueError):
            equal_mean([])
        with self.assertRaises(ValueError):
            equal_mean([1, np.nan])

    def test_factorial_interaction_uses_paired_difference_in_differences(self):
        out = paired_factorial_interaction(
            [0.0, 1.0], [1.0, 2.0], [2.0, 3.0], [4.0, 6.0])
        np.testing.assert_allclose(out, [1.0, 2.0])

    def test_factorial_interaction_rejects_unpaired_shapes(self):
        with self.assertRaises(ValueError):
            paired_factorial_interaction([0.0], [0.0, 1.0],
                                         [0.0], [0.0])

    def test_factorial_cells_share_paired_latent_target(self):
        kwargs = {"tree_to_built": .1, "built_to_tree": .1}
        neutral = one_realization(np.random.default_rng(2026), **kwargs)
        label_only = one_realization(np.random.default_rng(2026),
                                     ambiguity_label_error=True, **kwargs)
        residual_only = one_realization(np.random.default_rng(2026),
                                        ambiguity_residual_effect=True, **kwargs)
        joint = one_realization(np.random.default_rng(2026),
                                ambiguity_sensitive=True, **kwargs)
        self.assertEqual(neutral[0], label_only[0])
        self.assertEqual(residual_only[0], joint[0])
        self.assertEqual(neutral[2], label_only[2])
        self.assertEqual(neutral[2], residual_only[2])
        self.assertEqual(neutral[2], joint[2])

    def test_generator_is_reproducible(self):
        a = one_realization(np.random.default_rng(9))
        b = one_realization(np.random.default_rng(9))
        self.assertEqual(a, b)


if __name__ == "__main__":
    unittest.main()
