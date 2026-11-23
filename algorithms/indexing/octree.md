# Point-region octree

A point-region octree recursively partitions a three-dimensional box into
eight axis-aligned children. It is the direct 3D analogue of a point-region
quadtree, with one binary subdivision decision per coordinate.

## Operations

- **Insert:** route a point to one child at each internal node. A midpoint tie
  is assigned to the high side, making the child assignment unique.
- **Range query:** reject cells whose boxes do not intersect the query box;
  inspect points only in intersecting leaves.
- **Exact k-nearest neighbours:** visit cells in increasing lower-bound
  distance from the query to the cell box. Stop when the next lower bound is
  strictly greater than the current kth candidate distance.

## Practical details

Closed child boxes overlap on split planes for safe query pruning, but each
point is stored in exactly one child. Duplicate points remain distinct records.
A depth cap and midpoint-collapse check prevent unbounded subdivision for
coincident points and extreme floating-point coordinates.

The accompanying implementation is an in-memory 3D point index, not an
adaptive volumetric mesh or a production database index. Its kNN operation
uses Euclidean distance and deterministic insertion-order tie-breaking.


## Dynamic updates

The implementation supports lazy deletion by stable insertion ID and periodic whole-tree rebuilding when tombstones exceed the configured threshold. Manual rebuilding is available; insertion IDs remain stable and are not reused. This is a bounded dynamic-update baseline, not a locally rebalanced or disk-backed octree.
