import math
import pytest
from point_patterns import nearest_neighbor_distances, nearest_neighbor_cdf, ripley_k_translation, pair_correlation_from_k

def test_nearest_neighbor_distances_for_square():
    points=[(0,0),(1,0),(1,1),(0,1)]
    assert nearest_neighbor_distances(points)==pytest.approx([1,1,1,1])
    assert nearest_neighbor_cdf(points,[0.5,1,2])==pytest.approx([0,1,1])

def test_translation_k_zero_below_nearest_pair_and_monotone():
    points=[(2,2),(8,2),(2,8),(8,8)]
    radii=[1,6,9]
    values=ripley_k_translation(points,(0,0,10,10),radii)
    assert values[0]==0
    assert values[1] < values[2]
    assert all(v>=0 for v in values)

def test_k_translation_matches_hand_calculation_without_edge_loss():
    points=[(4,4),(6,4)]
    # For displacement (2,0), overlap fraction is 0.8; both ordered pairs count.
    result=ripley_k_translation(points,(0,0,10,10),[2])
    assert result[0]==pytest.approx(100/0.8)

def test_pair_correlation_from_poisson_reference_curve():
    radii=[1,2,3,4]
    k=[math.pi*r*r for r in radii]
    g=pair_correlation_from_k(radii,k)
    assert g[1]==pytest.approx(1.0,abs=0.2)
    assert g[2]==pytest.approx(1.0,abs=0.2)

def test_rejects_invalid_window_and_radii():
    with pytest.raises(ValueError):
        ripley_k_translation([(0,0),(1,1)],(0,0,0,1),[1])
    with pytest.raises(ValueError):
        nearest_neighbor_cdf([(0,0),(1,1)],[-1])


def test_inhomogeneous_k_translation_uses_pointwise_intensities_and_ordered_pairs():
    from point_patterns import ripley_k_inhomogeneous_translation
    points = [(4, 4), (6, 4)]
    # Rectangle overlap is 8*10=80; both ordered pairs contribute.
    got = ripley_k_inhomogeneous_translation(points, (0, 0, 10, 10), [1.9, 2.0],
                                              [0.02, 0.04])
    expected = 2.0 / (0.02 * 0.04 * 80.0)
    assert got == pytest.approx([0.0, expected])


def test_inhomogeneous_k_constant_intensity_matches_direct_formula():
    from point_patterns import ripley_k_inhomogeneous_translation
    points = [(2, 2), (5, 2), (2, 7)]
    lam = [0.03, 0.03, 0.03]
    got = ripley_k_inhomogeneous_translation(points, (0, 0, 10, 10), [3.0], lam)[0]
    expected = 0.0
    for i, (x, y) in enumerate(points):
        for j, (a, b) in enumerate(points):
            if i == j:
                continue
            overlap = (10 - abs(x-a)) * (10 - abs(y-b))
            if math.hypot(x-a, y-b) <= 3.0:
                expected += 1.0 / (lam[i] * lam[j] * overlap)
    assert got == pytest.approx(expected)


def test_inhomogeneous_k_rejects_invalid_intensity_and_count():
    from point_patterns import ripley_k_inhomogeneous_translation
    points = [(1, 1), (2, 2)]
    with pytest.raises(ValueError):
        ripley_k_inhomogeneous_translation(points, (0, 0, 5, 5), [1], [0.1])
    with pytest.raises(ValueError):
        ripley_k_inhomogeneous_translation(points, (0, 0, 5, 5), [1], [0.1, 0.0])
    with pytest.raises(ValueError):
        ripley_k_inhomogeneous_translation(points, (0, 0, 5, 5), [1], [float("nan"), 0.1])
