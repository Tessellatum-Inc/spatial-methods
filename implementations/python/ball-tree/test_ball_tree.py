import random
import pytest
from ball_tree import BallTree2D

def brute(points, query, k):
    return sorted(((i, ((p[0]-query[0])**2+(p[1]-query[1])**2)**0.5)
                   for i,p in enumerate(points)), key=lambda x:(x[1],x[0]))[:k]

def test_knn_matches_brute_force_on_seeded_clouds():
    rng=random.Random(72104)
    for size in (1,2,7,13,40,125):
        points=[(rng.uniform(-100,100),rng.uniform(-100,100)) for _ in range(size)]
        tree=BallTree2D(points,leaf_size=5)
        for _ in range(20):
            q=(rng.uniform(-120,120),rng.uniform(-120,120))
            k=rng.randint(1,size+5)
            actual,expected=tree.query(q,k),brute(points,q,k)
            assert [i for i,_ in actual]==[i for i,_ in expected]
            assert [d for _,d in actual]==pytest.approx([d for _,d in expected])

def test_radius_query_matches_oracle_and_includes_boundary():
    points=[(0,0),(3,4),(3,4),(5,0),(-2,0)]
    actual=BallTree2D(points,leaf_size=1).query_radius((0,0),5)
    expected=[(i,(x*x+y*y)**0.5) for i,(x,y) in enumerate(points)
              if (x*x+y*y)**0.5<=5]
    expected.sort(key=lambda x:(x[1],x[0]))
    assert [i for i,_ in actual]==[i for i,_ in expected]
    assert [d for _,d in actual]==pytest.approx([d for _,d in expected])

def test_duplicates_and_distance_ties_are_stable():
    tree=BallTree2D([(1,0),(-1,0),(1,0),(0,1)],leaf_size=1)
    assert tree.query((0,0),4)==[(0,1.0),(1,1.0),(2,1.0),(3,1.0)]

def test_empty_and_singleton():
    assert BallTree2D([]).query((0,0))==[]
    assert BallTree2D([]).query_radius((0,0),1)==[]
    assert BallTree2D([(2,3)]).query((0,0),4)==[(0,13**0.5)]

@pytest.mark.parametrize("value",[0,-1,True,1.5])
def test_invalid_leaf_size(value):
    with pytest.raises(ValueError): BallTree2D([],leaf_size=value)

@pytest.mark.parametrize("point",[(1,),(1,float("nan")),(0,float("inf"))])
def test_invalid_stored_points(point):
    with pytest.raises(ValueError): BallTree2D([point])

@pytest.mark.parametrize("k",[0,-1,True,1.5])
def test_invalid_k(k):
    with pytest.raises(ValueError): BallTree2D([(0,0)]).query((0,0),k)

@pytest.mark.parametrize("radius",[-1,float("nan"),float("inf"),True])
def test_invalid_radius(radius):
    with pytest.raises(ValueError): BallTree2D([(0,0)]).query_radius((0,0),radius)

def test_invalid_query():
    with pytest.raises(ValueError): BallTree2D([(0,0)]).query((float("nan"),0))
