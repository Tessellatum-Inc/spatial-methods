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
    assert cov[3][3] == pytest.approx(5.2)


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
