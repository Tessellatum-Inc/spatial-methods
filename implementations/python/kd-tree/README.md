# k-d tree: exact nearest-neighbour teaching implementation

This directory contains a static two-dimensional k-d tree that answers exact nearest-neighbour queries under planar Euclidean distance.

## Run it

Install the dependency and run the tests:

~~~bash
python -m pip install -r requirements.txt
python -m pytest -q
~~~

Example:

~~~python
from kd_tree import KDTree2D

points = [(0, 0), (2, 0), (4, 0), (1, 3)]
tree = KDTree2D(points)

print(tree.nearest((3.2, 0.5)))\nprint(tree.range_query((0, 0), (2, 2)))\nprint(tree.k_nearest((3.2, 0.5), 3))
~~~

`nearest(query)` returns the closest original input index and squared Euclidean distance, or `None` for an empty tree. `range_query(minimum, maximum)` returns all indices inside an inclusive rectangle. `k_nearest(query, k)` returns up to k `(index, squared_distance)` pairs, sorted by distance and then original index. All methods preserve deterministic tie handling.

## What it does

- validates finite 2D coordinates;
- builds a static tree by selecting the axis with the greatest spread at each recursive level;
- splits at the median, using original input index as a deterministic secondary sort key;
- visits the query-side subtree first;
- prunes the far subtree only when its split-plane lower bound is strictly worse than the current best distance;
- preserves original input indices.

## Limits

- Static after construction: no insert, delete or update operations.
- Two dimensions only.
- Planar Euclidean metric only; coordinates must already be in an appropriate Cartesian coordinate system.
- Does not provide dynamic insertion/deletion, range aggregates or all-neighbours-within-radius queries.
- The implementation favours clarity over low allocation overhead and production throughput.
- Worst-case query work can approach a full scan.

## Validation

Tests compare nearest-neighbour results with a brute-force oracle; range queries with an independent rectangle filter; and k-nearest results with a full-sort oracle over seeded clouds. Fixtures cover empty inputs, duplicates, equal-distance ties, split-plane queries, degenerate windows, k=0, k larger than the dataset, invalid coordinates and clustered/anisotropic data.

Read the [step-by-step implementation walkthrough](implementation-walkthrough.md) and the [k-d tree lesson](../../../algorithms/indexing/kd-tree-nearest-neighbour.md).
