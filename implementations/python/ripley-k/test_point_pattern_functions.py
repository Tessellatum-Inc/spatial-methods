import math
import random
import numpy as np
import pytest
from point_pattern_functions import nearest_neighbour_functions

def brute_nearest(a,b,exclude_self=False):
    result=[]
    for i,p in enumerate(a):
        distances=[math.dist(p,q) for j,q in enumerate(b) if not (exclude_self and i==j)]
        result.append(min(distances))
    return np.asarray(result)

def test_g_f_j_match_independent_pairwise_oracle():
    events=np.array([(0.,0.),(3.,0.),(0.,4.),(4.,4.)])
    tests=np.array([(1.,1.),(2.,2.),(5.,1.),(-1.,3.)])
    radii=np.array([0.,1.,2.,3.,5.])
    result=nearest_neighbour_functions(events,tests,radii)
    gd=brute_nearest(events,events,True); fd=brute_nearest(tests,events)
    eg=np.array([(gd<=r).mean() for r in radii]); ef=np.array([(fd<=r).mean() for r in radii])
    ej=np.divide(1-eg,1-ef,out=np.full_like(eg,np.nan),where=(1-ef)>0)
    assert result.event_nearest_distances==pytest.approx(gd)
    assert result.empty_space_distances==pytest.approx(fd)
    assert result.g_values==pytest.approx(eg)
    assert result.f_values==pytest.approx(ef)
    assert result.j_values==pytest.approx(ej,nan_ok=True)

def test_duplicate_events_and_inclusive_radius_ties():
    result=nearest_neighbour_functions([(0,0),(0,0),(2,0)],[(0,0),(1,0)],[0,1,2])
    assert result.g_values==pytest.approx([2/3,2/3,1])
    assert result.f_values==pytest.approx([0.5,1,1])
    assert math.isnan(result.j_values[1]) and math.isnan(result.j_values[2])

def test_seeded_random_patterns_match_oracle():
    rng=random.Random(55017)
    for n,m in ((2,3),(8,11),(35,27),(75,60)):
        events=np.array([(rng.random()*10,rng.random()*8) for _ in range(n)])
        tests=np.array([(rng.random()*10,rng.random()*8) for _ in range(m)])
        radii=np.linspace(0,8,19)
        result=nearest_neighbour_functions(events,tests,radii)
        gd=brute_nearest(events,events,True); fd=brute_nearest(tests,events)
        assert result.g_values==pytest.approx([(gd<=r).mean() for r in radii])
        assert result.f_values==pytest.approx([(fd<=r).mean() for r in radii])

def test_invalid_inputs_rejected():
    with pytest.raises(ValueError): nearest_neighbour_functions([(0,0)],[(0,0)],[1])
    with pytest.raises(ValueError): nearest_neighbour_functions([(0,0),(1,1)],[],[1])
    with pytest.raises(ValueError): nearest_neighbour_functions([(0,0),(1,1)],[(0,0)],[])
    with pytest.raises(ValueError): nearest_neighbour_functions([(0,0),(1,1)],[(0,0)],[-1])
    with pytest.raises(ValueError): nearest_neighbour_functions([(0,float('nan')),(1,1)],[(0,0)],[1])
