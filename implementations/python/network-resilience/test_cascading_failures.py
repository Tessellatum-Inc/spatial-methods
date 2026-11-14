import pytest
from cascading_failures import node_betweenness_load, motter_lai_cascade

def graph_with_alternate_route():
    # A square with a pendant source: removing one route increases load on the other.
    return {0:{1,3,4},1:{0,2},2:{1,3},3:{0,2},4:{0}}

def test_betweenness_load_excludes_endpoints_and_is_symmetric():
    g={0:{1},1:{0,2},2:{1}}; load=node_betweenness_load(g)
    assert load=={0:0.0,1:1.0,2:0.0}

def test_high_tolerance_prevents_additional_overload_failures():
    g=graph_with_alternate_route(); result=motter_lai_cascade(g,[1],tolerance=100)
    assert result['failed_nodes']=={1}
    assert result['additional_failures']==0

def test_zero_tolerance_can_trigger_synchronous_cascade():
    result=motter_lai_cascade(graph_with_alternate_route(),[1],tolerance=0)
    assert result['failed_nodes'] >= {1,3}
    assert result['additional_failures']>=1
    assert result['failure_rounds'][1] == (3,)
    assert result['cascade_size']<=5

def test_invalid_attacks_and_tolerance():
    g=graph_with_alternate_route()
    with pytest.raises(ValueError): motter_lai_cascade(g,[],tolerance=.2)
    with pytest.raises(ValueError): motter_lai_cascade(g,[1,1],tolerance=.2)
    with pytest.raises(ValueError): motter_lai_cascade(g,[99],tolerance=.2)
    with pytest.raises(ValueError): motter_lai_cascade(g,[1],tolerance=-.1)
    with pytest.raises(ValueError): motter_lai_cascade(g,[1],tolerance=float('nan'))
