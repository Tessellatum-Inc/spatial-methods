# Native Vatti-family scanbeam reference

This package is a from-scratch, exact-rational reference implementation of
selected Vatti-family polygon Boolean operations. It is deliberately not
presented as a complete production Vatti engine.

## Implemented pipeline

1. **Input decomposition:** extracts scanbeam levels, directed non-horizontal
   bounds, horizontal edges and local minima (including horizontal plateaus).
2. **Coincident-edge bundling:** groups active bounds by exact rational slope
   and intercept. Each bundle retains its member edges and accumulates subject
   and clip winding deltas independently. Opposite-direction copies therefore
   cancel or reinforce according to the selected fill rule, without generating
   duplicate crossing events.
3. **Neighbour-event sweep:** initializes the active order immediately above
   the lower scanbeam and schedules intersections only between adjacent
   bundles in a rational event heap. Multiway crossings at one coordinate are
   reordered atomically; newly adjacent pairs are then scheduled. Distinct
   crossing points at the same scanline are processed independently.
4. **Fill-state propagation:** evaluates subject and clip winding separately
   across each ordered bundle list for intersection, union, difference and
   XOR under even-odd, non-zero, positive or negative fill rules.
5. **Horizontal contacts:** records horizontal/bound endpoint and interior
   contacts plus horizontal/horizontal point and overlap events. Contact
   coordinates are inserted into cell-boundary noding before stitching.
   Horizontal edges define scanbeam-level boundaries; they do not contribute
   to the open-band winding count. At each level, one-sided below/above
   Boolean intervals are compared and explicit horizontal fill transitions
   are recorded. Shared horizontal edges with filled regions on both sides
   are correctly treated as internal seams.
6. **Cell and contour output:** emits exact-rational trapezoid/triangle cells,
   nodes unequal shared-edge subdivisions, cancels internal seams and walks
   the remaining directed boundary into closed rings. Disconnected shells and
   clockwise hole rings are retained.

The main public entry point is:

```python
from vatti_scanbeam import decompose_scanbeams, clip_rings

decomposition = decompose_scanbeams([subject_ring, clip_ring])
result = clip_rings(
    decomposition, subject_ring_ids={0}, clip_ring_ids={1},
    operation="intersection", fill_rule="non_zero",
)
# result.rings is a tuple of closed, exact-rational output rings.
```

## Verification

The test suite covers:

- All four Boolean operations on analytically calculable overlaps.
- Identical and opposite-direction coincident rings.
- Full and partial shared vertical boundaries.
- Shared horizontal boundaries and vertex-only contact.
- Three-way crossings and distinct crossing events at the same Y.
- Holes, disconnected shells, empty results and unequal seam subdivisions.
- Differential comparison with Shapely for area, symmetric-difference area and
  polygon component counts across 29 deterministic degeneracy and seeded rectangle fixtures.

Shapely is a test oracle only; it is not used by the clipping implementation.
The dependency is installed from this package's `requirements.txt`.

## Deliberate limitations

This is a neighbour-event reference sweep, not yet the complete Vatti
intersection-list algorithm. The implementation still needs the full local
minimum list / scanbeam table lifecycle, in-place active-edge maintenance and
the published horizontal processing rules for minima, maxima, joins and
ghost joins. Coincident and touching configurations beyond the current
regression matrix need broader randomized and adversarial differential tests.
The sweep currently uses rational arithmetic derived from decimal input
coordinates; input parsing itself currently converts coordinates to floats.

The older `crossings_in_band()` and `sweep_active_edge_slices()` functions
remain available as transparent all-pairs reference utilities. The production
Boolean sweep uses `bundle_active_edges()` and
`sweep_neighbour_ordered_bundles()`.
