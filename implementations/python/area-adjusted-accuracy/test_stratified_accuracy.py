import unittest

from stratified_accuracy import estimate_stratified_accuracy


class SamplingStrataAccuracyTests(unittest.TestCase):
    def setUp(self):
        # The three sampling strata (A/B/C) are deliberately not the map classes.
        self.rows = []
        grouped = {
            "A": [
                ("forest", "forest"), ("forest", "grass"),
                ("grass", "grass"), ("forest", "forest"),
            ],
            "B": [
                ("grass", "grass"), ("grass", "grass"),
                ("water", "forest"), ("grass", "water"),
            ],
            "C": [
                ("water", "water"), ("water", "water"),
                ("grass", "water"), ("forest", "water"),
            ],
        }
        for stratum, pairs in grouped.items():
            for map_class, reference_class in pairs:
                self.rows.append({
                    "sampling_stratum": stratum,
                    "map_class": map_class,
                    "reference_class": reference_class,
                })
        self.weights = {"A": 0.5, "B": 0.3, "C": 0.2}
        self.population_sizes = {"A": 40, "B": 30, "C": 20}

    def test_sampling_strata_can_differ_from_map_classes(self):
        result = estimate_stratified_accuracy(
            self.rows, self.weights, stratum_population_sizes=self.population_sizes
        )
        self.assertEqual(result["sample_counts_by_sampling_stratum"], {"A": 4, "B": 4, "C": 4})
        self.assertAlmostEqual(
            result["estimated_area_proportion_error_matrix"]["forest"]["forest"], 0.25
        )
        self.assertAlmostEqual(
            result["estimated_area_proportion_error_matrix"]["forest"]["grass"], 0.125
        )
        self.assertAlmostEqual(
            result["estimated_area_proportion_error_matrix"]["water"]["water"], 0.1
        )
        self.assertAlmostEqual(result["overall_accuracy"]["estimate"], 0.625)
        self.assertAlmostEqual(result["overall_accuracy"]["standard_error"], 0.15241117631809903)

    def test_mapped_and_reference_area_marginals_are_distinct(self):
        result = estimate_stratified_accuracy(self.rows, self.weights)
        self.assertAlmostEqual(
            result["mapped_class_area_proportions"]["forest"]["estimate"], 0.425
        )
        self.assertAlmostEqual(
            result["reference_class_area_proportions"]["forest"]["estimate"], 0.325
        )
        self.assertNotEqual(
            result["mapped_class_area_proportions"]["forest"]["estimate"],
            result["reference_class_area_proportions"]["forest"]["estimate"],
        )

    def test_class_accuracy_uses_ratio_of_area_adjusted_marginals(self):
        result = estimate_stratified_accuracy(self.rows, self.weights)
        self.assertAlmostEqual(
            result["users_accuracy_by_map_class"]["forest"]["estimate"],
            0.25 / 0.425,
        )
        self.assertAlmostEqual(
            result["producers_accuracy_by_reference_class"]["forest"]["estimate"],
            0.25 / 0.325,
        )

    def test_finite_population_correction_is_applied_per_sampling_stratum(self):
        result = estimate_stratified_accuracy(
            self.rows, self.weights, stratum_population_sizes=self.population_sizes
        )
        self.assertAlmostEqual(
            result["finite_population_correction_by_sampling_stratum"]["A"], 0.9
        )

    def test_rejects_unweighted_or_missing_sampling_strata(self):
        bad = self.rows + [{
            "sampling_stratum": "D", "map_class": "forest", "reference_class": "forest"
        }]
        with self.assertRaises(ValueError):
            estimate_stratified_accuracy(bad, self.weights)

    def test_requires_at_least_two_observations_per_sampling_stratum(self):
        with self.assertRaises(ValueError):
            estimate_stratified_accuracy(self.rows[:9], self.weights)

    def test_population_sizes_must_match_sampling_strata(self):
        with self.assertRaises(ValueError):
            estimate_stratified_accuracy(
                self.rows, self.weights, stratum_population_sizes={"A": 40, "B": 30}
            )

    def test_class_with_no_estimated_reference_area_has_undefined_producers_accuracy(self):
        rows = [
            {"sampling_stratum": "A", "map_class": "forest", "reference_class": "forest"},
            {"sampling_stratum": "A", "map_class": "forest", "reference_class": "forest"},
            {"sampling_stratum": "B", "map_class": "other_map_only", "reference_class": "forest"},
            {"sampling_stratum": "B", "map_class": "other_map_only", "reference_class": "forest"},
        ]
        result = estimate_stratified_accuracy(rows, {"A": 0.5, "B": 0.5})
        self.assertIsNone(result["producers_accuracy_by_reference_class"]["other_map_only"])


if __name__ == "__main__":
    unittest.main()
