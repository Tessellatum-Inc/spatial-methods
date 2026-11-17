# Point-region octree

A dependency-free 3D bucket point-region octree for point insertion, inclusive
axis-aligned range queries, and exact Euclidean k-nearest-neighbour queries.

## Contract

- Root extent is a closed 3D box; inserted points outside it are rejected.
- Mid-plane ties go to the high-side child independently on x, y and z.
- Range queries are inclusive and return original insertion IDs.
- kNN returns `(point_id, point, distance)`, sorted by distance then ID.
- Duplicate coordinates are retained. Leaves may exceed capacity at max depth
  or when floating-point midpoint subdivision can no longer progress.
- Query points for kNN need not lie inside the root extent.

## Complexity and limitations

For well-distributed data, insertion and range queries visit a small fraction
of the cells; pathological clustering can degrade to linear scans. The
implementation is a static-root teaching index with incremental insertion,
not a disk-backed octree, loose octree, adaptive mesh, or moving-object index.
The exact kNN traversal prunes cells using the Euclidean lower bound from the
query to each cell's bounding box; worst-case query cost remains O(n).

Run tests with `python -m pytest -q` from this directory.


## Dynamic deletion and rebuilding

`delete(point_id)` lazily removes an insertion ID while preserving all later IDs. Range and kNN queries ignore inactive records. When tombstones reach both the configured capacity and 30% of all inserted records, the tree is rebuilt from active points; `rebuild()` is also available explicitly. IDs are never reused. This is a global rebuild policy, not local subtree balancing or a disk-page update strategy.
