# Trajectory processing and sequence similarity

## Scope

This record covers a compact subset of trajectory processing methods: stay-point detection, spatial Douglas–Peucker simplification, dynamic time warping (DTW), and longest common subsequence (LCSS) similarity. These methods operate on ordered observations, not on an inferred road network.

## Methods and contracts

- **Stay-point detection:** A candidate interval begins at an observation and expands while subsequent observations remain within a spatial threshold of that first observation. It is emitted when elapsed time reaches a minimum duration. The returned representative location is the arithmetic centroid. This start-anchored rule is intentionally distinct from a maximum-diameter cluster or density-based detector.
- **Douglas–Peucker:** Recursively retain the point with greatest perpendicular distance from the current segment when that distance exceeds the tolerance. The implementation uses an explicit stack to avoid recursion-depth failures and returns original row indices.
- **DTW:** Dynamic programming minimises cumulative Euclidean point distance over monotone alignments. A Sakoe–Chiba index window restricts allowable warping. The returned value is cumulative cost, not a length-normalised score.
- **LCSS:** Dynamic programming finds the longest order-preserving subsequence of point pairs within a spatial tolerance and optional index window. The score is LCSS divided by the shorter sequence length.

## Coordinate and sampling assumptions

All coordinates must already be in one projected planar coordinate system and common linear unit. The methods do not convert longitude/latitude, correct GPS error, infer sampling intervals, or account for map-matching uncertainty. Timestamps must be numeric and non-decreasing.

## Complexity

Douglas–Peucker is O(n log n) on typical inputs and O(n²) in the worst case. DTW and LCSS require O(mn) time and O(n) memory with rolling dynamic-programming rows. Stay-point detection is O(n) for fixed dimensionality.

## Not covered

SQUISH, STTrace, opening-window and TD-TR compression; route recovery; trajectory imputation; TRACLUS; T-DBSCAN; continuous Fréchet distance; trajectory databases and indexed similarity search require separate records and tests.
