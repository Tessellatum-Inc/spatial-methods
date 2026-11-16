import numpy as np
import pytest
from ppi import pixel_purity_index

def test_reproducible_scores_and_candidate_order():
    rng = np.random.default_rng(4)
    endmembers = np.array([[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]])
    abundances = rng.dirichlet([1.5, 1.5, 1.5], size=400)
    cube = (abundances @ endmembers).reshape(20, 20, 3)
    a = pixel_purity_index(cube, 250, top_k=12, seed=17)
    b = pixel_purity_index(cube, 250, top_k=12, seed=17)
    assert np.array_equal(a["scores"], b["scores"])
    assert np.array_equal(a["candidate_indices"], b["candidate_indices"])
    assert a["candidate_spectra"].shape == (12, 3)
    assert np.all(np.diff(a["scores"].ravel()[a["candidate_indices"]]) <= 0)

def test_masked_pixels_are_excluded_and_marked():
    cube = np.random.default_rng(2).random((5, 6, 4))
    mask = np.ones((5, 6), dtype=bool)
    mask[0, :] = False
    out = pixel_purity_index(cube, 80, valid_mask=mask)
    assert np.all(out["scores"][0] == -1)
    assert np.all(out["candidate_indices"] >= 6)

def test_identical_spectra_tie_without_losing_votes():
    cube = np.ones((3, 4, 2))
    out = pixel_purity_index(cube, 20, seed=3)
    assert np.all(out["scores"] >= 0)
    assert out["scores"].sum() == 40
    assert np.array_equal(out["candidate_indices"], np.arange(12))

@pytest.mark.parametrize("kwargs", [
    {"n_projections": 0}, {"n_projections": -2}, {"top_k": 0}
])
def test_invalid_counts(kwargs):
    with pytest.raises(ValueError):
        pixel_purity_index(np.ones((2, 3, 2)), **kwargs)

def test_invalid_mask_and_empty_mask_rejected():
    cube = np.ones((2, 3, 2))
    with pytest.raises(ValueError):
        pixel_purity_index(cube, valid_mask=np.ones((2, 3), dtype=int))
    with pytest.raises(ValueError):
        pixel_purity_index(cube, valid_mask=np.zeros((2, 3), dtype=bool))
