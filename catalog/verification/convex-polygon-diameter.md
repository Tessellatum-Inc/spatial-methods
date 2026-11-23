# Source verification — convex-polygon diameter

## Identity

The rotating-calipers technique for convex polygon diameter is part of the classical computational-geometry treatment of antipodal pairs. Shamos (1978), *Computational Geometry*, PhD thesis, Yale University, is an early foundational source for computational geometry and rotating-caliper methods.

## Implemented scope

A monotone-chain convex hull is constructed from a finite point set, followed by a rotating-calipers antipodal-pair sweep to return one farthest pair and its Euclidean distance. The hull phase is O(n log n), and the sweep is O(h), where h is the hull size.

## Limitations

This does not compute a minimum-area oriented bounding rectangle or other rotating-calipers outputs. Floating-point cross products and a small comparison tolerance are used; exact predicates and robust degeneracy handling are not claimed. Coordinates must be planar Cartesian values in a common linear unit.

## Rights

The algorithm is independently implemented from its mathematical description; no source code or figures are reproduced.
