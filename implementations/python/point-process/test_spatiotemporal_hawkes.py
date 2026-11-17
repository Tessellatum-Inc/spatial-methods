import numpy as np
import pytest
from spatiotemporal_hawkes import simulate_spatiotemporal_hawkes


def test_hawkes_simulation_is_reproducible_and_sorted():
    kwargs = dict(background_rate=2.0, branching_ratio=0.65,
                  temporal_decay=1.4, spatial_scale=0.08,
                  window=(0, 0, 1, 1), horizon=8, seed=42)
    first = simulate_spatiotemporal_hawkes(**kwargs)
    second = simulate_spatiotemporal_hawkes(**kwargs)
    np.testing.assert_array_equal(first["times"], second["times"])
    np.testing.assert_array_equal(first["locations"], second["locations"])
    np.testing.assert_array_equal(first["parent_indices"], second["parent_indices"])
    assert np.all(np.diff(first["times"]) >= 0)


def test_hawkes_parent_links_are_earlier_and_generation_consistent():
    result = simulate_spatiotemporal_hawkes(3.0, 0.8, 1.0, 0.1, (0, 0, 1, 1), 12, seed=7)
    for i, parent in enumerate(result["parent_indices"]):
        if parent >= 0:
            assert parent < i
            assert result["times"][parent] < result["times"][i]
            assert result["generations"][i] == result["generations"][parent] + 1
        else:
            assert result["generations"][i] == 0
    assert result["n_events"] >= result["n_immigrants"]


def test_hawkes_zero_branching_ratio_is_poisson_immigrants_only():
    result = simulate_spatiotemporal_hawkes(4.0, 0.0, 1.0, 0.1, (-2, -1, 2, 3), 5, seed=19)
    assert result["n_events"] == result["n_immigrants"]
    assert np.all(result["parent_indices"] == -1)
    assert np.all(result["generations"] == 0)


def test_hawkes_periodic_locations_remain_inside_window():
    result = simulate_spatiotemporal_hawkes(5.0, 0.9, 0.8, 2.0, (10, -4, 11, -3), 10, seed=9)
    xy = result["locations"]
    assert np.all((xy[:, 0] >= 10) & (xy[:, 0] < 11))
    assert np.all((xy[:, 1] >= -4) & (xy[:, 1] < -3))
    assert result["boundary"] == "periodic"


@pytest.mark.parametrize("args", [
    (-1, 0.2, 1, 1, (0, 0, 1, 1), 1),
    (1, 1, 1, 1, (0, 0, 1, 1), 1),
    (1, 0.2, 0, 1, (0, 0, 1, 1), 1),
    (1, 0.2, 1, 0, (0, 0, 1, 1), 1),
    (1, 0.2, 1, 1, (0, 0, 0, 1), 1),
    (1, 0.2, 1, 1, (0, 0, 1, 1), 0),
])
def test_hawkes_rejects_invalid_parameters(args):
    with pytest.raises(ValueError):
        simulate_spatiotemporal_hawkes(*args)


def test_hawkes_enforces_event_safety_limit():
    with pytest.raises(RuntimeError):
        simulate_spatiotemporal_hawkes(1000, 0.5, 1, 0.1, (0, 0, 1, 1), 10, seed=1, max_events=2)
