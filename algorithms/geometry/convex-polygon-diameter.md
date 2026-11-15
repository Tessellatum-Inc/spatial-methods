# Convex-polygon diameter by rotating calipers

The diameter of a finite planar point set is the maximum Euclidean distance between any pair of its points. A farthest pair lies on the convex hull, so interior points can be discarded before the diameter search.

## Convex hull and antipodal pairs

The package first constructs a strict counter-clockwise monotone-chain convex hull. Rotating calipers then sweeps the hull edges and tracks the vertex farthest from each current edge. These opposite support points define antipodal pairs; the farthest pair among the candidates is the diameter.

The hull construction costs O(n log n). The antipodal sweep is linear in the number of hull vertices, giving O(n log n) overall.

## Scope and cautions

This implementation returns the two endpoint coordinates and their Euclidean separation. It accepts an arbitrary finite point cloud and constructs its hull internally. Degenerate inputs with zero, one or two unique points are handled explicitly. The code uses floating-point cross products and a small comparison tolerance; it is a teaching implementation, not an exact-predicate geometry kernel.

The diameter is not the minimum-area oriented bounding rectangle. A full rotating-calipers rectangle routine is a separate method and remains outside this implementation.

## Reproduction

See the [geometry metrics package](../../implementations/python/geometry-metrics/README.md), including tests against brute-force pairwise distances on seeded point clouds, and the [interactive lab](../../notebooks/geometry-metrics-lab.ipynb).
