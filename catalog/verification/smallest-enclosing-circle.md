# Source verification — smallest enclosing circle

## Identity

Welzl, E. (1991). “Smallest enclosing disks (balls and ellipsoids).” In *New Results and New Trends in Computer Science*, Lecture Notes in Computer Science 555, 359–370.

## Implemented scope

The teaching package implements a randomized iterative incremental construction for a finite planar point set. When a point falls outside the current circle, nested passes promote it and one or two earlier points to boundary constraints. The defining circle is a singleton, a two-point diameter circle, or a three-point circumcircle; collinear triples reduce to the farthest pair. Collinear triples reduce to the farthest pair.

## Limitations

The implementation uses floating-point containment tolerance and a local seeded random permutation. It is intended for modest teaching inputs, not a robust exact-arithmetic library or adversarially large data. Coordinates must be projected planar coordinates.

## Rights

The published algorithm is paraphrased; no source code or figures are reproduced.
