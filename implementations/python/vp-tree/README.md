# Vantage-point tree

An exact, dependency-free Euclidean vantage-point tree for static two-dimensional point data.

## Run

```bash
python -m pytest -q
```

## API

```python
from vp_tree import VantagePointTree

index = VantagePointTree([(0, 0), (4, 0), (0, 3), (2, 2)])
nearest = index.query((1, 1), k=2)
```

The query returns up to k `(point, distance)` pairs sorted by distance. Duplicate input observations are preserved; equal-distance results follow original input order.

## Construction and search

Each node stores a vantage point and partitions the remaining observations by distance from it. A median split keeps the tree balanced even when many distances tie. Query traversal uses the triangle inequality to prune a subtree only when its distance interval cannot improve the current kth-nearest result.

For n points, the median-sort construction is O(n log² n) time and O(n) storage. Query time is data-dependent and can degrade to O(n); no sublinear worst-case guarantee is claimed. The implementation is static, two-dimensional and Euclidean; it does not implement arbitrary metric objects or dynamic insertion/deletion.

## Verification

Tests compare 640 seeded randomized k-nearest queries against a brute-force distance sort and cover duplicates, deterministic tie handling, empty/singleton inputs, k larger than the data size and invalid coordinates.

## References

- Yianilos, P. N. (1993). Data structures and algorithms for nearest neighbor search in general metric spaces. *Proceedings of SODA*, 311–321.
- Chávez, E., Navarro, G., Baeza-Yates, R. and Marroquín, J. L. (2001). Searching in metric spaces. *ACM Computing Surveys*, 33(3), 273–321.
