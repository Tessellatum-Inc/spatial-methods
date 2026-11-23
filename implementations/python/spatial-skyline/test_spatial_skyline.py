import numpy as np
import pytest
from spatial_skyline import spatial_skyline

def test_tradeoffs_and_dominated_objects():
    assert spatial_skyline((0, 0), [(1,0),(2,0),(3,0),(4,0)], [[8],[5],[9],[2]]) == (0,1,3)

def test_maximised_attribute():
    assert spatial_skyline((0,0), [(1,0),(2,0),(3,0)], [[10,2],[8,4],[12,1]], minimize=[True,False]) == (0,1)

def test_query_location_changes_result():
    locations=[(0,0),(10,0),(5,0)]; attrs=[[8],[1],[4]]
    assert spatial_skyline((0,0),locations,attrs) == (0,1,2)
    assert spatial_skyline((10,0),locations,attrs) == (1,)

def test_equal_vectors_are_ties():
    assert spatial_skyline((0,0),[(1,0),(1,0),(2,0)],[[3],[3],[4]]) == (0,1)

def test_empty_and_singleton():
    assert spatial_skyline((0,0),np.empty((0,2)),np.empty((0,2))) == ()
    assert spatial_skyline((0,0),[(1,2)],[[5]]) == (0,)

@pytest.mark.parametrize("q,xy,a", [
    ((0,0,0),[(1,0)],[[1]]), ((float("nan"),0),[(1,0)],[[1]]),
    ((0,0),[(1,0,0)],[[1]]), ((0,0),[(float("inf"),0)],[[1]]),
    ((0,0),[(1,0)],[[float("nan")]]), ((0,0),[(1,0)],[]),
])
def test_invalid_inputs(q,xy,a):
    with pytest.raises(ValueError): spatial_skyline(q,xy,a)

def test_invalid_directions():
    with pytest.raises(ValueError,match="minimize"):
        spatial_skyline((0,0),[(1,0)],[[1,2]],minimize=[True])
    with pytest.raises(ValueError,match="minimize"):
        spatial_skyline((0,0),[(1,0)],[[1,2]],minimize=[1,0])

def test_seeded_pairwise_oracle():
    rng=np.random.default_rng(20261116)
    for _ in range(40):
        xy=rng.normal(size=(35,2)); a=rng.uniform(0,10,size=(35,3))
        directions=np.array([True,False,True]); q=np.array([0.3,-0.2])
        got=spatial_skyline(q,xy,a,minimize=directions)
        z=np.column_stack((np.sum((xy-q)**2,axis=1),np.where(directions[None,:],a,-a)))
        expected=tuple(i for i,c in enumerate(z) if not any(
            np.all(z[j]<=c) and np.any(z[j]<c) for j in range(len(z)) if j!=i))
        assert got==expected
