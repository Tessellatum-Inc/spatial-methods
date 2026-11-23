import pytest
from getis_ord import global_getis_ord_g, local_getis_ord_gistar

CHAIN = [[0,1,0,0],[1,0,1,0],[0,1,0,1],[0,0,1,0]]


def test_global_g_matches_pairwise_definition_and_expectation():
    result = global_getis_ord_g([1,2,3,4], CHAIN, permutations=0)
    assert result.statistic == pytest.approx(4/7)
    assert result.expected == pytest.approx(0.5)
    assert result.p_sim == 1
    assert result.simulated_mean is None


def test_global_g_is_invariant_to_positive_rescaling():
    a = global_getis_ord_g([1,2,3,4], CHAIN, permutations=0)
    b = global_getis_ord_g([10,20,30,40], CHAIN, permutations=0)
    assert a.statistic == pytest.approx(b.statistic)


def test_global_g_permutation_is_reproducible():
    a = global_getis_ord_g([1,2,3,4], CHAIN, permutations=199, seed=123)
    b = global_getis_ord_g([1,2,3,4], CHAIN, permutations=199, seed=123)
    assert a == b
    assert 0 < a.p_sim <= 1
    assert a.simulated_sd is not None


def test_global_g_rejects_nonpositive_values_and_invalid_weights():
    with pytest.raises(ValueError, match="positive values"):
        global_getis_ord_g([0,2,3], [[0,1,0],[1,0,1],[0,1,0]])
    with pytest.raises(ValueError, match="zero diagonal"):
        global_getis_ord_g([1,2,3], [[1,0,0],[1,0,1],[0,1,0]])


def test_local_gistar_matches_standard_randomisation_formula():
    values = [1,2,4,8]
    weights = [[1,1,0,0],[1,1,1,0],[0,1,1,1],[0,0,1,1]]
    result = local_getis_ord_gistar(values, weights)
    n = len(values)
    mean = sum(values)/n
    s = (sum(v*v for v in values)/n - mean*mean)**0.5
    for i, row in enumerate(weights):
        sw, sw2 = sum(row), sum(v*v for v in row)
        expected = (sum(a*b for a,b in zip(row,values))-mean*sw) / (
            s*((n*sw2-sw*sw)/(n-1))**0.5
        )
        assert result.z_score[i] == pytest.approx(expected)
        assert 0 <= result.p_two_sided_normal[i] <= 1


def test_gistar_requires_binary_weights_and_self_inclusion():
    with pytest.raises(ValueError, match="binary"):
        local_getis_ord_gistar([1,2,3], [[1,0.5,0],[1,1,0],[0,1,1]])
    with pytest.raises(ValueError, match="include the focal"):
        local_getis_ord_gistar([1,2,3], [[0,1,0],[1,1,0],[0,1,1]])


def test_gistar_rejects_constant_values_and_zero_variance_neighbourhood():
    with pytest.raises(ValueError, match="constant"):
        local_getis_ord_gistar([2,2,2], [[1,1,0],[1,1,1],[0,1,1]])
    with pytest.raises(ValueError, match="zero randomisation variance"):
        local_getis_ord_gistar([1,2,3], [[1,1,1],[1,1,1],[1,1,1]])
