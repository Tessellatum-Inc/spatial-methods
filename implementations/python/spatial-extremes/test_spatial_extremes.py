import numpy as np
import pytest
from spatial_extremes import f_madogram

def test_perfectly_comonotone_sites_have_zero_madogram_and_theta_one():
    x = np.arange(1.0, 31.0)
    result = f_madogram(np.column_stack([x, 7 * x + 2]), min_pairs=10)
    np.testing.assert_allclose(result["f_madogram"], 0.0)
    np.testing.assert_allclose(result["extremal_coefficient"], 1.0)

def test_independent_rank_orderings_approach_independence_limit():
    rng = np.random.default_rng(20261117)
    n = 1200
    a, b = rng.normal(size=n), rng.normal(size=n)
    result = f_madogram(np.column_stack([a, b]), min_pairs=100)
    nu = result["f_madogram"][0, 1]
    theta = result["extremal_coefficient"][0, 1]
    assert abs(nu - 1.0 / 6.0) < 0.015
    assert abs(theta - 2.0) < 0.12

def test_pairwise_complete_missingness_and_counts():
    a, b, c = np.arange(20.0), np.arange(20.0) + np.sin(np.arange(20.0)), np.arange(20.0) * 2
    a[[1, 4]] = np.nan
    b[[2, 4, 7]] = np.nan
    result = f_madogram(np.column_stack([a, b, c]), min_pairs=10)
    assert result["pair_counts"][0, 1] == 17
    assert result["pair_counts"][0, 2] == 18
    assert result["pair_counts"][1, 2] == 17
    assert np.allclose(result["f_madogram"], result["f_madogram"].T)

def test_ties_use_average_ranks_and_result_is_finite():
    data = np.array([[1, 1], [1, 2], [2, 2], [2, 3], [3, 3], [3, 4]], dtype=float)
    result = f_madogram(data, min_pairs=3)
    assert np.isfinite(result["f_madogram"][0, 1])
    assert np.isfinite(result["extremal_coefficient"][0, 1])

def test_coordinates_return_pairwise_distances():
    data = np.arange(30.0).reshape(10, 3)
    xy = np.array([[0, 0], [3, 4], [0, 4]], dtype=float)
    result = f_madogram(data, coordinates=xy, min_pairs=5)
    np.testing.assert_allclose(result["distances"], [[0, 5, 4], [5, 0, 3], [4, 3, 0]])

@pytest.mark.parametrize("data", [
    np.ones(10), np.ones((2, 3)), np.ones((10, 1)),
    np.array([[1, 2], [2, np.inf], [3, 4], [4, 5]], dtype=float),
])
def test_rejects_invalid_block_maxima(data):
    with pytest.raises(ValueError):
        f_madogram(data, min_pairs=3)

def test_rejects_insufficient_pairwise_overlap():
    data = np.column_stack([np.arange(10.0), np.arange(10.0)])
    data[:7, 1] = np.nan
    with pytest.raises(ValueError, match="pairwise-complete"):
        f_madogram(data, min_pairs=5)

def test_rejects_invalid_min_pairs_and_coordinates():
    data = np.arange(30.0).reshape(10, 3)
    with pytest.raises(ValueError):
        f_madogram(data, min_pairs=2)
    with pytest.raises(ValueError):
        f_madogram(data, coordinates=np.zeros((2, 2)), min_pairs=3)
