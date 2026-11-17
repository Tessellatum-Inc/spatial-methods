import numpy as np
import pytest
from ca_cfar import ca_cfar


def test_constant_background_has_no_detections():
    detections, threshold, noise = ca_cfar(np.ones((21, 21)), guard_cells=1, training_cells=3)
    assert not detections.any()
    assert np.isfinite(threshold[8, 8])
    assert noise[8, 8] == pytest.approx(1.0)


def test_strong_point_target_is_detected():
    image = np.ones((31, 31))
    image[15, 15] = 100.0
    detections, threshold, _ = ca_cfar(image, guard_cells=1, training_cells=4)
    assert detections[15, 15]
    assert image[15, 15] > threshold[15, 15]


def test_guard_region_excludes_target_from_training_ring():
    image = np.ones((31, 31))
    image[15, 15] = 1e6
    _, _, noise = ca_cfar(image, guard_cells=2, training_cells=3)
    assert noise[15, 15] == pytest.approx(1.0)


def test_border_and_nodata_are_not_detected():
    image = np.ones((15, 15))
    image[7, 7] = np.nan
    detections, threshold, noise = ca_cfar(image, guard_cells=1, training_cells=2)
    assert not detections[7, 7]
    assert np.isnan(threshold[7, 7]) and np.isnan(noise[7, 7])
    assert np.isnan(threshold[0, 0])


def test_nodata_in_training_window_invalidates_cell():
    image = np.ones((15, 15))
    image[7, 10] = np.nan
    _, threshold, _ = ca_cfar(image, guard_cells=1, training_cells=2)
    assert np.isnan(threshold[7, 7])


@pytest.mark.parametrize("pfa", [0, 1, -0.1, np.nan])
def test_invalid_false_alarm_probability(pfa):
    with pytest.raises(ValueError):
        ca_cfar(np.ones((5, 5)), false_alarm_rate=pfa)


def test_invalid_window_sizes():
    with pytest.raises(ValueError):
        ca_cfar(np.ones((5, 5)), guard_cells=-1)
    with pytest.raises(ValueError):
        ca_cfar(np.ones((5, 5)), training_cells=0)
