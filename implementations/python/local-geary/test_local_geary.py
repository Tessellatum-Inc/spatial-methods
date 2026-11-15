import pytest
from local_geary import local_geary

CHAIN = [[0,1,0,0],[1,0,1,0],[0,1,0,1],[0,0,1,0]]


def test_local_c_matches_weighted_squared_difference_formula():
    values = [1, 2, 4, 8]
    result = local_geary(values, CHAIN, permutations=0)
    expected = tuple(sum(CHAIN[i][j] * (values[i]-values[j])**2 for j in range(4))
                     for i in range(4))
    assert result.local_c == pytest.approx(expected)


def test_conditional_permutations_are_reproducible_and_bounded():
    a = local_geary([1,2,4,8], CHAIN, permutations=199, seed=17)
    b = local_geary([1,2,4,8], CHAIN, permutations=199, seed=17)
    assert a == b
    assert all(0 < p <= 1 for p in a.p_sim)


def test_islands_have_zero_local_c_and_neutral_p_value():
    weights = [[0,0,0],[1,0,0],[0,0,0]]
    result = local_geary([1,2,4], weights, permutations=99)
    assert result.local_c[0] == 0
    assert result.p_sim[0] == 1
    assert result.p_sim[2] == 1


def test_asymmetric_weights_are_supported_without_implicit_standardisation():
    weights = [[0,2,0],[0,0,3],[1,0,0]]
    result = local_geary([1,3,8], weights, permutations=0)
    assert result.local_c == pytest.approx((8,75,49))


@pytest.mark.parametrize("bad", [-1, 1.5, True])
def test_invalid_permutation_counts_are_rejected(bad):
    with pytest.raises(ValueError, match="permutations"):
        local_geary([1,2,3], [[0,1,0],[1,0,1],[0,1,0]], permutations=bad)


def test_invalid_inputs_are_rejected():
    with pytest.raises(ValueError, match="finite"):
        local_geary([1,float("nan"),3], [[0,1,0],[1,0,1],[0,1,0]])
    with pytest.raises(ValueError, match="self-weights"):
        local_geary([1,2,3], [[1,0,0],[1,0,1],[0,1,0]])
    with pytest.raises(ValueError, match="non-negative"):
        local_geary([1,2,3], [[0,-1,0],[1,0,1],[0,1,0]])
