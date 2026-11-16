import pytest
from trend_tests import mann_kendall, seasonal_mann_kendall, sen_slope, seasonal_sen_slope


def test_mann_kendall_detects_increasing_series():
    r = mann_kendall([1, 2, 3, 4, 5])
    assert r["s"] == 10 and r["tau_b"] == pytest.approx(1)
    assert r["z"] > 0 and r["p_value_two_sided"] < 0.1


def test_mann_kendall_detects_decreasing_series():
    r = mann_kendall([5, 4, 3, 2, 1])
    assert r["s"] == -10 and r["tau_b"] == pytest.approx(-1) and r["z"] < 0


def test_mann_kendall_tie_corrected_variance():
    r = mann_kendall([1, 1, 2, 2, 3])
    assert r["variance_s"] == pytest.approx(264 / 18) and r["s"] == 8


def test_constant_series_is_neutral():
    r = mann_kendall([3, 3, 3, 3])
    assert r["variance_s"] == 0 and r["z"] == 0
    assert r["p_value_two_sided"] == 1 and r["tau_b"] == 0


def test_sen_slope_linear_and_irregular_time():
    assert sen_slope([3, 5, 7, 9])["slope"] == pytest.approx(2)
    r = sen_slope([2, 6, 14], times=[0, 2, 6])
    assert r["slope"] == pytest.approx(2) and r["intercept"] == pytest.approx(2)


def test_mann_kendall_affine_invariance():
    a, b = mann_kendall([1, 4, 2, 8, 7]), mann_kendall([101, 104, 102, 108, 107])
    assert a["s"] == b["s"] and a["p_value_two_sided"] == pytest.approx(b["p_value_two_sided"])


@pytest.mark.parametrize("values", [[], [1], [1, float("nan")], [True, 2]])
def test_invalid_series_rejected(values):
    with pytest.raises(ValueError):
        mann_kendall(values)


def test_invalid_sen_time_axis_rejected():
    with pytest.raises(ValueError):
        sen_slope([1, 2, 3], times=[0, 1])
    with pytest.raises(ValueError):
        sen_slope([1, 2, 3], times=[0, 2, 1])


def test_seasonal_mk_compares_only_matching_seasons():
    values = [2, 100, 3, 101, 4, 102, 5, 103]
    r = seasonal_mann_kendall(values, ["warm", "cold"] * 4)
    assert r["s"] == 12 and r["season_count"] == 2
    assert r["seasons"]["warm"]["s"] == 6
    assert r["seasons"]["cold"]["s"] == 6
    assert r["z"] > 0


def test_seasonal_mk_tie_variance_is_summed_within_seasons():
    r = seasonal_mann_kendall([1, 1, 2, 2, 3, 3], ["a", "b"] * 3)
    assert r["s"] == 6
    assert r["variance_s"] == pytest.approx(22 / 3)
    assert r["seasonal_tau"] == pytest.approx(1)


def test_seasonal_sen_uses_only_within_season_pairs():
    r = seasonal_sen_slope([10, 100, 12, 102, 14, 104, 16, 106], ["warm", "cold"] * 4)
    assert r["slope"] == pytest.approx(2) and r["pair_count"] == 12


def test_seasonal_sen_supports_irregular_times():
    r = seasonal_sen_slope([2, 10, 6, 14, 14, 22], ["a", "b"] * 3,
                           times=[0, 0, 2, 2, 6, 6])
    assert r["slope"] == pytest.approx(2) and r["pair_count"] == 6


@pytest.mark.parametrize("seasons", [["a", "a"], [["a"], ["b"], ["a"]]])
def test_seasonal_mk_rejects_invalid_season_groups(seasons):
    values = [1, 2] if len(seasons) == 2 else [1, 2, 3]
    with pytest.raises(ValueError):
        seasonal_mann_kendall(values, seasons)


def test_seasonal_sen_requires_a_within_season_pair():
    with pytest.raises(ValueError):
        seasonal_sen_slope([1, 2], ["a", "b"])


def test_seasonal_methods_reject_length_mismatch():
    with pytest.raises(ValueError):
        seasonal_mann_kendall([1, 2, 3], ["a", "b"])
