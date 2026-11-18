import numpy as np
import pytest
from hansen_hurwitz import hansen_hurwitz


def test_hand_computed_draw_level_estimates_and_total_variance():
    # y/p values are [10, 20, 30]; total estimate = 20, sample variance = 100.
    r = hansen_hurwitz([2, 4, 6], [0.2, 0.2, 0.2])
    np.testing.assert_allclose(r.draw_estimates, [10, 20, 30])
    assert r.total_estimate == pytest.approx(20)
    assert r.total_variance_estimate == pytest.approx(100 / 3)
    assert r.mean_estimate is None and r.mean_variance_estimate is None


def test_duplicate_draws_are_kept_as_independent_draws():
    r = hansen_hurwitz([4, 4, 8], [0.5, 0.5, 0.25])
    np.testing.assert_allclose(r.draw_estimates, [8, 8, 32])
    assert r.total_estimate == pytest.approx(16)


def test_mean_and_variance_scale_with_known_population_size():
    r = hansen_hurwitz([2, 4, 6], [0.2, 0.2, 0.2], population_size=10)
    assert r.mean_estimate == pytest.approx(2)
    assert r.mean_variance_estimate == pytest.approx(r.total_variance_estimate / 100)


def test_single_draw_has_estimate_but_variance_is_unavailable():
    r = hansen_hurwitz([5], [0.1], population_size=20)
    assert r.total_estimate == pytest.approx(50)
    assert r.total_variance_estimate is None
    assert r.mean_estimate == pytest.approx(2.5)
    assert r.mean_variance_estimate is None


@pytest.mark.parametrize("values,probs", [
    ([], []), ([1, 2], [0.5]), ([float("nan")], [0.2]),
    ([1], [0]), ([1], [1.1]), ([1], [float("inf")])
])
def test_invalid_vectors_rejected(values, probs):
    with pytest.raises(ValueError):
        hansen_hurwitz(values, probs)


@pytest.mark.parametrize("n", [0, -2, 2.5, True])
def test_invalid_population_size_rejected(n):
    with pytest.raises(ValueError):
        hansen_hurwitz([1, 2], [0.5, 0.5], population_size=n)
