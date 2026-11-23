import pytest
from edge_reliability import edge_attack_curve, edge_betweenness_attack_order, largest_component_size_after_edge_removal, minimal_edge_cut_sets, monte_carlo_reliability, random_edge_attack_order

def path(): return {0:{1},1:{0,2},2:{1}}

def test_edge_removal_and_curve():
    g=path()
    assert largest_component_size_after_edge_removal(g,[(1,2)])==2
    c=edge_attack_curve(g,[(0,1),(1,2)])
    assert c["largest_component_fraction"]==pytest.approx([1,2/3,1/3])
    assert c["remaining_edge_fraction"]==pytest.approx([1,.5,0])

def test_orders_are_valid_and_seeded():
    g={0:{1,2},1:{0,2,3},2:{0,1,3},3:{1,2}}
    assert random_edge_attack_order(g,7)==random_edge_attack_order(g,7)
    assert set(edge_betweenness_attack_order(g))=={(0,1),(0,2),(1,2),(1,3),(2,3)}

def test_reliability_boundary_probabilities():
    g=path()
    assert monte_carlo_reliability(g,1,trials=20)["estimate"]==1
    assert monte_carlo_reliability(g,0,trials=20)["estimate"]==0

def test_k_terminal_estimate_is_reproducible():
    g=path()
    a=monte_carlo_reliability(g,.8,trials=5000,terminals=(0,2),seed=3)
    assert a==monte_carlo_reliability(g,.8,trials=5000,terminals=(0,2),seed=3)
    assert a["estimate"]==pytest.approx(.64,abs=.04)

def test_minimal_cuts():
    assert minimal_edge_cut_sets(path())==[((0,1),),((1,2),)]
    tri={0:{1,2},1:{0,2},2:{0,1}}
    assert minimal_edge_cut_sets(tri)==[((0,1),(0,2)),((0,1),(1,2)),((0,2),(1,2))]

def test_cut_validation_and_limit():
    with pytest.raises(ValueError): minimal_edge_cut_sets({0:{1},1:{0},2:set()})
    with pytest.raises(ValueError): minimal_edge_cut_sets({0:{1},1:{0,2},2:{1}},max_edges=1)
