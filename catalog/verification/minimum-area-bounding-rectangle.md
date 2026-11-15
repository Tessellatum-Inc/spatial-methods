# Source verification — minimum-area oriented bounding rectangle

## Identity

The minimum-area enclosing rectangle of a planar point set is a standard convex-geometry problem. Its support directions can be restricted to convex-hull edge orientations.

## Implemented scope

The teaching baseline constructs a monotone-chain convex hull, tests each hull-edge orientation, projects all hull vertices onto the edge direction and its normal, and selects the smallest area rectangle. This is O(h²) after hull construction.

## Limitations

This is not the optimal linear-time rotating-calipers rectangle algorithm. It uses floating-point projections and is intended as a transparent, testable baseline. It does not solve geodesic or ellipsoidal bounding problems.

## Rights

The mathematical method is independently implemented and paraphrased; no source code or figures are reproduced.
