import numpy as np
import pytest
from compositing import best_pixel_composite, medoid_composite, maximum_ndvi_composite


def test_best_pixel_selects_highest_quality_and_earliest_tie():
    cube = np.arange(3 * 2 * 2 * 2, dtype=float).reshape(3, 2, 2, 2)
    q = np.array([[[1, 5], [3, 2]], [[2, 5], [1, 4]], [[0, 1], [4, 3]]], float)
    out = best_pixel_composite(cube, q)
    assert out["selected_time_index"].tolist() == [[1, 0], [2, 1]]
    assert out["composite"][0, 1].tolist() == cube[0, 0, 1].tolist()
    assert out["selected_quality"][0, 1] == 5


def test_medoid_returns_an_observed_spectrum_and_respects_mask():
    cube = np.array([[[[0., 0.]]], [[[2., 2.]]], [[[100., 100.]]]])
    mask = np.array([[[True]], [[True]], [[False]]])
    out = medoid_composite(cube, valid_mask=mask)
    assert out["selected_time_index"][0, 0] == 0
    assert np.array_equal(out["composite"][0, 0], cube[0, 0, 0])
    assert out["valid_observation_count"][0, 0] == 2


def test_maximum_ndvi_selects_whole_spectrum_and_handles_invalid_dates():
    cube = np.array([
        [[[0.2, 0.3, 10.]]],
        [[[0.1, 0.7, 20.]]],
        [[[0.2, 0.8, 30.]]],
    ])
    mask = np.array([[[True]], [[False]], [[True]]])
    out = maximum_ndvi_composite(cube, red_band=0, nir_band=1, valid_mask=mask)
    assert out["selected_time_index"][0, 0] == 2
    assert np.array_equal(out["composite"][0, 0], cube[2, 0, 0])
    assert out["selected_ndvi"][0, 0] == pytest.approx(0.6)


def test_no_valid_observation_produces_nan_and_minus_one():
    cube = np.ones((2, 2, 3, 2))
    mask = np.zeros((2, 2, 3), dtype=bool)
    out = medoid_composite(cube, valid_mask=mask)
    assert np.all(out["selected_time_index"] == -1)
    assert np.all(np.isnan(out["composite"]))


def test_validation_rejects_bad_inputs():
    cube = np.ones((2, 2, 3, 2))
    with pytest.raises(ValueError):
        best_pixel_composite(cube, np.ones((2, 2, 2)))
    with pytest.raises(ValueError):
        medoid_composite(cube, valid_mask=np.ones((2, 3, 2)))
    with pytest.raises(ValueError):
        maximum_ndvi_composite(cube, 0, 0)
