import numpy as np
import pytest

from raster_distance import distance_to_targets, distance_transform_1d


def test_distance_is_zero_at_targets_and_increases_by_cell_spacing():
    targets = np.zeros((5, 5), dtype=bool)
    targets[2, 2] = True
    result = distance_to_targets(targets, cell_size=(10, 20))
    assert result[2, 2] == 0
    assert result[2, 3] == pytest.approx(20)
    assert result[3, 2] == pytest.approx(10)
    assert result[3, 3] == pytest.approx(np.hypot(10, 20))


def test_multiple_targets_use_nearest_euclidean_distance():
    targets = np.zeros((4, 5), dtype=bool)
    targets[0, 0] = True
    targets[3, 4] = True
    result = distance_to_targets(targets)
    assert result[0, 4] == pytest.approx(3)
    assert result[3, 0] == pytest.approx(3)


def test_rectangular_cells_use_anisotropic_sampling():
    targets = np.zeros((3, 3), dtype=bool)
    targets[0, 0] = True
    result = distance_to_targets(targets, cell_size=(2, 5))
    assert result[1, 0] == pytest.approx(2)
    assert result[0, 1] == pytest.approx(5)
    assert result[1, 1] == pytest.approx(np.hypot(2, 5))


@pytest.mark.parametrize("mask", [np.array([]), np.ones((2, 2, 2)), np.zeros((2, 2), dtype=bool)])
def test_invalid_or_target_free_masks_rejected(mask):
    with pytest.raises(ValueError):
        distance_to_targets(mask)


@pytest.mark.parametrize("spacing", [(0, 1), (1, -1), (float("inf"), 1), (1,), (float("nan"), 1)])
def test_invalid_cell_spacing_rejected(spacing):
    targets = np.zeros((2, 2), dtype=bool)
    targets[0, 0] = True
    with pytest.raises(ValueError):
        distance_to_targets(targets, cell_size=spacing)


def test_one_dimensional_lower_envelope_matches_brute_force():
    rng = np.random.default_rng(42)
    for n in (1, 2, 7, 31):
        for spacing in (0.5, 1.0, 3.5):
            values = rng.uniform(0, 20, size=n)
            values[rng.random(n) < 0.3] = np.inf
            if np.all(np.isinf(values)):
                values[0] = 2.0
            expected = np.array([
                min(values[i] + (spacing * (q - i)) ** 2 for i in range(n))
                for q in range(n)
            ])
            np.testing.assert_allclose(distance_transform_1d(values, spacing), expected)


def test_two_dimensional_transform_matches_brute_force_random_masks():
    rng = np.random.default_rng(123)
    for shape in ((1, 9), (8, 1), (5, 7), (11, 13)):
        for spacing in ((1.0, 1.0), (2.5, 0.75)):
            targets = rng.random(shape) < 0.18
            if not targets.any():
                targets[0, 0] = True
            result = distance_to_targets(targets, cell_size=spacing)
            locations = np.argwhere(targets)
            expected = np.empty(shape)
            for row in range(shape[0]):
                for col in range(shape[1]):
                    expected[row, col] = min(
                        np.hypot((row-r)*spacing[0], (col-c)*spacing[1])
                        for r, c in locations
                    )
            np.testing.assert_allclose(result, expected, rtol=1e-12, atol=1e-12)


def test_rows_without_targets_are_handled_by_infinite_intermediate_costs():
    targets = np.zeros((6, 5), dtype=bool)
    targets[3, 2] = True
    result = distance_to_targets(targets, cell_size=(2, 4))
    assert np.isfinite(result).all()
    assert result[0, 2] == pytest.approx(6.0)


def test_one_dimensional_transform_rejects_invalid_values_and_spacing():
    with pytest.raises(ValueError):
        distance_transform_1d(np.array([0.0, np.nan, 1.0]))
    with pytest.raises(ValueError):
        distance_transform_1d(np.array([0.0, -np.inf, 1.0]))
    with pytest.raises(ValueError):
        distance_transform_1d(np.array([0.0, 1.0]), 0.0)
    assert np.isinf(distance_transform_1d(np.array([np.inf, np.inf]))).all()


def test_scalar_cell_size_is_reported_as_invalid():
    targets = np.zeros((2, 2), dtype=bool)
    targets[0, 0] = True
    with pytest.raises(ValueError):
        distance_to_targets(targets, cell_size=5.0)


def test_chamfer_distance_uses_eight_neighbour_graph_metric():
    from raster_distance import chamfer_distance_to_targets
    targets = np.zeros((5, 5), dtype=bool)
    targets[0, 0] = True
    result = chamfer_distance_to_targets(targets)
    assert result[0, 1] == pytest.approx(1.0)
    assert result[1, 0] == pytest.approx(1.0)
    assert result[1, 1] == pytest.approx(np.sqrt(2.0))
    assert result[2, 1] == pytest.approx(1.0 + np.sqrt(2.0))


def test_chamfer_distance_matches_brute_force_octile_metric():
    from raster_distance import chamfer_distance_to_targets
    rng = np.random.default_rng(321)
    for shape in ((1, 7), (6, 1), (5, 8), (9, 11)):
        for spacing in ((1.0, 1.0), (2.0, 0.5)):
            targets = rng.random(shape) < .2
            if not targets.any():
                targets[0, 0] = True
            actual = chamfer_distance_to_targets(targets, cell_size=spacing)
            locations = np.argwhere(targets)
            expected = np.empty(shape)
            diagonal = np.hypot(*spacing)
            for row in range(shape[0]):
                for col in range(shape[1]):
                    costs = []
                    for target_row, target_col in locations:
                        dr, dc = abs(row-target_row), abs(col-target_col)
                        diagonal_steps = min(dr, dc)
                        costs.append(
                            diagonal_steps * diagonal
                            + (dr-diagonal_steps) * spacing[0]
                            + (dc-diagonal_steps) * spacing[1]
                        )
                    expected[row, col] = min(costs)
            np.testing.assert_allclose(actual, expected, rtol=1e-12, atol=1e-12)


def test_chamfer_distance_rejects_empty_target_mask_and_invalid_spacing():
    from raster_distance import chamfer_distance_to_targets
    with pytest.raises(ValueError):
        chamfer_distance_to_targets(np.zeros((3, 3), dtype=bool))
    with pytest.raises(ValueError):
        chamfer_distance_to_targets(np.eye(3, dtype=bool), cell_size=(1, 0))
