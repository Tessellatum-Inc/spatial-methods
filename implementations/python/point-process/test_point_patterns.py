import math
import pytest
from point_patterns import nearest_neighbor_distances, nearest_neighbor_cdf, ripley_k_translation, pair_correlation_from_k

def test_nearest_neighbor_distances_for_square():
    points=[(0,0),(1,0),(1,1),(0,1)]
    assert nearest_neighbor_distances(points)==pytest.approx([1,1,1,1])
    assert nearest_neighbor_cdf(points,[0.5,1,2])==pytest.approx([0,1,1])

def test_translation_k_zero_below_nearest_pair_and_monotone():
    points=[(2,2),(8,2),(2,8),(8,8)]
    radii=[1,6,9]
    values=ripley_k_translation(points,(0,0,10,10),radii)
    assert values[0]==0
    assert values[1] < values[2]
    assert all(v>=0 for v in values)

def test_k_translation_matches_hand_calculation_without_edge_loss():
    points=[(4,4),(6,4)]
    # For displacement (2,0), overlap fraction is 0.8; both ordered pairs count.
    result=ripley_k_translation(points,(0,0,10,10),[2])
    assert result[0]==pytest.approx(100/0.8)

def test_pair_correlation_from_poisson_reference_curve():
    radii=[1,2,3,4]
    k=[math.pi*r*r for r in radii]
    g=pair_correlation_from_k(radii,k)
    assert g[1]==pytest.approx(1.0,abs=0.2)
    assert g[2]==pytest.approx(1.0,abs=0.2)

def test_rejects_invalid_window_and_radii():
    with pytest.raises(ValueError):
        ripley_k_translation([(0,0),(1,1)],(0,0,0,1),[1])
    with pytest.raises(ValueError):
        nearest_neighbor_cdf([(0,0),(1,1)],[-1])


def test_inhomogeneous_k_translation_uses_pointwise_intensities_and_ordered_pairs():
    from point_patterns import ripley_k_inhomogeneous_translation
    points = [(4, 4), (6, 4)]
    # Rectangle overlap is 8*10=80; both ordered pairs contribute.
    got = ripley_k_inhomogeneous_translation(points, (0, 0, 10, 10), [1.9, 2.0],
                                              [0.02, 0.04])
    expected = 2.0 / (0.02 * 0.04 * 80.0)
    assert got == pytest.approx([0.0, expected])


def test_inhomogeneous_k_constant_intensity_matches_direct_formula():
    from point_patterns import ripley_k_inhomogeneous_translation
    points = [(2, 2), (5, 2), (2, 7)]
    lam = [0.03, 0.03, 0.03]
    got = ripley_k_inhomogeneous_translation(points, (0, 0, 10, 10), [3.0], lam)[0]
    expected = 0.0
    for i, (x, y) in enumerate(points):
        for j, (a, b) in enumerate(points):
            if i == j:
                continue
            overlap = (10 - abs(x-a)) * (10 - abs(y-b))
            if math.hypot(x-a, y-b) <= 3.0:
                expected += 1.0 / (lam[i] * lam[j] * overlap)
    assert got == pytest.approx(expected)


def test_inhomogeneous_k_rejects_invalid_intensity_and_count():
    from point_patterns import ripley_k_inhomogeneous_translation
    points = [(1, 1), (2, 2)]
    with pytest.raises(ValueError):
        ripley_k_inhomogeneous_translation(points, (0, 0, 5, 5), [1], [0.1])
    with pytest.raises(ValueError):
        ripley_k_inhomogeneous_translation(points, (0, 0, 5, 5), [1], [0.1, 0.0])
    with pytest.raises(ValueError):
        ripley_k_inhomogeneous_translation(points, (0, 0, 5, 5), [1], [float("nan"), 0.1])


def test_quadrat_counts_assign_upper_and_right_boundaries_to_last_cell():
    from point_patterns import quadrat_count_test
    result = quadrat_count_test(
        [(0, 0), (0.5, 0.5), (1, 1), (1, 0)],
        (0, 0, 1, 1), nx=2, ny=2, n_simulations=99, seed=4,
    )
    assert result["counts"] == [[1, 1], [0, 2]]
    assert result["expected_per_quadrat"] == pytest.approx(1.0)
    assert result["pearson_statistic"] == pytest.approx(2.0)
    assert result["degrees_of_freedom"] == 3


