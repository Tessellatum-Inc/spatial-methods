import numpy as np
import pytest

from time_geography import (
    contains_potential_path_points,
    potential_path_area,
    space_time_prism_slice,
)


def test_potential_path_area_is_circle_for_coincident_foci():
    result = potential_path_area((0, 0), (0, 0), duration=10, speed=2)
    assert result["semi_major"] == pytest.approx(10)
    assert result["semi_minor"] == pytest.approx(10)
    assert result["area"] == pytest.approx(np.pi * 100)


def test_potential_path_area_degenerate_line_at_minimum_duration():
    result = potential_path_area((0, 0), (10, 0), duration=5, speed=2)
    assert result["feasible"]
    assert result["semi_major"] == pytest.approx(5)
    assert result["semi_minor"] == pytest.approx(0)
    assert result["area"] == 0


def test_infeasible_budget_returns_empty_area():
    result = potential_path_area((0, 0), (10, 0), duration=4, speed=2)
    assert not result["feasible"]
    assert result["bounds"] is None


def test_point_membership_uses_sum_of_distances():
    mask = contains_potential_path_points(
        [(5, 0), (5, 2), (5, 4), (0, 0)],
        (0, 0), (10, 0), duration=6, speed=2,
    )
    assert mask.tolist() == [True, True, False, True]


def test_space_time_slice_has_correct_reachability_radii():
    result = space_time_prism_slice(
        (0, 0), (10, 0), departure_time=0, arrival_time=10, time=4, speed=2
    )
    assert result["disks"][0]["radius"] == pytest.approx(8)
    assert result["disks"][1]["radius"] == pytest.approx(12)


@pytest.mark.parametrize("kwargs", [
    {"duration": -1, "speed": 1},
    {"duration": 1, "speed": 0},
])
def test_invalid_duration_or_speed_rejected(kwargs):
    with pytest.raises(ValueError):
        potential_path_area((0, 0), (1, 0), **kwargs)


def test_invalid_time_slice_rejected():
    with pytest.raises(ValueError):
        space_time_prism_slice(
            (0, 0), (1, 0), departure_time=0, arrival_time=2, time=3, speed=1
        )
