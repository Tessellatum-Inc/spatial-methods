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


def _assert_tree_invariants(tree):
    seen = []
    leaf_depths = set()

    def visit(node, depth, is_root=False):
        assert node.bounds is None if not node.children else node.bounds is not None
        if not is_root:
            assert tree.min_entries <= len(node.children) <= tree.max_entries
        else:
            assert len(node.children) <= tree.max_entries or not node.leaf
        if node.leaf:
            leaf_depths.add(depth)
            seen.extend(item.index for item in node.children)
            for item in node.children:
                assert item.bounds == tree._records[item.index]
        else:
            assert node.children
            for child in node.children:
                assert child.parent is node
                visit(child, depth + 1)
        if node.children:
            expected = node.children[0].bounds
            for child in node.children[1:]:
                expected = (
                    min(expected[0], child.bounds[0]),
                    min(expected[1], child.bounds[1]),
                    max(expected[2], child.bounds[2]),
                    max(expected[3], child.bounds[3]),
                )
            assert node.bounds == expected

    visit(tree.root, 0, True)
    assert len(leaf_depths) <= 1
    assert sorted(seen) == list(range(len(tree._records)))


def test_forced_reinsertion_preserves_all_entries_and_tree_invariants():
    rng = random.Random(20261115)
    tree = RStarTree(max_entries=4)
    records = []
    for _ in range(600):
        x, y = rng.uniform(-100, 100), rng.uniform(-100, 100)
        w, h = rng.uniform(0.01, 8), rng.uniform(0.01, 8)
        box = (x, y, x + w, y + h)
        tree.insert(box)
        records.append(box)
    assert tree._reinsertion_count > 0
    _assert_tree_invariants(tree)
    for _ in range(300):
        x, y = rng.uniform(-110, 110), rng.uniform(-110, 110)
        q = (x, y, x + rng.uniform(0, 12), y + rng.uniform(0, 12))
        assert tree.query(q) == [i for i, b in enumerate(records) if intersects(b, q)]


def test_forced_reinsertion_handles_duplicate_and_degenerate_boxes():
    tree = RStarTree(max_entries=4)
    for i in range(80):
        tree.insert((0, 0, 0, 0) if i % 3 else (i, i, i, i))
    _assert_tree_invariants(tree)
    expected = [i for i in range(80) if i % 3 != 0 or i == 0]\n    assert tree.query((0, 0, 0, 0)) == expected
