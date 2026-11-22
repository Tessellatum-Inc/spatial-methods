import math

import pytest

from hydrographic_ray_tracing import trace_layered_water_column


def test_vertical_ray_in_homogeneous_water_matches_two_way_depth():
    result = trace_layered_water_column([100.0], [1500.0], 0.0, 0.1)
    assert result["depth_m"] == pytest.approx(75.0)
    assert result["horizontal_offset_m"] == pytest.approx(0.0)
    assert result["exit_angle_deg"] == pytest.approx(0.0)
    assert result["one_way_travel_time_s"] == pytest.approx(0.05)


def test_oblique_ray_matches_homogeneous_analytic_geometry():
    result = trace_layered_water_column([100.0], [1500.0], 30.0, 0.1)
    expected_depth = 1500.0 * 0.05 * math.cos(math.radians(30.0))
    assert result["depth_m"] == pytest.approx(expected_depth)
    assert result["horizontal_offset_m"] == pytest.approx(expected_depth * math.tan(math.radians(30.0)))
    assert result["exit_angle_deg"] == pytest.approx(30.0)


def test_negative_angle_produces_negative_horizontal_offset():
    positive = trace_layered_water_column([100.0], [1500.0], 25.0, 0.08)
    negative = trace_layered_water_column([100.0], [1500.0], -25.0, 0.08)
    assert negative["depth_m"] == pytest.approx(positive["depth_m"])
    assert negative["horizontal_offset_m"] == pytest.approx(-positive["horizontal_offset_m"])


def test_snell_horizontal_slowness_is_conserved_across_speed_interface():
    result = trace_layered_water_column([10.0, 100.0], [1500.0, 1600.0], 30.0, 0.1)
    theta_0 = math.radians(30.0)
    theta_1 = math.radians(result["exit_angle_deg"])
    p0 = math.sin(theta_0) / 1500.0
    p1 = math.sin(theta_1) / 1600.0
    assert p1 == pytest.approx(p0)
    assert result["layers_traversed"] == 2
    assert result["exit_angle_deg"] > 30.0


def test_ray_can_terminate_exactly_at_layer_boundary():
    result = trace_layered_water_column([10.0, 100.0], [1500.0, 1500.0], 0.0, 2 * 10.0 / 1500.0)
    assert result["depth_m"] == pytest.approx(10.0)
    assert result["layers_traversed"] == 1


@pytest.mark.parametrize(
    "depths,speeds,angle,time",
    [
        ([], [], 0.0, 0.1),
        ([10.0], [], 0.0, 0.1),
        ([10.0, 9.0], [1500.0, 1500.0], 0.0, 0.1),
        ([10.0], [0.0], 0.0, 0.1),
        ([10.0], [1500.0], 90.0, 0.1),
        ([10.0], [1500.0], 0.0, 0.0),
        ([10.0], [1500.0], 0.0, math.inf),
    ],
)
def test_invalid_inputs_are_rejected(depths, speeds, angle, time):
    with pytest.raises(ValueError):
        trace_layered_water_column(depths, speeds, angle, time)


def test_profile_must_extend_to_ray_endpoint():
    with pytest.raises(ValueError, match="does not extend"):
        trace_layered_water_column([10.0], [1500.0], 0.0, 0.1)


def test_critical_angle_condition_is_reported_not_clipped():
    with pytest.raises(ValueError, match="critical"):
        trace_layered_water_column([10.0, 100.0], [1500.0, 1800.0], 60.0, 0.04)
