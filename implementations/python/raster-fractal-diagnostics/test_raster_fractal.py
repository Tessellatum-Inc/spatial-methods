import numpy as np
import pytest

from raster_fractal import (
    box_counting_dimension,
    estimate_hurst_exponent,
    gliding_box_lacunarity,
)


def test_box_counting_full_square_has_dimension_two():
    raster = np.ones((64, 64))
    result = box_counting_dimension(raster, box_sizes=[1, 2, 4, 8, 16, 32, 64])
    assert result["occupied_box_counts"] == [4096, 1024, 256, 64, 16, 4, 1]
    assert result["dimension"] == pytest.approx(2.0)


def test_box_counting_empty_support_is_undefined():
    result = box_counting_dimension(np.zeros((16, 16)), box_sizes=[1, 2, 4, 8])
    assert result["dimension"] is None
    assert result["occupied_cells"] == 0


def test_box_counting_partial_edge_boxes_are_counted():
    result = box_counting_dimension(np.ones((5, 7)), box_sizes=[1, 2, 4])
    assert result["occupied_box_counts"] == [35, 12, 4]


def test_gliding_box_uniform_full_raster_has_unit_lacunarity():
    result = gliding_box_lacunarity(np.ones((8, 9)), box_size=3)
    assert result["lacunarity"] == pytest.approx(1.0)
    assert result["window_count"] == 42


def test_gliding_box_empty_support_is_undefined():
    result = gliding_box_lacunarity(np.zeros((5, 5)), box_size=2)
    assert result["lacunarity"] is None


def test_hurst_linear_ramp_has_expected_scaling():
    y, x = np.mgrid[:64, :64]
    result = estimate_hurst_exponent(x.astype(float), lags=[1, 2, 4, 8, 16])
    assert result["variogram_scaling_exponent"] == pytest.approx(2.0, abs=1e-10)
    assert result["hurst_exponent"] == pytest.approx(1.0, abs=1e-10)


@pytest.mark.parametrize("function,kwargs", [
    (box_counting_dimension, {"box_sizes": [1]}),
    (gliding_box_lacunarity, {"box_size": 0}),
    (estimate_hurst_exponent, {"lags": [1]}),
])
def test_invalid_scales_rejected(function, kwargs):
    with pytest.raises(ValueError):
        function(np.ones((8, 8)), **kwargs)


def test_nonfinite_and_wrong_dimension_rejected():
    with pytest.raises(ValueError):
        box_counting_dimension([[1, np.nan], [2, 3]])
    with pytest.raises(ValueError):
        estimate_hurst_exponent([1, 2, 3])
