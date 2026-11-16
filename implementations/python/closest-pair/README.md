# Closest pair of planar points

A dependency-free divide-and-conquer implementation returns the two closest input occurrences and their Euclidean distance. Duplicate coordinates are valid and return zero distance.

## Run

```bash
python -m pytest -q
```

## Method and complexity

Points are sorted once by x and y. Each recursive call splits the x-order in half, partitions the y-order by original point identity, solves both halves, and checks a constant-size neighbourhood in the y-ordered strip around the split. The recurrence is O(n log n) time with O(n log n) auxiliary allocation in this straightforward implementation.

The implementation requires at least two finite 2D points. It uses floating-point squared distances and ordinary comparisons; it is a teaching baseline rather than an exact-predicate kernel. The return pair is ordered by original input index, and equal-distance candidates in the split strip are also inspected so the original-index tie rule is applied consistently.
