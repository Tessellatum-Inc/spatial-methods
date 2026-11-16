import pytest
from st_dbscan import st_dbscan


def test_separates_spatial_clusters_and_marks_noise():
    points = [(0,0),(0.2,0),(10,10),(10.2,10),(5,5)]
    times = [0,1,0,1,100]
    result = st_dbscan(points, times, eps_spatial=1, eps_temporal=2, min_samples=2)
    assert result["labels"] == (0,0,1,1,-1)
    assert result["n_clusters"] == 2


def test_both_spatial_and_temporal_constraints_must_hold():
    points = [(0,0),(0.1,0),(0.2,0)]
    times = [0,10,20]
    result = st_dbscan(points, times, eps_spatial=1, eps_temporal=2, min_samples=2)
    assert result["labels"] == (-1,-1,-1)


def test_temporal_and_spatial_thresholds_are_inclusive():
    result = st_dbscan([(0,0),(1,0)], [0,5], eps_spatial=1,
                       eps_temporal=5, min_samples=2)
    assert result["labels"] == (0,0)


def test_ambiguous_border_is_assigned_to_first_reached_cluster():
    points = [(0,),(0.1,),(0.2,),(1.1,),(2,),(2.1,),(2.2,)]
    times = [0]*len(points)
    result = st_dbscan(points, times, eps_spatial=0.95, eps_temporal=0, min_samples=4)
    assert result["labels"][3] == 0
    assert not result["core_points"][3]
    assert not result["core_points"][3]
    assert result["labels"][:3] == (0,0,0)
    assert result["labels"][4:] == (1,1,1)


def test_zero_thresholds_allow_exact_duplicate_space_time_points():
    result = st_dbscan([(1,2),(1,2),(2,2)], [7,7,7],
                       eps_spatial=0, eps_temporal=0, min_samples=2)
    assert result["labels"] == (0,0,-1)


@pytest.mark.parametrize("bad", [-1, float("nan"), float("inf")])
def test_invalid_spatial_and_temporal_thresholds_are_rejected(bad):
    with pytest.raises(ValueError):
        st_dbscan([(0,0),(1,1)], [0,1], eps_spatial=bad, eps_temporal=1)
    with pytest.raises(ValueError):
        st_dbscan([(0,0),(1,1)], [0,1], eps_spatial=1, eps_temporal=bad)


@pytest.mark.parametrize("bad", [0, -1, 1.5, True])
def test_invalid_min_samples_is_rejected(bad):
    with pytest.raises(ValueError, match="min_samples"):
        st_dbscan([(0,0)], [0], eps_spatial=1, eps_temporal=1, min_samples=bad)


def test_invalid_coordinate_and_timestamp_shapes_are_rejected():
    with pytest.raises(ValueError, match="consistent"):
        st_dbscan([(0,0),(1,)], [0,1], eps_spatial=1, eps_temporal=1)
    with pytest.raises(ValueError, match="timestamps"):
        st_dbscan([(0,0),(1,1)], [0], eps_spatial=1, eps_temporal=1)
    with pytest.raises(ValueError, match="finite"):
        st_dbscan([(0,float("nan"))], [0], eps_spatial=1, eps_temporal=1)
