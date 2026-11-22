import pytest

from sounding_uncertainty import propagate_ray_traced_sounding_uncertainty

I = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]


def zero_covariance():
    return [[0.0] * 17 for _ in range(17)]


def args(covariance, endpoint=(0.0, 5.0), azimuth=0.0):
    return ([100.0, 200.0, 10.0], I, [1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0], I, endpoint, azimuth, covariance)


def test_ray_endpoint_maps_to_transducer_vector_and_sounding():
    result = propagate_ray_traced_sounding_uncertainty(*args(zero_covariance()))
    assert result["acoustic_vector_transducer"] == pytest.approx([0.0, 0.0, 5.0])
    assert result["point_navigation"] == pytest.approx([99.0, 200.0, 16.0])
    assert len(result["jacobian"]) == 3
    assert all(len(row) == 17 for row in result["jacobian"])


def test_ray_endpoint_covariance_propagates_into_navigation_coordinates():
    covariance = zero_covariance()
    covariance[15][15] = 4.0
    covariance[16][16] = 9.0
    result = propagate_ray_traced_sounding_uncertainty(*args(covariance))
    assert result["covariance"] == pytest.approx([
        [4.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 9.0]
    ])
    assert result["standard_uncertainties"] == pytest.approx([2.0, 0.0, 3.0])


def test_beam_azimuth_rotates_horizontal_endpoint_uncertainty():
    covariance = zero_covariance()
    covariance[15][15] = 4.0
    result = propagate_ray_traced_sounding_uncertainty(
        *args(covariance, endpoint=(10.0, 5.0), azimuth=90.0)
    )
    assert result["covariance"][0][0] == pytest.approx(0.0, abs=1e-12)
    assert result["covariance"][1][1] == pytest.approx(4.0)
    assert result["covariance"][2][2] == pytest.approx(0.0, abs=1e-12)


def test_ray_navigation_cross_covariance_is_retained():
    covariance = zero_covariance()
    covariance[0][0] = 1.0
    covariance[15][15] = 4.0
    covariance[0][15] = covariance[15][0] = 1.0
    result = propagate_ray_traced_sounding_uncertainty(*args(covariance))
    # Both terms affect navigation x in the same direction: 1 + 4 + 2.
    assert result["covariance"][0][0] == pytest.approx(7.0)


@pytest.mark.parametrize("endpoint,azimuth", [([1.0], 0.0), ([1.0, float("nan")], 0.0), ([1.0, 2.0], float("inf"))])
def test_invalid_ray_endpoint_or_azimuth_is_rejected(endpoint, azimuth):
    with pytest.raises(ValueError):
        propagate_ray_traced_sounding_uncertainty(*args(zero_covariance(), endpoint, azimuth))


def test_wrong_sized_or_asymmetric_covariance_is_rejected():
    with pytest.raises(ValueError):
        propagate_ray_traced_sounding_uncertainty(*args([[0.0] * 18 for _ in range(18)]))
    covariance = zero_covariance()
    covariance[0][1] = 1.0
    with pytest.raises(ValueError, match="symmetric"):
        propagate_ray_traced_sounding_uncertainty(*args(covariance))
