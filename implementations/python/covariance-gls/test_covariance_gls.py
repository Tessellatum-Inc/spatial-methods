import math
import unittest

from covariance_gls import (
    diagonal_covariance, generalized_least_squares,
    session_common_covariance, validate_covariance,
)


class CovarianceTests(unittest.TestCase):
    def test_valid_positive_semidefinite_singular_matrix(self):
        result = validate_covariance([[1.0, 1.0], [1.0, 1.0]])
        self.assertTrue(result["positive_semidefinite"])
        self.assertAlmostEqual(result["minimum_eigenvalue"], 0.0, places=10)

    def test_rejects_indefinite_matrix(self):
        with self.assertRaisesRegex(ValueError, "positive semidefinite"):
            validate_covariance([[1.0, 2.0], [2.0, 1.0]])

    def test_rejects_asymmetric_matrix(self):
        with self.assertRaisesRegex(ValueError, "symmetric"):
            validate_covariance([[1.0, 0.2], [0.1, 1.0]])

    def test_session_common_covariance(self):
        q = session_common_covariance([1.0, 2.0, 1.0], ["S1", "S1", "S2"], 0.5)
        self.assertAlmostEqual(q[0][0], 1.25)
        self.assertAlmostEqual(q[0][1], 0.25)
        self.assertAlmostEqual(q[0][2], 0.0)
        self.assertAlmostEqual(q[1][1], 4.25)

    def test_gls_accounts_for_correlation(self):
        a = [[1.0], [1.0]]
        y = [1.0, 1.0]
        q = [[1.0, 0.5], [0.5, 1.0]]
        estimate, covariance, residuals = generalized_least_squares(a, y, q)
        self.assertAlmostEqual(estimate[0], 1.0)
        self.assertAlmostEqual(covariance[0][0], 0.75)
        self.assertAlmostEqual(residuals[0], 0.0)
        self.assertAlmostEqual(residuals[1], 0.0)
        _, diagonal_cov, _ = generalized_least_squares(a, y, diagonal_covariance(q))
        self.assertAlmostEqual(diagonal_cov[0][0], 0.5)

    def test_gls_rejects_singular_observation_covariance(self):
        with self.assertRaisesRegex(ValueError, "positive definite"):
            generalized_least_squares([[1.0], [1.0]], [1.0, 1.0],
                                      [[1.0, 1.0], [1.0, 1.0]])


if __name__ == "__main__":
    unittest.main()
