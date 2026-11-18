import numpy as np
import pytest

from p_dispersion import solve_p_dispersion


def test_exact_max_min_selection_on_line():
    coordinates = np.array([0.0, 1.0, 4.0, 8.0, 10.0])
    distances = np.abs(coordinates[:, None] - coordinates[None, :])
    sites, separation = solve_p_dispersion(distances, p=3)
    assert sites == (0, 2, 3)
    assert separation == pytest.approx(4.0)


def test_square_tie_is_lexicographically_deterministic():
    points = np.array([[0, 0], [1, 0], [1, 1], [0, 1]], dtype=float)
    distances = np.linalg.norm(points[:, None, :] - points[None, :, :], axis=2)
    sites, separation = solve_p_dispersion(distances, p=2)
    assert sites == (0, 2)
    assert separation == pytest.approx(np.sqrt(2))


def test_p_equals_all_candidates_returns_global_minimum_pair_distance():
    distances = np.array([[0, 2, 5], [2, 0, 3], [5, 3, 0]], dtype=float)
    assert solve_p_dispersion(distances, p=3) == ((0, 1, 2), 2.0)


@pytest.mark.parametrize("matrix,p", [
    (np.ones((3, 2)), 2),
    (np.zeros((0, 0)), 2),
    (np.eye(3), 1),
    (np.eye(3), 4),
    (np.array([[0, 1], [2, 0]]), 2),
    (np.array([[1, 1], [1, 0]]), 2),
    (np.array([[0, np.nan], [np.nan, 0]]), 2),
    (np.array([[0, -1], [-1, 0]]), 2),
])
def test_invalid_distance_matrices_and_p_are_rejected(matrix, p):
    with pytest.raises(ValueError):
        solve_p_dispersion(matrix, p)


def test_duplicate_candidates_can_have_zero_optimal_separation():
    distances = np.array([[0, 0, 4], [0, 0, 4], [4, 4, 0]], dtype=float)
    sites, separation = solve_p_dispersion(distances, p=2)
    assert sites == (0, 2)
    assert separation == pytest.approx(4.0)