def test_quadrat_test_is_reproducible_and_uses_plus_one_pvalue():
    from point_patterns import quadrat_count_test
    points = [(0.1, 0.1), (0.2, 0.2), (0.3, 0.3), (0.8, 0.8)]
    a = quadrat_count_test(points, (0, 0, 1, 1), 2, 2, n_simulations=199, seed=42)
    b = quadrat_count_test(points, (0, 0, 1, 1), 2, 2, n_simulations=199, seed=42)
    assert a == b
    assert 1 / 200 <= a["pvalue"] <= 1
    assert sum(map(sum, a["counts"])) == len(points)


def test_quadrat_test_supports_one_point_and_multiple_grid_shapes():
    from point_patterns import quadrat_count_test
    result = quadrat_count_test([(0.5, 0.5)], (0, 0, 1, 1), 3, 2, n_simulations=19, seed=1)
    assert result["n_points"] == 1
    assert len(result["counts"]) == 2
    assert all(len(row) == 3 for row in result["counts"])


@pytest.mark.parametrize("kwargs", [
    {"nx": 0}, {"ny": 0}, {"nx": 1, "ny": 1},
    {"nx": 2.5}, {"n_simulations": 0}, {"n_simulations": 1.5},
    {"seed": True},
])
def test_quadrat_test_rejects_invalid_controls(kwargs):
    from point_patterns import quadrat_count_test
    with pytest.raises(ValueError):
        quadrat_count_test([(0.2, 0.2)], (0, 0, 1, 1), **kwargs)


def test_quadrat_test_rejects_invalid_window_points_and_duplicates():
    from point_patterns import quadrat_count_test
    with pytest.raises(ValueError):
        quadrat_count_test([(0.2, 0.2)], (0, 0, 0, 1))
    with pytest.raises(ValueError):
        quadrat_count_test([(1.2, 0.2)], (0, 0, 1, 1))
    with pytest.raises(ValueError):
        quadrat_count_test([(0.2, 0.2), (0.2, 0.2)], (0, 0, 1, 1))
    with pytest.raises(ValueError):
        quadrat_count_test([], (0, 0, 1, 1))


def test_empty_space_f_is_reproducible_and_monotone():
    from point_patterns import empty_space_cdf
    points = [(0.25, 0.25), (0.75, 0.75)]
    a = empty_space_cdf(points, (0, 0, 1, 1), [0.05, 0.2, 0.5], n_samples=500, seed=7)
    b = empty_space_cdf(points, (0, 0, 1, 1), [0.05, 0.2, 0.5], n_samples=500, seed=7)
    assert a == b
    assert a == sorted(a)
    assert all(0 <= value <= 1 for value in a)


def test_j_function_combines_g_and_f_and_marks_undefined_tail():
    from point_patterns import j_function
    g, f, j = j_function(
        [(0.25, 0.25), (0.75, 0.75)], (0, 0, 1, 1), [0.1, 2.0],
        n_samples=200, seed=3,
    )
    assert g[0] == 0
    assert f[0] <= f[1]
    assert math.isnan(j[1])
    if f[0] < 1:
        assert j[0] == pytest.approx((1 - g[0]) / (1 - f[0]))


def test_empty_space_rejects_invalid_controls():
    from point_patterns import empty_space_cdf
    points = [(0.2, 0.2), (0.8, 0.8)]
    with pytest.raises(ValueError, match="n_samples"):
        empty_space_cdf(points, (0, 0, 1, 1), [0.1], n_samples=0)
    with pytest.raises(ValueError, match="seed"):
        empty_space_cdf(points, (0, 0, 1, 1), [0.1], seed=True)
    with pytest.raises(ValueError, match="radii"):
        empty_space_cdf(points, (0, 0, 1, 1), [])


def test_cross_type_nearest_neighbor_cdf_uses_source_to_target_distances():
    from point_patterns import cross_nearest_neighbor_cdf
    pts = [(2, 2), (7, 7), (3, 2), (7, 8)]
    marks = ["A", "A", "B", "B"]
    assert cross_nearest_neighbor_cdf(pts, marks, "A", "B", [0.5, 1, 2]) == [0, 1, 1]


def test_cross_k_translation_matches_hand_calculation_and_independence_scale():
    from point_patterns import cross_ripley_k_translation
    pts = [(2, 2), (7, 7), (3, 2), (7, 8)]
    marks = ["A", "A", "B", "B"]
    got = cross_ripley_k_translation(pts, marks, (0, 0, 10, 10), "A", "B", [0.9, 1, 2])
    # Two cross pairs at distance one; each has overlap 90 and weight 100/90.
    assert got[0] == 0
    assert got[1] == pytest.approx(100 / 4 * 2 * (100 / 90))
    assert got[2] >= got[1]


