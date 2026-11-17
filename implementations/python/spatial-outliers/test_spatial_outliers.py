import numpy as np
import pytest

from spatial_outliers import (
    geographically_weighted_scores, local_outlier_factor, spatial_scatter_data,
    variogram_cloud, z_scores,
)


def test_z_scores_match_population_definition_and_constant_column():
    x = np.array([[1., 4.], [2., 4.], [3., 4.]])
    got = z_scores(x)
    np.testing.assert_allclose(got[:, 0], [-np.sqrt(1.5), 0, np.sqrt(1.5)])
    np.testing.assert_array_equal(got[:, 1], 0)


def test_spatial_scatter_uses_row_standardised_lag():
    values = np.array([1., 2., 5.])
    w = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]], dtype=float)
    observed, lag = spatial_scatter_data(values, w)
    np.testing.assert_allclose(observed, [-5/3, -2/3, 7/3])
    np.testing.assert_allclose(lag, [-2/3, 1/3, -2/3])


def test_variogram_cloud_matches_all_unique_pairs():
    d, g = variogram_cloud([[0, 0], [3, 0], [0, 4]], [1, 3, 5])
    np.testing.assert_allclose(d, [3, 4, 5])
    np.testing.assert_allclose(g, [2, 8, 2])


def test_lof_detects_isolated_point():
    x = np.array([[0., 0.], [.1, 0.], [0., .1], [.1, .1], [8., 8.]])
    scores = local_outlier_factor(x, k=2)
    assert scores[-1] > 5
    assert scores[-1] == pytest.approx(scores.max())


def test_lof_uniform_cloud_is_near_one():
    x = np.array([[0., 0.], [1., 0.], [0., 1.], [1., 1.]])
    np.testing.assert_allclose(local_outlier_factor(x, k=2), 1, atol=.25)


def test_weighted_local_score_flags_local_spike():
    xy = np.array([[0., 0.], [1., 0.], [0., 1.], [1., 1.], [.5, .5]])
    y = np.array([0., 0., 0., 0., 10.])
    scores = geographically_weighted_scores(xy, y, radius=2)
    assert scores[-1] > 1
    assert scores[-1] == pytest.approx(scores.max())


@pytest.mark.parametrize("call", [
    lambda: z_scores([1.]),
    lambda: spatial_scatter_data([1., 2.], [[0., 1.], [1., 1.]]),
    lambda: variogram_cloud([[0., 0.], [1., 1.]], [1.]),
    lambda: local_outlier_factor([[0.], [1.]], 2),
    lambda: geographically_weighted_scores([[0., 0.], [1., 1.]], [1., 2.], 0),
])
def test_invalid_inputs_raise(call):
    with pytest.raises(ValueError):
        call()
