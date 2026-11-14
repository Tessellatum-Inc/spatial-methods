import pytest
from rasterize import dda_line, bresenham_line, wu_line, supercover_line, scanline_fill

@pytest.mark.parametrize("start,end", [((0,0),(5,2)),((2,5),(0,0)),((0,0),(0,5)),((5,1),(1,5)),((3,3),(3,3))])
def test_bresenham_endpoints_and_connectivity(start,end):
    cells=bresenham_line(start,end)
    assert cells[0]==start
    assert cells[-1]==end
    assert all(max(abs(a[0]-b[0]),abs(a[1]-b[1]))==1 for a,b in zip(cells,cells[1:]))

def test_dda_and_wu_basic_contracts():
    assert dda_line((0,0),(0,0))==[(0,0)]
    assert dda_line((0,0),(3,0))==[(0,0),(1,0),(2,0),(3,0)]
    pixels=wu_line((0,0),(4,2))
    assert pixels and all(0<=w<=1 for _,_,w in pixels)

def test_supercover_includes_corner_touch_neighbours():
    cells=set(supercover_line((0.5,0.5),(2.5,2.5)))
    assert {(0,0),(1,1),(2,2)}.issubset(cells)
    assert {(1,0),(0,1)}.issubset(cells)

def test_scanline_fill_rectangle_by_cell_centres():
    grid=scanline_fill([(1,1),(4,1),(4,4),(1,4)],5,5)
    assert sum(sum(row) for row in grid)==9
    assert grid[1][1] and grid[3][3]
    assert not grid[0][0] and not grid[4][4]

def test_scanline_fill_rejects_degenerate_polygon():
    with pytest.raises(ValueError):
        scanline_fill([(0,0),(1,1)],3,3)

def test_supercover_includes_cells_touching_integer_endpoint():
    cells=set(supercover_line((0,0),(2,0)))
    assert {(-1,-1),(-1,0),(0,-1),(0,0),(1,-1),(1,0),(2,-1),(2,0)}.issubset(cells)
