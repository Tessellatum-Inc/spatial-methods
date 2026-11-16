import numpy as np
import pytest
from flow_routing import route_d_infinity,route_multiple_flow_direction,flow_accumulation,RoutingResult

def test_dinf_routes_planar_eastward_slope():
    z=np.array([[5.,4.,3.],[5.,4.,3.],[5.,4.,3.]])
    result=route_d_infinity(z)
    assert result.receiver_rows[1,1,0]==1
    assert result.receiver_cols[1,1,0]==2
    assert result.proportions[1,1,0]==pytest.approx(1)
    assert result.direction[1,1]==pytest.approx(0)

def test_dinf_receiver_weights_are_normalised():
    z=np.array([[9.,8.,7.],[9.,5.,4.],[9.,4.,3.]])
    result=route_d_infinity(z)
    assert result.proportions[1,1].sum()==pytest.approx(1)
    assert np.count_nonzero(result.proportions[1,1]) in (1,2)

def test_mfd_weights_all_lower_neighbours():
    z=np.array([[8.,7.,6.],[9.,5.,4.],[9.,4.,3.]])
    result=route_multiple_flow_direction(z)
    assert result.proportions[1,1].sum()==pytest.approx(1)
    assert np.count_nonzero(result.proportions[1,1])>=2
    assert np.all(result.proportions[1,1]>=0)

def test_mfd_exponent_changes_weights_not_receivers():
    z=np.array([[8.,7.,6.],[9.,5.,4.],[9.,4.,3.]])
    a=route_multiple_flow_direction(z,exponent=1)
    b=route_multiple_flow_direction(z,exponent=3)
    assert np.array_equal(a.receiver_rows>=0,b.receiver_rows>=0)
    assert not np.allclose(a.proportions,b.proportions)

def test_accumulation_conserves_unit_sources():
    result=route_multiple_flow_direction([[3.,2.,1.]])
    acc=flow_accumulation(result)
    assert acc[0,2]==pytest.approx(3)
    assert np.nansum(acc)==pytest.approx(6)

def test_accumulation_rejects_cycles():
    bad=RoutingResult(np.array([[[0]]]),np.array([[[0]]]),np.array([[[1.]]]),np.zeros((1,1)),np.zeros((1,1)))
    with pytest.raises(ValueError,match="cycle"): flow_accumulation(bad)

def test_nodata_and_flat_cells_are_terminals():
    z=np.array([[5.,4.,-9999.],[5.,4.,3.]])
    result=route_d_infinity(z,nodata=-9999)
    assert np.isnan(result.direction[0,2])
    assert result.proportions[0,2].sum()==0

def test_invalid_inputs_are_rejected():
    with pytest.raises(ValueError,match="2D"): route_d_infinity([1.,2.])
    with pytest.raises(ValueError,match="cellsize"): route_multiple_flow_direction([[1,2]],cellsize=(0,1))
    with pytest.raises(ValueError,match="exponent"): route_multiple_flow_direction([[2,1]],exponent=0)
