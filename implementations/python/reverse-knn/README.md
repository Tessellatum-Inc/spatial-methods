# Reverse k-nearest-neighbour queries

The function reverse_k_nearest_neighbors(data_points, query_points, k) returns
data record indices for which each query is among the k nearest external
locations.

The implementation builds the repository's static 2D k-d tree once. For each
query/data pair it radius-queries around the data point and counts only
indexed records strictly closer than the query. Fewer than k strictly closer
records means the query qualifies. Equal-distance ties are inclusive.

Run tests:

    PYTHONPATH=../kd-tree python -m pytest -q

Seeded tests compare the indexed implementation with an independent quadratic
oracle, including duplicate coordinates, ties, empty inputs and k > n.

## Scope

This is an exact planar Euclidean teaching implementation, not a specialised
reverse-nearest-neighbour index. It does not support geographic distances,
weighted metrics, dynamic updates or high-dimensional data. Worst-case work
can approach quadratic time per query when radius searches return many records.
