# Verification — native Vatti scanbeam foundation

## Implemented
- Scanbeam extraction from all ring vertices.
- Lower-to-upper non-horizontal edge records with original traversal winding.
- Horizontal edge records.
- Local-minimum extraction across single vertices and horizontal plateaus.
- Exact rational dx/dy ordering of local-minimum bounds.
- Active-edge ordering at a scanbeam-band midpoint.
- Exact pairwise crossing events strictly within a band.
- Crossing-level band subdivision and edge-order swaps on either side.
- Cumulative signed winding transition helper.
- Horizontal/bound endpoint and interior intersection events.
- Horizontal/horizontal point-contact and overlap classification.
- Four fill-rule winding predicates and four Boolean-operation truth tables.
- Subject/clip winding propagation over an explicitly ordered active-edge list.
- Boolean-result entry/exit transitions for intersection, union, difference and XOR.
- Full scanbeam reference pass coordinating level events, crossing-split band slices and subject/clip winding transitions.
- Exact-rational filled-cell decomposition for all four Boolean operations.
- Exact-rational cell-edge noding at shared vertices, including unequal subdivisions.
- Coincident active-edge bundling with independent subject/clip winding aggregation.
- Adjacent-bundle event-heap intersection scheduling and atomic multiway crossing reorder.
- Horizontal contact points inserted into cell-boundary noding before contour stitching.
- One-sided below/above fill-state comparison at every scanbeam level.
- Explicit horizontal fill-transition intervals, including suppression of false transitions on shared internal horizontal edges.
- Cancellation of internal cell seams and directed boundary face-walk.
- Closed contour output with disconnected shells and clockwise holes.
- Public reference API `clip_rings()` combining the sweep and contour assembly.

## Tests authored
- Rectangle scanbeam and minimum fixture.
- Overlapping-rectangle area checks for intersection (6), union (26), difference (10) and XOR (20).
- Crossing-split cell decomposition and scanbeam horizontal/minimum event records.
- Contour outputs for intersection, union, difference and two-component XOR.
- Nested-hole plus disconnected-shell preservation.
- Empty contour result and unequal shared-edge subdivision.
- Coincident and opposite-direction coincident rings.
- Full/partial shared boundaries and vertex-touching components.
- Three-way simultaneous crossing, distinct same-Y crossing events and neighbour-event order changes.
- Horizontal entry/exit transitions at scanbeam levels and shared-horizontal-edge continuity.
- Shapely differential area, symmetric-difference geometry and component comparisons across 29 deterministic fixtures and four operations.
- Clockwise/counter-clockwise equivalence.
- Non-horizontal minimum and horizontal bottom plateau.
- Multiple local minima.
- Active-edge order and exact bow-tie crossing event.
- Invalid band, non-finite and repeated-vertex inputs.

## Not implemented
- Full Vatti scanbeam event-list/LMT/SEL maintenance and optimized in-place active-edge updates.
- Full Vatti horizontal-edge processing rules for local minima, maxima and horizontal joins; current implementation records contacts and nodes output cell boundaries.
- Complete Vatti topological output policies for all coincident/touching configurations, including multiway horizontal/bound intersections.
- Production-grade Vatti intersection-list scheduling and complete horizontal edge transition semantics.

## CI result

- GitHub Actions run [43793055809](https://github.com/geo-dev-hub/spatial-analysis/actions/runs/43793055809), commit `8b493812c8b39a9e5167657ca94801a744f360e2`.
- `Test vatti-scanbeam`: **64 passed** on Python 3.13 with Shapely 2.2.0.
- The Vatti scanbeam package job completed successfully. The repository-wide workflow was still running when this ledger entry was prepared.