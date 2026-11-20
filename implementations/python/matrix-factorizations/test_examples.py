import unittest
import numpy as np

from examples import (
    cholesky_gls, lu_coordinate_system, qr_terrain_plane,
    svd_near_dependency, svd_pca,
)


class MatrixFactorizationExamplesTests(unittest.TestCase):
    def test_lu_pivoted_factorization_and_solution(self):
        result = lu_coordinate_system()
        np.testing.assert_allclose(result["A"], result["P"] @ result["L"] @ result["U"], atol=1e-12)
        np.testing.assert_allclose(result["solution"], [2., -1., 3.], atol=1e-12)
        self.assertLess(result["factorization_error"], 1e-12)

    def test_qr_least_squares_residual_orthogonality(self):
        result = qr_terrain_plane()
        np.testing.assert_allclose(result["coefficients"], [100., 2., -0.5], atol=0.03)
        self.assertLess(result["orthogonality_error"], 1e-10)
        self.assertGreaterEqual(result["residual_sum_squares"], 0.)

    def test_cholesky_gls_whitening(self):
        result = cholesky_gls()
        np.testing.assert_allclose(result["covariance_cholesky"] @ result["covariance_cholesky"].T,
                                   [[1., .3, .1, 0.], [.3, 1., .3, .1],
                                    [.1, .3, 1., .3], [0., .1, .3, 1.]], atol=1e-12)
        self.assertTrue(np.all(np.isfinite(result["coefficients"])))

    def test_svd_reports_singular_values_and_rank(self):
        result = svd_near_dependency()
        self.assertEqual(result["numerical_rank"], 2)
        self.assertGreater(result["singular_values"][0], result["singular_values"][1])

    def test_svd_pca_variance_order_and_reconstruction(self):
        result = svd_pca()
        self.assertGreaterEqual(result["explained_variances"][0], result["explained_variances"][1])
        reconstructed = result["scores"] @ result["principal_axes_as_rows"] + result["mean"]
        expected = np.array([[0., 0.], [1., 1.1], [2., 1.9],
                             [3., 3.2], [4., 3.9], [5., 5.1]])
        np.testing.assert_allclose(reconstructed, expected, atol=1e-12)


if __name__ == "__main__":
    unittest.main()
