import numpy as np
import pytest
from climate import climate_velocity, mahalanobis_climate_analogs


def test_mahalanobis_analog_order_matches_independent_quadratic_form():
    historical = np.array([[0., 0.], [1., 0.], [0., 2.], [2., 1.], [3., 2.]])
    future = np.array([[1.1, 0.2], [2.8, 1.7]])
    covariance = np.array([[2., .3], [.3, 1.5]])
    indices, distances = mahalanobis_climate_analogs(
        historical, future, n_analogs=3, covariance=covariance, regularization=0)
    inverse = np.linalg.inv(covariance)
    oracle = np.array([[np.sqrt((x-y) @ inverse @ (x-y))
                        for y in historical] for x in future])
    expected = np.argsort(oracle, axis=1, kind="stable")[:, :3]
    np.testing.assert_array_equal(indices, expected)
    np.testing.assert_allclose(distances, np.take_along_axis(oracle, expected, axis=1))


def test_analog_ranking_is_affine_scale_aware_and_seed_independent():
    rng = np.random.default_rng(19)
    historical = rng.normal(size=(100, 3))
    future = np.array([historical[17] + [0.01, 0.01, 0.01]])
    indices, distances = mahalanobis_climate_analogs(historical, future)
    assert indices[0, 0] == 17
    assert distances[0, 0] < .1


def test_analog_covariance_ridge_handles_collinear_variables():
    x = np.linspace(-2, 2, 30)
    historical = np.column_stack((x, 2*x))
    indices, distances = mahalanobis_climate_analogs(
        historical, np.array([[.1, .2]]), regularization=1e-6)
    assert indices.shape == distances.shape == (1, 1)
    assert np.isfinite(distances[0, 0])


def test_climate_velocity_matches_linear_isocline_displacement():
    result = climate_velocity(0.3, 0.02, 0.01)
    # v = -0.3 * (0.02, 0.01) / (0.02**2 + 0.01**2)
    assert result["velocity_x"] == pytest.approx(-12.0)
    assert result["velocity_y"] == pytest.approx(-6.0)
    assert result["speed"] == pytest.approx(np.sqrt(180.0))


def test_climate_velocity_broadcasts_and_marks_flat_gradients():
    result = climate_velocity(np.array([.1, .2]), [1., 0.], [0., 0.])
    np.testing.assert_allclose(result["velocity_x"][0], -.1)
    assert np.isinf(result["speed"][1])
    assert np.isnan(result["velocity_x"][1])


def test_climate_methods_reject_invalid_inputs():
    with pytest.raises(ValueError, match="historical"):
        mahalanobis_climate_analogs([[1., np.nan], [2., 3.]], [1., 2.])
    with pytest.raises(ValueError, match="n_analogs"):
        mahalanobis_climate_analogs(np.ones((3, 2)), [1., 2.], n_analogs=4)
    with pytest.raises(ValueError, match="positive"):
        climate_velocity(.1, 1., 1., minimum_gradient=0)
