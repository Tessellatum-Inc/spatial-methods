import pytest
from empirical_bayes import global_empirical_bayes, local_empirical_bayes

def test_global_estimator_matches_moment_formula():
    y, e = [2, 8, 20, 5], [100, 100, 100, 100]
    result = global_empirical_bayes(y, e)
    m = sum(y) / sum(e)
    rates = [a / b for a, b in zip(y, e)]
    s2 = sum(b * (r - m) ** 2 for b, r in zip(e, rates)) / sum(e)
    a = max(0.0, s2 - m / (sum(e) / len(e)))
    assert result["overall_rate"] == pytest.approx(m)
    assert result["between_area_variance"] == pytest.approx(a)
    for i, (rate, exposure) in enumerate(zip(rates, e)):
        c = a / (a + m / exposure) if a else 0.0
        assert result["shrinkage_factors"][i] == pytest.approx(c)
        assert result["estimates"][i] == pytest.approx(m + c * (rate - m))

def test_smaller_exposure_gets_stronger_shrinkage():
    r = global_empirical_bayes([0, 50, 300], [10, 100, 1000])
    assert r["between_area_variance"] > 0
    assert r["shrinkage_factors"][0] < r["shrinkage_factors"][1] < r["shrinkage_factors"][2]

def test_global_estimator_is_invariant_to_area_order():
    y, e = [2, 8, 20, 5], [100, 100, 100, 100]
    a = global_empirical_bayes(y, e)
    order = [2, 0, 3, 1]
    b = global_empirical_bayes([y[i] for i in order], [e[i] for i in order])
    assert b["overall_rate"] == pytest.approx(a["overall_rate"])
    assert b["between_area_variance"] == pytest.approx(a["between_area_variance"])
    assert b["estimates"] == pytest.approx([a["estimates"][i] for i in order])

def test_zero_between_area_variance_returns_pooled_rate():
    r = global_empirical_bayes([2, 4, 6], [10, 20, 30])
    assert r["between_area_variance"] == 0
    assert r["estimates"] == pytest.approx([0.2, 0.2, 0.2])

def test_zero_counts_are_supported():
    r = global_empirical_bayes([0, 0, 12], [100, 100, 100])
    assert r["estimates"][0] > 0
    assert r["estimates"][2] < 0.12
    assert all(x >= 0 for x in r["estimates"])

def test_local_estimator_uses_supplied_neighborhoods():
    r = local_empirical_bayes([1, 2, 30, 28], [100]*4, [[0,1],[0,1],[2,3],[2,3]])
    assert r["estimates"][0] == pytest.approx(r["estimates"][1])
    assert r["estimates"][2] == pytest.approx(r["estimates"][3])
    assert r["estimates"][0] < r["estimates"][2]

def test_local_full_neighborhood_matches_global():
    y, e = [1, 4, 9], [100, 100, 100]
    r = local_empirical_bayes(y, e, [[0,1,2]]*3)
    g = global_empirical_bayes(y, e)
    assert r["estimates"] == pytest.approx(g["estimates"])

@pytest.mark.parametrize("y,e", [
    ([], []), ([1,2], [1]), ([1.5,2], [10,10]), ([-1,2], [10,10]),
    ([1,float("nan")], [10,10]), ([1,2], [10,0]), ([1,2], [10,float("inf")])
])
def test_invalid_counts_or_exposures_rejected(y,e):
    with pytest.raises(ValueError):
        global_empirical_bayes(y,e)

def test_local_rejects_missing_self_duplicate_and_bad_indices():
    y,e = [1,2,3], [10,10,10]
    with pytest.raises(ValueError): local_empirical_bayes(y,e,[[1],[0,1],[1,2]])
    with pytest.raises(ValueError): local_empirical_bayes(y,e,[[0,0],[0,1],[1,2]])
    with pytest.raises(ValueError): local_empirical_bayes(y,e,[[0],[0,1],[1,9]])

def test_local_requires_one_neighborhood_per_area():
    with pytest.raises(ValueError):
        local_empirical_bayes([1,2],[10,10],[[0,1]])
