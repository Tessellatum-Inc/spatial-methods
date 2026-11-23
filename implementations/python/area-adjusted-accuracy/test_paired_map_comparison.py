import unittest

from paired_map_comparison import compare_maps


class PairedMapComparisonTests(unittest.TestCase):
    def setUp(self):
        self.rows = [
            {"sampling_stratum": "A", "map_class": "x", "baseline_map_class": "x", "reference_class": "x"},
            {"sampling_stratum": "A", "map_class": "y", "baseline_map_class": "x", "reference_class": "x"},
            {"sampling_stratum": "B", "map_class": "x", "baseline_map_class": "y", "reference_class": "x"},
            {"sampling_stratum": "B", "map_class": "y", "baseline_map_class": "y", "reference_class": "y"},
        ]
        self.weights = {"A": 0.6, "B": 0.4}

    def test_paired_difference_and_fpc_variance(self):
        result = compare_maps(
            self.rows,
            self.weights,
            baseline_column="baseline_map_class",
            stratum_population_sizes={"A": 10, "B": 8},
        )
        self.assertAlmostEqual(result["evaluated_map_overall_accuracy"], 0.7)
        self.assertAlmostEqual(result["baseline_map_overall_accuracy"], 0.8)
        difference = result["evaluated_minus_baseline_accuracy_difference"]
        self.assertAlmostEqual(difference["estimate"], -0.1)
        self.assertAlmostEqual(difference["standard_error"] ** 2, 0.102)
        self.assertAlmostEqual(difference["ci95_wald"][0], -0.1 - 1.96 * (0.102 ** 0.5))

    def test_without_population_sizes_uses_no_fpc(self):
        result = compare_maps(self.rows, self.weights, baseline_column="baseline_map_class")
        self.assertEqual(
            result["stratum_diagnostics"]["A"]["finite_population_correction"], 1.0
        )
        self.assertEqual(
            result["stratum_diagnostics"]["B"]["finite_population_correction"], 1.0
        )

    def test_custom_baseline_column(self):
        rows = [dict(row, other_baseline=row["baseline_map_class"]) for row in self.rows]
        result = compare_maps(rows, self.weights, baseline_column="other_baseline")
        self.assertAlmostEqual(
            result["evaluated_minus_baseline_accuracy_difference"]["estimate"], -0.1
        )

    def test_rejects_missing_weighted_stratum(self):
        with self.assertRaises(ValueError):
            compare_maps(self.rows[:2], self.weights)

    def test_rejects_population_smaller_than_sample(self):
        with self.assertRaises(ValueError):
            compare_maps(
                self.rows,
                self.weights,
                baseline_column="baseline_map_class",
                stratum_population_sizes={"A": 1, "B": 8},
            )


if __name__ == "__main__":
    unittest.main()
