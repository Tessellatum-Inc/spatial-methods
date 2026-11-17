import numpy as np
import pytest

from modified_shepard import ModifiedShepard2D, modified_shepard_interpolate


def sample_grid():
    x, y = np.meshgrid(np.linspace(-2, 2, 5), np.linspace(-2, 2, 5))
    points = np.column_stack((x.ravel(), y.ravel()))
    values = 3 + 2*points[:, 0] - points[:, 1] + .5*points[:, 0]**2 + .25*points[:, 0]*points[:, 1] - .75*points[:, 1]**2
    return points, values


def test_local_quadratic_variant_reproduces_quadratic_surface():
    points, values = sample_grid()
    model = ModifiedShepard2D(points, values, nw=12, nq=12)
    queries = np.array([[.2, .3], [-.7, 1.1], [1.4, -1.2]])
    expected = 3 + 2*queries[:, 0] - queries[:, 1] + .5*queries[:, 0]**2 + .25*queries[:, 0]*queries[:, 1] - .75*queries[:, 1]**2
    assert model.predict(queries) == pytest.approx(expected, abs=1e-9)


def test_exact_sample_locations_return_exact_observations():
    points, values = sample_grid()
    model = ModifiedShepard2D(points, values)
    assert model.predict(points) == pytest.approx(values)


def test_local_support_returns_none_far_outside_all_influence_radii():
    points = np.array([[0., 0.], [10., 0.], [0., 10.], [10., 10.],
                       [5., 0.], [0., 5.], [10., 5.], [5., 10.]])
    values = np.arange(len(points), dtype=float)
    model = ModifiedShepard2D(points, values, nw=2, nq=5)
    assert model.predict([[1000., 1000.]]) == [None]


def test_linear_fallback_handles_locally_collinear_neighbourhoods():
    points = np.array([[0.,0.],[1.,0.],[2.,0.],[3.,0.],[4.,0.],
                       [0.,1.],[1.,1.],[2.,1.],[3.,1.],[4.,1.]])
    values = 2 + points[:,0] - 3*points[:,1]
    model = ModifiedShepard2D(points, values, nw=5, nq=5)
    assert model.predict([[1.5, .5]]) == pytest.approx([.5], abs=1e-9)


@pytest.mark.parametrize("nw,nq", [(1, 5), (2, 4), (20, 5), (5, 20), (True, 5), (5, 5.5)])
def test_invalid_neighbourhood_controls_are_rejected(nw, nq):
    points, values = sample_grid()
    with pytest.raises(ValueError):
        ModifiedShepard2D(points, values, nw=nw, nq=nq)


@pytest.mark.parametrize("points,values", [
    ([[0,0],[1,0],[0,1],[1,1],[2,0]], [1,2,3,4,5]),
    ([[0,0],[1,0],[2,0],[3,0],[4,0],[5,0]], [1,2,3,4,5,6]),
    ([[0,0],[1,0],[0,1],[1,1],[0,0],[2,2]], [1,2,3,4,5,6]),
    ([[0,0],[1,0],[0,1],[1,1],[2,0],[2,1]], [1,2,3,4,float("nan"),6]),
])
def test_invalid_or_degenerate_training_data_are_rejected(points, values):
    with pytest.raises(ValueError):
        ModifiedShepard2D(points, values)


def test_empty_queries_and_invalid_query_shape():
    points, values = sample_grid()
    model = ModifiedShepard2D(points, values)
    assert model.predict(np.empty((0, 2))) == []
    with pytest.raises(ValueError):
        model.predict([[0, 1, 2]])
    with pytest.raises(ValueError):
        model.predict([[0, float("inf")]])
