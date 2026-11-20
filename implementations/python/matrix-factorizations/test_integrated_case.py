import unittest

import numpy as np

from integrated_case import run_case


class IntegratedSpatialCaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = run_case()

    def test_affine_control_recovers_declared_mapping(self):
        np.testing.assert_allclose(
            self.result["affine_x_parameters"], [1.02, -0.10, 500.0], atol=1e-12
        )
        np.testing.assert_allclose(
            self.result["affine_y_parameters"], [0.10, 1.05, 1000.0], atol=1e-12
        )

    def test_affine_control_geometry_is_nonsingular(self):
        self.assertTrue(np.isfinite(self.result["affine_control_condition_number"]))
        self.assertGreater(self.result["affine_control_condition_number"], 1.0)

    def test_gls_and_ols_are_finite_and_not_identical(self):
        ols = self.result["ols_plane_parameters"]
        gls = self.result["gls_plane_parameters"]
        self.assertTrue(np.all(np.isfinite(ols)))
        self.assertTrue(np.all(np.isfinite(gls)))
        self.assertGreater(np.linalg.norm(ols - gls), 1e-10)

    def test_svd_reports_full_column_rank(self):
        self.assertEqual(self.result["whitened_design_numerical_rank"], 3)
        values = self.result["whitened_design_singular_values"]
        self.assertTrue(np.all(values[:-1] >= values[1:]))
        self.assertGreater(values[-1], self.result["rank_tolerance"])

    def test_whitened_residual_diagnostic_is_finite(self):
        self.assertTrue(np.isfinite(self.result["gls_whitened_residual_norm"]))
        self.assertGreaterEqual(self.result["gls_whitened_residual_norm"], 0.0)


if __name__ == "__main__":
    unittest.main()
