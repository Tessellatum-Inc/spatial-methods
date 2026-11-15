# Source verification — smallest enclosing circle

## Identity

Welzl, E. (1991). “Smallest enclosing disks (balls and ellipsoids).” In *New Results and New Trends in Computer Science*, Lecture Notes in Computer Science 555, 359–370.

## Implemented scope

The teaching package implements randomized Welzl recursion for a finite planar point set. The boundary set contains at most three points; one and two point cases use a singleton and diameter circle, while three non-collinear points use a circumcircle. Collinear triples reduce to the farthest pair.

## Limitations

The implementation uses floating-point containment tolerance and a local seeded random permutation. It is intended for modest teaching inputs, not a robust exact-arithmetic library or adversarially large data. Coordinates must be projected planar coordinates.

## Rights

The published algorithm is paraphrased; no source code or figures are reproduced.
