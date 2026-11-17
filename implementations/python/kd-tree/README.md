# k-d tree: exact 2D spatial queries

This directory contains a static two-dimensional k-d tree and a scapegoat-style dynamic k-d tree for planar Euclidean nearest-neighbour, k-nearest-neighbour, radius and orthogonal range queries.

## Run it

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

## Example

```python
from kd_tree import KDTree2D

tree = KDTree2D([(0, 0), (2, 0), (4, 0), (1, 3)])
print(tree.nearest((3.2, 0.5)))
print(tree.k_nearest((3.2, 0.5), 3))
print(tree.range_query((0, 0), (2, 2)))
print(tree.radius_query((0, 0), 2.5))
```

## Query contracts

- `nearest(query)` returns `(original_index, squared_distance)`, or `None` for an empty tree.
- `k_nearest(query, k)` returns up to k pairs `(original_index, squared_distance)`, ordered by distance and then original index. It returns an empty list for k=0 or an empty tree, and rejects negative or non-integer k.
- `range_query(minimum, maximum)` returns all original indices inside the inclusive rectangle defined by its lower-left and upper-right corners. Results are sorted by original index.
- `radius_query(query, radius)` returns all original indices within the inclusive Euclidean radius, sorted by original index.

All inputs must contain finite 2D coordinates. The tree uses deterministic median partitioning, selects the axis with greatest spread at each node, and preserves original input indices.

## Complexity and limitations

Construction is balanced by median selection, although this straightforward implementation repeatedly sorts recursive partitions and allocates slices. Nearest and k-nearest queries use split-plane branch-and-bound; range queries recurse only into half-spaces intersecting the query interval. Query work is data-dependent and can approach a full scan in unfavourable distributions. Both trees are planar 2D Euclidean indexes. The original KDTree2D is static; DynamicKDTree2D supports insert/delete with subtree rebuilding, but does not provide worst-case logarithmic update guarantees or geodesic distance.

## Verification

Tests compare nearest-neighbour results with a brute-force oracle, range queries with an independent rectangle filter, radius queries with a brute-force distance filter, and k-nearest results with a full-sort oracle over seeded point clouds. Fixtures include empty input, duplicates, distance ties, split-plane cases, degenerate rectangle windows, k=0, k larger than the dataset, invalid coordinates and clustered/anisotropic data.

See the [step-by-step implementation walkthrough](implementation-walkthrough.md) and the [k-d tree lesson](../../../algorithms/indexing/kd-tree-nearest-neighbour.md).



## Dynamic index

`DynamicKDTree2D` assigns stable monotonically increasing IDs on insertion.
Deletion is lazy; a subtree is rebuilt when its inactive fraction exceeds
the configured threshold. Insertions also rebuild a subtree when one child
becomes too large. The alpha parameter must lie strictly between 0.5 and 1.
All query methods ignore deleted records and preserve stable-ID tie-breaking.

This is a small dynamic reference implementation, not a disk-backed R-tree
or a worst-case logarithmic update guarantee. A rebuild costs O(m log² m)
for a subtree of m active points in this implementation; adversarial update
sequences can trigger repeated rebuilds. Query performance remains
distribution-dependent.
