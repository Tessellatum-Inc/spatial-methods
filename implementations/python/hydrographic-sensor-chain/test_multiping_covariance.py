import pytest
from multiping_covariance import assemble_multiping_jacobian, clock_offset_and_drift_sensitivities, propagate_multiping_covariance

def test_shared_clock_offset_creates_cross_ping_covariance():
    local=[[[1.0],[0.0],[0.0]],[[1.0],[0.0],[0.0]]]
    shared=[[[1.0],[0.0],[0.0]],[[2.0],[0.0],[0.0]]]
    result=propagate_multiping_covariance(local,shared,[[0,0,0],[0,0,0],[0,0,0.25]])
    c=result["covariance"]
    assert c[0][3]==pytest.approx(0.5) and c[3][0]==pytest.approx(0.5)
    assert c[0][0]==pytest.approx(0.25) and c[3][3]==pytest.approx(1.0)

def test_independent_ping_jitter_has_no_cross_ping_covariance():
    local=[[[0.0,1.0],[0.0,0.0],[0.0,0.0]],
           [[0.0,1.0],[0.0,0.0],[0.0,0.0]]]
    shared=[[[0.0],[0.0],[0.0]],[[0.0],[0.0],[0.0]]]
    c=[[0.0]*5 for _ in range(5)]; c[1][1]=0.04; c[3][3]=0.09
    out=propagate_multiping_covariance(local,shared,c)["covariance"]
    assert out[0][3]==pytest.approx(0.0)
    assert out[0][0]==pytest.approx(0.04) and out[3][3]==pytest.approx(0.09)

def test_clock_offset_and_drift_columns():
    out=clock_offset_and_drift_sensitivities([[1,2,0],[0,3,4]],[100,105],100)
    assert out==[[[1.0,0.0],[2.0,0.0],[0.0,0.0]],[[0.0,0.0],[3.0,15.0],[4.0,20.0]]]

def test_shared_and_local_block_order():
    j=assemble_multiping_jacobian(
        [[[1,0],[0,0],[0,0]],[[0,1],[0,0],[0,0]]],
        [[[2],[0],[0]],[[3],[0],[0]]])
    assert len(j)==6 and j[0]==[1,0,0,0,2] and j[3]==[0,0,0,1,3]

def test_rejects_bad_shapes_and_asymmetric_covariance():
    with pytest.raises(ValueError):
        assemble_multiping_jacobian([[[1],[2]]],[[[1],[2]]])
    with pytest.raises(ValueError):
        propagate_multiping_covariance([[[1],[0],[0]],[[1],[0],[0]]],
          [[[1],[0],[0]],[[1],[0],[0]]],[[1,0,0],[0.2,1,0],[0,0,1]])


def test_time_aligned_multiping_clock_offset_and_drift_create_cross_ping_covariance():
    from multiping_covariance import propagate_time_aligned_multiping_covariance
    local = [[[0.0], [0.0], [0.0]], [[0.0], [0.0], [0.0]]]
    shared = [[[0.0], [0.0], [0.0]], [[0.0], [0.0], [0.0]]]
    # [local_1, local_2, calibration, clock_offset, clock_drift]
    c = [[0.0] * 5 for _ in range(5)]
    c[3][3] = 0.25
    c[4][4] = 0.04
    c[3][4] = c[4][3] = 0.01
    out = propagate_time_aligned_multiping_covariance(
        local, shared, [[1, 0, 0], [2, 0, 0]], [100, 105], 100, c)
    cov = out["covariance"]
    assert cov[0][3] == pytest.approx(0.6)
    assert cov[0][0] == pytest.approx(0.25)
    assert cov[3][3] == pytest.approx(5.4)


def test_time_aligned_multiping_retains_cross_ping_navigation_covariance():
    from multiping_covariance import propagate_time_aligned_multiping_covariance
    local = [[[1.0], [0.0], [0.0]], [[1.0], [0.0], [0.0]]]
    shared = [[[0.0], [0.0], [0.0]], [[0.0], [0.0], [0.0]]]
    # Two correlated local position states, one shared calibration and two clocks.
    c = [[0.0] * 5 for _ in range(5)]
    c[0][0] = c[1][1] = 1.0
    c[0][1] = c[1][0] = 0.3
    out = propagate_time_aligned_multiping_covariance(
        local, shared, [[0, 0, 0], [0, 0, 0]], [100, 105], 100, c)
    assert out["covariance"][0][3] == pytest.approx(0.3)


