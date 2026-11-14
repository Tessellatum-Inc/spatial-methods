import numpy as np
import pytest
from kde import gaussian_spatial_intensity, gaussian_spacetime_intensity


def test_single_event_at_event_location_has_gaussian_peak():
    result = gaussian_spatial_intensity([[0., 0.]], [[0., 0.]], 2.0)
    assert result[0] == pytest.approx(1.0 / (2.0 * np.pi * 4.0))


def test_intensity_is_sum_not_probability_density_normalised_by_event_count():
    one = gaussian_spatial_intensity([[0., 0.]], [[0., 0.]], 1.0)
    two = gaussian_spatial_intensity([[0., 0.], [0., 0.]], [[0., 0.]], 1.0)
    assert two[0] == pytest.approx(2.0 * one[0])


def test_weights_scale_intensity():
    a = gaussian_spatial_intensity([[0., 0.]], [[0., 0.]], 1.0, weights=[3.0])
    b = gaussian_spatial_intensity([[0., 0.]], [[0., 0.]], 1.0)
    assert a[0] == pytest.approx(3.0 * b[0])


def test_spacetime_kernel_factorizes_for_one_event():
    spatial = gaussian_spatial_intensity([[0., 0.]], [[0., 0.]], 2.0)[0]
    result = gaussian_spacetime_intensity([[0., 0.]], [0.], [[0., 0.]], [0.],
                                          2.0, 3.0)[0]
    assert result == pytest.approx(spatial / (np.sqrt(2.0 * np.pi) * 3.0))


@pytest.mark.parametrize("events,query,h", [
    ([[0., 0., 1.]], [[0., 0.]], 1.0),
    ([[0., 0.]], [[0., 0.]], 0.0),
    ([[0., 0.]], [[0., 0.]], np.inf),
    ([], [[0., 0.]], 1.0),
])
def test_spatial_invalid_inputs(events, query, h):
    with pytest.raises(ValueError):
        gaussian_spatial_intensity(events, query, h)


def test_spacetime_rejects_mismatched_times():
    with pytest.raises(ValueError):
        gaussian_spacetime_intensity([[0., 0.]], [0., 1.], [[0., 0.]], [0.], 1.0, 1.0)
