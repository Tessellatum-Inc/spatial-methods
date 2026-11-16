# Geometry methods

- [Point in polygon](point-in-polygon.md)
- [Polygon intersection](polygon-intersection.md)
- [Segment intersection](segment-intersection.md)
- [Bentley–Ottmann](bentley-ottmann.md)
- [Line simplification](simplification.md)
- [Polygon coverage simplification](coverage-simplification.md)
- [Precision models and snap rounding](precision-models.md)
- [Snap rounding noder](snap-rounding.md)
- [Polygon offsetting](offsetting.md)
- [Proximity graphs](proximity-graphs.md)
- [Planar point location](point-location.md)

These records are part of the broader [algorithm collection](../README.md). The source inventory identifies the methods to investigate; each record documents its own scope, assumptions and evidence.

- [Y-monotone partition and triangulation](monotone-triangulation.md) — start/end/split/merge/regular sweep for simple polygons, followed by stack triangulation of monotone pieces.
- [Ear clipping](ear-clipping.md) — triangulate a simple polygon ring by repeatedly removing an interior ear.

- [Convex decomposition](convex-decomposition.md) — partition a polygon into convex pieces, and distinguish exact from approximate objectives.

- [Minkowski sums](minkowski-sum.md) — combine sets by vector addition; connect convex edge merging, convolution and configuration-space obstacles.

- [Medial axis](medial-axis.md) — locate centres of maximal interior discs through boundary-feature distance.
- [Straight skeleton](straight-skeleton.md) — trace wavefront vertices as polygon edges move inward in parallel.

- [Convex Minkowski-sum implementation](../../implementations/python/minkowski-convex/README.md) — exact rational edge merge, tests and intern walkthrough.

- [Convex decomposition implementation](../../implementations/python/convex-decomposition/README.md) — exact-predicate greedy triangle merging, tests and walkthrough.

- [Delaunay-filtered proximity graphs](../../implementations/python/proximity-graphs/README.md) — sparse candidate filtering for Gabriel and RNG, with documented degeneracy limits.

- [Hausdorff and Fréchet distances](hausdorff-frechet.md) — distinguish finite sampled-set Hausdorff distance from order-sensitive discrete Fréchet distance.
- [Smallest enclosing circle](smallest-enclosing-circle.md) — compute the minimum-radius Euclidean circle containing a finite planar point set.
- [Geometry metrics implementation](../../implementations/python/geometry-metrics/README.md) — tested Hausdorff, discrete Fréchet and randomized Welzl baselines.
- [Convex-polygon diameter](convex-polygon-diameter.md) — find a farthest pair with a rotating-calipers antipodal sweep.
- [Pole of inaccessibility / Polylabel](pole-of-inaccessibility-polylabel.md) — approximate the maximum-clearance interior point of a polygon, including holes.
- [Minimum-area oriented bounding rectangle](minimum-area-bounding-rectangle.md) — find a minimum-area enclosing rectangle by testing convex-hull edge orientations.

- [Alpha shapes](alpha-shapes.md) — parameterise a non-convex envelope by filtering Delaunay triangles using circumradius.
- [Alpha-shape implementation](../../implementations/python/alpha-shapes/README.md) — Delaunay triangle filtering, boundary-ring extraction and numerical tests.
- [Visibility polygons](visibility-polygons.md) — compute the region visible from an interior viewpoint in a polygonal environment.
- [Laplacian and Taubin mesh smoothing](mesh-smoothing.md) — smooth triangular meshes while documenting shrinkage and feature-preservation limits.
- [Half-edge mesh topology](half-edge-mesh.md) — indexed face cycles, symmetric twins, boundary edges and adjacency for oriented triangle meshes.
- [Conservative mesh repair](mesh-repair.md) — weld near-duplicate vertices, remove collapsed/duplicate faces and consistently orient components.
- [Isotropic-style remeshing](isotropic-remeshing.md) — split/collapse/flip edges with topology checks and tangential relaxation.
- [Winged-edge topology](winged-edge.md) — static polygon-mesh edges with left/right faces and four wing references.
- [Quad-edge topology](quad-edge.md) — Guibas–Stolfi four-dart representation and core topological operators.

- [Weiler–Atherton polygon intersection](weiler-atherton.md) — linked-boundary traversal for simple concave rings and disconnected intersection components.

- [Vatti polygon clipping](vatti-clipping.md) — general Boolean clipping; current runnable package is a transparently classified Clipper/Pyclipper adapter, not a from-scratch scanbeam implementation.
- [Native Vatti scanbeam foundation](vatti-scanbeam.md) — scanbeam levels, bound edges, horizontal edges and local minima; active-edge processing remains outstanding.
- [Vatti-family clipping adapter](../../implementations/python/vatti-clipping/README.md) — integer-grid Boolean operations, fill rules, disconnected components and shell/hole hierarchy.

- [Martinez–Rueda sweep-line front end](martinez-rueda.md) — initial event-queue, segment-intersection and splitting stage; full Boolean classification and stitching remain outstanding.

- [Martinez–Rueda polygon overlay](martinez-rueda.md) — staged Boolean overlay with oriented ring stitching and explicit shell/hole component assembly.

- [BSP tree constructive solid geometry](bsp-csg.md) — split convex 3D boundary polygons by planes and implement union, intersection and difference.
- [BSP CSG implementation](../../implementations/python/bsp-csg/README.md) — floating-tolerance polygon splitting and box-based Boolean volume tests.

- [Constrained Delaunay triangulation](constrained-delaunay.md) — polygon-boundary CDT with exact-predicate Lawson flips, plus non-crossing interior diagonals between existing polygon vertices.
- [DCEL polygon subdivision core](dcel-arrangements.md) — construct half-edge topology from already-noded face rings, with explicit exterior-cycle traversal.
