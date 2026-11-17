import numpy as np
import pytest
from cfar import ca_cfar_2d,os_cfar_2d

def test_homogeneous_background_is_not_detected():
    x=np.ones((21,21))
    for fn in (ca_cfar_2d,os_cfar_2d):
        out=fn(x,1,3)
        assert out.valid[10,10] and out.threshold[10,10]>1
        assert not out.detections[10,10]

def test_point_target_is_detected():
    x=np.ones((25,25)); x[12,12]=1000
    assert ca_cfar_2d(x,1,4).detections[12,12]
    assert os_cfar_2d(x,1,4).detections[12,12]

def test_guard_ring_excludes_adjacent_bright_cell():
    x=np.ones((21,21)); x[10,11]=1e6
    assert ca_cfar_2d(x,1,3).background[10,10]==pytest.approx(1)

def test_missing_training_cells_are_ignored_and_missing_cut_invalid():
    x=np.ones((21,21)); x[10,9]=np.nan
    out=os_cfar_2d(x,1,3,rank=10)
    assert out.valid[10,10]
    x[10,10]=np.nan
    assert not os_cfar_2d(x,1,3,rank=10).valid[10,10]

def test_borders_are_not_evaluated():
    out=ca_cfar_2d(np.ones((10,10)),1,3)
    assert not out.valid[0,0] and not out.valid[2,3]
    assert out.valid[3,3]

@pytest.mark.parametrize("kwargs",[{"guard_cells":-1},{"training_cells":0},{"guard_cells":2,"training_cells":2},{"false_alarm_rate":1.0},{"false_alarm_rate":0.0}])
def test_bad_parameters(kwargs):
    with pytest.raises(ValueError): ca_cfar_2d(np.ones((10,10)),**kwargs)

def test_os_rank_validation():
    with pytest.raises(ValueError): os_cfar_2d(np.ones((15,15)),1,3,rank=1000)

def test_lower_false_alarm_rate_gives_higher_threshold():
    x=np.ones((15,15))
    a=os_cfar_2d(x,1,3,false_alarm_rate=1e-5)
    b=os_cfar_2d(x,1,3,false_alarm_rate=1e-2)
    assert a.threshold[7,7]>b.threshold[7,7]
