import numpy as np
import pytest
from scipy.spatial import QhullError

from voronoi_delaunay import build_tessellations


def test_three_non_collinear_sites_produce_one_delaunay_triangle():
    result = build_tessellations([(0, 0), (2, 0), (0, 2)])
    assert result.delaunay.simplices.shape == (1, 3)
    assert result.voronoi.vertices.shape == (1, 2)


def test_square_produces_two_triangles_and_one_voronoi_vertex():
    result = build_tessellations([(0, 0), (2, 0), (2, 2), (0, 2)])
    assert result.delaunay.simplices.shape == (2, 3)
    assert result.voronoi.vertices.shape == (1, 2)


def test_interior_site_is_included_in_triangulation():
    result = build_tessellations([(0, 0), (4, 0), (4, 4), (0, 4), (2, 2)])
    used = set(result.delaunay.simplices.ravel().tolist())
    assert used == set(range(5))


def test_voronoi_vertex_is_equidistant_from_at_least_three_sites():
    points = [(0, 0), (2, 0), (0, 2)]
    result = build_tessellations(points)
    vertex = result.voronoi.vertices[0]
    distances = np.linalg.norm(result.points - vertex, axis=1)
    assert np.max(distances) - np.min(distances) < 1e-10


def test_delaunay_triangles_obey_empty_circumcircle_property():
    points = np.array([(0, 0), (4, 0), (4, 4), (0, 4), (2, 1), (1, 3)], dtype=float)
    result = build_tessellations(points)
    for simplex in result.delaunay.simplices:
        a, b, c = result.points[simplex]
        matrix = 2 * np.array([b - a, c - a])
        rhs = np.array([b @ b - a @ a, c @ c - a @ a])
        centre = np.linalg.solve(matrix, rhs)
        radius2 = np.sum((centre - a) ** 2)
        distances2 = np.sum((result.points - centre) ** 2, axis=1)
        outside = np.ones(len(points), dtype=bool)
        outside[simplex] = False
        assert np.all(distances2[outside] >= radius2 - 1e-9)


def test_duplicate_sites_are_rejected():
    with pytest.raises(ValueError, match="duplicate"):
        build_tessellations([(0, 0), (1, 0), (0, 1), (0, 0)])


def test_collinear_sites_are_rejected():
    with pytest.raises(ValueError, match="collinear"):
        build_tessellations([(0, 0), (1, 1), (2, 2), (3, 3)])


def test_too_few_sites_are_rejected():
    with pytest.raises(ValueError, match="at least three"):
        build_tessellations([(0, 0), (1, 0)])


def test_wrong_coordinate_shape_is_rejected():
    with pytest.raises(ValueError, match="n-by-2"):
        build_tessellations([(0, 0, 0), (1, 0, 0), (0, 1, 0)])


def test_non_finite_sites_are_rejected():
    with pytest.raises(ValueError, match="finite"):
        build_tessellations([(0, 0), (1, 0), (0, float("nan"))])


def test_returned_site_array_is_read_only():
    result = build_tessellations([(0, 0), (1, 0), (0, 1)])
    with pytest.raises(ValueError):
        result.points[0, 0] = 99


def test_alpha_shape_right_triangle_circumradius_threshold():
    from voronoi_delaunay import build_alpha_shape
    points = [(0, 0), (2, 0), (0, 2)]
    excluded = build_alpha_shape(points, max_circumradius=1.0)
    assert excluded.triangles == ()
    assert excluded.boundary_edges == ()
    included = build_alpha_shape(points, max_circumradius=np.sqrt(2))
    assert len(included.triangles) == 1
    assert len(included.boundary_edges) == 3


def test_alpha_shape_square_removes_internal_delaunay_diagonal():
    from voronoi_delaunay import build_alpha_shape
    result = build_alpha_shape(
        [(0, 0), (2, 0), (2, 2), (0, 2)], max_circumradius=np.sqrt(2)
    )
    assert len(result.triangles) == 2
    assert len(result.boundary_edges) == 4
    assert all(tuple(sorted(edge)) != tuple(sorted((0, 2)))
               for edge in result.boundary_edges)


def test_alpha_shape_boundary_edges_have_one_incident_retained_triangle():
    from collections import Counter
    from voronoi_delaunay import build_alpha_shape
    result = build_alpha_shape(
        [(0, 0), (4, 0), (4, 4), (0, 4), (2, 1), (1, 3)],
        max_circumradius=3.0,
    )
    counts = Counter(
        tuple(sorted(edge))
        for triangle in result.triangles
        for edge in ((triangle[0], triangle[1]),
                     (triangle[1], triangle[2]),
                     (triangle[2], triangle[0]))
    )
    assert {tuple(sorted(e)) for e in result.boundary_edges} == {
        edge for edge, count in counts.items() if count == 1
    }
    assert all(count in (1, 2) for count in counts.values())


def test_alpha_shape_matches_independent_circumradius_filter():
    import random
    from voronoi_delaunay import build_alpha_shape
    rng = random.Random(20261115)
    points = np.array(
        [(rng.uniform(-5, 5), rng.uniform(-5, 5)) for _ in range(25)]
    )
    threshold = 2.25
    result = build_alpha_shape(points, max_circumradius=threshold)
    expected = set()
    for simplex in result.triangles:
        a, b, c = points[list(simplex)]
        side_a = np.linalg.norm(b-c)
        side_b = np.linalg.norm(a-c)
        side_c = np.linalg.norm(a-b)
        twice_area = abs((b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0]))
        independent_radius = side_a*side_b*side_c/(2*twice_area)
        assert independent_radius <= threshold + 1e-12
        expected.add(tuple(sorted(simplex)))
    all_expected = set()
    reference = build_tessellations(points).delaunay
    for simplex in reference.simplices:
        a, b, c = points[simplex]
        twice_area = abs((b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0]))
        radius = (np.linalg.norm(b-c)*np.linalg.norm(a-c)
                  * np.linalg.norm(a-b)/(2*twice_area))
        if radius <= threshold:
            all_expected.add(tuple(sorted(int(v) for v in simplex)))
    assert expected == all_expected


@pytest.mark.parametrize("bad", [0, -1, float("nan"), float("inf")])
def test_alpha_shape_rejects_invalid_radius(bad):
    from voronoi_delaunay import build_alpha_shape
    with pytest.raises(ValueError, match="max_circumradius"):
        build_alpha_shape([(0, 0), (1, 0), (0, 1)], max_circumradius=bad)


def test_alpha_shape_rejects_invalid_sites():
    from voronoi_delaunay import build_alpha_shape
    with pytest.raises(ValueError, match="collinear"):
        build_alpha_shape([(0, 0), (1, 1), (2, 2)], max_circumradius=2)
