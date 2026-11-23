# Exercise: continuous Fréchet distance

## Goal

Compare two polygonal curves when the geometry between vertices matters. Distinguish the continuous Fréchet distance from the discrete vertex-sequence metric.

## Tasks

1. Compute the discrete and continuous Fréchet distances between the coarse segment `[(0, 0), (2, 0)]` and the same segment sampled at `x = 0, 0.5, 1, 1.5, 2`. Explain why the two answers differ.
2. Use two parallel horizontal curves one unit apart. Check the free-space decision at thresholds 0.99 and 1.0.
3. Reverse one curve. Explain why traversal direction affects the result.
4. Move one endpoint while leaving the rest of the curve unchanged. Identify the endpoint lower bound on the continuous distance.
5. Tighten the bisection tolerance from 1e-3 to 1e-7. Record the change in the returned upper bound and the computation cost.
6. Construct a pair with a sharp bend and explain why comparing only corresponding vertices can miss a continuous bottleneck.

## Interpretation

The decision routine propagates reachable intervals through the Alt–Godau free-space diagram. The distance routine bisects the threshold and returns an upper bound within the requested absolute tolerance, subject to floating-point arithmetic. The implementation is a transparent O(mn) teaching baseline, not an exact symbolic solver.

## References

- Eiter, T. and Mannila, H. (1994). *Computing Discrete Fréchet Distance*. Technical Report CD-TR 94/64.
- Alt, H. and Godau, M. (1995). *Computing the Fréchet distance between two polygonal curves*. International Journal of Computational Geometry & Applications, 5(1–2), 75–91.
- [Hausdorff and Fréchet lesson](../algorithms/geometry/hausdorff-frechet.md)
- [Geometry metrics implementation](../implementations/python/geometry-metrics/README.md)
- [Geometry metrics lab](../notebooks/geometry-metrics-lab.ipynb)
