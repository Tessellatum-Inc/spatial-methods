import pytest

from proximity_graphs import (
    beta_skeleton,
    delaunay_filtered_gabriel_graph,
    delaunay_filtered_rng,
    delaunay_euclidean_mst,
    euclidean_mst,
    euclidean_mst_prim,
    gabriel_graph,
    relative_neighborhood_graph,
    yao_graph,
    yao_graph_kdtree,
)


SQUARE = [(0, 0), (1, 0), (1, 1), (0, 1)]


def test_gabriel_graph_open_disk_convention_keeps_square_diagonal_ties():
    edges = gabriel_graph(SQUARE)
    # The other square corners lie on the diameter-circle boundary, not inside it.
    assert len(edges) == 6
    assert (0, 1) in edges and (0, 3) in edges
    assert (0, 2) in edges


def test_rng_is_subset_of_gabriel_graph_for_fixture():
    gabriel = set(gabriel_graph(SQUARE))
    rng = set(relative_neighborhood_graph(SQUARE))
    assert rng <= gabriel


def test_rng_blocks_long_edge_with_intermediate_point():
    points = [(0, 0), (2, 0), (1, 0.1)]
    assert (0, 1) not in relative_neighborhood_graph(points)


def test_mst_has_n_minus_one_edges_and_connects_points():
    points = [(0, 0), (2, 0), (2, 2), (0, 2)]
    edges = euclidean_mst(points)
    assert len(edges) == len(points) - 1
    assert sum(edge[2] for edge in edges) == pytest.approx(6.0)


def test_mst_empty_and_singleton():
    assert euclidean_mst([]) == []
    assert euclidean_mst([(1, 2)]) == []


@pytest.mark.parametrize("function", [
    gabriel_graph, relative_neighborhood_graph, euclidean_mst
])
def test_duplicate_points_rejected(function):
    with pytest.raises(ValueError):
        function([(0, 0), (0, 0)])


@pytest.mark.parametrize("function", [
    gabriel_graph, relative_neighborhood_graph, euclidean_mst
])
def test_non_finite_points_rejected(function):
    with pytest.raises(ValueError):
        function([(0, 0), (1, float("inf"))])


def test_beta_skeleton_endpoints_match_gabriel_and_rng_definitions():
    assert beta_skeleton(SQUARE, 1.0) == gabriel_graph(SQUARE)
    assert beta_skeleton(SQUARE, 2.0) == relative_neighborhood_graph(SQUARE)


def test_beta_skeleton_rejects_out_of_scope_beta():
    with pytest.raises(ValueError):
        beta_skeleton(SQUARE, 2.5)


def test_yao_graph_returns_valid_undirected_edges():
    points = [(0, 0), (2, 0), (2, 2), (0, 2), (1, 1)]
    edges = yao_graph(points, cones=4)
    assert edges
    assert all(i < j and 0 <= i < len(points) and 0 <= j < len(points)
               for i, j in edges)
    assert edges == sorted(set(edges))


def test_yao_graph_rejects_invalid_cone_count():
    with pytest.raises(ValueError):
        yao_graph(SQUARE, cones=2)


GENERAL_POSITION = [(0, 0), (4, 0), (5, 3), (2, 5), (-1, 3), (1, 2)]


def test_delaunay_filtered_gabriel_matches_all_pairs_on_general_position_fixture():
    assert delaunay_filtered_gabriel_graph(GENERAL_POSITION) == gabriel_graph(GENERAL_POSITION)


def test_delaunay_filtered_rng_matches_all_pairs_on_general_position_fixture():
    assert delaunay_filtered_rng(GENERAL_POSITION) == relative_neighborhood_graph(GENERAL_POSITION)


@pytest.mark.parametrize("function", [delaunay_filtered_gabriel_graph, delaunay_filtered_rng])
def test_delaunay_filtered_variants_reject_collinear_sites(function):
    with pytest.raises(ValueError, match="collinear"):
        function([(0, 0), (1, 1), (2, 2), (3, 3)])


@pytest.mark.parametrize("function", [delaunay_filtered_gabriel_graph, delaunay_filtered_rng])
def test_delaunay_filtered_variants_require_three_sites(function):
    with pytest.raises(ValueError, match="three points"):
        function([(0, 0), (1, 0)])



