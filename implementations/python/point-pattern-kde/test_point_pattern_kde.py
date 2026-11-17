import numpy as np
import pytest

from point_pattern_kde import gaussian_kde, silverman_bandwidth


def test_single_point_density_matches_gaussian_kernel_at_grid_centre():
    density, xs, ys = gaussian_kde(
        [(0.5, 0.5)],
        bounds=(0, 1, 0, 1),
        grid_shape=(1, 1),
        bandwidth=1.0,
    )
    assert xs.tolist() == [0.5]
    assert ys.tolist() == [0.5]
    assert density[0, 0] == pytest.approx(1 / (2 * np.pi))


def test_single_point_surface_is_symmetric_around_event():
    density, _, _ = gaussian_kde(
        [(1, 1)],
        bounds=(0, 2, 0, 2),
        grid_shape=(2, 2),
        bandwidth=0.5,
    )
    assert density[0, 0] == pytest.approx(density[0, 1])
    assert density[0, 0] == pytest.approx(density[1, 0])
    assert density[0, 0] == pytest.approx(density[1, 1])


def test_weights_scale_the_intensity_linearly():
    base, _, _ = gaussian_kde(
        [(0.5, 0.5)], bounds=(0, 1, 0, 1), grid_shape=(1, 1), bandwidth=1
    )
    weighted, _, _ = gaussian_kde(
        [(0.5, 0.5)], bounds=(0, 1, 0, 1), grid_shape=(1, 1), bandwidth=1,
        weights=[3],
    )
    assert weighted[0, 0] == pytest.approx(3 * base[0, 0])


def test_chunk_size_does_not_change_results():
    points = [(1, 1), (2, 2), (3, 1)]
    a, _, _ = gaussian_kde(points, bounds=(0, 4, 0, 4), grid_shape=(8, 8), bandwidth=0.8, chunk_size=3)
    b, _, _ = gaussian_kde(points, bounds=(0, 4, 0, 4), grid_shape=(8, 8), bandwidth=0.8, chunk_size=1000)
    np.testing.assert_allclose(a, b)


def test_bounds_must_contain_events():
    with pytest.raises(ValueError, match="inside bounds"):
        gaussian_kde([(2, 2)], bounds=(0, 1, 0, 1), bandwidth=1)


@pytest.mark.parametrize("bandwidth", [0, -1, float("inf"), float("nan"), "wide"])
def test_invalid_bandwidth_is_rejected(bandwidth):
    with pytest.raises(ValueError, match="bandwidth"):
        gaussian_kde([(0.5, 0.5)], bounds=(0, 1, 0, 1), bandwidth=bandwidth)


def test_invalid_event_shape_and_nonfinite_coordinates_are_rejected():
    with pytest.raises(ValueError, match="shape"):
        gaussian_kde([1, 2], bounds=(0, 1, 0, 1), bandwidth=1)
    with pytest.raises(ValueError, match="finite"):
        gaussian_kde([(float("nan"), 0.5)], bounds=(0, 1, 0, 1), bandwidth=1)


def test_invalid_weights_and_grid_shape_are_rejected():
    with pytest.raises(ValueError, match="weights"):
        gaussian_kde([(0.5, 0.5)], bounds=(0, 1, 0, 1), bandwidth=1, weights=[1, 2])
    with pytest.raises(ValueError, match="weights"):
        gaussian_kde([(0.5, 0.5)], bounds=(0, 1, 0, 1), bandwidth=1, weights=[-1])
    with pytest.raises(ValueError, match="grid_shape"):
        gaussian_kde([(0.5, 0.5)], bounds=(0, 1, 0, 1), bandwidth=1, grid_shape=(0, 1))


