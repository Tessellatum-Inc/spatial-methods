import numpy as np
import pytest

from spatial_scan import monte_carlo_poisson_scan, poisson_spatial_scan


def test_scan_detects_compact_high_rate_cluster():
    coords = np.array([[0., 0.], [1., 0.], [10., 0.], [11., 0.], [20., 0.]])
    cases = np.array([9, 8, 1, 1, 1])
    population = np.full(5, 100.0)
    result = poisson_spatial_scan(
        coords, cases, population, max_population_fraction=0.5, min_cases=2
    )
    assert set(result["member_indices"]) == {0, 1}
    assert result["cases_inside"] == 17
    assert result["expected_cases_inside"] == pytest.approx(8.0)
    assert result["log_likelihood_ratio"] > 0
    assert result["relative_risk"] > 1


def test_scan_uses_population_offset_not_raw_case_counts():
    coords = np.array([[0., 0.], [1., 0.], [10., 0.], [11., 0.]])
    cases = np.array([2, 2, 2, 20])
    population = np.array([100., 100., 100., 1000.])
    result = poisson_spatial_scan(
        coords, cases, population, max_population_fraction=0.5, min_cases=2
    )
    assert result["log_likelihood_ratio"] == pytest.approx(0.0)


def test_scan_includes_all_equal_distance_ties():
    coords = np.array([[0., 0.], [1., 0.], [-1., 0.], [0., 2.]])
    cases = np.array([0, 3, 3, 0])
    population = np.full(4, 100.0)
    result = poisson_spatial_scan(
        coords, cases, population, max_population_fraction=0.75, min_cases=2
    )
    assert set(result["member_indices"]) == {0, 1, 2}


def test_scan_returns_zero_when_no_candidate_is_elevated():
    coords = np.array([[0., 0.], [1., 0.], [10., 0.], [11., 0.]])
    cases = np.array([1, 1, 1, 1])
    population = np.full(4, 100.0)
    result = poisson_spatial_scan(coords, cases, population, min_cases=2)
    assert result["log_likelihood_ratio"] == pytest.approx(0.0)


def test_monte_carlo_scan_is_reproducible_and_returns_plus_one_pvalue():
    coords = np.array([[0., 0.], [1., 0.], [10., 0.], [11., 0.], [20., 0.]])
    cases = np.array([9, 8, 1, 1, 1])
    population = np.full(5, 100.0)
    first = monte_carlo_poisson_scan(
        coords, cases, population, n_simulations=49, rng=123
    )
    second = monte_carlo_poisson_scan(
        coords, cases, population, n_simulations=49, rng=123
    )
    assert first["p_value"] == second["p_value"]
    np.testing.assert_array_equal(
        first["simulated_maxima"], second["simulated_maxima"]
    )
    assert 1 / 50 <= first["p_value"] <= 1.0
    assert first["n_simulations"] == 49


@pytest.mark.parametrize("bad", [
    (np.array([[0., 0.]]), np.array([1]), np.array([1.])),
    (np.array([[0., 0.], [1., 1.]]), np.array([1.5, 0]), np.array([1., 1.])),
    (np.array([[0., 0.], [1., 1.]]), np.array([1, 0]), np.array([1., 0.])),
    (np.array([[0., 0.], [1., 1.]]), np.array([0, 0]), np.array([1., 1.])),
])
def test_scan_rejects_invalid_inputs(bad):
    with pytest.raises(ValueError):
        poisson_spatial_scan(*bad)


def test_scan_rejects_invalid_scan_controls():
    coords = np.array([[0., 0.], [1., 0.]])
    with pytest.raises(ValueError):
        poisson_spatial_scan(coords, [1, 0], [1, 1], max_population_fraction=0.0)
    with pytest.raises(ValueError):
        poisson_spatial_scan(coords, [1, 0], [1, 1], min_cases=0)
    with pytest.raises(ValueError):
        monte_carlo_poisson_scan(coords, [1, 0], [1, 1], n_simulations=0)



def test_besag_newell_identifies_compact_cluster_and_includes_distance_ties():
    from spatial_scan import besag_newell_scan
    coords = np.array([[0., 0.], [1., 0.], [-1., 0.], [10., 0.]])
    cases = np.array([8, 5, 5, 0])
    population = np.full(4, 100)
    result = besag_newell_scan(coords, cases, population, k=10, alpha=0.05)
    centre = result["local_results"][0]
    assert set(centre["member_indices"]) == {0, 1, 2}
    assert centre["cases_inside"] == 18
    assert centre["population_inside"] == 300
    assert centre["expected_cases_inside"] == pytest.approx(13.5)
    assert centre["p_value"] < 0.05
    assert centre["is_cluster"]


def test_besag_newell_uses_exact_hypergeometric_tail():
    from spatial_scan import _hypergeometric_upper_tail
    # Drawing 10 cases among 20 people, with 5 people in the zone: P(X >= 5) = C(15,5)/C(20,10).
    assert _hypergeometric_upper_tail(20, 5, 10, 5) == pytest.approx(3003 / 184756)


def test_besag_newell_global_monte_carlo_is_reproducible():
    from spatial_scan import monte_carlo_besag_newell
    coords = np.array([[0., 0.], [1., 0.], [10., 0.], [11., 0.], [20., 0.]])
    cases = np.array([9, 8, 1, 1, 1])
    population = np.full(5, 100)
    a = monte_carlo_besag_newell(coords, cases, population, k=10,
                                 n_simulations=39, rng=123)
    b = monte_carlo_besag_newell(coords, cases, population, k=10,
                                 n_simulations=39, rng=123)
    assert a["p_value"] == b["p_value"]
    np.testing.assert_array_equal(a["simulated_significant_counts"],
                                  b["simulated_significant_counts"])
    assert 1 / 40 <= a["p_value"] <= 1
    assert a["n_simulations"] == 39


@pytest.mark.parametrize("bad", [
    (np.array([[0., 0.]]), np.array([1]), np.array([10])),
    (np.array([[0., 0.], [1., 1.]]), np.array([1.5, 0]), np.array([10, 10])),
    (np.array([[0., 0.], [1., 1.]]), np.array([1, 0]), np.array([10, 0])),
    (np.array([[0., 0.], [1., 1.]]), np.array([1, 0]), np.array([10.5, 10])),
])
def test_besag_newell_rejects_invalid_inputs(bad):
    from spatial_scan import besag_newell_scan
    with pytest.raises(ValueError):
        besag_newell_scan(*bad, k=1)


def test_besag_newell_rejects_invalid_controls_and_population_smaller_than_cases():
    from spatial_scan import besag_newell_scan, monte_carlo_besag_newell
    coords = np.array([[0., 0.], [1., 1.]])
    with pytest.raises(ValueError):
        besag_newell_scan(coords, [1, 0], [10, 10], k=0)
    with pytest.raises(ValueError):
        besag_newell_scan(coords, [1, 0], [10, 10], alpha=1)
    with pytest.raises(ValueError):
        besag_newell_scan(coords, [2, 0], [1, 1], k=1)
    with pytest.raises(ValueError):
        monte_carlo_besag_newell(coords, [1, 0], [10, 10], k=1,
                                 n_simulations=0)
