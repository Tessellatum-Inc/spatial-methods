# Trajectory processing and similarity

This package provides small-data, dependency-light reference implementations for four trajectory operations:

- start-anchored stay-point detection using a spatial radius and minimum elapsed duration;
- planar Douglas–Peucker simplification with retained source-row indices;
- Euclidean dynamic time warping (DTW), optionally constrained by a Sakoe–Chiba index window;
- longest common subsequence (LCSS) similarity with spatial tolerance and optional index-window constraint.

## Coordinate and time contract

Coordinates must be projected planar x/y values in common linear units. The package does not reproject longitude/latitude, interpret a CRS, or handle geodesic distances. Timestamps are finite numeric values in one consistent unit, normally seconds, and must be non-decreasing.

## Important limitations

Stay points are accumulated relative to the first point in each candidate interval; the detector does not guarantee that every pair in a reported stay lies within the threshold. Douglas–Peucker is a spatial-only simplifier. DTW and LCSS operate on ordered point sequences and use Euclidean point distance; neither is a map-matching or route-recovery algorithm. The implementation does not include SQUISH, STTrace, opening-window or TD-TR compression, trajectory imputation, TRACLUS, T-DBSCAN, continuous Fréchet distance, or indexed similarity search.

All methods are deterministic and intended for teaching, reproducible analysis, and small-to-medium trajectories. DTW and LCSS use dynamic programming with O(mn) time and O(n) memory.
