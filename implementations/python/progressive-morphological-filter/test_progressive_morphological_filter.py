import numpy as np
import pytest
from progressive_morphological_filter import progressive_morphological_filter


def test_flat_ground_and_raised_objects_are_separated():
    xx, yy = np.meshgrid(np.arange(12.), np.arange(12.))
    ground = np.column_stack([xx.ravel(), yy.ravel(), np.zeros(xx.size)])
    objects = np.array([[3.2, 3.2, 3.0], [7.2, 7.2, 4.0], [9.2, 2.2, 2.0]])
    points = np.vstack([ground, objects])
    mask = progressive_morphological_filter(points, cell_size=1.0,
        window_sizes=(3, 5, 9), initial_distance=.15, slope=.05, max_distance=.5)
    assert np.all(mask[:len(ground)])
    assert not np.any(mask[len(ground):])


def test_sloped_surface_is_retained_with_progressive_threshold():
    xx, yy = np.meshgrid(np.arange(10.), np.arange(10.))
    z = .08 * xx + .04 * yy
    points = np.column_stack([xx.ravel(), yy.ravel(), z.ravel()])
    mask = progressive_morphological_filter(points, cell_size=1,
        window_sizes=(3, 5), initial_distance=.1, slope=.2, max_distance=1)
    assert np.all(mask)


def test_permutation_does_not_change_classification_by_coordinate():
    base = np.array([[x, y, 0.] for x in range(6) for y in range(6)])
    objects = np.array([[2., 2., 2.], [4., 4., 3.]])
    points = np.vstack([base, objects])
    expected = progressive_morphological_filter(points, window_sizes=(3, 5))
    order = np.random.default_rng(4).permutation(len(points))
    actual = progressive_morphological_filter(points[order], window_sizes=(3, 5))
    assert np.array_equal(actual[np.argsort(order)], expected)


def test_rejects_invalid_inputs_and_grid_explosion():
    with pytest.raises(ValueError):
        progressive_morphological_filter([[0, 0]])
    with pytest.raises(ValueError):
        progressive_morphological_filter([[0, 0, 0]], cell_size=0)
    with pytest.raises(ValueError):
        progressive_morphological_filter([[0, 0, 0]], window_sizes=(2, 3))
    with pytest.raises(ValueError):
        progressive_morphological_filter([[0, 0, 0], [100, 100, 0]], cell_size=.01, max_cells=100)