def test_cross_pair_correlation_matches_finite_difference_of_k():
    from point_patterns import cross_pair_correlation_from_k
    radii = [1, 2, 3, 4]
    k = [math.pi*r*r for r in radii]
    got = cross_pair_correlation_from_k(radii, k)
    assert got[1] == pytest.approx(1, abs=0.2)
    assert got[2] == pytest.approx(1, abs=0.2)


def test_cross_j_returns_g_f_and_j_with_seeded_empty_space_sampling():
    from point_patterns import cross_j_function
    pts = [(2, 2), (7, 7), (3, 2), (7, 8)]
    marks = ["A", "A", "B", "B"]
    a = cross_j_function(pts, marks, (0, 0, 10, 10), "A", "B",
                         [0.5, 1, 20], n_samples=500, seed=12)
    b = cross_j_function(pts, marks, (0, 0, 10, 10), "A", "B",
                         [0.5, 1, 20], n_samples=500, seed=12)
    g, f, j = a
    g2, f2, j2 = b
    assert g == g2 and f == f2
    assert j[:-1] == pytest.approx(j2[:-1])
    assert g == [0, 1, 1]
    assert all(0 <= value <= 1 for value in f)
    assert math.isnan(j[-1]) and math.isnan(j2[-1])


@pytest.mark.parametrize("bad_marks", [
    ["A", "A"], ["A", "A", "A", "A"], ["A", "A", "B", None]
])
def test_cross_type_methods_reject_missing_or_invalid_mark_groups(bad_marks):
    from point_patterns import cross_nearest_neighbor_cdf, cross_ripley_k_translation
    pts = [(2, 2), (7, 7), (3, 2), (7, 8)]
    with pytest.raises(ValueError):
        cross_nearest_neighbor_cdf(pts, bad_marks, "A", "B", [1])
    with pytest.raises(ValueError):
        cross_ripley_k_translation(pts, bad_marks, (0, 0, 10, 10), "A", "B", [1])


def test_cross_type_methods_reject_same_type_and_bad_controls():
    from point_patterns import cross_nearest_neighbor_cdf, cross_j_function
    pts = [(2, 2), (7, 7), (3, 2), (7, 8)]
    marks = ["A", "A", "B", "B"]
    with pytest.raises(ValueError):
        cross_nearest_neighbor_cdf(pts, marks, "A", "A", [1])
    with pytest.raises(ValueError):
        cross_j_function(pts, marks, (0, 0, 10, 10), "A", "B", [1], n_samples=0)


def test_homogeneous_poisson_simulator_is_seeded_and_inside_window():
    from point_patterns import simulate_homogeneous_poisson
    a = simulate_homogeneous_poisson((0, 0, 10, 5), 0.4, seed=31)
    b = simulate_homogeneous_poisson((0, 0, 10, 5), 0.4, seed=31)
    assert a == b
    assert all(0 <= x <= 10 and 0 <= y <= 5 for x, y in a)


def test_homogeneous_poisson_zero_intensity_returns_empty_pattern():
    from point_patterns import simulate_homogeneous_poisson
    assert simulate_homogeneous_poisson((0, 0, 1, 1), 0, seed=1) == []


def test_thomas_simulator_is_seeded_and_clips_to_target_window():
    from point_patterns import simulate_thomas_process
    a = simulate_thomas_process((0, 0, 10, 10), 0.08, 8, 0.5, seed=17)
    b = simulate_thomas_process((0, 0, 10, 10), 0.08, 8, 0.5, seed=17)
    assert a == b
    assert all(0 <= x <= 10 and 0 <= y <= 10 for x, y in a)


def test_thomas_simulator_zero_parent_intensity_returns_empty_pattern():
    from point_patterns import simulate_thomas_process
    assert simulate_thomas_process((0, 0, 1, 1), 0, 5, 0.2, seed=3) == []


@pytest.mark.parametrize("args", [
    ((0, 0, 1, 1), -1), ((0, 0, 1, 1), float("nan")),
])
def test_homogeneous_poisson_rejects_invalid_intensity(args):
    from point_patterns import simulate_homogeneous_poisson
    with pytest.raises(ValueError):
        simulate_homogeneous_poisson(args[0], args[1], seed=1)


