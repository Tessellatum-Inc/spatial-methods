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
        self.assertLessEqual(forest["estimated_area_ci95_wald"][0], forest["estimated_area"])
        self.assertGreaterEqual(forest["estimated_area_ci95_wald"][1], forest["estimated_area"])

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

    def test_advanced_three_class_case_reproduces_weighted_results(self):
        rows = (
            [{"map_class": "forest", "reference_class": "forest"}] * 17
            + [{"map_class": "forest", "reference_class": "agriculture"}] * 2
            + [{"map_class": "forest", "reference_class": "water"}]
            + [{"map_class": "agriculture", "reference_class": "forest"}] * 6
            + [{"map_class": "agriculture", "reference_class": "agriculture"}] * 12
            + [{"map_class": "agriculture", "reference_class": "water"}] * 2
            + [{"map_class": "water", "reference_class": "forest"}] * 15
            + [{"map_class": "water", "reference_class": "agriculture"}] * 5
            + [{"map_class": "water", "reference_class": "water"}] * 20
        )
        result = estimate_stratified_accuracy(
            rows, {"forest": 0.70, "agriculture": 0.25, "water": 0.05},
            total_area=12000
        )
        self.assertEqual(result["sample_counts_by_mapped_class"],
                         {"forest": 20, "agriculture": 20, "water": 40})
        self.assertAlmostEqual(result["overall_accuracy"]["estimate"], 0.77)
        self.assertAlmostEqual(result["overall_accuracy"]["standard_error"], 0.0639816944)
        self.assertAlmostEqual(
            result["reference_class_area_proportions"]["forest"]["estimate"], 0.68875
        )
        self.assertAlmostEqual(
            result["reference_class_area_proportions"]["agriculture"]["estimate"], 0.22625
        )
        self.assertAlmostEqual(
            result["reference_class_area_proportions"]["water"]["estimated_area"], 1020.0
        )
        self.assertAlmostEqual(
            result["producers_accuracy_by_reference_class"]["water"]["estimate"],
            0.025 / 0.085
        )

    def test_producer_accuracy_is_undefined_for_unobserved_reference_class(self):
        rows = [
            {"map_class": "forest", "reference_class": "forest"},
            {"map_class": "forest", "reference_class": "forest"},
            {"map_class": "water", "reference_class": "forest"},
            {"map_class": "water", "reference_class": "forest"},
        ]
        result = estimate_stratified_accuracy(rows, {"forest": 0.8, "water": 0.2})
        self.assertIsNone(result["producers_accuracy_by_reference_class"]["water"])
