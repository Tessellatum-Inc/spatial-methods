import pytest
from local_morans_i import local_morans_i

CHAIN = [
    [0, 1, 0, 0],
    [1, 0, 1, 0],
    [0, 1, 0, 1],
    [0, 0, 1, 0],
]


def test_local_statistic_uses_documented_standardised_scaling():
    result = local_morans_i([1, 2, 3, 4], CHAIN, permutations=0)
    z = result.standardized_values
    expected = [(3 / 4) * z[i] * sum(CHAIN[i][j] * z[j] for j in range(4))
                for i in range(4)]
    assert result.local_i == pytest.approx(expected)


def test_high_high_quadrant_code_matches_documented_convention():
    result = local_morans_i([10, 9, 1, 2], CHAIN, permutations=0)
    assert result.quadrant[0] == 1


def test_conditional_permutation_is_reproducible_and_returns_valid_p_values():
    a = local_morans_i([1, 2, 3, 4], CHAIN, permutations=199, seed=42)
    b = local_morans_i([1, 2, 3, 4], CHAIN, permutations=199, seed=42)
    assert a == b
    assert all(0 < p <= 1 for p in a.p_sim)


def test_islands_have_zero_lag_and_neutral_p_value():
    weights = [[0, 0, 0], [1, 0, 0], [0, 0, 0]]
    result = local_morans_i([1, 2, 4], weights, permutations=99)
    assert result.spatial_lag[0] == 0
    assert result.p_sim[0] == 1
    assert result.p_sim[2] == 1


def test_asymmetric_and_non_row_standardised_weights_are_supported():
    weights = [[0, 2, 0], [0, 0, 3], [1, 0, 0]]
    result = local_morans_i([1, 3, 8], weights, permutations=25, seed=2)
    assert len(result.local_i) == 3


@pytest.mark.parametrize("bad", [-1, 1.5, True])
def test_invalid_permutation_counts_are_rejected(bad):
    with pytest.raises(ValueError, match="permutations"):
        local_morans_i([1, 2, 3], [[0, 1, 0], [1, 0, 1], [0, 1, 0]],
                       permutations=bad)


def test_constant_values_and_invalid_weights_are_rejected():
    with pytest.raises(ValueError, match="constant"):
        local_morans_i([2, 2, 2], [[0, 1, 0], [1, 0, 1], [0, 1, 0]])
    with pytest.raises(ValueError, match="self-weights"):
        local_morans_i([1, 2, 3], [[1, 0, 0], [1, 0, 1], [0, 1, 0]])
    with pytest.raises(ValueError, match="non-negative"):
        local_morans_i([1, 2, 3], [[0, -1, 0], [1, 0, 1], [0, 1, 0]])
