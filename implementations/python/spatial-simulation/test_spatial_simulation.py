import numpy as np
import pytest

from spatial_simulation import (
    life_like_step,
    live_neighbor_count,
    same_group_share,
    schelling_step,
    simulate_life_like,
    simulate_schelling,
)


def test_live_neighbor_count_excludes_center_and_respects_fixed_edges():
    grid = np.zeros((3, 3), dtype=np.uint8)
    grid[0, 0] = grid[0, 1] = grid[1, 0] = 1
    counts = live_neighbor_count(grid)
    assert counts[0, 0] == 2
    assert counts[1, 1] == 3
    assert counts[2, 2] == 0


def test_periodic_neighborhood_wraps_edges():
    grid = np.zeros((3, 3), dtype=np.uint8)
    grid[0, 0] = 1
    counts = live_neighbor_count(grid, periodic=True)
    assert counts[2, 2] == 1


def test_von_neumann_neighborhood_has_four_neighbors():
    grid = np.ones((3, 3), dtype=np.uint8)
    counts = live_neighbor_count(grid, neighborhood="von_neumann")
    assert counts[1, 1] == 4
    assert counts[0, 0] == 2


def test_blinker_oscillates_under_conways_rule():
    grid = np.zeros((5, 5), dtype=np.uint8)
    grid[2, 1:4] = 1
    first = life_like_step(grid)
    expected = np.zeros_like(grid)
    expected[1:4, 2] = 1
    assert np.array_equal(first, expected)
    assert np.array_equal(life_like_step(first), grid)


def test_zero_steps_returns_copy():
    grid = np.array([[0, 1], [1, 0]], dtype=np.uint8)
    result = simulate_life_like(grid, 0)
    assert np.array_equal(result, grid)
    assert result is not grid


def test_invalid_automaton_inputs():
    with pytest.raises(ValueError):
        life_like_step(np.array([[0, 2]]))
    with pytest.raises(ValueError):
        simulate_life_like(np.zeros((2, 2), dtype=int), -1)
    with pytest.raises(ValueError):
        live_neighbor_count(np.zeros((2, 2), dtype=int), neighborhood="hex")


def test_schelling_share_uses_only_occupied_neighbors():
    grid = np.array([[1, 0, 2], [1, 1, 0], [0, 0, 2]])
    assert same_group_share(grid, 0, 0) == 1.0
    assert same_group_share(grid, 0, 2) == 0.0


def test_schelling_moves_preserve_group_counts_and_empty_count():
    grid = np.array([
        [1, 2, 0, 0],
        [2, 1, 0, 0],
        [1, 2, 0, 0],
    ])
    moved, n = schelling_step(grid, tolerance=0.6, seed=12)
    assert n > 0
    assert np.array_equal(np.unique(grid, return_counts=True)[1],
                          np.unique(moved, return_counts=True)[1])
    assert np.count_nonzero(moved == 0) == np.count_nonzero(grid == 0)


def test_schelling_seed_is_reproducible():
    grid = np.array([[1, 2, 0], [2, 1, 0], [1, 2, 0]])
    a, moves_a = schelling_step(grid, tolerance=0.7, seed=4)
    b, moves_b = schelling_step(grid, tolerance=0.7, seed=4)
    assert moves_a == moves_b
    assert np.array_equal(a, b)


def test_schelling_simulation_stops_when_stable_or_at_limit():
    stable = np.ones((2, 2), dtype=int)
    result = simulate_schelling(stable, tolerance=0.5, seed=1)
    assert result.converged
    assert result.moves_per_step == (0,)
    limited = simulate_schelling(np.array([[1, 2, 0], [2, 1, 0]]),
                                 tolerance=1.0, max_iterations=1, seed=1)
    assert len(limited.moves_per_step) <= 1


def test_invalid_schelling_controls():
    grid = np.array([[1, 0], [2, 0]])
    with pytest.raises(ValueError):
        schelling_step(grid, tolerance=1.1)
    with pytest.raises(ValueError):
        simulate_schelling(grid, max_iterations=-1)
    with pytest.raises(ValueError):
        schelling_step(np.array([[1, -1], [0, 2]]))


from spatial_simulation import forest_fire_step, percolates, sample_site_percolation


def test_site_percolation_probability_endpoints_and_seed():
    assert sample_site_percolation((4, 5), 0.0, seed=1).sum() == 0
    assert sample_site_percolation((4, 5), 1.0, seed=1).all()
    a = sample_site_percolation((20, 20), 0.45, seed=7)
    b = sample_site_percolation((20, 20), 0.45, seed=7)
    assert np.array_equal(a, b)


def test_percolation_requires_top_to_bottom_occupied_path():
    connected = np.array([
        [1, 0, 0],
        [1, 1, 0],
        [0, 1, 0],
    ], dtype=bool)
    disconnected = np.array([
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
    ], dtype=bool)
    assert percolates(connected)
    assert not percolates(disconnected)
    assert percolates(disconnected, neighborhood="moore")


def test_percolation_validates_grid_and_neighborhood():
    with pytest.raises(ValueError):
        percolates(np.array([[0, 2]]))
    with pytest.raises(ValueError):
        percolates(np.ones((2, 2)), neighborhood="hexagonal")
    with pytest.raises(ValueError):
        sample_site_percolation((0, 2), 0.5)


def test_forest_fire_burning_tree_empty_transition_rules():
    grid = np.array([
        [0, 1, 0],
        [0, 2, 0],
        [0, 0, 0],
    ], dtype=np.uint8)
    result = forest_fire_step(
        grid, growth_probability=0.0, lightning_probability=0.0,
        neighborhood="von_neumann", seed=2,
    )
    assert result[1, 1] == 0
    assert result[0, 1] == 2
    assert result[2, 1] == 2
    assert result[0, 0] == 0


def test_forest_fire_lightning_and_growth_probability_endpoints():
    trees = np.ones((3, 3), dtype=np.uint8)
    lightning = forest_fire_step(
        trees, growth_probability=0.0, lightning_probability=1.0, seed=3
    )
    assert np.all(lightning == 2)
    empty = np.zeros((3, 3), dtype=np.uint8)
    growth = forest_fire_step(
        empty, growth_probability=1.0, lightning_probability=0.0, seed=3
    )
    assert np.all(growth == 1)


def test_forest_fire_is_seeded_and_validates_parameters():
    grid = np.array([[0, 1, 2], [1, 0, 1]], dtype=np.uint8)
    a = forest_fire_step(
        grid, growth_probability=0.2, lightning_probability=0.1, seed=42
    )
    b = forest_fire_step(
        grid, growth_probability=0.2, lightning_probability=0.1, seed=42
    )
    assert np.array_equal(a, b)
    with pytest.raises(ValueError):
        forest_fire_step(grid, growth_probability=1.1, lightning_probability=0.1)
    with pytest.raises(ValueError):
        forest_fire_step(np.array([[3]]), growth_probability=0.1,
                         lightning_probability=0.1)
