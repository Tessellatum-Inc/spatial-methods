import math

import pytest

from hydrographic_ray_tracing import (
    trace_layered_water_column,
    trace_layered_water_column_with_sensitivities,
)


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
    assert math.sin(theta_1) / 1600.0 == pytest.approx(math.sin(theta_0) / 1500.0)
    assert result["layers_traversed"] == 2
    assert result["exit_angle_deg"] > 30.0


def test_ray_can_terminate_exactly_at_layer_boundary():
    result = trace_layered_water_column([10.0, 100.0], [1500.0, 1500.0], 0.0, 2 * 10.0 / 1500.0)
    assert result["depth_m"] == pytest.approx(10.0)
    assert result["layers_traversed"] == 1


@pytest.mark.parametrize(
    "depths,speeds,angle,time",
    [
        ([], [], 0.0, 0.1), ([10.0], [], 0.0, 0.1),
        ([10.0, 9.0], [1500.0, 1500.0], 0.0, 0.1),
        ([10.0], [0.0], 0.0, 0.1), ([10.0], [1500.0], 90.0, 0.1),
        ([10.0], [1500.0], 0.0, 0.0), ([10.0], [1500.0], 0.0, math.inf),
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


def test_sensitivity_jacobian_matches_independent_perturbation_oracle():
    args = ([100.0, 300.0], [1490.0, 1520.0], 24.0, 0.12)
    result = trace_layered_water_column_with_sensitivities(*args)
    jac = result["jacobian"]
    params = [1490.0, 1520.0, 24.0, 0.12]
    steps = [0.01, 0.01, 1e-4, 1e-7]
    for col, step in enumerate(steps):
        hi, lo = params[:], params[:]
        hi[col] += step
        lo[col] -= step
        high = trace_layered_water_column(args[0], hi[:2], hi[2], hi[3])
        low = trace_layered_water_column(args[0], lo[:2], lo[2], lo[3])
        for row, key in enumerate(("horizontal_offset_m", "depth_m")):
            expected = (high[key] - low[key]) / (2 * step)
            assert jac[row][col] == pytest.approx(expected, rel=2e-4, abs=1e-7)


def test_homogeneous_vertical_time_sensitivity_is_half_sound_speed():
    result = trace_layered_water_column_with_sensitivities([200.0], [1500.0], 0.0, 0.1)
    assert result["jacobian"][1][0] == pytest.approx(0.05, rel=1e-7)
    assert result["jacobian"][1][2] == pytest.approx(750.0, rel=1e-7)
    assert result["jacobian"][0][1] == pytest.approx(0.0, abs=1e-9)


def test_correlated_profile_covariance_propagates_to_endpoint():
    covariance = [
        [4.0, 1.0, 0.0, 0.0],
        [1.0, 9.0, 0.0, 0.0],
        [0.0, 0.0, 0.01, 0.0],
        [0.0, 0.0, 0.0, 1e-8],
    ]
    result = trace_layered_water_column_with_sensitivities(
        [100.0, 300.0], [1490.0, 1520.0], 24.0, 0.12, covariance
    )
    j = result["jacobian"]
    expected = [[sum(j[r][i] * covariance[i][k] * j[s][k]
                     for i in range(4) for k in range(4))
                 for s in range(2)] for r in range(2)]
    for r in range(2):
        assert result["endpoint_covariance"][r] == pytest.approx(expected[r])


def test_zero_input_covariance_gives_zero_endpoint_covariance():
    result = trace_layered_water_column_with_sensitivities(
        [200.0], [1500.0], 20.0, 0.1, [[0.0] * 3 for _ in range(3)]
    )
    assert result["endpoint_covariance"] == [[0.0, 0.0], [0.0, 0.0]]


@pytest.mark.parametrize(
    "covariance",
    [
        [[1.0, 2.0], [0.0, 1.0]],
        [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, -1.0]],
        [[1.0]],
    ],
)
def test_invalid_input_covariance_is_rejected(covariance):
    with pytest.raises(ValueError):
        trace_layered_water_column_with_sensitivities(
            [200.0], [1500.0], 20.0, 0.1, covariance
        )


def test_sensitivity_rejects_perturbation_that_changes_ray_branch():
    # The unperturbed ray terminates exactly at the first interface.
    with pytest.raises(ValueError, match="stable sensitivity"):
        trace_layered_water_column_with_sensitivities(
            [10.0, 100.0], [1500.0, 1500.0], 0.0, 2 * 10.0 / 1500.0
        )
