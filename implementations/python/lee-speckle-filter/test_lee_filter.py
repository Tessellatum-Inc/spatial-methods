import numpy as np
import pytest
from lee_filter import lee_filter


def test_constant_image_is_preserved():
    image = np.full((7, 8), 12.5)
    np.testing.assert_allclose(lee_filter(image), image)


def test_impulse_is_smoothed_without_negative_values():
    image = np.ones((9, 9))
    image[4, 4] = 30.0
    result = lee_filter(image, window_size=3)
    assert result[4, 4] < image[4, 4]
    assert np.all(result >= 0)


def test_nan_is_nodata_and_does_not_contaminate_neighbours():
    image = np.ones((5, 5))
    image[2, 2] = np.nan
    result = lee_filter(image)
    assert np.isnan(result[2, 2])
    assert np.isfinite(result[1, 1])


def test_all_nodata_remains_nodata():
    assert np.isnan(lee_filter(np.full((3, 3), np.nan))).all()


@pytest.mark.parametrize("window", [0, 2, 4, True, 3.5])
def test_invalid_window_rejected(window):
    with pytest.raises(ValueError):
        lee_filter(np.ones((4, 4)), window_size=window)


def test_invalid_values_and_enl_rejected():
    with pytest.raises(ValueError):
        lee_filter([[1., -1.], [2., 3.]])
    with pytest.raises(ValueError):
        lee_filter(np.ones((3, 3)), equivalent_looks=0)


def test_non_square_raster_and_clipped_edges():
    image = np.arange(20, dtype=float).reshape(4, 5)
    result = lee_filter(image, window_size=3, equivalent_looks=4)
    assert result.shape == image.shape
    assert np.isfinite(result).all()
