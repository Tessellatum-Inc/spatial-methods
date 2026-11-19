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


if __name__ == "__main__":
    unittest.main()
