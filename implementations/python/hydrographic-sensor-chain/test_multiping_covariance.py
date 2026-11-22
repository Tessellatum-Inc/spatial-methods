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
