import math
import pytest
from models import theil_sen, pettitt, viterbi


def test_theil_sen_resists_single_extreme_outlier():
    slope, intercept = theil_sen([0, 1, 2, 3, 4], [1, 3, 5, 7, 100])
    assert slope == pytest.approx(2.0)
    assert intercept == pytest.approx(1.0)


def test_theil_sen_rejects_duplicate_only_x():
    with pytest.raises(ValueError):
        theil_sen([1, 1, 1], [2, 3, 4])


def test_pettitt_detects_rank_shift():
    split, statistic, p = pettitt([0, 1, 0, 1, 8, 9, 8, 10])
    assert split == 4
    assert statistic > 0
    assert 0 <= p <= 1


def test_viterbi_decodes_most_likely_state_sequence():
    path, score = viterbi(
        [0, 0, 1, 1],
        [0.6, 0.4],
        [[0.9, 0.1], [0.1, 0.9]],
        [[0.9, 0.1], [0.2, 0.8]],
    )
    assert path == [0, 0, 1, 1]
    assert math.isfinite(score)


def test_viterbi_rejects_invalid_probability_rows():
    with pytest.raises(ValueError):
        viterbi([0], [0.5, 0.5], [[0.8, 0.8], [0.2, 0.8]], [[1], [1]])


def test_viterbi_rejects_invalid_observation_symbol():
    with pytest.raises(ValueError):
        viterbi([2], [1.0], [[1.0]], [[1.0, 0.0]])


def test_viterbi_rejects_impossible_sequence():
    with pytest.raises(ValueError):
        viterbi([0, 1], [1.0, 0.0], [[1.0, 0.0], [0.0, 1.0]], [[1.0, 0.0], [0.0, 1.0]])
