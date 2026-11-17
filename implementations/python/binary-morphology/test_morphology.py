import numpy as np
import pytest

from morphology import (
    closing, connected_components, dilation, erosion, geodesic_reconstruction,
    hit_or_miss, opening,
)


def test_erosion_and_dilation_use_false_outside_boundary():
    image = np.ones((3, 3), dtype=bool)
    cross = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], dtype=bool)
    assert erosion(image, cross).sum() == 1
    point = np.zeros((5, 5), dtype=bool)
    point[2, 2] = True
    assert dilation(point, cross).sum() == 5


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
    assert np.array_equal(erosion(a, s)[1:-1, 1:-1], (~dilation(~a, s))[1:-1, 1:-1])


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

def test_zhang_suen_thinning_reduces_solid_region_and_is_idempotent():
    from morphology import zhang_suen_thinning
    image = np.zeros((11, 11), bool)
    image[2:9, 2:9] = True
    skeleton = zhang_suen_thinning(image)
    assert skeleton.sum() < image.sum()
    assert np.all(skeleton <= image)
    assert np.array_equal(zhang_suen_thinning(skeleton), skeleton)
    assert connected_components(skeleton, 8)[1].tolist() == [int(skeleton.sum())]


def test_zhang_suen_preserves_one_pixel_line_and_rejects_iteration_limit():
    from morphology import zhang_suen_thinning
    line = np.zeros((5, 9), bool)
    line[2, 1:8] = True
    assert np.array_equal(zhang_suen_thinning(line), line)
    block = np.ones((7, 7), bool)
    with pytest.raises(RuntimeError):
        zhang_suen_thinning(block, max_iterations=1)
    with pytest.raises(ValueError):
        zhang_suen_thinning(block, max_iterations=-1)

def test_two_pass_components_matches_independent_flood_fill_on_seeded_masks():
    from morphology import two_pass_connected_components
    rng = np.random.default_rng(2026)
    for connectivity in (4, 8):
        for _ in range(20):
            image = rng.random((13, 17)) > .68
            labels_a, sizes_a = connected_components(image, connectivity)
            labels_b, sizes_b = two_pass_connected_components(image, connectivity)
            assert sizes_b.tolist() == sizes_a.tolist()
            assert np.array_equal(labels_b > 0, labels_a > 0)
            # Compare component equivalence, not arbitrary numeric label IDs.
            for y1, x1 in zip(*np.nonzero(image)):
                for y2, x2 in zip(*np.nonzero(image)):
                    assert (labels_a[y1, x1] == labels_a[y2, x2]) == (
                        labels_b[y1, x1] == labels_b[y2, x2]
                    )


def test_two_pass_components_handles_empty_and_single_component_masks():
    from morphology import two_pass_connected_components
    labels, sizes = two_pass_connected_components(np.zeros((4, 5), bool))
    assert labels.sum() == 0
    assert sizes.size == 0
    image = np.ones((4, 5), bool)
    labels, sizes = two_pass_connected_components(image, 4)
    assert np.unique(labels).tolist() == [1]
    assert sizes.tolist() == [20]

def test_binary_granulometry_is_monotone_and_conserves_pattern_spectrum():
    from morphology import binary_granulometry
    image = np.zeros((15, 15), bool)
    image[3:12, 3:12] = True
    image[6, 6] = False
    result = binary_granulometry(image, [0, 1, 2])
    areas, spectrum = result["areas"], result["pattern_spectrum"]
    assert result["radii"].tolist() == [0, 1, 2]
    assert areas[0] == int(image.sum())
    assert np.all(np.diff(areas) <= 0)
    assert np.all(spectrum >= 0)
    assert int(spectrum.sum()) == int(areas[0] - areas[-1])
    assert areas[-1] < areas[0]


def test_binary_granulometry_rejects_empty_duplicate_or_invalid_radii():
    from morphology import binary_granulometry
    image = np.ones((7, 7), bool)
    for radii in ([], [1, 1], [2, 1], [-1], [1.5], [True]):
        with pytest.raises(ValueError):
            binary_granulometry(image, radii)
