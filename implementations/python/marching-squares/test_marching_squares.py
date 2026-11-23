import numpy as np
import pytest
from marching_squares import marching_squares


def test_linear_plane_contour_interpolates_edges():
    z = np.array([[0., 1.], [0., 1.]])
    result = marching_squares(z, [0.5])[0.5]
    np.testing.assert_allclose(result, [[[0.5,0.0],[0.5,1.0]]])


def test_uses_rectilinear_coordinates_and_multiple_levels():
    z = np.array([[0., 2.], [0., 2.]])
    result = marching_squares(z, [0.5, 1.5], x=[10, 14], y=[20, 24])
    np.testing.assert_allclose(result[0.5][0,:,0], [11,11])
    np.testing.assert_allclose(result[1.5][0,:,0], [13,13])


def test_skips_cells_with_nodata_or_invalid_mask():
    z = np.array([[0., 1., 0.], [0., 1., 0.]])
    z[0, 1] = np.nan
    assert marching_squares(z, [0.5])[0.5].shape == (0,2,2)
    z[0, 1] = 1.
    assert marching_squares(z, [0.5], valid=[[1,0,1],[1,1,1]])[0.5].shape == (0,2,2)


def test_saddle_cell_is_split_into_two_segments():
    z = np.array([[1., 0.], [0., 1.]])
    result = marching_squares(z, [0.5])[0.5]
    assert result.shape == (2,2,2)
    assert np.isfinite(result).all()


def test_flat_cells_do_not_emit_duplicate_contours():
    assert marching_squares(np.ones((2,2)), [1.0])[1.0].shape == (0,2,2)


def test_validates_grid_and_axes():
    with pytest.raises(ValueError, match="at least two"):
        marching_squares([[1]], [0.5])
    with pytest.raises(ValueError, match="strictly increasing"):
        marching_squares([[0,1],[0,1]], [0.5], x=[1,0])
    with pytest.raises(ValueError, match="valid mask"):
        marching_squares([[0,1],[0,1]], [0.5], valid=[[1,1]])
