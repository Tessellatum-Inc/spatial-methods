import random
import pytest
from rstar_tree import RStarTree

def intersects(a,b):
    return not (a[2]<b[0] or b[2]<a[0] or a[3]<b[1] or b[3]<a[1])

def test_incremental_queries_match_brute_force():
    rng=random.Random(921); tree=RStarTree(max_entries=5); records=[]
    for _ in range(250):
        x,y=rng.uniform(-20,20),rng.uniform(-20,20)
        w,h=rng.uniform(0,4),rng.uniform(0,4)
        box=(x,y,x+w,y+h)
        assert tree.insert(box)==len(records)
        records.append(box)
    assert len(tree)==len(records)
    for _ in range(120):
        x,y=rng.uniform(-22,22),rng.uniform(-22,22)
        q=(x,y,x+rng.uniform(0,8),y+rng.uniform(0,8))
        assert tree.query(q)==[i for i,b in enumerate(records) if intersects(b,q)]

def test_closed_touch_and_duplicates():
    tree=RStarTree(max_entries=4)
    for b in [(0,0,1,1),(1,1,2,2),(0,0,1,1)]: tree.insert(b)
    assert tree.query((1,1,1,1))==[0,1,2]

def test_empty_and_degenerate():
    tree=RStarTree()
    assert tree.query((0,0,1,1))==[]
    tree.insert((2,2,2,2))
    assert tree.query((2,2,2,2))==[0]

@pytest.mark.parametrize("capacity",[0,1,3,True,4.5])
def test_bad_capacity(capacity):
    with pytest.raises(ValueError): RStarTree(max_entries=capacity)

@pytest.mark.parametrize("box",[(0,0,1),(2,0,1,1),(0,0,float("inf"),1)])
def test_bad_bounds(box):
    with pytest.raises(ValueError): RStarTree().insert(box)

def test_bad_query():
    with pytest.raises(ValueError): RStarTree().query((0,0,1))
