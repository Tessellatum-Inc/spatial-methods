# Pole of inaccessibility and Polylabel

The pole of inaccessibility of a polygon is the interior point whose distance to the polygon boundary is maximised. The radius of the largest circle centred at that point and contained by the polygon is the maximum boundary clearance. This is a useful label anchor for irregular polygons because a centroid may lie outside a concave polygon or inside a hole.

## Signed distance objective

For a candidate point p, define its signed distance as the minimum Euclidean distance to any exterior or hole boundary segment, positive when p lies in the polygon and negative otherwise. The objective is to maximise this signed distance.

## Best-first subdivision

Polylabel-style search covers the polygon bounding box with square cells. For a cell with centre c and half-size h, the signed distance d(c) gives a lower bound and

[
d_{max}=d(c)+hsqrt{2}
]

is an upper bound on the best possible value anywhere in that cell. A max-priority queue visits cells in descending upper-bound order. Cells whose upper bound cannot improve the current best by more than the requested precision are pruned; the others are split into four children.

The implementation returns the best point, its boundary clearance, and the number of cells examined. Its precision parameter is an absolute coordinate-unit tolerance, not a guarantee of exact optimality.

## Polygon holes and assumptions

The signed-distance test excludes points inside hole rings and measures clearance to both exterior and hole boundaries. Inputs must form a valid planar polygon with one exterior ring and optional interior rings. Self-intersections, invalid ring topology and geographic/geodesic coordinates are not repaired automatically.

## Distinguish related problems

- **Pole of inaccessibility:** maximise distance to the polygon boundary; Polylabel is an approximate best-first method.
- **Largest empty circle among sites:** maximise distance to a set of sites subject to a specified domain; this may have different constraints and candidate structure.
- **Smallest enclosing circle:** minimise the radius of a circle containing a point set; this is the opposite geometric objective.

## Reproduction

See the [geometry metrics package](../../implementations/python/geometry-metrics/README.md), [verification note](../../catalog/verification/pole-of-inaccessibility-polylabel.md) and [interactive geometry lab](../../notebooks/geometry-metrics-lab.ipynb).