@pytest.mark.parametrize("params", [
    ( -1, 2, 1), (1, -2, 1), (1, 2, 0), (1, 2, 1, 0)
])
def test_thomas_rejects_invalid_parameters(params):
    from point_patterns import simulate_thomas_process
    with pytest.raises(ValueError):
        if len(params) == 3:
            simulate_thomas_process((0, 0, 1, 1), *params, seed=1)
        else:
            simulate_thomas_process((0, 0, 1, 1), *params[:3], seed=1, buffer_sigma=params[3])


def test_matern_cluster_simulator_is_seeded_and_inside_window():
    from point_patterns import simulate_matern_cluster_process
    a = simulate_matern_cluster_process((0, 0, 10, 10), 0.08, 8, 0.7, seed=41)
    b = simulate_matern_cluster_process((0, 0, 10, 10), 0.08, 8, 0.7, seed=41)
    assert a == b
    assert all(0 <= x <= 10 and 0 <= y <= 10 for x, y in a)


def test_matern_cluster_zero_parameters_return_empty_pattern():
    from point_patterns import simulate_matern_cluster_process
    assert simulate_matern_cluster_process((0, 0, 1, 1), 0, 5, 0.2, seed=2) == []
    assert simulate_matern_cluster_process((0, 0, 1, 1), 2, 0, 0.2, seed=2) == []


@pytest.mark.parametrize("params", [
    (-1, 2, 1), (1, -2, 1), (1, 2, 0), (float("nan"), 2, 1),
])
def test_matern_cluster_rejects_invalid_parameters(params):
    from point_patterns import simulate_matern_cluster_process
    with pytest.raises(ValueError):
        simulate_matern_cluster_process((0, 0, 1, 1), *params, seed=1)


def test_matern_cluster_rejects_non_integer_seed():
    from point_patterns import simulate_matern_cluster_process
    with pytest.raises(ValueError, match="seed"):
        simulate_matern_cluster_process((0, 0, 1, 1), 1, 2, 0.2, seed=True)


def test_log_gaussian_cox_simulator_is_seeded_and_inside_window():
    from point_patterns import simulate_log_gaussian_cox_process
    a = simulate_log_gaussian_cox_process((0, 0, 10, 10), 0.5, 0.7, 2.0,
                                          nx=4, ny=3, seed=29)
    b = simulate_log_gaussian_cox_process((0, 0, 10, 10), 0.5, 0.7, 2.0,
                                          nx=4, ny=3, seed=29)
    assert a == b
    assert all(0 <= x <= 10 and 0 <= y <= 10 for x, y in a)


def test_log_gaussian_cox_zero_intensity_returns_empty_pattern():
    from point_patterns import simulate_log_gaussian_cox_process
    assert simulate_log_gaussian_cox_process((0, 0, 1, 1), 0, 1, 1) == []


@pytest.mark.parametrize("params", [
    (-1, 1, 1), (1, -1, 1), (1, 1, 0), (float("nan"), 1, 1),
])
def test_log_gaussian_cox_rejects_invalid_model_parameters(params):
    from point_patterns import simulate_log_gaussian_cox_process
    with pytest.raises(ValueError):
        simulate_log_gaussian_cox_process((0, 0, 1, 1), *params, nx=2, ny=2)


def test_log_gaussian_cox_rejects_oversized_or_invalid_grid():
    from point_patterns import simulate_log_gaussian_cox_process
    with pytest.raises(ValueError, match="225"):
        simulate_log_gaussian_cox_process((0, 0, 1, 1), 1, 0.2, 1, nx=16, ny=16)
    with pytest.raises(ValueError, match="positive integers"):
        simulate_log_gaussian_cox_process((0, 0, 1, 1), 1, 0.2, 1, nx=0, ny=2)


def test_small_cholesky_factor_reconstructs_covariance():
    from point_patterns import _cholesky_lower
    lower = _cholesky_lower([[4.0, 2.0], [2.0, 3.0]])
    assert lower[0] == pytest.approx([2.0, 0.0])
    assert lower[1] == pytest.approx([1.0, 2 ** 0.5])


def test_strauss_simulator_is_seeded_and_inside_window():
    from point_patterns import simulate_strauss_process
    a = simulate_strauss_process((0, 0, 10, 10), 0.08, 0.35, 0.7,
                                 burn_in=300, n_steps=500, seed=31)
    b = simulate_strauss_process((0, 0, 10, 10), 0.08, 0.35, 0.7,
                                 burn_in=300, n_steps=500, seed=31)
    assert a == b
    assert all(0 <= x <= 10 and 0 <= y <= 10 for x, y in a)


