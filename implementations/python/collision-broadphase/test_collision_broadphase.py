import pytest
from collision_broadphase import (
    brute_force_pairs, build_bvh, bvh_pairs, bvh_query, intersects,
    spatial_hash_pairs, sweep_and_prune,
)


def sample_boxes():
    return [(0,0,2,2), (1,1,3,3), (3,3,4,4), (5,0,6,1), (2,0,2,1)]


def test_inclusive_aabb_intersection():
    assert intersects((0,0,1,1), (1,1,2,2))
    assert not intersects((0,0,1,1), (1.01,0,2,1))


def test_sweep_and_prune_matches_brute_force():
    boxes = sample_boxes()
    assert sweep_and_prune(boxes) == brute_force_pairs(boxes)


@pytest.mark.parametrize("cell", [0.25, 1, 2, 10])
def test_spatial_hash_matches_brute_force(cell):
    boxes = sample_boxes()
    assert spatial_hash_pairs(boxes, cell) == brute_force_pairs(boxes)


def test_bvh_pairs_and_queries():
    boxes = sample_boxes()
    tree, data = build_bvh(boxes, leaf_size=1)
    assert bvh_pairs(boxes, leaf_size=1) == brute_force_pairs(boxes)
    assert bvh_query(tree, data, (0,0,0,0)) == [0]
    assert bvh_query(None, [], (0,0,1,1)) == []


def test_empty_and_singleton_inputs():
    assert sweep_and_prune([]) == set()
    assert spatial_hash_pairs([], 1) == set()
    assert bvh_pairs([]) == set()
    assert bvh_pairs([(0,0,1,1)]) == set()


def test_invalid_boxes_and_parameters():
    with pytest.raises(ValueError): sweep_and_prune([(0,0,1)])
    with pytest.raises(ValueError): spatial_hash_pairs([(0,0,1,1)], 0)
    with pytest.raises(ValueError): build_bvh([(0,0,1,1)], 0)
    with pytest.raises(ValueError): bvh_query(None, [], (2,0,1,1))
