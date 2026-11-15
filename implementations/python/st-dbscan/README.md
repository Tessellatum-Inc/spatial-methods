# Spatiotemporal DBSCAN

Dependency-free O(n²) reference implementation of ST-DBSCAN.

## Run

~~~bash
python -m pip install -r requirements.txt
python -m pytest -q
~~~

## Contract

- Spatial distance is Euclidean in the caller's projected coordinate space.
- A neighbour must satisfy both the inclusive spatial and temporal thresholds.
- Timestamps are numeric and use one consistent unit; spatial coordinates
  likewise use one consistent linear unit.
- min_samples includes the focal point.
- Ambiguous border points are assigned to the first cluster reached in input
  order. This makes the implementation deterministic for a fixed input order.
- The simple all-pairs neighbourhood search is intended for teaching and
  modest data, not large spatiotemporal indexes.

This implementation is ST-DBSCAN, not T-DBSCAN: it uses one spatial and one
temporal threshold, not a separate density threshold for each dimension.
See the [canonical note](../../../algorithms/statistics/st-dbscan.md) and
[source verification record](../../../catalog/verification/st-dbscan.md).