def test_adaptive_kde_alpha_zero_matches_fixed_estimator():
    from point_pattern_kde import adaptive_gaussian_kde
    points = [(1, 1), (2, 2), (3, 1)]
    fixed, xs, ys = gaussian_kde(points, bounds=(0, 4, 0, 4), grid_shape=(7, 9), bandwidth=0.7)
    adaptive, ax, ay, local = adaptive_gaussian_kde(
        points, bounds=(0, 4, 0, 4), grid_shape=(7, 9), bandwidth=0.7, alpha=0
    )
    np.testing.assert_allclose(adaptive, fixed)
    np.testing.assert_array_equal(ax, xs)
    np.testing.assert_array_equal(ay, ys)
    np.testing.assert_allclose(local, 0.7)


def test_adaptive_kde_matches_independent_variable_bandwidth_oracle():
    from point_pattern_kde import adaptive_gaussian_kde
    points = np.array([(0.5, 0.5), (1.5, 1.5), (3.0, 1.0), (3.2, 1.1)])
    density, xs, ys, local = adaptive_gaussian_kde(
        points, bounds=(0, 4, 0, 2), grid_shape=(4, 8), bandwidth=0.8,
        bandwidth_factor_bounds=(0.3, 3.0), chunk_size=5
    )
    assert np.all(local >= 0.8 * 0.3) and np.all(local <= 0.8 * 3.0)
    for row, y in enumerate(ys):
        for col, x in enumerate(xs):
            expected = sum(np.exp(-((x-px)**2+(y-py)**2)/(2*h*h))/(2*np.pi*h*h)
                           for (px, py), h in zip(points, local))
            assert density[row, col] == pytest.approx(expected)


def test_adaptive_kde_single_event_and_weight_scaling():
    from point_pattern_kde import adaptive_gaussian_kde
    args = dict(bounds=(0, 2, 0, 2), grid_shape=(3, 3), bandwidth=0.6)
    base, _, _, local = adaptive_gaussian_kde([(1, 1)], **args)
    weighted, _, _, weighted_local = adaptive_gaussian_kde([(1, 1)], weights=[4], **args)
    np.testing.assert_allclose(weighted, 4 * base)
    np.testing.assert_allclose(local, weighted_local)


def test_loo_bandwidth_selection_matches_independent_score():
    from point_pattern_kde import select_bandwidth_loo
    points = np.array([(0, 0), (0.2, 0.1), (1.5, 1.2), (1.7, 1.1)])
    candidates = [0.15, 0.4, 0.9]
    best, scores = select_bandwidth_loo(points, candidates)
    expected = []
    for h in candidates:
        values = []
        for i, point in enumerate(points):
            density = sum(np.exp(-np.sum((point-other)**2)/(2*h*h))/(2*np.pi*h*h)
                          for j, other in enumerate(points) if i != j) / (len(points)-1)
            values.append(np.log(density))
        expected.append((h, sum(values)/len(values)))
    assert [h for h, _ in scores] == candidates
    assert [s for _, s in scores] == pytest.approx([s for _, s in expected])
    assert best == max(expected, key=lambda item: item[1])[0]


def test_loo_weighted_selection_and_invalid_inputs():
    from point_pattern_kde import select_bandwidth_loo, adaptive_gaussian_kde
    best, scores = select_bandwidth_loo([(0, 0), (1, 0), (2, 0)], [0.2, 1.0], weights=[1, 2, 1])
    assert best in (0.2, 1.0) and len(scores) == 2
    with pytest.raises(ValueError):
        select_bandwidth_loo([(0, 0)], [1])
    with pytest.raises(ValueError):
        select_bandwidth_loo([(0, 0), (1, 1)], [0])
    with pytest.raises(ValueError):
        adaptive_gaussian_kde([(0.5, 0.5)], bounds=(0, 1, 0, 1), bandwidth=1, alpha=2)


