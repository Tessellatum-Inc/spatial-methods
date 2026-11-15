import pytest
from community import louvain_communities, modularity

def graph():
    g={u:{} for u in range(8)}
    for block in (range(4),range(4,8)):
        for u in block:
            for v in block:
                if u<v: g[u][v]=g[v][u]=1.
    g[3][4]=g[4][3]=.05
    return g

def test_two_dense_communities_and_modularity_gain():
    g=graph(); c=louvain_communities(g,seed=7)
    assert {frozenset(x) for x in c}=={frozenset(range(4)),frozenset(range(4,8))}
    assert modularity(g,c)>modularity(g,[set(g)])

def test_seeded_repeatability():
    g=graph()
    assert louvain_communities(g,seed=11)==louvain_communities(g,seed=11)

def test_empty_and_isolates():
    assert louvain_communities({})==[]
    assert {frozenset(x) for x in louvain_communities({"a":[],"b":[]})}=={frozenset({"a"}),frozenset({"b"})}

def test_asymmetric_and_duplicate_edges():
    assert louvain_communities({0:[1,1],1:[]})==[{0,1}]

def test_resolution():
    g=graph()
    assert len(louvain_communities(g,resolution=2))>=len(louvain_communities(g,resolution=.5))

@pytest.mark.parametrize("kw",[{"resolution":0},{"resolution":float("nan")},{"max_levels":0},{"max_passes":True}])
def test_invalid_options(kw):
    with pytest.raises(ValueError): louvain_communities({0:[]},**kw)

def test_modularity_partition_validation():
    with pytest.raises(ValueError,match="partition"): modularity({0:[1],1:[0]},[{0}])
