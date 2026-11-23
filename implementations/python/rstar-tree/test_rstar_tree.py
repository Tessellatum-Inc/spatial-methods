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
        elif is_root:
            assert len(node.children) <= tree.max_entries
            if not node.leaf:
                assert 2 <= len(node.children)
        else:
            assert tree.min_entries <= len(node.children) <= tree.max_entries
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
    assert sorted(seen) == [i for i, active in enumerate(tree._active) if active]
    assert len(tree) == sum(tree._active)


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
    expected = [i for i in range(80) if i % 3 != 0 or i == 0]
    assert tree.query((0, 0, 0, 0)) == expected


def test_delete_condenses_tree_and_matches_brute_force():
    rng = random.Random(20261116)
    tree = RStarTree(max_entries=4)
    records = []
    for _ in range(420):
        x, y = rng.uniform(-50, 50), rng.uniform(-50, 50)
        w, h = rng.uniform(0.1, 5), rng.uniform(0.1, 5)
        box = (x, y, x + w, y + h)
        tree.insert(box)
        records.append(box)
    deleted = set(rng.sample(range(len(records)), 280))
    for index in sorted(deleted):
        assert tree.delete(index) is True
        assert tree.delete(index) is False
    assert len(tree) == len(records) - len(deleted)
    _assert_tree_invariants(tree)
    for _ in range(240):
        x, y = rng.uniform(-55, 55), rng.uniform(-55, 55)
        q = (x, y, x + rng.uniform(0, 8), y + rng.uniform(0, 8))
        expected = [i for i, box in enumerate(records)
                    if i not in deleted and intersects(box, q)]
        assert tree.query(q) == expected


def test_delete_all_records_collapses_to_empty_root():
    tree = RStarTree(max_entries=4)
    ids = [tree.insert((i, 0, i + 0.5, 1)) for i in range(60)]
    for index in reversed(ids):
        assert tree.delete(index)
    assert len(tree) == 0
    assert tree.query((-1, -1, 100, 2)) == []
    assert tree.root.leaf
    assert tree.root.children == []


@pytest.mark.parametrize("index", [True, 1.5, "1"])
def test_delete_rejects_non_integer_ids(index):
    tree = RStarTree()
    tree.insert((0, 0, 1, 1))
    with pytest.raises(ValueError):
        tree.delete(index)


def test_best_first_k_nearest_matches_rectangle_distance_oracle():
    rng = random.Random(20261117)
    tree = RStarTree(max_entries=4)
    records = []
    for _ in range(360):
        x, y = rng.uniform(-40, 40), rng.uniform(-40, 40)
        w, h = rng.uniform(0, 6), rng.uniform(0, 6)
        box = (x, y, x + w, y + h)
        tree.insert(box)
        records.append(box)
    for _ in range(100):
        point = (rng.uniform(-45, 45), rng.uniform(-45, 45))
        expected = []
        for index, box in enumerate(records):
            dx = max(box[0] - point[0], 0.0, point[0] - box[2])
            dy = max(box[1] - point[1], 0.0, point[1] - box[3])
            expected.append((index, dx * dx + dy * dy))
        expected.sort(key=lambda item: (item[1], item[0]))
        for k in (1, 3, 17, 500):
            assert tree.k_nearest(point, k) == expected[:k]


def test_k_nearest_closed_rectangles_ties_and_deleted_records():
    tree = RStarTree(max_entries=4)
    ids = [tree.insert(box) for box in [
        (1, 0, 2, 1), (-2, 0, -1, 1), (0, 0, 0, 0), (5, 5, 6, 6)
    ]]
    assert tree.k_nearest((0, 0), 3) == [(2, 0.0), (0, 1.0), (1, 1.0)]
    assert tree.delete(ids[0])
    assert tree.k_nearest((0, 0), 3) == [(2, 0.0), (1, 1.0), (3, 50.0)]


@pytest.mark.parametrize("k", [0, -1, True, 1.5])
def test_k_nearest_rejects_invalid_k(k):
    with pytest.raises(ValueError):
        RStarTree().k_nearest((0, 0), k)


def test_k_nearest_rejects_non_finite_point():
    with pytest.raises(ValueError):
        RStarTree().k_nearest((float("nan"), 0), 1)
