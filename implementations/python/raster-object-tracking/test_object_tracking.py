import numpy as np
import pytest
from object_tracking import track_labeled_objects


def test_persistent_object_keeps_track_id_under_translation_with_overlap():
    a = np.zeros((6, 6), dtype=int); a[1:4, 1:4] = 1
    b = np.zeros((6, 6), dtype=int); b[2:5, 1:4] = 7
    out = track_labeled_objects([a, b])
    assert out["track_ids"][(0, 1)] == out["track_ids"][(1, 7)]
    assert len(out["links"]) == 1
    assert out["links"][0]["iou"] == pytest.approx(2 / 4)


def test_split_is_retained_as_two_association_edges():
    a = np.zeros((5, 6), dtype=int); a[1:4, 1:5] = 1
    b = np.zeros_like(a); b[1:4, 1:3] = 4; b[1:4, 3:5] = 9
    out = track_labeled_objects([a, b])
    assert len(out["links"]) == 2
    assert len(out["split_events"]) == 1
    assert out["split_events"][0]["parent"] == (0, 1)
    assert len({out["track_ids"][(1, 4)], out["track_ids"][(1, 9)]}) == 2


def test_merge_is_retained_and_primary_id_is_deterministic():
    a = np.zeros((5, 6), dtype=int); a[1:4, 1:3] = 2; a[1:4, 3:5] = 5
    b = np.zeros_like(a); b[1:4, 1:5] = 8
    out = track_labeled_objects([a, b])
    assert len(out["links"]) == 2
    assert len(out["merge_events"]) == 1
    assert out["track_ids"][(1, 8)] == out["track_ids"][(0, 2)]


def test_no_overlap_starts_a_new_track():
    a = np.zeros((4, 4), dtype=int); a[0, 0] = 1
    b = np.zeros_like(a); b[3, 3] = 1
    out = track_labeled_objects([a, b])
    assert out["links"] == []
    assert out["track_ids"][(0, 1)] != out["track_ids"][(1, 1)]


def test_validation():
    with pytest.raises(ValueError):
        track_labeled_objects([])
    with pytest.raises(ValueError):
        track_labeled_objects([np.zeros((2, 2), dtype=int), np.zeros((3, 2), dtype=int)])
    with pytest.raises(ValueError):
        track_labeled_objects([np.array([[-1]], dtype=int)])
    with pytest.raises(ValueError):
        track_labeled_objects([np.zeros((2, 2), dtype=int)], min_iou=1.5)
