import numpy as np
import pytest
from transform import transform_points

def test_geographic_origin_maps_to_projected_origin():
    result=transform_points([[0,0]],"EPSG:4326","EPSG:3857")
    np.testing.assert_allclose(result,[[0,0]],atol=1e-8)

def test_web_mercator_known_coordinate_and_round_trip():
    point=np.array([[10.0,50.0]])
    projected=transform_points(point,"EPSG:4326","EPSG:3857")
    np.testing.assert_allclose(projected,[[1113194.9079,6446275.8410]],rtol=1e-6)
    restored=transform_points(projected,"EPSG:3857","EPSG:4326")
    np.testing.assert_allclose(restored,point,atol=1e-8)

def test_always_xy_means_longitude_then_latitude():
    projected=transform_points([[9.0,0.0]],"EPSG:4326","EPSG:32632")
    np.testing.assert_allclose(projected,[[500000,0]],atol=1e-5)

def test_same_crs_preserves_coordinates():
    points=np.array([[12.5,-4.25],[0,0]])
    np.testing.assert_allclose(transform_points(points,"EPSG:4326","EPSG:4326"),points)

def test_invalid_shapes_nonfinite_coordinates_and_crs_are_rejected():
    with pytest.raises(ValueError,match="N×2"):
        transform_points([[1,2,3]],"EPSG:4326","EPSG:3857")
    with pytest.raises(ValueError,match="finite"):
        transform_points([[np.nan,0]],"EPSG:4326","EPSG:3857")
    with pytest.raises(ValueError,match="failed"):
        transform_points([[0,0]],"not-a-real-crs","EPSG:3857")


def test_ellipsoidal_inverse_and_direct_round_trip():
    from transform import geodesic_direct, geodesic_inverse
    start = np.array([[179.9, 0.0], [10.0, 50.0]])
    end = np.array([[-179.9, 0.0], [10.2, 50.1]])
    inverse = geodesic_inverse(start, end)
    assert inverse["distance_metres"][0] == pytest.approx(22263.898, rel=2e-5)
    restored = geodesic_direct(start, inverse["forward_azimuth_degrees"],
                               inverse["distance_metres"])
    np.testing.assert_allclose(restored, end, atol=1e-8)


def test_geodesic_inverse_handles_near_antipodal_points():
    from transform import geodesic_inverse
    result = geodesic_inverse([[0, 0]], [[179.999, 0.001]])
    assert np.isfinite(result["distance_metres"]).all()
    assert 19_000_000 < result["distance_metres"][0] < 21_000_000


def test_ellipsoidal_polygon_area_is_orientation_sensitive_when_signed():
    from transform import geodesic_polygon_area
    ring = [[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]
    forward = geodesic_polygon_area(ring, signed=True)
    reverse = geodesic_polygon_area(ring[::-1], signed=True)
    assert forward["area_square_metres"] == pytest.approx(abs(forward["signed_area_square_metres"]))
    assert forward["perimeter_metres"] > 400_000
    assert forward["signed_area_square_metres"] == pytest.approx(-reverse["signed_area_square_metres"])
    assert forward["area_square_metres"] > 12_000_000_000


def test_geodesic_buffer_crosses_antimeridian_and_has_requested_radius():
    from transform import geodesic_point_buffer, geodesic_inverse
    ring = geodesic_point_buffer((179.8, 0.0), 100_000, vertices=36)
    assert ring.shape == (36, 2)
    assert np.any(ring[:, 0] < 0) and np.any(ring[:, 0] > 0)
    distances = geodesic_inverse(np.repeat([[179.8, 0.0]], len(ring), axis=0), ring)
    np.testing.assert_allclose(distances["distance_metres"], 100_000, atol=1e-6)


def test_geodesic_functions_validate_shapes_units_and_ellipsoid():
    from transform import geodesic_direct, geodesic_inverse, geodesic_point_buffer, geodesic_polygon_area
    with pytest.raises(ValueError, match="matching"):
        geodesic_inverse([[0, 0]], [[1, 1], [2, 2]])
    with pytest.raises(ValueError, match="latitude"):
        geodesic_inverse([[0, 91]], [[1, 1]])
    with pytest.raises(ValueError, match="distance"):
        geodesic_direct([[0, 0]], 0, -1)
    with pytest.raises(ValueError, match="vertices"):
        geodesic_point_buffer((0, 0), 100, vertices=4)
    with pytest.raises(ValueError, match="at least three"):
        geodesic_polygon_area([[0, 0], [1, 1], [0, 0]])
    with pytest.raises(ValueError, match="ellipsoid"):
        geodesic_point_buffer((0, 0), 100, ellipsoid="not-an-ellipsoid")
