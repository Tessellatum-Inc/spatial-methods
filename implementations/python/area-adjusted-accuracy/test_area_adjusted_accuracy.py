import unittest

from area_adjusted_accuracy import estimate_stratified_accuracy


class AreaAdjustedAccuracyTests(unittest.TestCase):
    def setUp(self):
        # Two mapped-class strata, four sampled units in each.
        # Map-area proportions are deliberately unequal.
        self.rows = [
            {"map_class": "forest", "reference_class": "forest"},
            {"map_class": "forest", "reference_class": "forest"},
            {"map_class": "forest", "reference_class": "other"},
            {"map_class": "forest", "reference_class": "forest"},
            {"map_class": "other", "reference_class": "other"},
            {"map_class": "other", "reference_class": "forest"},
            {"map_class": "other", "reference_class": "other"},
            {"map_class": "other", "reference_class": "other"},
        ]
        self.weights = {"forest": 0.6, "other": 0.4}

    def test_area_weighted_matrix_and_overall_accuracy(self):
        result = estimate_stratified_accuracy(self.rows, self.weights, total_area=1000)
        self.assertAlmostEqual(result["estimated_area_proportion_error_matrix"]["forest"]["forest"], 0.45)
        self.assertAlmostEqual(result["estimated_area_proportion_error_matrix"]["forest"]["other"], 0.15)
        self.assertAlmostEqual(result["overall_accuracy"]["estimate"], 0.75)
        self.assertAlmostEqual(result["overall_accuracy"]["standard_error"], (0.6**2 * 0.75*0.25/3 + 0.4**2 * 0.75*0.25/3)**0.5)

    def test_reference_area_is_adjusted_from_reference_labels(self):
        result = estimate_stratified_accuracy(self.rows, self.weights, total_area=1000)
        forest = result["reference_class_area_proportions"]["forest"]
        self.assertAlmostEqual(forest["estimate"], 0.55)
        self.assertAlmostEqual(forest["estimated_area"], 550.0)
        self.assertEqual(set(forest["estimated_area_ci95_wald"]), {forest["estimated_area_ci95_wald"][0], forest["estimated_area_ci95_wald"][1]})

    def test_users_accuracy_uses_mapped_stratum(self):
        result = estimate_stratified_accuracy(self.rows, self.weights)
        self.assertAlmostEqual(result["users_accuracy_by_mapped_class"]["forest"]["estimate"], 0.75)
        self.assertAlmostEqual(result["users_accuracy_by_mapped_class"]["other"]["estimate"], 0.75)

    def test_producers_accuracy_uses_reference_column(self):
        result = estimate_stratified_accuracy(self.rows, self.weights)
        # Forest: correctly mapped forest area / estimated reference forest area.
        self.assertAlmostEqual(result["producers_accuracy_by_reference_class"]["forest"]["estimate"], 0.45/0.55)

    def test_rejects_weights_that_do_not_sum_to_one(self):
        with self.assertRaises(ValueError):
            estimate_stratified_accuracy(self.rows, {"forest": 0.6, "other": 0.5})

    def test_rejects_missing_stratum_sample(self):
        with self.assertRaises(ValueError):
            estimate_stratified_accuracy(
                [r for r in self.rows if r["map_class"] != "other"],
                self.weights
            )

    def test_requires_two_samples_per_stratum(self):
        with self.assertRaises(ValueError):
            estimate_stratified_accuracy(
                self.rows[:5], self.weights
            )

    def test_rejects_unknown_mapped_class(self):
        bad = self.rows + [{"map_class": "water", "reference_class": "water"}]
        with self.assertRaises(ValueError):
            estimate_stratified_accuracy(bad, self.weights)

