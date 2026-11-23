import numpy as np
import pytest

from polynomial_trend_surface import PolynomialTrendSurface, fit_trend_surface


def grid():
    x, y = np.meshgrid(np.linspace(-2, 2, 5), np.linspace(-3, 3, 6))
    return np.column_stack((x.ravel(), y.ravel()))


def test_quadratic_surface_is_reproduced_at_samples_and_new_locations():
    points = grid()
    values = 4 + 2*points[:, 0] - 3*points[:, 1] + .5*points[:, 0]**2 + 1.2*points[:, 0]*points[:, 1] - .7*points[:, 1]**2
    model = PolynomialTrendSurface(points, values, degree=2)
    queries = np.array([[.2, .7], [-1.1, 2.2], [3., -4.]])
    expected = 4 + 2*queries[:, 0] - 3*queries[:, 1] + .5*queries[:, 0]**2 + 1.2*queries[:, 0]*queries[:, 1] - .7*queries[:, 1]**2
    assert model.predict(points) == pytest.approx(values, abs=1e-10)
    assert model.predict(queries) == pytest.approx(expected, abs=1e-10)
    assert model.rmse_ < 1e-10
    assert model.r_squared_ == pytest.approx(1.0)


def test_linear_model_and_constant_model():
    points = grid()
    linear = PolynomialTrendSurface(points, 7 + 2*points[:, 0] - points[:, 1], degree=1)
    assert linear.predict([[.5, .25]]) == pytest.approx([7.75])
    constant = PolynomialTrendSurface(points, np.full(len(points), 9.), degree=0)
    assert constant.predict([[.5, .25]]) == pytest.approx([9.])


def test_weighted_least_squares_changes_fit_toward_high_weight_observation():
    points = grid()
    values = 1 + points[:, 0] - 2*points[:, 1]
    values[0] += 20
    ordinary = PolynomialTrendSurface(points, values, degree=1)
    weights = np.ones(len(points))
    weights[0] = 1000
    weighted = PolynomialTrendSurface(points, values, degree=1, weights=weights)
    assert abs(weighted.predict([points[0]])[0] - values[0]) < abs(ordinary.predict([points[0]])[0] - values[0])


def test_coordinate_translation_and_scale_preserve_predictions():
    points = grid()
    values = 3 + points[:, 0] - 2*points[:, 1] + .2*points[:, 0]**2
    queries = np.array([[.3, .4], [-1.2, 1.1]])
    original = fit_trend_surface(points, values, degree=2).predict(queries)
    transformed = points * 1000 + [1e6, -2e6]
    transformed_queries = queries * 1000 + [1e6, -2e6]
    changed = fit_trend_surface(transformed, values, degree=2).predict(transformed_queries)
    assert changed == pytest.approx(original, abs=1e-8)


def test_empty_query_result():
    model = PolynomialTrendSurface(grid(), np.arange(len(grid())), degree=1)
    assert model.predict(np.empty((0, 2))).size == 0


@pytest.mark.parametrize("degree", [-1, 4, 1.5, True, "2"])
def test_invalid_degree_is_rejected(degree):
    with pytest.raises(ValueError):
        PolynomialTrendSurface(grid(), np.arange(len(grid())), degree=degree)


@pytest.mark.parametrize("weights", [[0]*30, [-1]*30, [1, 2], [float("nan")]*30])
def test_invalid_weights_are_rejected(weights):
    with pytest.raises(ValueError):
        PolynomialTrendSurface(grid(), np.arange(len(grid())), weights=weights)


@pytest.mark.parametrize("points,values", [
    ([[0, 0], [1, 0]], [1, 2]),
    ([[0, 0], [1, 0], [2, 0], [3, 0]], [1, 2, 3, 4]),
    ([[0, 0], [1, 0], [0, 1]], [1, 2]),
    ([[0, 0], [1, 0], [0, 1]], [1, float("inf"), 3]),
])
def test_invalid_or_unidentifiable_training_data_are_rejected(points, values):
    with pytest.raises(ValueError):
        PolynomialTrendSurface(points, values, degree=1)


def test_rank_deficiency_for_too_few_points_at_requested_degree():
    points = np.array([[0.,0.],[1.,0.],[0.,1.],[1.,1.]])
    with pytest.raises(ValueError):
        PolynomialTrendSurface(points, [1,2,3,4], degree=2)


def test_invalid_queries_are_rejected():
    model = PolynomialTrendSurface(grid(), np.arange(len(grid())), degree=1)
    with pytest.raises(ValueError):
        model.predict([[0, float("nan")]])
    with pytest.raises(ValueError):
        model.predict([[0, 1, 2]])
