# Spatiotemporal DBSCAN (ST-DBSCAN)

Stable ID: \`SA-STAT-ST-DBSCAN\` · Draft 0.1 · Source compendium section 2

## Question

Ordinary DBSCAN groups points using spatial proximity alone. For trajectories,
events or observations collected over time, points should often be close in
both space and time before they count as neighbours.

ST-DBSCAN requires both conditions:

\[
d_s(p_i,p_j) \leq \varepsilon_s
\qquad\text{and}\qquad
|t_i-t_j| \leq \varepsilon_t.
\]

The spatial threshold \(\varepsilon_s\) is measured in the coordinate units
supplied by the analyst. The temporal threshold \(\varepsilon_t\) uses the
timestamp unit supplied by the analyst.

## Core points and cluster expansion

As in DBSCAN, the neighbourhood includes the point itself. A point is core
when its spatiotemporal neighbourhood contains at least \`min_samples\` points.
Clusters expand from core points through their neighbours. Points that are
not core and are never reached from a core point are labelled noise.

A border point can be within reach of more than one cluster. This reference
implementation resolves that ambiguity deterministically: the first cluster
reached in input order claims the border point.

## Implementation scope

The repository baseline uses Euclidean distance in the supplied projected
coordinate space and absolute timestamp difference. It uses an all-pairs
neighbour search, so runtime is quadratic in the number of observations.
The implementation supports arbitrary fixed spatial dimension, non-negative
inclusive thresholds, and explicit input validation.

It does not implement T-DBSCAN's separate density thresholds, trajectory
similarity, geographic/geodesic distance, time-varying thresholds, indexed
large-data search, weighted density, or distributed clustering.

## Interpretation

A cluster represents observations that are connected through a chain of
spatiotemporal neighbourhood relations. It does not imply that every pair of
points in a cluster is directly within both thresholds. Threshold choice
strongly affects the result and should be justified in the measurement units.

## Implementation

See [implementations/python/st-dbscan](../../implementations/python/st-dbscan/README.md)
for the tested reference implementation and its deterministic border policy.
The [source verification note](../../catalog/verification/st-dbscan.md)
records the tested scope and remaining review items.

## Reference

Birant, D. and Kut, A. (2007). ST-DBSCAN: An algorithm for clustering
spatial-temporal data. *Data & Knowledge Engineering*, 60(1), 208–221.
