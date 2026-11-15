# Source verification — smallest enclosing circle

## Identity

Welzl, E. (1991). “Smallest enclosing disks (balls and ellipsoids).” In *New Results and New Trends in Computer Science*, Lecture Notes in Computer Science 555, 359–370.

## Implemented scope

The teaching package implements a randomized iterative incremental construction for a finite planar point set. When a point falls outside the current circle, nested passes promote it and one or two earlier points to boundary constraints. The defining circle is a singleton, a two-point diameter circle, or a three-point circumcircle; collinear triples reduce to the farthest pair. Collinear triples reduce to the farthest pair.

## Limitations

The implementation uses a local seeded random permutation, iterative nested boundary constraints, a local-coordinate circumcircle formula and ULP-scaled containment tolerance. It is intended for teaching, not a robust exact-arithmetic library. Coordinates must be projected planar coordinates.

## Differential and stress tests

- 250 seeded random point sets (up to 10 points) compared against an independent oracle that enumerates singleton, diameter and circumcircle candidates.
- 5,000-point containment stress test to exercise the iterative implementation without recursion-depth dependence.
- Equilateral-triangle fixtures translated to large coordinate offsets and scaled from 1e-9 to unit size, checking circumcentre and radius stability within representable floating-point precision.

## Rights

The published algorithm is paraphrased; no source code or figures are reproduced.
