import numpy as np
import pytest

from tin_interpolation import TINInterpolator2D, tin_interpolate


VERTICES = np.array([[0., 0.], [2., 0.], [2., 2.], [0., 2.]])
TRIANGLES = np.array([[0, 1, 2], [0, 2, 3]])
VALUES = 5 + 2*VERTICES[:, 0] - 3*VERTICES[:, 1]


def test_affine_plane_is_reproduced_inside_both_triangles():
    queries = [[.5, .25], [1.5, .5], [.25, 1.5]]
    expected = [5 + 2*x - 3*y for x, y in queries]
    assert tin_interpolate(VERTICES, VALUES, TRIANGLES, queries) == pytest.approx(expected)


def test_vertices_and_shared_diagonal_are_interpolated():
    result = tin_interpolate(VERTICES, VALUES, TRIANGLES, [[0, 0], [2, 2], [1, 1]])
    assert result == pytest.approx([VALUES[0], VALUES[2], 4.0])


def test_outside_mesh_returns_none_and_empty_queries_return_empty_list():
    model = TINInterpolator2D(VERTICES, VALUES, TRIANGLES)
    assert model.predict([[3, 1], [-1, 0]]) == [None, None]
    assert model.predict(np.empty((0, 2))) == []


def test_mesh_holes_remain_unsupported():
    model = TINInterpolator2D(VERTICES, VALUES, [[0, 1, 2]])
    assert model.predict([[.25, 1.5]]) == [None]


@pytest.mark.parametrize("vertices,values,triangles", [
    (VERTICES, VALUES[:-1], TRIANGLES),
    (VERTICES, VALUES, [[0, 1, 9]]),
    (VERTICES, VALUES, [[0, 0, 1]]),
    (VERTICES, VALUES, [[0, 1, 2], [2, 1, 0]]),
    ([[0, 0], [1, 0], [2, 0]], [1, 2, 3], [[0, 1, 2]]),
    ([[0, 0], [1, 0], [0, 1], [0, 0]], [1, 2, 3, 4], [[0, 1, 2]]),
])
def test_invalid_meshes_are_rejected(vertices, values, triangles):
    with pytest.raises(ValueError):
        TINInterpolator2D(vertices, values, triangles)


@pytest.mark.parametrize("triangles", [
    [[0., 1., 2.]], [[0, 1]], [], [[0, 1, 2], [0, 1, 2]],
])
def test_invalid_triangle_arrays_are_rejected(triangles):
    with pytest.raises(ValueError):
        TINInterpolator2D(VERTICES, VALUES, triangles)


@pytest.mark.parametrize("tolerance", [-1, float("nan"), float("inf"), True, "1"])
def test_invalid_tolerance_is_rejected(tolerance):
    with pytest.raises(ValueError):
        TINInterpolator2D(VERTICES, VALUES, TRIANGLES, tolerance=tolerance)


@pytest.mark.parametrize("queries", [
    [[0, float("nan")]], [[0]], [[0, 0, 0]],
])
def test_invalid_queries_are_rejected(queries):
    with pytest.raises(ValueError):
        TINInterpolator2D(VERTICES, VALUES, TRIANGLES).predict(queries)
