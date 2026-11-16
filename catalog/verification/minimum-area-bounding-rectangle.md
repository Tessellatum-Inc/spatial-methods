# Source verification — minimum-area oriented bounding rectangle

## Identity

The minimum-area enclosing rectangle of a planar point set is a standard convex-geometry problem. Its support directions can be restricted to convex-hull edge orientations.

## Implemented scope

Two implementations are provided. The transparent baseline constructs a monotone-chain convex hull and scans all hull vertices for each hull-edge orientation, costing O(h²). The four-support rotating-calipers implementation advances the extrema along the edge direction and its normal monotonically around the hull, costing O(h) after hull construction. Seeded tests compare the calipers area with the quadratic baseline across 100 random point clouds.

## Limitations

The calipers routine uses floating-point support comparisons and is not an exact-predicate construction. It is tested against the transparent baseline, but this is not a formal proof of numerical robustness for adversarial degeneracies. It does not solve geodesic or ellipsoidal bounding problems.

## Rights

The mathematical method is independently implemented and paraphrased; no source code or figures are reproduced.
