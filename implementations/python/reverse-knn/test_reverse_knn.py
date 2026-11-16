import random
import pytest
from reverse_knn import reverse_k_nearest_neighbors

def brute_force(data, queries, k):
    out = []
    for qx, qy in queries:
        found = []
        for i, (x, y) in enumerate(data):
            qd = (qx-x)**2 + (qy-y)**2
            closer = sum((px-x)**2 + (py-y)**2 < qd
                         for j, (px, py) in enumerate(data) if j != i)
            if closer < k:
                found.append(i)
        out.append(found)
    return out

def test_known_reverse_nearest_neighbour():
    assert reverse_k_nearest_neighbors([(0,0),(2,0),(10,0)], [(0.1,0)], 1) == [[0,1]]

def test_ties_are_inclusive():
    assert reverse_k_nearest_neighbors([(-1,0),(1,0),(0,4)], [(0,0)], 1) == [[0,1,2]]

def test_duplicate_records_remain_distinct():
    # For k=1 each duplicate is beaten by its coincident peer; for k=2
    # both duplicate records and the distant record qualify.
    data = [(0,0),(0,0),(5,0)]
    assert reverse_k_nearest_neighbors(data, [(1,0)], 1) == [[2]]
    assert reverse_k_nearest_neighbors(data, [(1,0)], 2) == [[0,1,2]]

def test_empty_inputs_and_large_k():
    assert reverse_k_nearest_neighbors([], [(0,0)], 1) == [[]]
    assert reverse_k_nearest_neighbors([(0,0)], [], 1) == []
    assert reverse_k_nearest_neighbors([(0,0),(2,0)], [(100,0)], 3) == [[0,1]]

def test_seeded_random_matches_independent_quadratic_oracle():
    rng = random.Random(20261115)
    for n in (1,2,5,20,75):
        data = [(rng.randint(-15,15),rng.randint(-15,15)) for _ in range(n)]
        queries = [(rng.uniform(-20,20),rng.uniform(-20,20)) for _ in range(12)]
        for k in (1,2,4,n+1):
            assert reverse_k_nearest_neighbors(data,queries,k) == brute_force(data,queries,k)

@pytest.mark.parametrize("k", [0,-1,1.5,True,"2"])
def test_invalid_k(k):
    with pytest.raises(ValueError):
        reverse_k_nearest_neighbors([(0,0)],[(1,1)],k)

@pytest.mark.parametrize("points", [[(float("nan"),0)],[(0,float("inf"))],[(0,1,2)]])
def test_invalid_coordinates(points):
    with pytest.raises(ValueError):
        reverse_k_nearest_neighbors(points,[(0,0)],1)
