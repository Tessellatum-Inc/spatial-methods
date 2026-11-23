import math
import pytest

from bivariate_morans import bivariate_morans_i, row_standardize


def test_row_standardization_and_islands():
    result = row_standardize([[0, 2, 2], [1, 0, 0], [0, 0, 0]])
    assert result == [[0, .5, .5], [1, 0, 0], [0, 0, 0]]


def test_two_unit_hand_calculation():
    result = bivariate_morans_i([0, 1], [0, 1], [[0, 1], [1, 0]])
    assert result["I"] == pytest.approx(-1.0)


def test_directionality_is_not_symmetric_in_general():
    weights = [[0, 1, 0], [0, 0, 1], [1, 0, 0]]
    xy = bivariate_morans_i([1, 2, 4], [4, 1, 3], weights)["I"]
    yx = bivariate_morans_i([4, 1, 3], [1, 2, 4], weights)["I"]
    assert not math.isclose(xy, yx)


def test_permutations_are_reproducible_and_bounded():
    args = ([1, 2, 4, 3], [4, 1, 3, 2],
            [[0, 1, 0, 0], [1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0]])
    a = bivariate_morans_i(*args, permutations=99, seed=42)
    b = bivariate_morans_i(*args, permutations=99, seed=42)
    assert a == b
    assert len(a["simulations"]) == 99
    assert 1 / 100 <= a["p_sim"] <= 1


@pytest.mark.parametrize("x,y,w", [
    ([], [], []),
    ([1, 2], [1], [[0, 1], [1, 0]]),
    ([1, 1], [1, 2], [[0, 1], [1, 0]]),
    ([1, 2], [2, 3], [[0, 1]]),
    ([1], [2], [[0]]),
    ([1, 2], [2, 3], [[1, 1], [1, 0]]),
    ([1, 2], [2, 3], [[0, 0], [0, 0]]),
    ([1, 2], [2, 3], [[0, float("nan")], [1, 0]]),
])
def test_invalid_inputs_raise(x, y, w):
    with pytest.raises(ValueError):
        bivariate_morans_i(x, y, w)


def test_zero_permutations_returns_no_inference():
    result = bivariate_morans_i([0, 1, 2], [2, 1, 0],
                                [[0, 1, 0], [1, 0, 1], [0, 1, 0]])
    assert result["permutations"] == 0
    assert result["p_sim"] is None
