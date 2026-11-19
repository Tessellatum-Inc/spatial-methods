import unittest

from constrained_gls import constrained_gls


class ConstrainedGLSTests(unittest.TestCase):
    def test_inner_constraint_resolves_translation_defect(self):
        # Three unknown heights; only two differences are observed.
        a = [[-1.0, 1.0, 0.0], [0.0, -1.0, 1.0]]
        y = [1.0, 1.0]
        q = [[1.0, 0.0], [0.0, 1.0]]
        c = [[1.0, 1.0, 1.0]]
        estimate, covariance, residuals, _ = constrained_gls(a, y, q, c, [0.0])
        self.assertAlmostEqual(sum(estimate), 0.0, places=10)
        for actual, expected in zip(estimate, [-1.0, 0.0, 1.0]):
            self.assertAlmostEqual(actual, expected, places=10)
        self.assertTrue(all(abs(v) < 1e-10 for v in residuals))
        self.assertAlmostEqual(sum(sum(row) for row in covariance), 0.0, places=9)

    def test_exact_nonzero_constraint(self):
        a = [[1.0], [1.0]]
        y = [2.0, 4.0]
        q = [[1.0, 0.0], [0.0, 1.0]]
        estimate, _, residuals, _ = constrained_gls(a, y, q, [[1.0]], [3.0])
        self.assertAlmostEqual(estimate[0], 3.0)
        self.assertAlmostEqual(residuals[0], -1.0)
        self.assertAlmostEqual(residuals[1], 1.0)

    def test_rejects_constraint_that_does_not_remove_defect(self):
        a = [[-1.0, 1.0, 0.0], [0.0, -1.0, 1.0]]
        with self.assertRaisesRegex(ValueError, "singular"):
            constrained_gls(a, [1.0, 1.0], [[1.0, 0.0], [0.0, 1.0]],
                            [[1.0, 0.0, 0.0]], [0.0])

    def test_rejects_singular_observation_covariance(self):
        a = [[-1.0, 1.0, 0.0], [0.0, -1.0, 1.0]]
        with self.assertRaisesRegex(ValueError, "positive definite"):
            constrained_gls(a, [1.0, 1.0], [[1.0, 1.0], [1.0, 1.0]],
                            [[1.0, 1.0, 1.0]], [0.0])

    def test_synthetic_exercise_e_network(self):
        import csv
        from pathlib import Path

        root = Path(__file__).resolve().parents[3]
        data = root / "data" / "measurement" / "exercise-c-synthetic-control-network.csv"
        points = ("A", "B", "C", "D", "E")
        design, observed, sigmas = [], [], []
        with data.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                coefficients = [0.0] * len(points)
                coefficients[points.index(row["from_point"])] -= 1.0
                coefficients[points.index(row["to_point"])] += 1.0
                design.append(coefficients)
                observed.append(float(row["observed_delta_h_m"]))
                sigmas.append(float(row["assumed_sigma_mm"]) / 1000.0)
        covariance = [[sigmas[i] ** 2 if i == j else 0.0
                       for j in range(len(sigmas))]
                      for i in range(len(sigmas))]
        estimate, _, residuals, _ = constrained_gls(
            design, observed, covariance, [[1.0] * len(points)], [0.0]
        )
        expected = [-1.460669, -0.259813, 0.539797, 0.240307, 0.940378]
        for actual, target in zip(estimate, expected):
            self.assertAlmostEqual(actual, target, places=6)
        self.assertAlmostEqual(sum(estimate), 0.0, places=10)
        self.assertEqual(len(residuals), 9)


if __name__ == "__main__":
    unittest.main()
