import numpy as np
import pytest
from lee_filter import lee_filter


def test_constant_field_is_preserved():
    image = np.full((7, 8), 12.5)
    assert np.allclose(lee_filter(image, 2.0), image)


def test_zero_noise_variance_returns_local_observation():
    image = np.arange(25, dtype=float).reshape(5, 5)
    assert np.allclose(lee_filter(image, 0.0), image)


def test_positive_noise_suppresses_local_impulse():
    image = np.full((7, 7), 10.0)
    image[3, 3] = 100.0
    filtered = lee_filter(image, 20.0, 3)
    assert 10 < filtered[3, 3] < 100
    assert np.isfinite(filtered).all()


def test_nodata_is_ignored_and_preserved():
    image = np.full((5, 5), 4.0)
    image[2, 2] = np.nan
    result = lee_filter(image, 1.0)
    assert np.isnan(result[2, 2])
    assert np.allclose(result[np.isfinite(result)], 4.0)


@pytest.mark.parametrize("kwargs", [
    {"noise_variance": -1}, {"noise_variance": float("nan")},
    {"noise_variance": 1, "window_size": 2},
    {"noise_variance": 1, "window_size": 4},
    {"noise_variance": 1, "min_valid": 0},
])
def test_invalid_parameters(kwargs):
    with pytest.raises(ValueError):
        lee_filter(np.ones((3, 3)), **kwargs)


def test_requires_nonempty_2d_input():
    with pytest.raises(ValueError):
        lee_filter(np.ones(5), 1)
    with pytest.raises(ValueError):
        lee_filter(np.empty((0, 2)), 1)
