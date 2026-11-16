import numpy as np
import pytest
from flows import cluster_od_flows, line_flow_kde, flow_density_hotspots


def test_dbscan_separates_two_od_corridors_and_noise():
    origins = np.array([[0.,0.],[.1,0.],[0.,.1],[10.,10.],[10.1,10.],[10.,10.1],[50.,50.]])
    destinations = origins + np.array([5.,0.])
    labels = cluster_od_flows(origins, destinations, eps=.5, min_samples=2)
    assert labels[0] == labels[1] == labels[2]
    assert labels[3] == labels[4] == labels[5]
    assert labels[0] != labels[3]
    assert labels[6] == -1


def test_line_kde_is_symmetric_about_a_horizontal_flow():
    x = np.linspace(-2., 12., 57)
    y = np.linspace(-4., 4., 33)
    z = line_flow_kde([[0.,0.]], [[10.,0.]], x, y,
                      bandwidth=.8, quadrature_order=24)
    np.testing.assert_allclose(z, z[::-1], atol=1e-14)
    assert z.max() > z[0, 0]


def test_line_kde_scales_linearly_with_flow_weight():
    x = np.linspace(-1., 5., 21)
    y = np.linspace(-2., 2., 17)
    a = line_flow_kde([[0.,0.]], [[4.,0.]], x, y, bandwidth=.7)
    b = line_flow_kde([[0.,0.]], [[4.,0.]], x, y, bandwidth=.7, weights=[3.])
    np.testing.assert_allclose(b, 3*a, rtol=1e-13, atol=1e-15)


def test_zero_length_flow_reduces_to_point_gaussian_kernel():
    x, y = np.array([0.]), np.array([0.])
    z = line_flow_kde([[0.,0.]], [[0.,0.]], x, y,
                      bandwidth=2., quadrature_order=4)
    assert z[0,0] == pytest.approx(1/(2*np.pi*4))


def test_hotspot_extraction_finds_single_peak():
    z = np.zeros((7,7))
    z[3,3] = 10.
    result = flow_density_hotspots(z, quantile=.99, neighbourhood_size=3)
    np.testing.assert_array_equal(result["rows_cols"], [[3,3]])
    assert result["mask"][3,3]


def test_flow_analysis_rejects_invalid_inputs():
    with pytest.raises(ValueError, match="matching"):
        cluster_od_flows([[0.,0.]], [[1.,1.],[2.,2.]], eps=1.)
    with pytest.raises(ValueError, match="bandwidth"):
        line_flow_kde([[0.,0.]], [[1.,1.]], [0.], [0.], bandwidth=0.)
    with pytest.raises(ValueError, match="odd"):
        flow_density_hotspots(np.ones((3,3)), neighbourhood_size=2)


def test_functional_regions_cluster_reciprocal_od_flow_blocks():
    from flows import functional_regions_from_flows
    matrix = np.zeros((8, 8))
    for block in (range(4), range(4, 8)):
        for i in block:
            for j in block:
                if i != j:
                    matrix[i, j] = 10.
    matrix[3, 4] = matrix[4, 3] = .1
    regions = functional_regions_from_flows(matrix, seed=7)
    assert {frozenset(x) for x in regions} == {frozenset(range(4)), frozenset(range(4, 8))}


def test_functional_regions_respect_contiguity_edges():
    from flows import functional_regions_from_flows
    matrix = np.ones((4, 4)) - np.eye(4)
    adjacency = [[1], [0, 2], [1, 3], [2]]
    regions = functional_regions_from_flows(matrix, adjacency=adjacency, seed=3)
    assert set().union(*regions) == set(range(4))


def test_functional_regions_validate_matrix_and_adjacency():
    from flows import functional_regions_from_flows
    with pytest.raises(ValueError, match="square"):
        functional_regions_from_flows([[0., 1.]])
    with pytest.raises(ValueError, match="adjacency"):
        functional_regions_from_flows(np.zeros((2, 2)), adjacency=[[1]])
