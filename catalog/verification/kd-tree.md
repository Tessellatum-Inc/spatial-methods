# Verification record: 2D k-d tree

## Implementation

- **Code:** `implementations/python/kd-tree/kd_tree.py`
- **Tests:** `implementations/python/kd-tree/test_kd_tree.py`
- **Index:** static median-partitioned 2D k-d tree; axis selected by greatest coordinate spread
- **Queries:** exact 1-nearest, exact k-nearest with a bounded max-heap, inclusive orthogonal rectangle reporting
- **Metric:** planar Euclidean distance; returns original input indices
- **Limitations:** static, two-dimensional, no geodesic metric or dynamic updates; worst-case query work can approach a full scan

## Differential verification

- 1-nearest queries are compared with an independent full-scan minimum oracle, including ties and duplicate sites.
- k-nearest queries are compared with an independent full-sort oracle over seeded clouds, including k=0, k larger than n and equal-distance ties.
- Rectangle queries are compared with an independent point-by-point inclusive window filter over seeded integer-coordinate clouds, including zero-width and zero-height windows and duplicate coordinates.
- Invalid coordinate dimensions, non-finite coordinates, invalid rectangle bounds and invalid k values are rejected.

The test cases are committed. Their execution status must be checked in GitHub Actions for the latest commit; the presence of tests is not evidence of a passing run.