def test_adaptive_pilot_bandwidths_match_independent_abramsom_rule():
    from point_pattern_kde import adaptive_gaussian_kde
    points = np.array([(0, 0), (0.1, 0), (0.2, 0), (3, 0), (3.2, 0)], dtype=float)
    h, alpha = 0.7, 0.5
    _, _, _, actual = adaptive_gaussian_kde(
        points, bounds=(-1, 4, -1, 1), grid_shape=(2, 5), bandwidth=h,
        alpha=alpha, bandwidth_factor_bounds=(0.1, 10.0)
    )
    delta = points[:, None, :] - points[None, :, :]
    squared = np.sum(delta * delta, axis=2)
    np.fill_diagonal(squared, np.inf)
    pilot = np.exp(-squared / (2*h*h)).sum(axis=1) / (2*np.pi*h*h*(len(points)-1))
    geometric = np.exp(np.mean(np.log(pilot)))
    expected = h * (geometric / pilot) ** alpha
    np.testing.assert_allclose(actual, expected)


def test_zero_weight_events_do_not_change_adaptive_pilot_for_active_events():
    from point_pattern_kde import adaptive_gaussian_kde
    base_points = [(0, 0), (0.2, 0), (2, 0)]
    base = adaptive_gaussian_kde(
        base_points, bounds=(-1, 3, -1, 1), grid_shape=(3, 5), bandwidth=0.6
    )
    extended = adaptive_gaussian_kde(
        base_points + [(2.8, 0)], bounds=(-1, 3, -1, 1), grid_shape=(3, 5),
        bandwidth=0.6, weights=[1, 1, 1, 0]
    )
    np.testing.assert_allclose(base[0], extended[0])
    np.testing.assert_allclose(base[3], extended[3][:3])


def test_silverman_bandwidth_matches_bivariate_normal_reference_formula():
    points = np.array([(-1, -1), (-1, 1), (1, -1), (1, 1)], dtype=float)
    expected = np.sqrt(4 / 3) * 4 ** (-1 / 6)
    assert silverman_bandwidth(points) == pytest.approx(expected)


def test_silverman_bandwidth_is_translation_and_scale_equivariant():
    points = np.array([(0, 0), (1, 0), (0, 1), (1, 1)], dtype=float)
    base = silverman_bandwidth(points)
    transformed = 7 + 3 * points + np.array([0, -9])
    assert silverman_bandwidth(transformed) == pytest.approx(3 * base)


def test_silverman_bandwidth_equal_weights_match_unweighted():
    points = np.array([(0, 0), (1, 0), (0, 2), (2, 1)], dtype=float)
    assert silverman_bandwidth(points, weights=[1, 1, 1, 1]) == pytest.approx(
        silverman_bandwidth(points)
    )


def test_silverman_bandwidth_uses_kish_effective_sample_size():
    points = np.array([(0, 0), (1, 0), (0, 1), (1, 1)], dtype=float)
    weights = np.array([1, 2, 2, 1], dtype=float)
    mean = np.average(points, axis=0, weights=weights)
    denominator = weights.sum() - np.dot(weights, weights) / weights.sum()
    variance = np.sum(weights[:, None] * (points - mean) ** 2, axis=0) / denominator
    effective_n = weights.sum() ** 2 / np.dot(weights, weights)
    expected = np.sqrt(np.mean(variance)) * effective_n ** (-1 / 6)
    assert silverman_bandwidth(points, weights=weights) == pytest.approx(expected)


@pytest.mark.parametrize("points", [
    [(0, 0)],
    [(1, 1), (1, 1), (1, 1)],
    [(0, 0), (float("nan"), 1)],
    [1, 2],
])
def test_silverman_bandwidth_rejects_invalid_or_degenerate_points(points):
    with pytest.raises(ValueError):
        silverman_bandwidth(points)


@pytest.mark.parametrize("weights", [
    [1],
    [-1, 1],
    [0, 0],
    [1, 0],
    [1, float("nan")],
])
def test_silverman_bandwidth_rejects_invalid_weights(weights):
    with pytest.raises(ValueError):
        silverman_bandwidth([(0, 0), (1, 0)], weights=weights)
