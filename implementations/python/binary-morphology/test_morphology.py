import numpy as np
import pytest

from morphology import (
    closing, connected_components, dilation, erosion, geodesic_reconstruction,
    hit_or_miss, opening,
)


def test_erosion_and_dilation_use_false_outside_boundary():
    image = np.ones((3, 3), dtype=bool)
    cross = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], dtype=bool)
    assert erosion(image, cross).sum() == 5
    assert dilation(np.array([[1]], dtype=bool), cross).sum() == 5


def test_opening_and_closing_are_idempotent():
    image = np.zeros((9, 9), dtype=bool)
    image[2:7, 2:7] = True
    image[0, 0] = True
    structure = np.ones((3, 3), dtype=bool)
    opened = opening(image, structure)
    closed = closing(image, structure)
    assert np.array_equal(opening(opened, structure), opened)
    assert np.array_equal(closing(closed, structure), closed)


def test_morphology_is_monotone_and_dual_under_complement():
    rng = np.random.default_rng(31)
    a = rng.random((12, 13)) > .6
    b = a | (rng.random((12, 13)) > .8)
    s = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], bool)
    assert np.all(erosion(a, s) <= erosion(b, s))
    assert np.all(dilation(a, s) <= dilation(b, s))
    assert np.array_equal(erosion(a, s), ~dilation(~a, s))


def test_hit_or_miss_detects_cross_pattern():
    image = np.zeros((5, 5), bool)
    image[2, 2] = image[1, 2] = image[3, 2] = image[2, 1] = image[2, 3] = True
    fg = np.array([[0,1,0],[1,1,1],[0,1,0]], bool)
    bg = np.array([[1,0,1],[0,0,0],[1,0,1]], bool)
    result = hit_or_miss(image, fg, bg)
    assert result[2, 2]
    assert result.sum() == 1


def test_reconstruction_recovers_only_marker_connected_mask_component():
    mask = np.zeros((7, 9), bool)
    mask[1:6, 1:4] = True
    mask[1:6, 6:8] = True
    marker = np.zeros_like(mask)
    marker[3, 2] = True
    result = geodesic_reconstruction(marker, mask)
    assert np.array_equal(result, mask & (np.indices(mask.shape)[1] < 5))
    with pytest.raises(ValueError):
        geodesic_reconstruction(mask, marker)
    with pytest.raises(RuntimeError):
        geodesic_reconstruction(marker, mask, max_iterations=1)


def test_connected_components_respects_four_and_eight_connectivity():
    image = np.eye(4, dtype=bool)
    labels4, sizes4 = connected_components(image, 4)
    labels8, sizes8 = connected_components(image, 8)
    assert len(sizes4) == 4
    assert sizes4.tolist() == [1, 1, 1, 1]
    assert len(sizes8) == 1
    assert sizes8.tolist() == [4]
    assert labels8[0, 0] == 1


@pytest.mark.parametrize("bad", [np.array([]), np.ones(3), np.ones((2, 2, 2))])
def test_rejects_non_2d_or_empty_images(bad):
    with pytest.raises(ValueError):
        dilation(bad)


def test_rejects_invalid_structures_and_connectivity():
    with pytest.raises(ValueError):
        dilation(np.ones((3, 3)), np.zeros((3, 3)))
    with pytest.raises(ValueError):
        connected_components(np.ones((2, 2)), 6)
