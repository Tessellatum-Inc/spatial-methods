import numpy as np
import pytest
from terrain_travel import (langmuir_time_seconds, least_cost_time, naismith_time_seconds,
    tobler_edge_time_seconds, tobler_speed_kmh)

def test_tobler_speed_and_directional_edge_cost():
    assert tobler_speed_kmh(-.05)==pytest.approx(6.)
    assert tobler_speed_kmh(0.)==pytest.approx(5.0367421)
    assert tobler_speed_kmh(.1)<tobler_speed_kmh(0.)
    assert tobler_edge_time_seconds(100,10)>tobler_edge_time_seconds(100,-10)

def test_naismith_base_rates():
    assert naismith_time_seconds(5000,0)==pytest.approx(3600)
    assert naismith_time_seconds(0,600)==pytest.approx(3600)
    assert naismith_time_seconds(5000,600)==pytest.approx(7200)

def test_langmuir_descent_corrections():
    base=naismith_time_seconds(5000,0)
    assert langmuir_time_seconds(5000,0,300,3)==pytest.approx(base)
    assert langmuir_time_seconds(5000,0,300,10)==pytest.approx(base-600)
    assert langmuir_time_seconds(5000,0,300,15)==pytest.approx(base+600)

def test_tobler_raster_time_is_directional():
    z=np.array([[0.,10.]])
    up=least_cost_time(z,[(0,0)],model="tobler",cell_size_x=100,connectivity=4)
    down=least_cost_time(z,[(0,1)],model="tobler",cell_size_x=100,connectivity=4)
    assert up[0,1]>down[0,0]

def test_naismith_and_langmuir_raster_times():
    z=np.array([[0.,10.]])
    n=least_cost_time(z,[(0,0)],model="naismith",cell_size_x=100,connectivity=4)
    l=least_cost_time(z,[(0,0)],model="langmuir",cell_size_x=100,connectivity=4)
    assert n[0,1]==pytest.approx(100/5000*3600+10/600*3600)
    np.testing.assert_allclose(l,n)

def test_nodata_barriers_and_multiple_sources():
    z=np.array([[0.,np.nan,2.],[0.,np.nan,2.]])
    out=least_cost_time(z,[(0,0)],model="naismith",connectivity=4)
    assert np.isnan(out[0,1]) and np.isinf(out[0,2])
    flat=least_cost_time(np.zeros((1,5)),[(0,0),(0,4)],model="naismith",connectivity=4)
    np.testing.assert_allclose(flat,[[0,0.72,1.44,0.72,0]])

def test_validation():
    with pytest.raises(ValueError,match="model"): least_cost_time([[0]],[(0,0)],model="other")
    with pytest.raises(ValueError,match="source"): least_cost_time([[np.nan]],[(0,0)])
    with pytest.raises(ValueError,match="outside"): least_cost_time([[0]],[(1,0)])
    with pytest.raises(ValueError,match="positive"): least_cost_time([[0]],[(0,0)],cell_size_x=0)
    with pytest.raises(ValueError,match="non-negative"): naismith_time_seconds(10,-1)
