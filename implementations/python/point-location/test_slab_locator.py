import pytest

from slab_locator import BOUNDARY, SlabPointLocator


def rect(x1, y1, x2, y2):
    return [(x1, y1), (x2, y1), (x2, y2), (x1, y2), (x1, y1)]


def test_locates_inside_outside_and_boundary():
    locator = SlabPointLocator({"park": [rect(0, 0, 4, 4)]})
    assert locator.locate(2, 2) == "park"
    assert locator.locate(5, 2) is None
    assert locator.locate(2, 0) == BOUNDARY


def test_adjacent_faces_are_distinguished_on_either_side_of_shared_edge():
    locator = SlabPointLocator({
        "west": [rect(0, 0, 2, 2)],
        "east": [rect(2, 0, 4, 2)],
    })
    assert locator.locate(1, 1) == "west"
    assert locator.locate(3, 1) == "east"
    assert locator.locate(2, 1) == BOUNDARY


def test_hole_is_outside_face():
    shell = rect(0, 0, 6, 6)
    hole = rect(2, 2, 4, 4)
    locator = SlabPointLocator({"parcel": [shell, hole]})
    assert locator.locate(1, 1) == "parcel"
    assert locator.locate(3, 3) is None


def test_vertex_and_vertical_edge_queries_use_event_line_policy():
    locator = SlabPointLocator({"face": [rect(0, 0, 3, 3)]})
    assert locator.locate(0, 1) == BOUNDARY
    assert locator.locate(0, 0) == BOUNDARY
    assert locator.locate(0, 4) is None


def test_queries_outside_x_extent_are_outside():
    locator = SlabPointLocator({"face": [rect(0, 0, 3, 3)]})
    assert locator.locate(-1, 1) is None
    assert locator.locate(4, 1) is None


def test_invalid_open_ring_rejected():
    with pytest.raises(ValueError):
        SlabPointLocator({"bad": [[(0, 0), (1, 0), (1, 1), (0, 1)]]})


def test_non_finite_query_rejected():
    locator = SlabPointLocator({"face": [rect(0, 0, 3, 3)]})
    with pytest.raises(ValueError):
        locator.locate(float("nan"), 1)


def test_overlapping_polygons_rejected():
    with pytest.raises(ValueError):
        SlabPointLocator({
            "a": [rect(0, 0, 3, 3)],
            "b": [rect(2, 2, 4, 4)],
        })



def test_seeded_random_disjoint_faces_against_rectangle_oracle():
    """Exercise slab ordering and queries across many x-event intervals."""
    import random

    rng = random.Random(20261115)
    faces = {}
    bounds = {}
    # Place each rectangle in its own 10-by-10 cell, so interiors cannot
    # overlap while widths, heights and offsets vary independently.
    for row in range(6):
        for column in range(6):
            face_id = f"f-{row}-{column}"
            x0 = column * 10 + rng.uniform(0.1, 2.0)
            y0 = row * 10 + rng.uniform(0.1, 2.0)
            x1 = column * 10 + rng.uniform(6.0, 9.8)
            y1 = row * 10 + rng.uniform(6.0, 9.8)
            faces[face_id] = [rect(x0, y0, x1, y1)]
            bounds[face_id] = (x0, y0, x1, y1)

    locator = SlabPointLocator(faces)
    for _ in range(2000):
        x = rng.uniform(-5, 65)
        y = rng.uniform(-5, 65)
        expected = None
        for face_id, (x0, y0, x1, y1) in bounds.items():
            if x0 < x < x1 and y0 < y < y1:
                expected = face_id
                break
            if (x0 <= x <= x1 and y0 <= y <= y1
                    and (x == x0 or x == x1 or y == y0 or y == y1)):
                expected = BOUNDARY
                break
        assert locator.locate(x, y) == expected


def test_seeded_adjacent_rectangle_grid_preserves_shared_boundaries():
    """Every shared vertical seam is boundary, not assigned to either face."""
    faces = {}
    for row in range(5):
        for column in range(5):
            faces[f"{row}-{column}"] = [
                rect(column * 2, row * 2, (column + 1) * 2, (row + 1) * 2)
            ]
    locator = SlabPointLocator(faces)
    for row in range(5):
        for column in range(5):
            assert locator.locate(column * 2 + 1, row * 2 + 1) == f"{row}-{column}"
            assert locator.locate(column * 2 + 2, row * 2 + 1) == BOUNDARY
            assert locator.locate(column * 2 + 1, row * 2 + 2) == BOUNDARY


def test_event_line_epsilon_classifies_near_vertical_boundary_consistently():
    locator = SlabPointLocator({"face": [rect(0, 0, 3, 3)]}, epsilon=1e-8)
    assert locator.locate(1e-9, 1.5) == BOUNDARY
    assert locator.locate(-1e-9, 1.5) == BOUNDARY
    assert locator.locate(1e-9, 4.0) is None


def test_event_line_epsilon_handles_both_neighbouring_event_coordinates():
    locator = SlabPointLocator({
        "west": [rect(0, 0, 2, 2)],
        "east": [rect(2, 0, 4, 2)],
    }, epsilon=1e-6)
    assert locator.locate(2 - 5e-7, 1) == BOUNDARY
    assert locator.locate(2 + 5e-7, 1) == BOUNDARY
    assert locator.locate(2 + 2e-6, 1) == "east"