def test_delaunay_euclidean_mst_matches_complete_graph_reference_on_seeded_clouds():
    import random

    rng = random.Random(20261117)
    for size in (2, 3, 4, 8, 15, 40, 100):
        for _ in range(8):
            points = []
            while len(points) < size:
                candidate = (rng.uniform(-100, 100), rng.uniform(-100, 100))
                if candidate not in points:
                    points.append(candidate)
            expected = euclidean_mst(points)
            actual = delaunay_euclidean_mst(points)
            assert len(actual) == size - 1
            assert sum(edge[2] for edge in actual) == pytest.approx(
                sum(edge[2] for edge in expected), rel=1e-11, abs=1e-11
            )
            assert all(i != j and 0 <= i < size and 0 <= j < size
                       for i, j, _weight in actual)


def test_delaunay_euclidean_mst_handles_collinear_and_small_inputs():
    assert delaunay_euclidean_mst([]) == []
    assert delaunay_euclidean_mst([(0, 0)]) == []
    assert delaunay_euclidean_mst([(0, 0), (3, 4)]) == [(0, 1, 5.0)]
    points = [(3, 6), (-2, -4), (0, 0), (1, 2), (-1, -2)]
    result = delaunay_euclidean_mst(points)
    assert len(result) == len(points) - 1
    assert sum(edge[2] for edge in result) == pytest.approx(5 * (5 ** 0.5))


def test_delaunay_euclidean_mst_rejects_duplicate_and_non_finite_sites():
    with pytest.raises(ValueError):
        delaunay_euclidean_mst([(0, 0), (0, 0)])
    with pytest.raises(ValueError):
        delaunay_euclidean_mst([(0, 0), (1, float("nan"))])


def test_kdtree_yao_matches_quadratic_reference_on_seeded_clouds():
    import random
    rng = random.Random(20261115)
    for size in (2, 3, 8, 25, 80):
        for cones in (3, 4, 8, 16):
            points = []
            while len(points) < size:
                candidate = (rng.uniform(-50, 50), rng.uniform(-50, 50))
                if candidate not in points:
                    points.append(candidate)
            for orientation in (0.0, 0.137):
                assert yao_graph_kdtree(points, cones, orientation) == yao_graph(
                    points, cones, orientation
                )


def test_kdtree_yao_handles_empty_singleton_and_tied_directions():
    assert yao_graph_kdtree([]) == []
    assert yao_graph_kdtree([(1, 2)]) == []
    points = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]
    assert yao_graph_kdtree(points, cones=4) == yao_graph(points, cones=4)


def test_kdtree_yao_rejects_invalid_cones_and_coordinates():
    with pytest.raises(ValueError):
        yao_graph_kdtree(SQUARE, cones=True)
    with pytest.raises(ValueError):
        yao_graph_kdtree([(0, 0), (float("nan"), 1)])


def test_prim_mst_matches_kruskal_and_delaunay_on_seeded_clouds():
    import random

    rng = random.Random(20261118)
    for size in (0, 1, 2, 3, 5, 12, 35, 100, 250):
        for _ in range(6):
            points = []
            while len(points) < size:
                candidate = (rng.uniform(-1000, 1000), rng.uniform(-1000, 1000))
                if candidate not in points:
                    points.append(candidate)
            prim = euclidean_mst_prim(points)
            kruskal = euclidean_mst(points)
            assert len(prim) == max(0, size - 1)
            assert sum(edge[2] for edge in prim) == pytest.approx(
                sum(edge[2] for edge in kruskal), rel=1e-11, abs=1e-11
            )
            if size >= 2:
                sparse = delaunay_euclidean_mst(points)
                assert sum(edge[2] for edge in prim) == pytest.approx(
                    sum(edge[2] for edge in sparse), rel=1e-11, abs=1e-11
                )


def test_prim_mst_handles_collinear_and_equal_distance_sites():
    collinear = [(4, 8), (0, 0), (3, 6), (1, 2), (2, 4)]
    result = euclidean_mst_prim(collinear)
    assert len(result) == len(collinear) - 1
    assert sum(edge[2] for edge in result) == pytest.approx(4 * (5 ** 0.5))
    square = euclidean_mst_prim(SQUARE)
    assert len(square) == 3
    assert sum(edge[2] for edge in square) == pytest.approx(3.0)


