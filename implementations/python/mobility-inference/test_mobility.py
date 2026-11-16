import numpy as np
import pytest
from mobility import detect_staypoints, infer_home_work, activity_space_metrics


def test_staypoint_detection_finds_two_dwell_episodes():
    xy = np.array([[0.,0.],[1.,0.],[.5,.2],[10.,0.],[10.2,.1],[10.,.2]])
    ts = np.array([0.,300.,600.,3600.,3900.,4200.])
    stays = detect_staypoints(xy, ts, radius=2., minimum_duration=500.)
    assert len(stays) == 2
    assert stays[0]["duration"] == 600.
    np.testing.assert_allclose(stays[0]["centroid"], [0.5, 0.0666666667])


def test_home_work_inference_uses_night_and_day_dwell_clusters():
    stays = []
    for start in [21*3600, 22*3600, 23*3600]:
        stays.append({"centroid": np.array([0. + len(stays)*.1, 0.]),
                      "start": start, "duration": 8*3600.})
    for start in [10*3600, 11*3600, 12*3600]:
        stays.append({"centroid": np.array([100. + (len(stays)-3)*.1, 0.]),
                      "start": start, "duration": 7*3600.})
    result = infer_home_work(stays, eps=2., timezone_offset_hours=0)
    np.testing.assert_allclose(result["home"]["location"], [.1,0.])
    np.testing.assert_allclose(result["work"]["location"], [100.1,0.])
    assert result["home"]["visits"] == 3


def test_activity_space_metrics_match_direct_radius_and_triangle_area():
    xy = np.array([[0.,0.],[2.,0.],[0.,2.]])
    result = activity_space_metrics(xy)
    centre = xy.mean(axis=0)
    expected = np.sqrt(np.mean(np.sum((xy-centre)**2, axis=1)))
    assert result["radius_of_gyration"] == pytest.approx(expected)
    assert result["convex_hull_area"] == pytest.approx(2.)


def test_staypoint_and_activity_inputs_are_validated():
    with pytest.raises(ValueError, match="strictly increasing"):
        detect_staypoints([[0.,0.],[1.,1.]], [1.,1.], radius=1., minimum_duration=1.)
    with pytest.raises(ValueError, match="non-empty"):
        activity_space_metrics(np.empty((0,2)))
