import unittest
import numpy as np

from explorations.radar.compare_opera_surat_r009_processors import db, residual_metrics, regression_summary


class OperaCrossProcessorMathTests(unittest.TestCase):
    def test_gamma0_ellipsoid_reconstruction_convention(self):
        gamma0_terrain = np.array([0.1, 0.2], dtype=float)
        anf = np.array([1.2, 0.8], dtype=float)
        theta = np.array([40.0, 45.0], dtype=float)
        reconstructed = gamma0_terrain * anf * np.tan(np.deg2rad(theta))
        expected = np.array([0.1 * 1.2 * np.tan(np.deg2rad(40)),
                             0.2 * 0.8 * np.tan(np.deg2rad(45))])
        np.testing.assert_allclose(reconstructed, expected)
        delta = db(gamma0_terrain) - db(reconstructed)
        predicted = -10 * np.log10(anf) - 10 * np.log10(np.tan(np.deg2rad(theta)))
        np.testing.assert_allclose(delta, predicted)

    def test_residual_metrics(self):
        metrics = residual_metrics(np.array([-1.0, 0.0, 1.0]))
        self.assertEqual(metrics["count"], 3)
        self.assertAlmostEqual(metrics["bias_mean_db"], 0.0)
        self.assertAlmostEqual(metrics["mae_db"], 2 / 3)
        self.assertAlmostEqual(metrics["rmse_db"], np.sqrt(2 / 3))

    def test_regression(self):
        predicted = np.arange(20, dtype=float)
        observed = 0.5 + 1.2 * predicted
        result = regression_summary(observed, predicted)
        self.assertAlmostEqual(result["slope"], 1.2)
        self.assertAlmostEqual(result["intercept_db"], 0.5)
        self.assertAlmostEqual(result["r_squared"], 1.0)


if __name__ == "__main__":
    unittest.main()
