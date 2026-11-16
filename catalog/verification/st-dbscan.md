# Source verification — spatiotemporal DBSCAN

## Identity and bibliography

The method is ST-DBSCAN (spatiotemporal DBSCAN), described by Birant, D. and
Kut, A. (2007), “ST-DBSCAN: An algorithm for clustering spatial-temporal data,”
*Data & Knowledge Engineering*, 60(1), 208–221. The method requires a point to
satisfy spatial and temporal neighbourhood conditions. Confirm publisher
metadata against the primary journal record before marking bibliography
verification complete.

## Technical claims

This repository baseline defines a neighbour by the conjunction of an
inclusive Euclidean spatial-distance threshold and an inclusive absolute
time-difference threshold. The min_samples count includes the focal point.
Core-point expansion follows DBSCAN. Ambiguous border points are assigned to
the first cluster reached in input order, so the result is deterministic for
a fixed input order.

## Implementation and reproduction

The dependency-free implementation is in
`implementations/python/st-dbscan`. Tests cover separate space-time clusters,
noise, the conjunction of thresholds, inclusive boundaries, deterministic
border assignment, exact duplicate points, and invalid controls.

This is an O(n²) all-pairs teaching implementation. It does not implement
T-DBSCAN, trajectory similarity, geodesic distance, adaptive thresholds,
spatial indexing or distributed clustering. CI must pass before recording
the package as verified.

## Rights

The implementation, tests and explanation are original repository work.
No third-party source code or figures are reproduced. Source-entry identity,
bibliography and rights review remain separate from implementation status.
