import numpy as np
import pytest
from voronoi_intensity import voronoi_intensity


def test_single_site_owns_full_window():
    r=voronoi_intensity([[5,5]],[0,0,10,8])
    np.testing.assert_allclose(r["areas"],[80])
    np.testing.assert_allclose(r["intensity"],[1/80])


def test_two_sites_split_rectangular_window_at_bisector():
    r=voronoi_intensity([[2,5],[8,5]],[0,0,10,10])
    np.testing.assert_allclose(r["areas"],[50,50],atol=1e-10)
    np.testing.assert_allclose(r["intensity"],[.02,.02])
    np.testing.assert_allclose(sum(r["areas"]),100)


def test_grid_cells_partition_window_and_are_convex_polygons():
    pts=[[2.5,2.5],[7.5,2.5],[2.5,7.5],[7.5,7.5]]
    r=voronoi_intensity(pts,[0,0,10,10])
    np.testing.assert_allclose(r["areas"],[25]*4,atol=1e-10)
    for cell in r["cells"]:
        assert cell.shape[0]>=3 and cell.shape[1]==2


@pytest.mark.parametrize("pts,window",[
    ([[1,1],[1,1]],[0,0,2,2]),
    ([[3,1]],[0,0,2,2]),
    ([[1,1]],[2,0,0,2]),
    ([[1,np.nan]],[0,0,2,2]),
    ([],[0,0,2,2]),
])
def test_invalid_sites_and_window(pts,window):
    with pytest.raises(ValueError): voronoi_intensity(pts,window)


def test_asymmetric_sites_have_positive_cells_and_mass_partition():
    pts=[[1,1],[4,2],[2,5],[8,8]]
    r=voronoi_intensity(pts,[0,0,10,10])
    assert np.all(r["areas"]>0)
    assert np.sum(r["areas"])==pytest.approx(100)
    np.testing.assert_allclose(r["intensity"],1/r["areas"])
