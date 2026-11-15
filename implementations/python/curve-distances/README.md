# Discrete Hausdorff and Frechet distances

Dependency-free implementations for finite planar point sequences.

## Run

```bash
python -m pytest -q
```

## Methods and interpretation

- `directed_hausdorff(A, B)`: maximum, over vertices in A, of the distance to the nearest vertex in B.
- `hausdorff_distance(A, B)`: maximum of the two directed distances. This is a discrete point-set/vertex-sequence Hausdorff distance.
- `discrete_frechet_distance(A, B)`: dynamic programming over monotone, endpoint-preserving couplings of the two vertex sequences. It respects sequence order and is often useful for comparing sampled trajectories.

For m and n vertices, the Hausdorff routines take O(mn) time; the discrete Frechet routine takes O(mn) time and O(n) auxiliary memory.

## Important distinction

These routines compare supplied vertices. They do not compute the continuous Hausdorff or continuous Frechet distance between polygonal curves, where closest points may lie in segment interiors. Sampling more densely can improve an approximation in suitable settings, but does not turn these routines into exact continuous algorithms. Coordinates must use a common Cartesian metric coordinate system when the result is interpreted as a distance.

Inputs must be non-empty sequences of finite 2D points. Invalid inputs raise `ValueError`.

## Verification

Tests include directed-versus-symmetric Hausdorff examples, translation and symmetry properties, known Frechet alignments, the inequality that discrete Frechet distance is at least the discrete Hausdorff distance, invalid-input handling, and 250 seeded randomized comparisons against a separately written full-matrix Frechet recurrence.

## References

- Alt, H. and Godau, M. (1995). Computing the Frechet distance between two polygonal curves. *International Journal of Computational Geometry & Applications*, 5(1–2), 75–91.
- Eiter, T. and Mannila, H. (1994). Computing discrete Frechet distance. Technical Report CD-TR 94/64, TU Vienna.
- Huttenlocher, D. P., Klanderman, G. A. and Rucklidge, W. J. (1993). Comparing images using the Hausdorff distance. *IEEE Transactions on Pattern Analysis and Machine Intelligence*, 15(9), 850–863.
