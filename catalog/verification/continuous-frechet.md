# Source verification — continuous Fréchet distance

## Identity and bibliography

The continuous Fréchet distance for polygonal curves is treated by Alt, H. and Godau, M. (1995), “Computing the Fréchet distance between two polygonal curves,” *International Journal of Computational Geometry & Applications*, 5(1–2), 75–91.

## Implemented scope

The geometry-metrics package implements the free-space decision procedure on the parameter-space cell grid and approximates the minimum leash length by bisection. The decision routine propagates reachable intervals along cell boundaries. The distance routine returns an upper bound within the requested absolute tolerance, subject to floating-point arithmetic.

## Verification

Tests include:
- two different samplings of the same segment (continuous distance zero while discrete distance is positive);
- parallel curves with a known unit separation and threshold checks immediately below and at the separation;
- symmetry;
- endpoint lower bounds;
- singleton-curve handling and invalid parameter rejection.

## Limitations

This is a transparent O(mn) time and memory teaching implementation, not an exact symbolic solver or an output-sensitive decision algorithm. It uses planar Euclidean coordinates and floating-point interval calculations. The test suite does not constitute an independent formal proof of the full Alt–Godau algorithm.

## Rights

The implementation is independently written from the mathematical description. No source code, paper text or figures are reproduced.
