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



def test_tango_statistic_matches_quadratic_form_and_decays_with_distance():
    from spatial_scan import tango_statistic
    coords = np.array([[0., 0.], [1., 0.], [10., 0.]])
    cases = np.array([8, 1, 1])
    population = np.array([100., 100., 100.])
    result = tango_statistic(coords, cases, population, phi=2.0)
    delta = result["observed_proportions"] - result["expected_proportions"]
    expected = float(delta @ result["closeness_matrix"] @ delta)
    assert result["statistic"] == pytest.approx(expected)
    assert result["closeness_matrix"][0, 1] > result["closeness_matrix"][0, 2]
    assert np.allclose(result["closeness_matrix"], result["closeness_matrix"].T)
    assert result["statistic"] >= 0


def test_tango_monte_carlo_test_is_reproducible_and_plus_one_corrected():
    from spatial_scan import monte_carlo_tango_test
    coords = np.array([[0., 0.], [1., 0.], [10., 0.], [11., 0.]])
    cases = np.array([12, 8, 1, 1])
    population = np.full(4, 100.)
    a = monte_carlo_tango_test(coords, cases, population, phi=2.0,
                               n_simulations=39, rng=42)
    b = monte_carlo_tango_test(coords, cases, population, phi=2.0,
                               n_simulations=39, rng=42)
    assert a["p_value"] == b["p_value"]
    np.testing.assert_array_equal(a["simulated_statistics"], b["simulated_statistics"])
    assert 1 / 40 <= a["p_value"] <= 1


@pytest.mark.parametrize("bad", [
    (np.array([[0., 0.]]), np.array([1]), np.array([10.])),
    (np.array([[0., 0.], [1., 1.]]), np.array([1.5, 0]), np.array([10., 10.])),
    (np.array([[0., 0.], [1., 1.]]), np.array([0, 0]), np.array([10., 10.])),
    (np.array([[0., 0.], [1., 1.]]), np.array([1, 0]), np.array([10., 0.])),
])
def test_tango_rejects_invalid_data(bad):
    from spatial_scan import tango_statistic
    with pytest.raises(ValueError):
        tango_statistic(*bad, phi=1.0)


def test_tango_rejects_invalid_phi_and_simulation_count():
    from spatial_scan import tango_statistic, monte_carlo_tango_test
    coords = np.array([[0., 0.], [1., 1.]])
    with pytest.raises(ValueError):
        tango_statistic(coords, [1, 0], [10, 10], phi=0)
    with pytest.raises(ValueError):
        monte_carlo_tango_test(coords, [1, 0], [10, 10], phi=1,
                               n_simulations=0)



def test_elliptical_scan_detects_elongated_cluster_and_reports_geometry():
    from spatial_scan import elliptical_poisson_scan
    coords = np.array([
        [0., 0.], [2., 0.], [4., 0.], [6., 0.],
        [0., 4.], [2., 4.], [4., 4.], [6., 4.],
        [0., 10.], [2., 10.], [4., 10.], [6., 10.],
    ])
    cases = np.array([8, 8, 8, 8, 7, 7, 7, 7, 1, 1, 1, 1])
    population = np.full(len(coords), 100.)
    result = elliptical_poisson_scan(
        coords, cases, population, shape_ratios=(1., 2., 4.),
        angles_degrees=(0., 90.), max_population_fraction=0.75,
        min_cases=2,
    )
    assert result["log_likelihood_ratio"] > 0
    assert result["shape_ratio"] >= 1
    assert result["semi_major_axis"] >= result["semi_minor_axis"]
    assert result["angle_degrees"] in (0., 90.)
    assert set(result["member_indices"]).issubset(set(range(len(coords))))


def test_elliptical_scan_includes_equal_ellipse_radius_ties():
    from spatial_scan import elliptical_poisson_scan
    coords = np.array([[0., 0.], [1., 0.], [-1., 0.], [0., 5.]])
    cases = np.array([0, 1, 1, 0])
    population = np.full(4, 100.)
    result = elliptical_poisson_scan(
        coords, cases, population, shape_ratios=(1.,),
        angles_degrees=(0.,), max_population_fraction=0.75,
        min_cases=2,
    )
    assert set(result["member_indices"]) == {0, 1, 2}


def test_elliptical_monte_carlo_is_reproducible_and_plus_one_corrected():
    from spatial_scan import monte_carlo_elliptical_poisson_scan
    coords = np.array([[0., 0.], [1., 0.], [10., 0.], [11., 0.], [20., 0.]])
    cases = np.array([9, 8, 1, 1, 1])
    population = np.full(5, 100.)
    kwargs = dict(n_simulations=29, shape_ratios=(1., 2.),
                  angles_degrees=(0., 90.), rng=91)
    a = monte_carlo_elliptical_poisson_scan(coords, cases, population, **kwargs)
    b = monte_carlo_elliptical_poisson_scan(coords, cases, population, **kwargs)
    assert a["p_value"] == b["p_value"]
    np.testing.assert_array_equal(a["simulated_maxima"], b["simulated_maxima"])
    assert 1 / 30 <= a["p_value"] <= 1


@pytest.mark.parametrize("shapes,angles", [
    ((), (0.,)),
    ((0.5,), (0.,)),
    ((1., np.nan), (0.,)),
    ((1.,), (180.,)),
    ((1.,), ()),
])
def test_elliptical_scan_rejects_invalid_candidate_grids(shapes, angles):
    from spatial_scan import elliptical_poisson_scan
    coords = np.array([[0., 0.], [1., 1.]])
    with pytest.raises(ValueError):
        elliptical_poisson_scan(coords, [1, 0], [10, 10],
                                shape_ratios=shapes, angles_degrees=angles)


