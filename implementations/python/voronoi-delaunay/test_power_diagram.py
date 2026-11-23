import numpy as np
import pytest
from power_diagram import power_diagram,polygon_area


def test_two_unweighted_sites_split_rectangle_at_midpoint():
    cells=power_diagram([[2,5],[8,5]],bounds=(0,0,10,10))
    assert polygon_area(cells[0])==pytest.approx(50)
    assert polygon_area(cells[1])==pytest.approx(50)
    assert max(x for x,y in cells[0])==pytest.approx(5)
    assert min(x for x,y in cells[1])==pytest.approx(5)


def test_power_weight_moves_bisector_and_partitions_area():
    cells=power_diagram([[2,5],[8,5]],weights=[0,24],bounds=(0,0,10,10))
    assert max(x for x,y in cells[0])==pytest.approx(3)
    assert min(x for x,y in cells[1])==pytest.approx(3)
    assert polygon_area(cells[0])==pytest.approx(30)
    assert polygon_area(cells[1])==pytest.approx(70)


def test_single_site_covers_entire_clipping_rectangle():
    cell=power_diagram([[100,-20]],bounds=(-2,-3,4,5))[0]
    assert polygon_area(cell)==pytest.approx(48)


def test_dominated_site_can_have_empty_power_cell():
    cells=power_diagram([[0,0],[1,0]],weights=[0,1e4],bounds=(-1,-1,2,1))
    assert cells[0]==[]
    assert polygon_area(cells[1])==pytest.approx(6)


def test_cells_partition_rectangle_for_multiple_sites():
    cells=power_diagram([[1,1],[4,1],[2,4],[4,4]],weights=[0,.2,-.1,.5],bounds=(0,0,5,5))
    assert sum(polygon_area(cell) for cell in cells)==pytest.approx(25,abs=1e-8)


@pytest.mark.parametrize("sites,weights,bounds",[
    ([],None,(0,0,1,1)),([[0,0],[0,0]],None,(0,0,1,1)),
    ([[0,0]], [1,2],(0,0,1,1)),([[0,0]],None,(0,0,0,1)),
    ([[float("nan"),0]],None,(0,0,1,1)),
])
def test_invalid_power_diagram_inputs(sites,weights,bounds):
    with pytest.raises(ValueError):
        power_diagram(sites,weights=weights,bounds=bounds)


def test_adding_a_common_constant_to_all_weights_preserves_the_diagram():
    sites=[[2,5],[8,5],[4,8]]
    a=power_diagram(sites,weights=[0,24,5],bounds=(0,0,10,10))
    b=power_diagram(sites,weights=[1e12,1e12+24,1e12+5],bounds=(0,0,10,10))
    for left,right in zip(a,b):
        assert polygon_area(left)==pytest.approx(polygon_area(right),abs=1e-8)