@pytest.mark.parametrize("points", [
    [(0, 0), (0, 0)],
    [(0, 0), (float("nan"), 1)],
    [(0, 0), (1, float("inf"))],
])
def test_prim_mst_rejects_duplicate_and_non_finite_sites(points):
    with pytest.raises(ValueError):
        euclidean_mst_prim(points)



def _assert_spanning_tree_edges(points, edges):
    """Check a returned edge list is a connected, acyclic spanning tree."""
    n = len(points)
    if n <= 1:
        assert edges == []
        return
    assert len(edges) == n - 1
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for i, j, _weight in edges:
        assert 0 <= i < n and 0 <= j < n and i != j
        ri, rj = find(i), find(j)
        assert ri != rj, "MST output contains a cycle"
        parent[ri] = rj
    assert len({find(i) for i in range(n)}) == 1


def test_three_mst_constructions_match_on_integer_grid_tie_heavy_clouds():
    """Differentially test degeneracies, cocircular ties and repeated distances."""
    import random

    rng = random.Random(20261119)
    for size in range(2, 24):
        for _ in range(8):
            sites = set()
            while len(sites) < size:
                sites.add((rng.randint(-8, 8), rng.randint(-8, 8)))
            points = list(sites)
            reference = euclidean_mst(points)
            prim = euclidean_mst_prim(points)
            delaunay = delaunay_euclidean_mst(points)
            reference_length = sum(edge[2] for edge in reference)
            for result in (prim, delaunay):
                _assert_spanning_tree_edges(points, result)
                assert sum(edge[2] for edge in result) == pytest.approx(
                    reference_length, rel=1e-11, abs=1e-11
                )


def test_delaunay_mst_cocircular_and_symmetric_fixtures():
    fixtures = [
        [(1, 0), (0, 1), (-1, 0), (0, -1)],
        [(3, 4), (4, 3), (-3, 4), (-4, 3), (-3, -4), (-4, -3), (3, -4), (4, -3)],
        [(0, 0), (2, 0), (2, 2), (0, 2), (1, 1), (1, 0), (2, 1), (1, 2), (0, 1)],
    ]
    for points in fixtures:
        reference = euclidean_mst(points)
        actual = delaunay_euclidean_mst(points)
        _assert_spanning_tree_edges(points, actual)
        assert sum(edge[2] for edge in actual) == pytest.approx(
            sum(edge[2] for edge in reference), rel=1e-11, abs=1e-11
        )


def test_indexed_yao_matches_reference_on_integer_lattice_ties():
    import random

    rng = random.Random(20261120)
    for size in (5, 10, 20, 35):
        for _ in range(5):
            sites = set()
            while len(sites) < size:
                sites.add((rng.randint(-5, 5), rng.randint(-5, 5)))
            points = list(sites)
            for cones in (3, 4, 6, 8):
                for orientation in (0.0, 0.25):
                    assert yao_graph_kdtree(points, cones, orientation) == yao_graph(
                        points, cones, orientation
                    )


@pytest.mark.parametrize("beta", [1.0, 1.25, 1.5, 1.75, 2.0])
def test_indexed_delaunay_beta_skeleton_matches_all_pairs_on_general_position(beta):
    from proximity_graphs import delaunay_filtered_beta_skeleton
    import random
    rng = random.Random(20261121)
    for size in (5, 12, 30, 75):
        points = []
        while len(points) < size:
            candidate = (rng.uniform(-30, 30), rng.uniform(-30, 30))
            if candidate not in points:
                points.append(candidate)
        assert delaunay_filtered_beta_skeleton(points, beta) == beta_skeleton(points, beta)


def test_indexed_delaunay_beta_skeleton_rejects_collinear_and_invalid_beta():
    from proximity_graphs import delaunay_filtered_beta_skeleton
    with pytest.raises(ValueError, match="collinear"):
        delaunay_filtered_beta_skeleton([(0, 0), (1, 1), (2, 2)])
    with pytest.raises(ValueError):
        delaunay_filtered_beta_skeleton(SQUARE, True)
    with pytest.raises(ValueError):
        delaunay_filtered_beta_skeleton(SQUARE, 2.1)


def test_indexed_delaunay_beta_skeleton_empty_and_small_inputs_rejected():
    from proximity_graphs import delaunay_filtered_beta_skeleton
    with pytest.raises(ValueError, match="three points"):
        delaunay_filtered_beta_skeleton([])
