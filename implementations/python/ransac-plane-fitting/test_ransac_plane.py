import numpy as np
import pytest
from ransac_plane import ransac_plane


def test_recovers_plane_with_outliers():
    rng = np.random.default_rng(5)
    x = rng.uniform(-5, 5, 150)
    y = rng.uniform(-5, 5, 150)
    z = 2*x - .5*y + 3 + rng.normal(0, .002, 150)
    inliers = np.column_stack([x, y, z])
    outliers = rng.uniform(-5, 5, (50, 3))
    points = np.vstack([inliers, outliers])
    result = ransac_plane(points, distance_threshold=.01, max_trials=500, min_inliers=140, random_state=12)
    assert result["n_inliers"] >= 145
    assert np.mean(result["residuals"][:150]) < .004
    assert np.count_nonzero(result["inliers"][150:]) <= 2
    expected = np.array([-2., .5, 1.])
    expected /= np.linalg.norm(expected)
    assert abs(float(result["normal"] @ expected)) > .999


def test_seeded_fit_is_reproducible():
    rng = np.random.default_rng(3)
    xy = rng.normal(size=(80, 2))
    points = np.column_stack([xy, .2*xy[:, 0] + .4*xy[:, 1]])
    a = ransac_plane(points, distance_threshold=1e-8, random_state=8)
    b = ransac_plane(points, distance_threshold=1e-8, random_state=8)
    assert np.allclose(a["normal"], b["normal"])
    assert np.array_equal(a["inliers"], b["inliers"])


@pytest.mark.parametrize("kwargs", [
    {"distance_threshold": 0}, {"max_trials": 0}, {"min_inliers": 2},
])
def test_invalid_controls_raise(kwargs):
    with pytest.raises(ValueError):
        ransac_plane(np.eye(3), **kwargs)


def test_degenerate_collinear_cloud_fails_cleanly():
    points = np.column_stack([np.arange(10.), np.zeros(10), np.zeros(10)])
    with pytest.raises(ValueError):
        ransac_plane(points, random_state=1)