def test_ray_traced_multiping_composes_local_ray_inputs_and_shared_profile():
    from multiping_covariance import assemble_ray_traced_multiping_jacobian

    sensor = []
    for _ in range(2):
        matrix = [[0.0] * 17 for _ in range(3)]
        matrix[0][15] = 1.0
        sensor.append(matrix)
    rays = [
        [[2.0, 5.0, 11.0], [3.0, 7.0, 13.0]],
        [[4.0, 6.0, 12.0], [8.0, 9.0, 14.0]],
    ]
    jacobian = assemble_ray_traced_multiping_jacobian(sensor, rays)
    assert len(jacobian) == 6
    # Per ping: 15 sensor states, launch angle, travel time; then one shared speed.
    assert jacobian[0][15:17] == pytest.approx([5.0, 11.0])
    assert jacobian[0][34] == pytest.approx(2.0)
    assert jacobian[3][32:34] == pytest.approx([6.0, 12.0])
    assert jacobian[3][34] == pytest.approx(4.0)


def test_shared_sound_speed_error_creates_cross_ping_sounding_covariance():
    from multiping_covariance import propagate_ray_traced_multiping_covariance

    sensor = []
    for _ in range(2):
        matrix = [[0.0] * 17 for _ in range(3)]
        matrix[0][15] = 1.0
        sensor.append(matrix)
    rays = [
        [[2.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
        [[4.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
    ]
    # 17 local inputs per ping, followed by one shared sound-speed parameter.
    covariance = [[0.0] * 35 for _ in range(35)]
    covariance[34][34] = 0.25
    result = propagate_ray_traced_multiping_covariance(sensor, rays, covariance)
    output = result["covariance"]
    assert output[0][0] == pytest.approx(1.0)
    assert output[0][3] == pytest.approx(2.0)
    assert output[3][0] == pytest.approx(2.0)
    assert output[3][3] == pytest.approx(4.0)


def test_ray_traced_multiping_retains_correlated_ping_travel_time_errors():
    from multiping_covariance import propagate_ray_traced_multiping_covariance

    sensor = []
    for _ in range(2):
        matrix = [[0.0] * 17 for _ in range(3)]
        matrix[0][15] = 1.0
        sensor.append(matrix)
    rays = [
        [[0.0, 0.0, 1.0], [0.0, 0.0, 0.0]],
        [[0.0, 0.0, 2.0], [0.0, 0.0, 0.0]],
    ]
    covariance = [[0.0] * 35 for _ in range(35)]
    # Travel-time columns are 16 and 33 in the assembled input vector.
    covariance[16][16] = 0.04
    covariance[33][33] = 0.09
    covariance[16][33] = covariance[33][16] = 0.03
    output = propagate_ray_traced_multiping_covariance(
        sensor, rays, covariance)["covariance"]
    assert output[0][0] == pytest.approx(0.04)
    assert output[0][3] == pytest.approx(0.06)
    assert output[3][3] == pytest.approx(0.36)


def test_ray_traced_multiping_rejects_mismatched_ray_jacobian_count():
    from multiping_covariance import assemble_ray_traced_multiping_jacobian

    sensor = [[[0.0] * 17 for _ in range(3)]]
    with pytest.raises(ValueError):
        assemble_ray_traced_multiping_jacobian(sensor, [])


def test_time_aligned_ray_traced_multiping_appends_epoch_clock_columns():
    from multiping_covariance import assemble_time_aligned_ray_traced_multiping_jacobian

    sensor = []
    for _ in range(2):
        matrix = [[0.0] * 17 for _ in range(3)]
        matrix[0][15] = 1.0
        sensor.append(matrix)
    rays = [
        [[1.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
        [[2.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
    ]
    time_sensitivities = [[3.0, 4.0, 5.0], [6.0, 7.0, 8.0]]
    jacobian = assemble_time_aligned_ray_traced_multiping_jacobian(
        sensor, rays, time_sensitivities)
    assert len(jacobian) == 6
    # Two local 17-state blocks + one shared profile + two epoch offsets.
    assert len(jacobian[0]) == 37
    assert jacobian[0][-2:] == pytest.approx([3.0, 0.0])
    assert jacobian[1][-2:] == pytest.approx([4.0, 0.0])
    assert jacobian[3][-2:] == pytest.approx([0.0, 6.0])
    assert jacobian[5][-2:] == pytest.approx([0.0, 8.0])


def test_time_aligned_ray_traced_multiping_propagates_clock_cross_covariance():
    from multiping_covariance import propagate_time_aligned_ray_traced_multiping_covariance

    sensor = []
    for _ in range(2):
        matrix = [[0.0] * 17 for _ in range(3)]
        matrix[0][15] = 1.0
        sensor.append(matrix)
    rays = [
        [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
        [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
    ]
    time_sensitivities = [[1.0, 0.0, 0.0], [1.0, 0.0, 0.0]]
    covariance = [[0.0] * 37 for _ in range(37)]
    # Correlated epoch-offset errors: Var=[4,9], Cov=2.
    covariance[35][35] = 4.0
    covariance[36][36] = 9.0
    covariance[35][36] = covariance[36][35] = 2.0
    result = propagate_time_aligned_ray_traced_multiping_covariance(
        sensor, rays, time_sensitivities, covariance)
    output = result["covariance"]
    assert output[0][0] == pytest.approx(4.0)
    assert output[0][3] == pytest.approx(2.0)
    assert output[3][0] == pytest.approx(2.0)
    assert output[3][3] == pytest.approx(9.0)


def test_time_aligned_ray_traced_multiping_rejects_bad_time_sensitivity():
    from multiping_covariance import assemble_time_aligned_ray_traced_multiping_jacobian

    sensor = [[[0.0] * 17 for _ in range(3)]]
    rays = [[[1.0, 0.0, 0.0], [0.0, 0.0, 0.0]]]
    with pytest.raises(ValueError):
        assemble_time_aligned_ray_traced_multiping_jacobian(
            sensor, rays, [[1.0, float("nan"), 2.0]])

def test_time_aligned_ray_traced_multiping_rejects_asymmetric_covariance():
    from multiping_covariance import propagate_time_aligned_ray_traced_multiping_covariance

    sensor = [[[0.0] * 17 for _ in range(3)]]
    rays = [[[1.0, 0.0, 0.0], [0.0, 0.0, 0.0]]]
    sensitivities = [[1.0, 0.0, 0.0]]
    covariance = [[0.0] * 19 for _ in range(19)]
    covariance[0][1] = 0.1
    with pytest.raises(ValueError, match="must be symmetric"):
        propagate_time_aligned_ray_traced_multiping_covariance(
            sensor, rays, sensitivities, covariance)

def test_trajectory_results_drive_ray_and_epoch_jacobian_composition():
    from multiping_covariance import assemble_time_aligned_ray_traced_multiping_jacobian_from_trajectory

    trajectory_result = {
        "jacobian": [[0.0] * 19 for _ in range(3)],
        "time_offset_sensitivity": [7.0, 8.0, 9.0],
    }
    trajectory_result["jacobian"][0][15] = 1.0
    trajectory_result["jacobian"][1][16] = 1.0
    trajectory_result["jacobian"][2][17] = 1.0
    trajectory_result["jacobian"][0][18] = 7.0
    trajectory_result["jacobian"][1][18] = 8.0
    trajectory_result["jacobian"][2][18] = 9.0
    ray = [[2.0, 3.0, 4.0], [5.0, 6.0, 7.0]]
    jacobian = assemble_time_aligned_ray_traced_multiping_jacobian_from_trajectory(
        [trajectory_result], [ray], [90.0])
    # At 90 degrees, horizontal endpoint maps to transducer +y.
    assert jacobian[0][15:17] == pytest.approx([0.0, 0.0])
    assert jacobian[1][15:17] == pytest.approx([3.0, 4.0])
    assert jacobian[2][15:17] == pytest.approx([6.0, 7.0])
    assert jacobian[0][-1] == pytest.approx(7.0)
    assert jacobian[1][-1] == pytest.approx(8.0)
    assert jacobian[2][-1] == pytest.approx(9.0)


def test_trajectory_composition_rejects_wrong_jacobian_shape():
    from multiping_covariance import assemble_time_aligned_ray_traced_multiping_jacobian_from_trajectory

    with pytest.raises(ValueError, match="3x19"):
        assemble_time_aligned_ray_traced_multiping_jacobian_from_trajectory(
            [{"jacobian": [[0.0] * 18 for _ in range(3)]}],
            [[[1.0, 0.0, 0.0], [0.0, 0.0, 0.0]]], [0.0])



def test_trajectory_ray_covariance_uses_process_derived_offset_drift_states():
    from clock_state_covariance import propagate_clock_state_covariance
    from multiping_covariance import (
        assemble_time_aligned_ray_traced_stochastic_clock_multiping_jacobian_from_trajectory,
        propagate_time_aligned_ray_traced_stochastic_clock_multiping_covariance_from_trajectory,
    )

    results = []
    for sensitivity in ([2.0, 0.0, 0.0], [3.0, 0.0, 0.0]):
        matrix = [[0.0] * 19 for _ in range(3)]
        matrix[0][18] = sensitivity[0]
        results.append({"jacobian": matrix, "time_offset_sensitivity": sensitivity})
    rays = [
        [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
        [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
    ]
    clock = propagate_clock_state_covariance(
        [100.0, 105.0], [[0.25, 0.01], [0.01, 0.04]], 0.5
    )
    jacobian = assemble_time_aligned_ray_traced_stochastic_clock_multiping_jacobian_from_trajectory(
        results, rays, [0.0, 0.0], [100.0, 105.0], [0.04, 0.06], clock
    )
    # Two pings: 17 local variables each, one profile variable, four clock states.
    assert len(jacobian[0]) == 39
    assert jacobian[0][-4:] == pytest.approx([2.0, -0.04 * 0.0, 0.0, 0.0])
    assert jacobian[3][-4:] == pytest.approx([0.0, 0.0, 3.0, -0.06 * 0.0])

    covariance = [[0.0] * 39 for _ in range(39)]
    for i in range(4):
        for j in range(4):
            covariance[35 + i][35 + j] = clock["joint_state_covariance"][i][j]
    result = propagate_time_aligned_ray_traced_stochastic_clock_multiping_covariance_from_trajectory(
        results, rays, [0.0, 0.0], [100.0, 105.0], [0.04, 0.06], clock, covariance
    )
    output = result["covariance"]
    expected = clock["offset_covariance"]
    assert output[0][0] == pytest.approx(4.0 * expected[0][0])
    assert output[0][3] == pytest.approx(6.0 * expected[0][1])
    assert output[3][3] == pytest.approx(9.0 * expected[1][1])


def test_trajectory_stochastic_clock_rejects_covariance_not_from_clock_process():
    from clock_state_covariance import propagate_clock_state_covariance
    from multiping_covariance import propagate_time_aligned_ray_traced_stochastic_clock_multiping_covariance_from_trajectory

    result = {"jacobian": [[0.0] * 19 for _ in range(3)],
              "time_offset_sensitivity": [1.0, 0.0, 0.0]}
    clock = propagate_clock_state_covariance([0.0], [[1.0, 0.0], [0.0, 1.0]], 0.0)
    covariance = [[0.0] * 20 for _ in range(20)]
    with pytest.raises(ValueError, match="must match the propagated clock process"):
        propagate_time_aligned_ray_traced_stochastic_clock_multiping_covariance_from_trajectory(
            [result], [[[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]],
            [0.0], [0.0], [0.04], clock, covariance
        )


def test_trajectory_stochastic_clock_rejects_mismatched_ping_epochs():
    from clock_state_covariance import propagate_clock_state_covariance
    from multiping_covariance import assemble_time_aligned_ray_traced_stochastic_clock_multiping_jacobian_from_trajectory

    result = {"jacobian": [[0.0] * 19 for _ in range(3)],
              "time_offset_sensitivity": [1.0, 0.0, 0.0]}
    clock = propagate_clock_state_covariance([10.0], [[0.0, 0.0], [0.0, 0.0]], 0.0)
    with pytest.raises(ValueError, match="must equal the supplied ping epochs"):
        assemble_time_aligned_ray_traced_stochastic_clock_multiping_jacobian_from_trajectory(
            [result], [[[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]],
            [0.0], [0.04], [11.0], clock
        )


def test_clock_drift_changes_acoustic_travel_time_sensitivity_separately_from_epoch_offset():
    from clock_state_covariance import propagate_clock_state_covariance
    from multiping_covariance import assemble_time_aligned_ray_traced_stochastic_clock_multiping_jacobian_from_trajectory

    results = []
    for sensitivity in (2.0, 3.0):
        matrix = [[0.0] * 19 for _ in range(3)]
        # Identity acoustic-vector map for a vertical beam and unit
        # endpoint travel-time sensitivity in the depth component.
        matrix[2][17] = 1.0
        matrix[0][18] = sensitivity
        results.append({"jacobian": matrix, "time_offset_sensitivity": [sensitivity, 0.0, 0.0]})
    rays = [
        [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
        [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
    ]
    # Ray endpoint depth derivative with respect to measured two-way time.
    rays = [
        [[0.0, 0.0, 0.0], [0.0, 0.0, 1.0]],
        [[0.0, 0.0, 0.0], [0.0, 0.0, 2.0]],
    ]
    clock = propagate_clock_state_covariance(
        [100.0, 105.0], [[0.25, 0.01], [0.01, 0.04]], 0.5
    )
    jacobian = assemble_time_aligned_ray_traced_stochastic_clock_multiping_jacobian_from_trajectory(
        results, rays, [0.0, 0.0], [100.0, 105.0], [0.04, 0.06], clock
    )
    # The navigation epoch offset acts in x; acoustic clock drift acts in z.
    assert jacobian[0][-4:] == pytest.approx([2.0, 0.0, 0.0, 0.0])
    assert jacobian[2][-4:] == pytest.approx([0.0, -0.04, 0.0, 0.0])
    assert jacobian[3][-4:] == pytest.approx([0.0, 0.0, 3.0, 0.0])
    assert jacobian[5][-4:] == pytest.approx([0.0, 0.0, 0.0, -0.12])


def test_clock_drift_requires_one_nonnegative_two_way_time_per_ping():
    from clock_state_covariance import propagate_clock_state_covariance
    from multiping_covariance import assemble_time_aligned_ray_traced_stochastic_clock_multiping_jacobian_from_trajectory

    result = {"jacobian": [[0.0] * 19 for _ in range(3)],
              "time_offset_sensitivity": [1.0, 0.0, 0.0]}
    clock = propagate_clock_state_covariance([0.0], [[1.0, 0.0], [0.0, 1.0]], 0.0)
    with pytest.raises(ValueError, match="finite and non-negative"):
        assemble_time_aligned_ray_traced_stochastic_clock_multiping_jacobian_from_trajectory(
            [result], [[[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]],
            [0.0], [0.0], [-0.01], clock
        )


def test_event_clock_jacobian_maps_navigation_and_acoustic_interval_to_event_offsets():
    from clock_state_covariance import propagate_clock_elapsed_interval_covariance
    from multiping_covariance import assemble_time_aligned_ray_traced_event_clock_multiping_jacobian_from_trajectory

    matrix = [[0.0] * 19 for _ in range(3)]
    matrix[0][18] = 2.0
    matrix[2][17] = 1.0
    trajectory = {"jacobian": matrix, "time_offset_sensitivity": [2.0, 0.0, 0.0]}
    # Ray travel-time derivative in the depth row is 1.5.
    ray = [[0.0, 0.0, 0.0], [0.0, 0.0, 1.5]]
    clock = propagate_clock_elapsed_interval_covariance(
        [10.0], [10.04], [[0.0, 0.0], [0.0, 0.0]], 0.25,
        additional_epochs_s=[10.0]
    )
    jacobian = assemble_time_aligned_ray_traced_event_clock_multiping_jacobian_from_trajectory(
        [trajectory], [ray], [0.0], [10.0], [10.0], [10.04], clock
    )
    # Local inputs (17), one shared profile, then [tx offset,tx drift,rx offset,rx drift].
    assert len(jacobian[0]) == 22
    assert jacobian[0][-4:] == pytest.approx([2.0, 0.0, 0.0, 0.0])
    assert jacobian[2][-4:] == pytest.approx([1.5, 0.0, -1.5, 0.0])


def test_event_clock_propagator_checks_process_derived_event_covariance():
    from clock_state_covariance import propagate_clock_elapsed_interval_covariance
    from multiping_covariance import propagate_time_aligned_ray_traced_event_clock_multiping_covariance_from_trajectory

    matrix = [[0.0] * 19 for _ in range(3)]
    matrix[2][17] = 1.0
    trajectory = {"jacobian": matrix, "time_offset_sensitivity": [0.0, 0.0, 0.0]}
    ray = [[0.0, 0.0, 0.0], [0.0, 0.0, 1.0]]
    clock = propagate_clock_elapsed_interval_covariance(
        [0.0], [0.1], [[0.0, 0.0], [0.0, 0.0]], 0.5,
        additional_epochs_s=[0.0]
    )
    # One local block + one profile + four event-state values.
    covariance = [[0.0] * 22 for _ in range(22)]
    for i in range(4):
        for j in range(4):
            covariance[18 + i][18 + j] = clock["joint_event_state_covariance"][i][j]
    result = propagate_time_aligned_ray_traced_event_clock_multiping_covariance_from_trajectory(
        [trajectory], [ray], [0.0], [0.0], [0.0], [0.1], clock, covariance
    )
    assert result["covariance"][2][2] == pytest.approx(0.5 * 0.1 ** 3 / 3.0)
    covariance[18][18] += 1.0
    with pytest.raises(ValueError, match="must match the propagated clock process"):
        propagate_time_aligned_ray_traced_event_clock_multiping_covariance_from_trajectory(
            [trajectory], [ray], [0.0], [0.0], [0.0], [0.1], clock, covariance
        )


def test_event_clock_jacobian_rejects_different_transmit_receive_pairing():
    from clock_state_covariance import propagate_clock_elapsed_interval_covariance
    from multiping_covariance import assemble_time_aligned_ray_traced_event_clock_multiping_jacobian_from_trajectory

    trajectories = []
    for _ in range(2):
        matrix = [[0.0] * 19 for _ in range(3)]
        matrix[0][15] = 1.0
        trajectories.append({
            "jacobian": matrix,
            "time_offset_sensitivity": [0.0, 0.0, 0.0],
        })
    rays = [
        [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
        [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
    ]
    clock = propagate_clock_elapsed_interval_covariance(
        [0.0, 1.0], [2.0, 3.0], [[0.0, 0.0], [0.0, 0.0]], 0.1
    )
    # All four epochs remain present and both intervals remain positive, but
    # swapping receive events changes which clock errors belong to each ping.
    with pytest.raises(ValueError, match="must match the clock event covariance pairing"):
        assemble_time_aligned_ray_traced_event_clock_multiping_jacobian_from_trajectory(
            trajectories, rays, [0.0, 0.0], [0.0, 1.0],
            [0.0, 1.0], [3.0, 2.0], clock
        )




def test_temporal_profile_jacobian_assigns_each_ping_to_its_epoch_block():
    from multiping_covariance import (
        assemble_time_aligned_ray_traced_temporal_profile_multiping_jacobian_from_trajectory,
    )

    trajectories = []
    for _ in range(2):
        matrix = [[0.0] * 19 for _ in range(3)]
        matrix[0][15] = 1.0
        trajectories.append({
            "jacobian": matrix,
            "time_offset_sensitivity": [0.0, 0.0, 0.0],
        })
    rays = [
        [[2.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
        [[4.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
    ]
    profile = {
        "profile_epochs_s": [0.0, 10.0],
        "layer_count": 1,
        "joint_profile_covariance": [[1.0, 0.5], [0.5, 1.0]],
    }
    jacobian = assemble_time_aligned_ray_traced_temporal_profile_multiping_jacobian_from_trajectory(
        trajectories, rays, [0.0, 0.0], [0, 1], profile
    )
    # [34 ping-local, 2 epoch-major profile, 2 navigation-offset] columns.
    assert len(jacobian[0]) == 38
    assert jacobian[0][34:36] == pytest.approx([2.0, 0.0])
    assert jacobian[3][34:36] == pytest.approx([0.0, 4.0])


def test_temporal_profile_covariance_propagates_cross_epoch_sounding_correlation():
    from multiping_covariance import (
        propagate_time_aligned_ray_traced_temporal_profile_multiping_covariance_from_trajectory,
    )

    trajectories = []
    for _ in range(2):
        matrix = [[0.0] * 19 for _ in range(3)]
        matrix[0][15] = 1.0
        trajectories.append({
            "jacobian": matrix,
            "time_offset_sensitivity": [0.0, 0.0, 0.0],
        })
    rays = [
        [[2.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
        [[4.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
    ]
    profile = {
        "profile_epochs_s": [0.0, 10.0],
        "layer_count": 1,
        "joint_profile_covariance": [[1.0, 0.5], [0.5, 1.0]],
    }
    covariance = [[0.0] * 38 for _ in range(38)]
    covariance[34][34] = 1.0
    covariance[34][35] = covariance[35][34] = 0.5
    covariance[35][35] = 1.0
    result = propagate_time_aligned_ray_traced_temporal_profile_multiping_covariance_from_trajectory(
        trajectories, rays, [0.0, 0.0], [0, 1], profile, covariance
    )
    output = result["covariance"]
    assert output[0][0] == pytest.approx(4.0)
    assert output[0][3] == pytest.approx(4.0)
    assert output[3][0] == pytest.approx(4.0)
    assert output[3][3] == pytest.approx(16.0)


def test_temporal_profile_jacobian_rejects_out_of_range_epoch_index():
    from multiping_covariance import (
        assemble_time_aligned_ray_traced_temporal_profile_multiping_jacobian_from_trajectory,
    )

    trajectory = {
        "jacobian": [[0.0] * 19 for _ in range(3)],
        "time_offset_sensitivity": [0.0, 0.0, 0.0],
    }
    profile = {
        "profile_epochs_s": [0.0],
        "layer_count": 1,
        "joint_profile_covariance": [[1.0]],
    }
    with pytest.raises(ValueError, match="outside the profile epoch range"):
        assemble_time_aligned_ray_traced_temporal_profile_multiping_jacobian_from_trajectory(
            [trajectory], [[[1.0, 0.0, 0.0], [0.0, 0.0, 0.0]]],
            [0.0], [1], profile
        )


def test_temporal_profile_propagation_rejects_covariance_block_mismatch():
    from multiping_covariance import (
        propagate_time_aligned_ray_traced_temporal_profile_multiping_covariance_from_trajectory,
    )

    trajectory = {
        "jacobian": [[0.0] * 19 for _ in range(3)],
        "time_offset_sensitivity": [0.0, 0.0, 0.0],
    }
    profile = {
        "profile_epochs_s": [0.0],
        "layer_count": 1,
        "joint_profile_covariance": [[1.0]],
    }
    covariance = [[0.0] * 19 for _ in range(19)]
    with pytest.raises(ValueError, match="must match the temporal profile model"):
        propagate_time_aligned_ray_traced_temporal_profile_multiping_covariance_from_trajectory(
            [trajectory], [[[1.0, 0.0, 0.0], [0.0, 0.0, 0.0]]],
            [0.0], [0], profile, covariance
        )



def test_interpolated_profile_sensitivities_map_back_to_source_observations():
    from multiping_covariance import (
        assemble_interpolated_profile_time_aligned_ray_traced_multiping_jacobian_from_trajectory,
        propagate_interpolated_profile_time_aligned_ray_traced_multiping_covariance_from_trajectory,
    )

    trajectories = []
    for _ in range(2):
        matrix = [[0.0] * 19 for _ in range(3)]
        matrix[0][15] = 1.0
        trajectories.append({"jacobian": matrix, "time_offset_sensitivity": [0.0, 0.0, 0.0]})
    rays = [
        [[2.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
        [[4.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
    ]
    source_covariance = [[1.0, 0.5], [0.5, 1.0]]
    interpolation = {
        "query_epochs_s": [2.0, 8.0],
        "source_profile_epochs_s": [0.0, 10.0],
        "layer_count": 1,
        "interpolation_operator": [[0.8, 0.2], [0.2, 0.8]],
        "source_joint_profile_covariance": source_covariance,
    }
    jacobian = assemble_interpolated_profile_time_aligned_ray_traced_multiping_jacobian_from_trajectory(
        trajectories, rays, [0.0, 0.0], [0, 1], interpolation
    )
    # Mid-interval query sensitivities 2 and 4 map through H=[0.8,0.2]
    # and H=[0.2,0.8] into the original observed-profile states.
    assert len(jacobian[0]) == 38
    assert jacobian[0][34:36] == pytest.approx([1.6, 0.4])
    assert jacobian[3][34:36] == pytest.approx([0.8, 3.2])

    covariance = [[0.0] * 38 for _ in range(38)]
    covariance[34][34] = source_covariance[0][0]
    covariance[34][35] = source_covariance[0][1]
    covariance[35][34] = source_covariance[1][0]
    covariance[35][35] = source_covariance[1][1]
    propagated = propagate_interpolated_profile_time_aligned_ray_traced_multiping_covariance_from_trajectory(
        trajectories, rays, [0.0, 0.0], [0, 1], interpolation, covariance
    )
    expected_cross = sum(
        jacobian[0][34 + i] * source_covariance[i][j] * jacobian[3][34 + j]
        for i in range(2) for j in range(2)
    )
    assert propagated["covariance"][0][3] == pytest.approx(expected_cross)


def test_interpolated_profile_multiping_rejects_invalid_query_index_and_source_block():
    from multiping_covariance import (
        assemble_interpolated_profile_time_aligned_ray_traced_multiping_jacobian_from_trajectory,
        propagate_interpolated_profile_time_aligned_ray_traced_multiping_covariance_from_trajectory,
    )
    trajectory = {"jacobian": [[0.0] * 19 for _ in range(3)],
                  "time_offset_sensitivity": [0.0, 0.0, 0.0]}
    interpolation = {
        "query_epochs_s": [5.0],
        "source_profile_epochs_s": [0.0, 10.0],
        "layer_count": 1,
        "interpolation_operator": [[0.5, 0.5]],
        "source_joint_profile_covariance": [[1.0, 0.5], [0.5, 1.0]],
    }
    ray = [[[1.0, 0.0, 0.0], [0.0, 0.0, 0.0]]]
    with pytest.raises(ValueError, match="outside the query profile range"):
        assemble_interpolated_profile_time_aligned_ray_traced_multiping_jacobian_from_trajectory(
            [trajectory], ray, [0.0], [1], interpolation
        )
    covariance = [[0.0] * 20 for _ in range(20)]
    with pytest.raises(ValueError, match="source profile covariance block"):
        propagate_interpolated_profile_time_aligned_ray_traced_multiping_covariance_from_trajectory(
            [trajectory], ray, [0.0], [0], interpolation, covariance
        )


def test_ou_conditional_profile_residuals_propagate_across_multiple_pings():
    from multiping_covariance import (
        assemble_ou_conditional_profile_time_aligned_ray_traced_multiping_jacobian_from_trajectory,
        propagate_ou_conditional_profile_time_aligned_ray_traced_multiping_covariance_from_trajectory,
    )
    trajectories = []
    for _ in range(2):
        matrix = [[0.0] * 19 for _ in range(3)]
        matrix[0][15] = 1.0
        trajectories.append({"jacobian": matrix, "time_offset_sensitivity": [0.0, 0.0, 0.0]})
    rays = [
        [[2.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
        [[4.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
    ]
    conditional = {
        "query_epochs_s": [2.0, 8.0],
        "layer_count": 1,
        "conditional_joint_profile_covariance": [[0.5, 0.2], [0.2, 0.6]],
    }
    jacobian = assemble_ou_conditional_profile_time_aligned_ray_traced_multiping_jacobian_from_trajectory(
        trajectories, rays, [0.0, 0.0], [0, 1], conditional
    )
    assert len(jacobian[0]) == 38
    assert jacobian[0][34:36] == pytest.approx([2.0, 0.0])
    assert jacobian[3][34:36] == pytest.approx([0.0, 4.0])

    covariance = [[0.0] * 38 for _ in range(38)]
    covariance[34][34] = 0.5
    covariance[34][35] = covariance[35][34] = 0.2
    covariance[35][35] = 0.6
    result = propagate_ou_conditional_profile_time_aligned_ray_traced_multiping_covariance_from_trajectory(
        trajectories, rays, [0.0, 0.0], [0, 1], conditional, covariance
    )
    assert result["covariance"][0][0] == pytest.approx(2.0)
    assert result["covariance"][0][3] == pytest.approx(1.6)
    assert result["covariance"][3][3] == pytest.approx(9.6)


def test_ou_conditional_profile_multiping_rejects_bad_query_index_and_covariance():
    from multiping_covariance import (
        assemble_ou_conditional_profile_time_aligned_ray_traced_multiping_jacobian_from_trajectory,
        propagate_ou_conditional_profile_time_aligned_ray_traced_multiping_covariance_from_trajectory,
    )
    trajectory = {
        "jacobian": [[0.0] * 19 for _ in range(3)],
        "time_offset_sensitivity": [0.0, 0.0, 0.0],
    }
    ray = [[[1.0, 0.0, 0.0], [0.0, 0.0, 0.0]]]
    conditional = {
        "query_epochs_s": [5.0],
        "layer_count": 1,
        "conditional_joint_profile_covariance": [[1.0]],
    }
    with pytest.raises(ValueError, match="outside the query profile range"):
        assemble_ou_conditional_profile_time_aligned_ray_traced_multiping_jacobian_from_trajectory(
            [trajectory], ray, [0.0], [1], conditional
        )
    covariance = [[0.0] * 19 for _ in range(19)]
    with pytest.raises(ValueError, match="must match the OU conditional covariance"):
        propagate_ou_conditional_profile_time_aligned_ray_traced_multiping_covariance_from_trajectory(
            [trajectory], ray, [0.0], [0], conditional, covariance
        )
