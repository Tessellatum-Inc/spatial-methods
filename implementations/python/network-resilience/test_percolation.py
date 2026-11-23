import pytest
from percolation import largest_component_size, degree_targeted_order, random_attack_order, node_attack_curve

def test_largest_component_size_on_disconnected_graph():
    graph={0:{1},1:{0,2},2:{1},3:set(),4:{5},5:{4}}
    assert largest_component_size(graph)==3

def test_degree_attack_fragments_star_immediately():
    graph={0:{1,2,3,4},1:{0},2:{0},3:{0},4:{0}}
    order=degree_targeted_order(graph)
    assert order[0]==0
    curve=node_attack_curve(graph,order)
    assert curve["largest_component_fraction"][1]==pytest.approx(0.2)
    assert curve["remaining_fraction"][-1]==0

def test_path_removal_curve_uses_original_node_denominator():
    graph={0:{1},1:{0,2},2:{1,3},3:{2}}
    curve=node_attack_curve(graph,[1,2,0,3])
    assert curve["largest_component_fraction"][0]==1
    assert curve["largest_component_fraction"][1]==pytest.approx(0.5)
    assert curve["remaining_fraction"][1]==pytest.approx(0.75)

def test_random_order_is_reproducible_and_validated():
    graph={0:{1},1:{0,2},2:{1}}
    assert random_attack_order(graph,42)==random_attack_order(graph,42)
    with pytest.raises(ValueError):
        node_attack_curve(graph,[0,1])
