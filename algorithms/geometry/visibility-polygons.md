# Visibility polygons: what can a viewpoint see?

Given a viewpoint inside a simple polygonal environment, its visibility polygon is the subset of the environment that can be connected to the viewpoint by a segment that stays inside the polygon. Reflex vertices create occlusion boundaries; convex polygons have no such occlusion when the viewpoint is interior.

## Reference algorithm: angular ray casting

A transparent reference method casts rays toward every boundary vertex and at small angular offsets on either side. Each ray is intersected with every polygon edge; the nearest intersection is retained. Sorting these hits by angle constructs the visible boundary.

For n polygon vertices this uses O(n) rays and O(n) edge checks per ray, plus O(n log n) sorting: O(n² log n) time. It is simple to inspect and useful for small scenes, but is not the optimal algorithm.

A rotational sweep can achieve O(n log n) time by sorting vertex events by angle and maintaining the polygon edges that intersect the sweep ray in an ordered active structure. The nearest active edge determines the visibility boundary between events.

## Input and numerical assumptions

The current reference implementation requires a simple polygon without holes and a viewpoint strictly inside it. It assumes finite planar coordinates. The angular perturbation is a numerical device for resolving visibility discontinuities around vertex directions; it is not a robust exact-predicate solution. The implementation does not validate polygon simplicity, handle holes, or guarantee stable results for nearly coincident geometry.

## GIS and graphics applications

- Line-of-sight and local visibility within building footprints or enclosed sites.
- Visibility constraints in facility siting and surveillance analysis.
- Robot navigation and motion planning among polygonal obstacles.
- Viewshed primitives for vector-based environments.

For large or high-assurance workloads, use a robust rotational-sweep implementation and explicit topology validation.

## Implementation and verification

The dependency-free reference code and tests are in [implementations/python/visibility-polygon](../../implementations/python/visibility-polygon/README.md). Tests include a convex rectangle, an L-shaped concave polygon with a known occluded region, ring-closure invariance and invalid inputs.

## References

- O'Rourke, J. (1987). *Art Gallery Theorems and Algorithms*. Oxford University Press.
- Ghosh, S. K. (2007). *Visibility Algorithms in the Plane*. Cambridge University Press.
