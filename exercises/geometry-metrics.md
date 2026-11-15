# Exercise — compare geometries and enclose a point set

## Task

Use the geometry-metrics package to compare two digitised routes and compute a minimum enclosing circle for a set of facility or observation points.

1. Compute directed and symmetric Hausdorff distances for two point samples.
2. Reverse the vertex order of one route. Explain why Hausdorff distance is unchanged while discrete Fréchet distance can change.
3. Add intermediate vertices to one route without changing its underlying straight segments. Observe how the discrete distance can respond to sampling.
4. Compute the smallest enclosing circle and verify that every input point lies inside it.
5. Repeat with a different seed and discuss numerical reproducibility.
6. For a concave polygon with a hole, compute its pole of inaccessibility at two precision settings and compare the returned boundary clearance and cell count.
7. Compute the minimum-area oriented bounding rectangle for an oblique point cloud and compare its area with the axis-aligned bounding box.

## Deliverables

- A short table of the three distance values.
- A plot of both route samples, the enclosing circle and the polygon pole-of-inaccessibility point and the oriented bounding rectangle.
- A paragraph explaining why sampled-point Hausdorff, discrete Fréchet and continuous-curve distance are different objects.

## Constraints

Use projected planar coordinates. State the units. Do not describe the Welzl teaching implementation as exact arithmetic or a production-scale robust geometry engine.
