import pytest
from partition import kernighan_lin_bisection

def cut(g, a, b):
    return sum(w for u, ns in g.items() for v, w in ns.items() if u in a and v in b)

def test_finds_two_dense_communities_with_weak_bridge():
    g={
      0:{1:5,2:1},1:{0:5,2:1},2:{0:1,1:1,3:0.1},
      3:{2:0.1,4:5,5:1},4:{3:5,5:1},5:{3:1,4:1}
    }
    a,b=kernighan_lin_bisection(g,initial=({0,1,3},{2,4,5}))
    assert {frozenset(a),frozenset(b)}=={frozenset({0,1,2}),frozenset({3,4,5})}
    assert len(a)==len(b)==3

def test_unweighted_and_deterministic():
    g={0:[1],1:[0,2],2:[1,3],3:[2]}
    assert kernighan_lin_bisection(g)==kernighan_lin_bisection(g)

def test_isolates_are_supported():
    a,b=kernighan_lin_bisection({0:[],1:[],2:[],3:[]})
    assert len(a)==len(b)==2

@pytest.mark.parametrize("g", [{}, {0:[1],1:[0],2:[]}])
def test_empty_or_odd_graph_rejected(g):
    with pytest.raises(ValueError,match="even"):
        kernighan_lin_bisection(g)

def test_initial_partition_must_be_balanced_and_cover_nodes():
    with pytest.raises(ValueError,match="initial"):
        kernighan_lin_bisection({0:[1],1:[0],2:[3],3:[2]},initial=({0,1,2},{3}))

def test_invalid_weights_rejected():
    with pytest.raises(ValueError,match="weights"):
        kernighan_lin_bisection({0:{1:-1},1:{0:-1}})
    with pytest.raises(ValueError,match="weights"):
        kernighan_lin_bisection({0:{1:float("inf")},1:{0:1}})
