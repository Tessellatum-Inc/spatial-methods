import unittest
import numpy as np
from explorations.radar.simulate_tree_built_label_error import (
    apply_label_confusion, class_mae_contrast, equal_mean, one_realization
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

    def test_confusion_rejects_invalid_probabilities(self):
        with self.assertRaises(ValueError):
            apply_label_confusion(["T"], np.random.default_rng(1), 1.1, 0)

    def test_class_mae_contrast_uses_labels_not_pixel_weights_between_strata(self):
        self.assertAlmostEqual(class_mae_contrast(
            ["T", "T", "B", "B"], [2, 4, 1, 1]), 2.0)

    def test_missing_class_support_returns_none(self):
        self.assertIsNone(class_mae_contrast(["T", "T"], [1, 2]))

    def test_equal_mean_rejects_empty_and_nonfinite(self):
        with self.assertRaises(ValueError):
            equal_mean([])
        with self.assertRaises(ValueError):
            equal_mean([1, np.nan])

    def test_generator_is_reproducible(self):
        a = one_realization(np.random.default_rng(9))
        b = one_realization(np.random.default_rng(9))
        self.assertEqual(a, b)


if __name__ == "__main__":
    unittest.main()
