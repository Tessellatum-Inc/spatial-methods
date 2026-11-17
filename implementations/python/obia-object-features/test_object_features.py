import numpy as np
import pytest
from object_features import summarize_objects


def test_single_object_geometry_and_spectral_stats():
    image = np.array([[1., 2.], [3., 4.]])
    result = summarize_objects(image, np.zeros((2, 2), dtype=int))
    obj = result["objects"][0]
    assert obj["area"] == 4
    assert obj["centroid"] == (0.5, 0.5)
    assert obj["bbox"] == (0, 0, 2, 2)
    assert obj["perimeter_4"] == 8
    assert obj["band_mean"] == (2.5,)


def test_two_objects_adjacency_and_multiband_means():
    image = np.dstack([np.ones((2, 3)), np.full((2, 3), 5.)])
    labels = np.array([[1, 1, 2], [1, 2, 2]])
    result = summarize_objects(image, labels)
    assert [x["label"] for x in result["objects"]] == [1, 2]
    assert result["adjacency"] == [{"labels": (1, 2), "shared_edges": 2}]
    assert result["objects"][0]["band_mean"] == (1., 5.)


def test_negative_labels_are_ignored():
    result = summarize_objects(np.ones((2, 2)), np.array([[0, -1], [0, -1]]))
    assert [x["label"] for x in result["objects"]] == [0]
    assert result["objects"][0]["area"] == 2


def test_nan_values_are_omitted_from_band_statistics():
    image = np.array([[1., np.nan], [3., 4.]])
    obj = summarize_objects(image, np.zeros((2, 2), dtype=int))["objects"][0]
    assert obj["area"] == 4
    assert obj["band_mean"] == (pytest.approx(8/3),)


def test_all_nodata_band_reports_nan_statistics():
    image = np.full((2, 2), np.nan)
    obj = summarize_objects(image, np.zeros((2, 2), dtype=int))["objects"][0]
    assert np.isnan(obj["band_mean"][0])


def test_shape_and_label_validation():
    with pytest.raises(ValueError):
        summarize_objects(np.ones((2, 2)), np.ones((3, 3), dtype=int))
    with pytest.raises(ValueError):
        summarize_objects(np.ones((2, 2)), np.ones((2, 2), dtype=float))
