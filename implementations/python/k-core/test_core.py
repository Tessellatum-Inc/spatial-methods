import pytest
from core import core_numbers, k_core

def test_path():
    assert core_numbers({0:[1],1:[0,2],2:[1,3],3:[2]}) == {0:1,1:1,2:1,3:1}

def test_triangle_with_tail():
    g={0:[1,2],1:[0,2],2:[0,1,3],3:[2]}
    assert core_numbers(g) == {3:1,2:2,0:2,1:2}
    assert k_core(g,2) == {0:{1,2},1:{0,2},2:{0,1}}

def test_clique_and_disconnected_isolate():
    g={u:[v for v in range(5) if v!=u] for u in range(5)}
    assert set(core_numbers(g).values()) == {4}
    assert core_numbers({"a":["b"],"b":[],"x":[]}) == {"x":0,"a":1,"b":1}

def test_normalises_asymmetric_duplicates_and_loops():
    assert core_numbers({"a":["a","b","b"],"b":[]}) == {"a":1,"b":1}

def test_neighbour_only_nodes_and_empty():
    assert core_numbers({"a":["b"]}) == {"a":1,"b":1}
    assert core_numbers({}) == {}

def test_zero_core_contains_isolates():
    assert k_core({"a":[],"b":[]},0) == {"a":set(),"b":set()}

@pytest.mark.parametrize("k",[-1,1.2,True])
def test_invalid_k(k):
    with pytest.raises(ValueError,match="k"):
        k_core({"a":[]},k)
