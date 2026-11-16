# Exact 2D ball tree

A dependency-free static Euclidean index supporting exact k-nearest-neighbour
and inclusive radius queries. Each node stores a ball enclosing every record
in its subtree. Queries use the lower bound max(0, distance(query, centre) -
radius) to prune subtrees safely.

## Run
~~~bash
python -m pytest -q
~~~

## Contract
- Input records are finite planar coordinates; duplicate coordinates remain
  distinct records.
- kNN results are (input_index, distance), ordered by distance then input
  index. If k exceeds the data size, all records are returned.
- Radius queries include records exactly on the radius.
- The tree is static and two-dimensional; no alternate metrics, updates or
  disk-backed pages are provided.

Construction uses deterministic median splits along the widest coordinate
range and computes an enclosing ball at each node. Query cost is data-dependent:
well-separated balls prune effectively, but worst-case search remains linear.
This is an exact teaching index, not a uniformly logarithmic query guarantee.
