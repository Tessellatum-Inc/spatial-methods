import pytest
from partition import spectral_bisection

def test_finds_two_dense_blocks_joined_by_weak_bridge():
    g={u:{} for u in range(8)}
    for block in (range(4),range(4,8)):
        for u in block:
            for v in block:
                if u<v: g[u][v]=g[v][u]=1.
    g[3][4]=g[4][3]=.01
    a,b=spectral_bisection(g)
    assert {frozenset(a),frozenset(b)}=={frozenset(range(4)),frozenset(range(4,8))}

def test_path_returns_nonempty_partition():
    a,b=spectral_bisection({0:[1],1:[0,2],2:[1,3],3:[2]})
    assert a|b=={0,1,2,3} and a&b==set() and a and b

def test_disconnected_components_have_zero_cut_partition():
    a,b=spectral_bisection({0:[1],1:[0],2:[3],3:[2]})
    assert {frozenset(a),frozenset(b)}=={frozenset({0,1}),frozenset({2,3})}

def test_isolates_are_assigned_and_all_nodes_preserved():
    a,b=spectral_bisection({0:[1],1:[0],2:[],3:[]})
    assert a|b=={0,1,2,3} and a&b==set()

def test_all_isolates_split_deterministically():
    assert spectral_bisection({0:[],1:[],2:[],3:[]})==({0,1},{2,3})

def test_invalid_weights_and_too_small_graph():
    with pytest.raises(ValueError,match="two"): spectral_bisection({0:[]})
    with pytest.raises(ValueError,match="weights"): spectral_bisection({0:{1:-1},1:{0:-1}})
