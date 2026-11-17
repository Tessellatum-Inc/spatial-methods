import numpy as np
import pytest
from survey_estimators import horvitz_thompson


def test_horvitz_thompson_total_and_mean_under_srs_without_replacement():
    pi = np.array([.5, .5])
    pi2 = np.array([[.5, 1/6], [1/6, .5]])
    result = horvitz_thompson([10, 20], pi, pi2, population_size=4)
    assert result["total"] == pytest.approx(60)
    assert result["mean"] == pytest.approx(15)
    assert result["variance_total"] == pytest.approx(1100/3)
    assert result["variance_mean"] == pytest.approx(1100/48)


def test_horvitz_thompson_census_has_zero_variance():
    result = horvitz_thompson([3, 4], [1, 1], [[1, 1], [1, 1]], population_size=2)
    assert result["total"] == pytest.approx(7)
    assert result["variance_total"] == pytest.approx(0)


@pytest.mark.parametrize("pi,pi2", [
    ([0, .5], [[0, .1], [.1, .5]]),
    ([.5, .5], [[.5, .1], [.2, .5]]),
    ([.5, .5], [[.4, .1], [.1, .5]]),
    ([.5, .5], [[.5, 0], [0, .5]]),
])
def test_horvitz_thompson_rejects_invalid_probability_design(pi, pi2):
    with pytest.raises(ValueError):
        horvitz_thompson([1, 2], pi, pi2)


def test_horvitz_thompson_rejects_invalid_values_and_population_size():
    with pytest.raises(ValueError):
        horvitz_thompson([1, float("nan")], [.5, .5], [[.5, .2], [.2, .5]])
    with pytest.raises(ValueError):
        horvitz_thompson([1, 2], [.5, .5], [[.5, .2], [.2, .5]], population_size=1)


def test_hansen_hurwitz_total_variance_and_mean_with_replacement():
    from survey_estimators import hansen_hurwitz
    result=hansen_hurwitz([10,20,10,20],[.5,.5,.5,.5],population_size=3)
    assert result["total"]==pytest.approx(30)
    assert result["variance_total"]==pytest.approx(100/3)
    assert result["standard_error_total"]==pytest.approx(np.sqrt(100/3))
    assert result["mean"]==pytest.approx(10)
    assert result["variance_mean"]==pytest.approx(100/27)


def test_hansen_hurwitz_one_draw_has_no_variance_estimate():
    from survey_estimators import hansen_hurwitz
    result=hansen_hurwitz([12],[.25],population_size=8)
    assert result["total"]==pytest.approx(48)
    assert result["variance_total"] is None
    assert result["standard_error_total"] is None


@pytest.mark.parametrize("values,probabilities",[
    ([],[]),([1,2],[.5]),([1,2],[0,.5]),([1,2],[.5,1.1]),
    ([1,float("nan")],[.5,.5]),
])
def test_hansen_hurwitz_rejects_invalid_draws(values,probabilities):
    from survey_estimators import hansen_hurwitz
    with pytest.raises(ValueError):
        hansen_hurwitz(values,probabilities)


def test_hansen_hurwitz_rejects_invalid_population_size():
    from survey_estimators import hansen_hurwitz
    with pytest.raises(ValueError):
        hansen_hurwitz([1,2],[.5,.5],population_size=0)
