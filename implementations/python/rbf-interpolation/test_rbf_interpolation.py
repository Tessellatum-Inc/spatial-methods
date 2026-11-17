import numpy as np
import pytest

from rbf_interpolation import RBFInterpolator2D, rbf_interpolate


POINTS = np.array([[0., 0.], [1., 0.], [0., 1.], [1., 1.], [.3, .7]])
AFFINE = 2.0 + 3.0 * POINTS[:, 0] - 4.0 * POINTS[:, 1]


@pytest.mark.parametrize("kernel", ["thin_plate", "cubic", "gaussian"])
def test_affine_field_is_reproduced(kernel):
    model = RBFInterpolator2D(POINTS, AFFINE, kernel=kernel)
    queries = np.array([[.2, .4], [.8, .1], [1.4, -.2]])
    expected = 2.0 + 3.0 * queries[:, 0] - 4.0 * queries[:, 1]
    assert model.predict(queries) == pytest.approx(expected, abs=1e-9)


@pytest.mark.parametrize("kernel", ["thin_plate", "cubic", "gaussian"])
def test_zero_smoothing_interpolates_training_values(kernel):
    model = RBFInterpolator2D(POINTS, np.sin(POINTS[:, 0]) + POINTS[:, 1], kernel=kernel)
    assert model.predict(POINTS) == pytest.approx(
        np.sin(POINTS[:, 0]) + POINTS[:, 1], abs=1e-8
    )


def test_smoothing_regularizes_noisy_observations():
    values = AFFINE.copy()
    values[2] += 5
    exact = RBFInterpolator2D(POINTS, values, smoothing=0)
    smooth = RBFInterpolator2D(POINTS, values, smoothing=2)
    assert np.linalg.norm(smooth.predict(POINTS) - values) > 0
    assert np.linalg.norm(smooth.predict(POINTS) - AFFINE) < np.linalg.norm(exact.predict(POINTS) - AFFINE)


def test_coordinate_translation_and_scale_do_not_change_affine_prediction():
    queries = np.array([[.2, .3], [.8, .9]])
    original = rbf_interpolate(POINTS, AFFINE, queries)
    transform = np.array([1e6, -2e6]) + POINTS * 1000
    transformed_queries = np.array([1e6, -2e6]) + queries * 1000
    transformed = rbf_interpolate(transform, AFFINE, transformed_queries)
    assert transformed == pytest.approx(original, abs=1e-8)


def test_empty_query_array_returns_empty_predictions():
    assert rbf_interpolate(POINTS, AFFINE, np.empty((0, 2))).size == 0


@pytest.mark.parametrize("kwargs", [
    {"kernel": "unknown"}, {"kernel": []}, {"epsilon": 0}, {"epsilon": float("nan")},
    {"epsilon": "1"}, pytest.param({"epsilon": 10**10000}, id="epsilon-huge-int"),
    {"smoothing": -1}, {"smoothing": float("inf")},
    {"smoothing": "0"}, pytest.param({"smoothing": 10**10000}, id="smoothing-huge-int"),
])
def test_invalid_controls_are_rejected(kwargs):
    with pytest.raises(ValueError):
        RBFInterpolator2D(POINTS, AFFINE, **kwargs)


@pytest.mark.parametrize("points,values", [
    ([[0, 0], [1, 0]], [1, 2]),
    ([[0, 0], [1, 0], [2, 0]], [1, 2, 3]),
    ([[0, 0], [1, 0], [0, 1], [0, 0]], [1, 2, 3, 4]),
    ([[0, 0], [1, 0], [0, 1]], [1, float("nan"), 3]),
])
def test_invalid_or_degenerate_training_data_are_rejected(points, values):
    with pytest.raises(ValueError):
        RBFInterpolator2D(points, values)


@pytest.mark.parametrize("queries", [
    [[0, float("inf")]], [[0]], [[0, 0, 0]],
])
def test_invalid_queries_are_rejected(queries):
    model = RBFInterpolator2D(POINTS, AFFINE)
    with pytest.raises(ValueError):
        model.predict(queries)


def test_bool_parameters_are_rejected():
    with pytest.raises(ValueError):
        RBFInterpolator2D(POINTS, AFFINE, epsilon=True)
    with pytest.raises(ValueError):
        RBFInterpolator2D(POINTS, AFFINE, smoothing=True)
