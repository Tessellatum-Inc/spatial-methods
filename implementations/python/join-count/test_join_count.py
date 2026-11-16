import pytest
from join_count import join_count_test

PATH = [[0,1,0,0],[1,0,1,0],[0,1,0,1],[0,0,1,0]]


def test_join_counts_and_randomisation_expectations_on_path():
    result = join_count_test([1,1,0,0], PATH, permutations=0)
    assert result.observed == (1,1,1)
    assert result.expected == pytest.approx((0.5,0.5,2.0))
    assert result.n_edges == 3
    assert result.n_black == result.n_white == 2


def test_complete_graph_expectations_match_combinatorial_pair_probabilities():
    n = 4
    weights = [[0 if i == j else 1 for j in range(n)] for i in range(n)]
    result = join_count_test([1,1,0,0], weights, permutations=0)
    assert result.observed == (1,1,4)
    assert result.expected == pytest.approx((1,1,4))


def test_conditional_permutations_are_reproducible_and_preserve_composition():
    a = join_count_test([1,1,0,0], PATH, permutations=199, seed=21)
    b = join_count_test([1,1,0,0], PATH, permutations=199, seed=21)
    assert a == b
    assert all(0 < p <= 1 for p in a.p_upper + a.p_lower)


def test_all_one_class_has_only_same_class_joins():
    result = join_count_test([1,1,1,1], PATH, permutations=99)
    assert result.observed == (3,0,0)
    assert result.expected == pytest.approx((3,0,0))
    assert result.p_upper[0] == 1


@pytest.mark.parametrize("bad", [-1, 1.5, True])
def test_invalid_permutation_counts_are_rejected(bad):
    with pytest.raises(ValueError, match="permutations"):
        join_count_test([1,0,1,0], PATH, permutations=bad)


def test_invalid_labels_and_weight_matrices_are_rejected():
    with pytest.raises(ValueError, match="binary"):
        join_count_test([1,2,0,0], PATH)
    with pytest.raises(ValueError, match="symmetric"):
        join_count_test([1,1,0,0], [[0,1,0,0],[0,0,1,0],[0,1,0,1],[0,0,1,0]])
    with pytest.raises(ValueError, match="zero diagonal"):
        join_count_test([1,1,0,0], [[1,0,0,0],[0,0,1,0],[0,1,0,1],[0,0,1,0]])
    with pytest.raises(ValueError, match="at least one"):
        join_count_test([1,1,0,0], [[0]*4 for _ in range(4)])
