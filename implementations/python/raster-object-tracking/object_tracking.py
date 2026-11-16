"""Overlap-based identity association for labeled raster objects."""
from __future__ import annotations
import numpy as np


def track_labeled_objects(label_frames, *, min_iou=0.0, min_overlap=1):
    """Associate positive labels across consecutive, equal-shaped frames.

    The method records every qualifying overlap edge (including split/merge
    edges) and assigns persistent IDs through a deterministic greedy one-to-one
    maximum-IoU continuation. Non-overlapping objects start new tracks.
    Background is label 0. Frames may be 2-D or 3-D integer label arrays.
    """
    frames = [np.asarray(frame) for frame in label_frames]
    if len(frames) < 1:
        raise ValueError("at least one label frame is required")
    shape = frames[0].shape
    if len(shape) not in (2, 3) or any(n < 1 for n in shape):
        raise ValueError("frames must be non-empty 2-D or 3-D arrays")
    for frame in frames:
        if frame.shape != shape or frame.dtype.kind not in "iu":
            raise ValueError("all frames must have the same shape and integer labels")
        if np.any(frame < 0):
            raise ValueError("labels must be non-negative; zero is background")
    if not np.isfinite(min_iou) or not 0 <= min_iou <= 1:
        raise ValueError("min_iou must be between zero and one")
    if not isinstance(min_overlap, (int, np.integer)) or min_overlap < 1:
        raise ValueError("min_overlap must be a positive integer")

    labels_by_frame = [np.unique(f[f > 0]).astype(int).tolist() for f in frames]
    sizes = [{int(k): int(v) for k, v in zip(*np.unique(f[f > 0], return_counts=True))}
             for f in frames]
    centroids = []
    for f, labels in zip(frames, labels_by_frame):
        coords = np.indices(f.shape, dtype=float)
        centroids.append({
            label: np.array([coords[d][f == label].mean() for d in range(f.ndim)])
            for label in labels
        })

    nodes = [(t, label) for t, labels in enumerate(labels_by_frame) for label in labels]
    links = []
    track_ids = {}
    next_track = 1
    for label in labels_by_frame[0]:
        track_ids[(0, label)] = next_track
        next_track += 1

    for t in range(len(frames) - 1):
        left, right = frames[t].ravel(), frames[t + 1].ravel()
        both = (left > 0) & (right > 0)
        pairs, intersections = np.unique(
            np.column_stack((left[both], right[both])), axis=0, return_counts=True
        ) if np.any(both) else (np.empty((0, 2), dtype=int), np.empty(0, dtype=int))
        candidates = []
        for (a, b), count in zip(pairs, intersections):
            a, b, count = int(a), int(b), int(count)
            union = sizes[t][a] + sizes[t + 1][b] - count
            iou = count / union
            if count >= min_overlap and iou >= min_iou:
                distance = float(np.linalg.norm(centroids[t][a] - centroids[t + 1][b]))
                candidates.append((a, b, count, iou, distance))
        candidates.sort(key=lambda item: (-item[3], -item[2], item[0], item[1]))
        for a, b, count, iou, distance in candidates:
            links.append({
                "from": (t, a), "to": (t + 1, b),
                "intersection": count, "iou": float(iou),
                "centroid_distance": distance,
            })
        # Greedy one-to-one primary continuations. Secondary overlap edges
        # remain in links and expose split/merge topology.
        used_left, used_right = set(), set()
        primary = []
        for a, b, count, iou, distance in candidates:
            if a not in used_left and b not in used_right:
                used_left.add(a); used_right.add(b)
                primary.append((a, b))
        primary_by_child = {b: a for a, b in primary}
        for b in labels_by_frame[t + 1]:
            parent = primary_by_child.get(b)
            if parent is not None and (t, parent) in track_ids:
                track_ids[(t + 1, b)] = track_ids[(t, parent)]
            else:
                track_ids[(t + 1, b)] = next_track
                next_track += 1

    split_events = []
    merge_events = []
    for t in range(len(frames) - 1):
        outgoing = {}
        incoming = {}
        for edge in links:
            if edge["from"][0] == t:
                outgoing.setdefault(edge["from"], []).append(edge["to"])
                incoming.setdefault(edge["to"], []).append(edge["from"])
        split_events.extend({"time": t, "parent": node, "children": children}
                            for node, children in outgoing.items() if len(children) > 1)
        merge_events.extend({"time": t + 1, "child": node, "parents": parents}
                            for node, parents in incoming.items() if len(parents) > 1)
    return {
        "nodes": nodes, "links": links, "track_ids": track_ids,
        "split_events": split_events, "merge_events": merge_events,
    }
