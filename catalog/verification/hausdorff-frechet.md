# Source verification — Hausdorff and Fréchet distances

## Identity

Hausdorff distance is a set-distance metric: the directed version is the maximum distance from elements in one set to their nearest element in the other; the symmetric version is the maximum of the two directed values. The discrete Fréchet distance measures similarity between ordered vertex sequences using a max-min dynamic program. It is not the continuous Fréchet distance.

- Eiter & Mannila (1994), *Computing Discrete Fréchet Distance*, Technical Report CD-TR 94/64, Vienna University of Technology.
- Alt & Godau (1995), “Computing the Fréchet distance between two polygonal curves,” *International Journal of Computational Geometry & Applications*, 5(1–2), 75–91.

## Implemented scope

The previously overlooked `implementations/python/geometry-metrics/` package is a direct package mapping for the canonical record. Its README describes:
- Directed and symmetric Hausdorff distance for finite point sets (vertex/sample-point distance, not continuous line/segment geometry).
- Discrete Fréchet for ordered vertex sequences, O(mn) time and O(n) rolling-row memory.
- Continuous Fréchet decision by Alt–Godau free-space reachability and distance approximation by bisection to absolute tolerance.
- Additional related geometry metrics, each with separate limitations.

The package is dependency-free and has tests. A package name/README match does not substitute for CI evidence or validation of every algorithm variant.

## Limits

Planar Euclidean coordinates must share a CRS and linear units. Hausdorff here treats the input as sampled points. Discrete Fréchet is not continuous Fréchet. The implementation's continuous decision/approximation component is a separate method and must be evaluated independently.

## Rights

Bibliographic metadata and original explanations only. No source paper text, figures or data are reproduced.