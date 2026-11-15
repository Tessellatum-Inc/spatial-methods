# Minimum-area oriented bounding rectangle

An oriented bounding rectangle encloses a planar point set while allowing its axes to rotate. The minimum-area rectangle is the enclosing rectangle with the smallest area. It differs from an axis-aligned bounding box, which is constrained to the coordinate axes.

## Why the convex hull is sufficient

A minimum-area enclosing rectangle has each side supported by the convex hull. Interior points cannot determine an extreme support line, so the algorithm first computes the convex hull and then tests orientations parallel to hull edges.

## Projection method

For a candidate unit edge direction u and its perpendicular v, project each hull vertex p onto both axes:

[
s=pcdot u,qquad t=pcdot v.
]

The rectangle extents are the minimum and maximum s and t values. Its area is the product of the two side lengths. Transform the four projection-space corners back into the original coordinate system and retain the smallest-area candidate.

The current teaching baseline scans every hull vertex for every hull-edge orientation. It is O(h²) after hull construction, not the optimal linear-time rotating-calipers sweep. The separate convex-diameter routine does implement an antipodal rotating-calipers sweep.

## Scope and cautions

The routine returns four counter-clockwise corners, area and the selected edge angle. It handles empty, singleton and collinear point sets. Floating-point projections are used; exact predicates are not claimed. The result is planar and Euclidean, not geodesic.

See the [geometry metrics package](../../implementations/python/geometry-metrics/README.md) and its [interactive lab](../../notebooks/geometry-metrics-lab.ipynb).
