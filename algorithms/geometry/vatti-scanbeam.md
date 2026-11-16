# Native Vatti scanbeam decomposition

Vatti's general polygon clipping method processes polygon contours through
scanbeams, active edges, local minima, horizontal edges and intersection
events. The native component implemented here extracts the geometric
primitives needed to initialise and inspect that process.

The package
[implementations/python/vatti-scanbeam](../../implementations/python/vatti-scanbeam/README.md)
provides:
- sorted unique scanbeam levels;
- non-horizontal bounds stored lower-to-upper with original traversal winding;
- explicit horizontal-edge records;
- local-minimum pairs, including horizontal bottom plateaus;
- exact rational slope ordering for the two bounds at each minimum;
- active-edge ordering at a scanbeam-band midpoint;
- exact pairwise crossing events within a band;
- band subdivision at crossing levels and active-edge reordering on either side;
- cumulative signed winding transitions in left-to-right edge order;
- horizontal/bound endpoint and interior intersection events;
- horizontal/horizontal point contacts and positive-length overlaps, classified separately;
- fill-rule predicates for even-odd, non-zero, positive and negative winding;
- Boolean point-classification truth tables for intersection, union, difference and XOR;
- subject/clip winding propagation and Boolean fill-state transition records over an ordered active-edge list;
- full reference sweep over all scanbeam bands, with horizontal/minimum level events and crossing-split slices;
- exact-rational filled trapezoid/triangle cell decomposition for intersection, union, difference and XOR.

The current crossing scheduler is an O(m²) reference calculation, not the
optimized neighbour-event scheduler used by a full sweep-line clipper. This
is a **partial native implementation**. Efficient neighbour-only intersection scheduling, incremental active-edge updates,
horizontal processing, fill-rule propagation and Boolean output construction
remain outstanding.

## References

- Vatti, B. R. (1992), "A generic solution to polygon clipping",
  *Communications of the ACM*, 35(7), 56–63.
- Clipper2 overview: https://www.angusj.com/clipper2/Docs/Overview.htm

## Boolean output contours

The native reference implementation now exposes `clip_rings(...)`, which
turns the Boolean sweep's exact-rational trapezoid/triangle cells into closed
rings. It nodes cell boundaries at shared vertices, cancels internal seams,
and stitches the remaining directed edges. Disconnected components and
clockwise hole rings are preserved. See the implementation README and
verification ledger for the current test matrix and limitations.


## Degeneracies and sweep scheduling

The Boolean sweep now coalesces coincident active bounds into operand-aware
winding bundles and schedules intersections between adjacent bundles through
an exact-rational event heap. Multiway crossings are reordered as a single
event. Horizontal contact coordinates are propagated into cell-boundary
noding before contour stitching.

Regression coverage includes coincident rings, opposite edge directions,
shared vertical and horizontal boundaries, partial collinear overlap,
vertex-only contact and multiway crossings. Shapely is used as an independent
test oracle for area and polygon-component comparisons; it is not a runtime
dependency of the clipping implementation.
