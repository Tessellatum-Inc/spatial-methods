# Ball trees for exact spatial nearest-neighbour search

A ball tree recursively partitions a point set. Each node stores a centre and
a radius enclosing every descendant. Unlike a k-d tree's axis-aligned cells,
the node bound is spherical (circular in 2D).

For query point q and a node ball (c,r), every descendant p satisfies

\[
d(q,p) \geq \max(0,d(q,c)-r).
\]

This lower bound supports exact branch-and-bound. For kNN, maintain the current
k best records and stop exploring a node only when its lower bound exceeds the
worst retained distance. For a radius query R, prune when the lower bound is
greater than R. Equality must not be pruned because the API includes boundary
points.

The companion [Python implementation](../../implementations/python/ball-tree/README.md)
uses deterministic median splits along the widest coordinate range. Each node
uses the arithmetic mean of its records as centre and the maximum centre-to-
record distance as its enclosing radius. Leaves retain original input indices,
so duplicate coordinates remain distinct and distance ties are deterministic.

Construction is approximately O(n log n) for balanced median splits, with
additional work to calculate enclosing radii at each level. Query cost depends
on how effectively balls separate the data and is O(n) in the worst case.
The implementation is static, two-dimensional and Euclidean.

Seeded random point clouds compare kNN and radius results against independent
brute-force calculations. Tests include duplicate records, exact-radius
inclusion, ties, empty data, k larger than n and invalid numeric inputs.
