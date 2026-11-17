import math
import pytest
from drainage_basin_morphometry import drainage_basin_morphometry

def sample():
 return drainage_basin_morphometry(area=100,perimeter=40,basin_length=10,relief=2,stream_lengths=[10,5,5],stream_counts={1:4,2:2,3:1})

def test_shape_formula_oracles():
 r=sample(); assert r["form_factor"]==pytest.approx(1)
 assert r["elongation_ratio"]==pytest.approx(2/math.sqrt(math.pi))
 assert r["circularity_ratio"]==pytest.approx(math.pi/4)
 assert r["compactness_coefficient"]==pytest.approx(2/math.sqrt(math.pi))

def test_network_formula_oracles():
 r=sample(); assert r["total_stream_length"]==20 and r["total_stream_count"]==7
 assert r["drainage_density"]==pytest.approx(.2) and r["stream_frequency"]==pytest.approx(.07)
 assert r["drainage_texture"]==pytest.approx(7/40) and r["bifurcation_ratios"]=={1:2,2:2}

def test_relief_metrics():
 r=sample(); assert r["relief_ratio"]==pytest.approx(.2) and r["ruggedness_number"]==pytest.approx(.4)

def test_empty_network_zero_relief():
 r=drainage_basin_morphometry(area=1,perimeter=4,basin_length=1,relief=0,stream_lengths=[],stream_counts={})
 assert r["drainage_density"]==r["relief_ratio"]==r["ruggedness_number"]==0

@pytest.mark.parametrize("kw",[
 dict(area=0,perimeter=1,basin_length=1,relief=1,stream_lengths=[],stream_counts={}),
 dict(area=1,perimeter=-1,basin_length=1,relief=1,stream_lengths=[],stream_counts={}),
 dict(area=1,perimeter=1,basin_length=1,relief=-1,stream_lengths=[],stream_counts={}),
 dict(area=1,perimeter=1,basin_length=1,relief=1,stream_lengths=[-1],stream_counts={}),
 dict(area=1,perimeter=1,basin_length=1,relief=1,stream_lengths=[],stream_counts={0:1}),
 dict(area=1,perimeter=1,basin_length=1,relief=1,stream_lengths=[],stream_counts={1:-1}),
])
def test_invalid_inputs(kw):
 with pytest.raises(ValueError): drainage_basin_morphometry(**kw)

def test_nonadjacent_orders_not_paired():
 r=drainage_basin_morphometry(area=10,perimeter=12,basin_length=4,relief=1,stream_lengths=[2],stream_counts={1:3,3:1})
 assert r["bifurcation_ratios"]=={}