def test_strauss_hard_core_sampler_never_returns_close_pairs():
    from point_patterns import simulate_strauss_process
    points = simulate_strauss_process((0, 0, 5, 5), 0.5, 0, 0.5,
                                      burn_in=1000, n_steps=2000, seed=8)
    for i, (x, y) in enumerate(points):
        for other_x, other_y in points[i+1:]:
            assert math.hypot(x-other_x, y-other_y) >= 0.5


def test_strauss_gamma_one_chain_is_seeded_and_valid():
    from point_patterns import simulate_strauss_process
    a = simulate_strauss_process((0, 0, 2, 2), 0.7, 1, 0.4,
                                 burn_in=300, n_steps=500, seed=9)
    b = simulate_strauss_process((0, 0, 2, 2), 0.7, 1, 0.4,
                                 burn_in=300, n_steps=500, seed=9)
    assert a == b
    assert all(0 <= x <= 2 and 0 <= y <= 2 for x, y in a)


def test_strauss_zero_activity_returns_empty_pattern():
    from point_patterns import simulate_strauss_process
    assert simulate_strauss_process((0, 0, 1, 1), 0, 0.5, 0.2, seed=3) == []


@pytest.mark.parametrize("params", [
    (-1, 0.5, 1), (1, -0.1, 1), (1, 1.1, 1), (1, 0.5, 0),
    (float("nan"), 0.5, 1),
])
def test_strauss_rejects_invalid_parameters(params):
    from point_patterns import simulate_strauss_process
    with pytest.raises(ValueError):
        simulate_strauss_process((0, 0, 1, 1), *params, burn_in=2, n_steps=2)


def test_strauss_rejects_invalid_iteration_counts_and_seed():
    from point_patterns import simulate_strauss_process
    with pytest.raises(ValueError, match="n_steps"):
        simulate_strauss_process((0, 0, 1, 1), 1, 0.5, 0.2, n_steps=0)
    with pytest.raises(ValueError, match="non-negative integers"):
        simulate_strauss_process((0, 0, 1, 1), 1, 0.5, 0.2, burn_in=-1)
    with pytest.raises(ValueError, match="seed"):
        simulate_strauss_process((0, 0, 1, 1), 1, 0.5, 0.2, seed=True)



def test_inhomogeneous_poisson_simulator_is_seeded_and_respects_zero_cells():
    from point_patterns import simulate_inhomogeneous_poisson
    grid=[[0.0, 80.0],[0.0, 0.0]]
    a=simulate_inhomogeneous_poisson(grid,(0,0,2,2),seed=71)
    b=simulate_inhomogeneous_poisson(grid,(0,0,2,2),seed=71)
    assert a == b
    assert len(a) > 0
    assert all(1.0 <= x <= 2.0 and 1.0 <= y <= 2.0 for x,y in a)


def test_inhomogeneous_poisson_zero_intensity_returns_no_events():
    from point_patterns import simulate_inhomogeneous_poisson
    assert simulate_inhomogeneous_poisson([[0,0],[0,0]],(0,0,1,1),seed=4) == []


def test_inhomogeneous_poisson_expected_count_matches_integrated_intensity():
    from point_patterns import simulate_inhomogeneous_poisson
    grid=[[0.2,1.4],[0.0,0.7]]
    counts=[len(simulate_inhomogeneous_poisson(grid,(0,0,2,2),seed=i))
            for i in range(1200)]
    expected=2.3
    assert np.mean(counts) == pytest.approx(expected, abs=0.12)


@pytest.mark.parametrize("grid", [[], [[-1]], [[float("nan")]], [[float("inf")]]])
def test_inhomogeneous_poisson_rejects_invalid_intensity_grid(grid):
    from point_patterns import simulate_inhomogeneous_poisson
    with pytest.raises(ValueError):
        simulate_inhomogeneous_poisson(grid,(0,0,1,1),seed=1)


def test_inhomogeneous_poisson_rejects_invalid_window_and_seed():
    from point_patterns import simulate_inhomogeneous_poisson
    with pytest.raises(ValueError,match="window"):
        simulate_inhomogeneous_poisson([[1]],(0,0,0,1),seed=1)
    with pytest.raises(ValueError,match="seed"):
        simulate_inhomogeneous_poisson([[1]],(0,0,1,1),seed=True)