def test_elliptical_scan_rejects_invalid_simulation_count():
    from spatial_scan import monte_carlo_elliptical_poisson_scan
    coords = np.array([[0., 0.], [1., 1.]])
    with pytest.raises(ValueError):
        monte_carlo_elliptical_poisson_scan(
            coords, [1, 0], [10, 10], n_simulations=0
        )



def test_ellipse_ratio_one_matches_circular_scan_candidate_family():
    from spatial_scan import elliptical_poisson_scan
    coords = np.array([[0., 0.], [1., 0.], [10., 0.], [11., 0.], [20., 0.]])
    cases = np.array([9, 8, 1, 1, 1])
    population = np.full(5, 100.)
    circular = poisson_spatial_scan(
        coords, cases, population, max_population_fraction=0.75, min_cases=2
    )
    elliptical = elliptical_poisson_scan(
        coords, cases, population, shape_ratios=(1.,),
        angles_degrees=(0., 45., 90.), max_population_fraction=0.75,
        min_cases=2,
    )
    assert elliptical["log_likelihood_ratio"] == pytest.approx(
        circular["log_likelihood_ratio"]
    )
    assert set(elliptical["member_indices"]) == set(circular["member_indices"])



def test_flexible_scan_finds_connected_irregular_zone():
    from spatial_scan import flexible_poisson_scan
    coords = np.array([[0., 0.], [1., 0.], [2., 0.], [3., 0.], [4., 0.]])
    adjacency = np.zeros((5, 5), dtype=bool)
    for i in range(4):
        adjacency[i, i + 1] = adjacency[i + 1, i] = True
    cases = np.array([8, 8, 8, 1, 1])
    population = np.full(5, 100.)
    result = flexible_poisson_scan(
        coords, cases, population, adjacency, max_cluster_size=3,
        max_population_fraction=0.8, min_cases=2,
    )
    assert result["log_likelihood_ratio"] > 0
    assert result["n_areas"] <= 3
    members = set(result["member_indices"])
    assert members
    assert all(any(adjacency[i, j] for j in members) for i in members if i != result["root_index"])


def test_flexible_scan_never_returns_a_disconnected_zone():
    from spatial_scan import flexible_poisson_scan
    coords = np.array([[0., 0.], [1., 0.], [2., 0.], [3., 0.]])
    adjacency = np.zeros((4, 4), dtype=bool)
    adjacency[0, 1] = adjacency[1, 0] = True
    adjacency[2, 3] = adjacency[3, 2] = True
    cases = np.array([0, 8, 8, 0])
    population = np.full(4, 100.)
    result = flexible_poisson_scan(
        coords, cases, population, adjacency, max_cluster_size=3,
        max_population_fraction=0.75, min_cases=2,
    )
    assert set(result["member_indices"]) in ({1, 2}, {0, 1, 2}, {1, 2, 3}, set())
    if result["member_indices"]:
        members = set(result["member_indices"])
        reached = {next(iter(members))}
        while True:
            expanded = reached | {
                j for i in reached for j in members if adjacency[i, j]
            }
            if expanded == reached:
                break
            reached = expanded
        assert reached == members


def test_flexible_scan_respects_candidate_size_and_is_reproducible():
    from spatial_scan import flexible_poisson_scan, monte_carlo_flexible_poisson_scan
    coords = np.array([[0., 0.], [1., 0.], [2., 0.], [3., 0.], [4., 0.]])
    adjacency = np.zeros((5, 5), dtype=bool)
    for i in range(4):
        adjacency[i, i + 1] = adjacency[i + 1, i] = True
    cases = np.array([8, 8, 8, 1, 1])
    population = np.full(5, 100.)
    result = flexible_poisson_scan(
        coords, cases, population, adjacency, max_cluster_size=2,
        max_population_fraction=0.8,
    )
    assert result["n_areas"] <= 2
    kwargs = dict(n_simulations=19, max_cluster_size=3,
                  max_population_fraction=0.8, rng=17)
    a = monte_carlo_flexible_poisson_scan(coords, cases, population, adjacency, **kwargs)
    b = monte_carlo_flexible_poisson_scan(coords, cases, population, adjacency, **kwargs)
    assert a["p_value"] == b["p_value"]
    np.testing.assert_array_equal(a["simulated_maxima"], b["simulated_maxima"])
    assert 1 / 20 <= a["p_value"] <= 1


@pytest.mark.parametrize("bad_graph", [
    np.zeros((3, 3)),
    np.array([[0., 1.], [0., 0.]]),
    np.array([[1., 0.], [0., 0.]]),
    np.array([[0., np.nan], [np.nan, 0.]]),
])
def test_flexible_scan_rejects_invalid_adjacency(bad_graph):
    from spatial_scan import flexible_poisson_scan
    coords = np.array([[0., 0.], [1., 1.]])
    with pytest.raises(ValueError):
        flexible_poisson_scan(coords, [1, 0], [10, 10], bad_graph)


def test_flexible_scan_rejects_invalid_size_and_simulation_controls():
    from spatial_scan import flexible_poisson_scan, monte_carlo_flexible_poisson_scan
    coords = np.array([[0., 0.], [1., 1.]])
    graph = np.array([[0, 1], [1, 0]])
    with pytest.raises(ValueError):
        flexible_poisson_scan(coords, [1, 0], [10, 10], graph, max_cluster_size=16)
    with pytest.raises(ValueError):
        monte_carlo_flexible_poisson_scan(
            coords, [1, 0], [10, 10], graph, n_simulations=0
        )
