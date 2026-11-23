import numpy as np
import pytest
from chm_crowns import segment_crowns


def test_two_canopy_peaks_produce_two_crowns():
    yy, xx = np.mgrid[:41, :61]
    left = 12 * np.exp(-((xx-17)**2 + (yy-20)**2) / (2*5**2))
    right = 10 * np.exp(-((xx-43)**2 + (yy-20)**2) / (2*5**2))
    chm = np.maximum(left, right)
    out = segment_crowns(chm, canopy_threshold=1, min_peak_height=3, window_size=7)
    assert len(out["seeds"]) == 2
    assert set(np.unique(out["labels"])) == {0, 1, 2}
    assert out["labels"][20, 17] != out["labels"][20, 43]
    assert np.all(out["labels"][chm < 1] == 0)


def test_plateau_is_one_seed_and_result_is_deterministic():
    chm = np.zeros((15, 15))
    chm[5:8, 5:8] = 8
    a = segment_crowns(chm, canopy_threshold=1, min_peak_height=4, window_size=3)
    b = segment_crowns(chm, canopy_threshold=1, min_peak_height=4, window_size=3)
    assert a["seeds"].shape == (1, 2)
    assert np.array_equal(a["seeds"], b["seeds"])
    assert np.array_equal(a["labels"], b["labels"])


def test_no_qualifying_treetop_returns_empty_labels():
    out = segment_crowns(np.ones((5, 5)), canopy_threshold=1, min_peak_height=2)
    assert not np.any(out["labels"])
    assert out["seeds"].shape == (0, 2)


@pytest.mark.parametrize("kwargs", [
    {"window_size": 2}, {"window_size": 0}, {"canopy_threshold": 3, "min_peak_height": 2},
    {"compactness": -1},
])
def test_invalid_controls_raise(kwargs):
    with pytest.raises(ValueError):
        segment_crowns(np.ones((5, 5))*4, **kwargs)


def test_nonfinite_cells_are_excluded():
    chm = np.full((7, 7), np.nan)
    chm[3, 3] = 5
    out = segment_crowns(chm, canopy_threshold=1, min_peak_height=2, window_size=3)
    assert out["seeds"].tolist() == [[3, 3]]
    assert out["labels"][3, 3] == 1
