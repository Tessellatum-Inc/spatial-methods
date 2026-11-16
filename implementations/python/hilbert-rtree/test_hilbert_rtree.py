import random
import pytest
from hilbert_rtree import HilbertPackedRTree, hilbert_index, _intersects

def test_hilbert_order_on_two_by_two_grid():
    assert [hilbert_index(x,y,bits=1) for x,y in [(0,0),(0,1),(1,1),(1,0)]] == [0,1,2,3]

def test_empty_and_single_entry():
    assert HilbertPackedRTree([]).query((0,0,1,1)) == []
    tree=HilbertPackedRTree([(0,0,1,1)])
    assert len(tree)==1 and tree.query((1,1,2,2))==[0]

def test_closed_boundary_touch_is_included():
    tree=HilbertPackedRTree([(0,0,1,1),(1,1,2,2)],node_capacity=2)
    assert tree.query((1,1,1,1)) == [0,1]

def test_random_queries_match_brute_force_for_multiple_capacities():
    rng=random.Random(20261116)
    boxes=[]
    for _ in range(350):
        x,y=rng.uniform(-50,50),rng.uniform(-50,50)
        w,h=rng.uniform(0,7),rng.uniform(0,7)
        boxes.append((x,y,x+w,y+h))
    queries=[]
    for _ in range(150):
        x,y=rng.uniform(-55,55),rng.uniform(-55,55)
        w,h=rng.uniform(0,12),rng.uniform(0,12)
        queries.append((x,y,x+w,y+h))
    for capacity in (2,3,5,8,16):
        tree=HilbertPackedRTree(boxes,node_capacity=capacity)
        for q in queries:
            assert tree.query(q)==[i for i,b in enumerate(boxes) if _intersects(b,q)]

def test_duplicate_centres_and_degenerate_boxes_are_retained():
    boxes=[(0,0,0,0)]*20+[(1,1,1,1)]*20
    tree=HilbertPackedRTree(boxes,node_capacity=3)
    assert tree.query((0,0,0,0))==list(range(20))
    assert tree.query((1,1,1,1))==list(range(20,40))

@pytest.mark.parametrize("capacity",[0,1,True,2.5])
def test_invalid_capacity(capacity):
    with pytest.raises(ValueError): HilbertPackedRTree([(0,0,1,1)],node_capacity=capacity)

@pytest.mark.parametrize("bits",[0,32,True,2.5])
def test_invalid_hilbert_bits(bits):
    with pytest.raises(ValueError): HilbertPackedRTree([(0,0,1,1)],hilbert_bits=bits)

@pytest.mark.parametrize("bounds",[(0,0,1),(2,0,1,1),(0,0,float("inf"),1)])
def test_invalid_bounds(bounds):
    with pytest.raises(ValueError): HilbertPackedRTree([bounds])

@pytest.mark.parametrize("coords",[(True,0),(0,False),(-1,0),(0,4),(1.2,0)])
def test_hilbert_index_rejects_invalid_grid_coordinates(coords):
    with pytest.raises(ValueError): hilbert_index(*coords,bits=2)
