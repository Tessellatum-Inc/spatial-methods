import numpy as np
import pytest
from thermal_hotspot import detect_thermal_hotspots


def test_isolated_hot_pixel_is_detected_against_local_background():
    image = np.full((21, 21), 300.0)
    image[10, 10] = 340.0
    out = detect_thermal_hotspots(image, absolute_threshold=320,
                                  min_local_excess=8, window_size=9)
    assert np.argwhere(out["hotspots"]).tolist() == [[10, 10]]
    assert out["background"][10, 10] == pytest.approx(300)
    assert out["excess"][10, 10] == pytest.approx(40)


def test_absolute_threshold_suppresses_warm_but_not_hot_enough_pixels():
    image = np.full((11, 11), 300.0)
    image[5, 5] = 315.0
    out = detect_thermal_hotspots(image, absolute_threshold=320,
                                  min_local_excess=5)
    assert not np.any(out["hotspots"])


def test_nan_cells_are_excluded():
    image = np.full((9, 9), 300.0)
    image[4, 4] = np.nan
    image[4, 5] = 340.0
    out = detect_thermal_hotspots(image, absolute_threshold=320)
    assert not out["hotspots"][4, 4]
    assert out["hotspots"][4, 5]


@pytest.mark.parametrize("kwargs", [
    {"window_size": 2}, {"window_size": 0}, {"min_local_excess": -1},
    {"mad_multiplier": -1},
])
def test_invalid_controls_raise(kwargs):
    with pytest.raises(ValueError):
        detect_thermal_hotspots(np.ones((5, 5))*300, absolute_threshold=320, **kwargs)


def test_uniform_scene_has_no_hotspots():
    out = detect_thermal_hotspots(np.full((7, 7), 300.), absolute_threshold=280)
    assert not np.any(out["hotspots"])
