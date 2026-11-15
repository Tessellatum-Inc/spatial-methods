# Implementation verification — static slab point location

## Implemented scope

The Python package preprocesses a restricted planar subdivision into vertical x-slabs. Each slab stores the ordered boundary-edge crossings and the face occupying each interval. A query uses binary search over x-events and then over the ordered crossing groups. Queries on event lines use a boundary-aware fallback scan.

The structure supports polygon faces with exterior and hole rings, pairwise interior-disjoint face interiors, explicit boundary results, and an outside/unbounded result. It is a static slab decomposition teaching implementation, not Seidel's randomized trapezoidal map.

## Complexity

The current straightforward construction scans edges for every slab, so preprocessing and storage can be O(n²) in the worst case. Strictly interior slab queries use O(log n) comparisons. Queries on event lines fall back to a scan of represented boundaries and are O(n) in the number of edges.

## Verification

Tests cover inside/outside/boundary queries, adjacent faces and shared edges, holes, vertical edges and event-line queries, invalid open rings, non-finite query values, and overlapping-face rejection. Seeded tests add 2,000 queries against a rectangle-membership oracle across 36 randomly sized disjoint faces and check every shared seam in a 5-by-5 adjacent-face grid.

## Limitations

The package assumes valid closed ring topology and non-crossing boundaries; it does not fully validate arbitrary planar subdivisions. It uses floating-point edge interpolation and a configurable epsilon. It does not implement randomized trapezoidal search DAGs or their expected O(log n) query guarantees.

## Reproduction

From the package directory: `python -m pip install -r requirements.txt && python -m pytest -q`.


## Event-line tolerance regression

The x-event lookup now applies the configured epsilon to the nearest event
coordinate on either side of the query. Queries within tolerance use the
boundary-aware event-line fallback, so points within epsilon of vertical
edges are not incorrectly assigned to a face by the open-slab search. Tests
cover both sides of a vertical edge and ensure nearby points outside the
polygon remain outside.


## Randomized trapezoidal decomposition reference (partial)

A separate `randomized_trapezoidal_map.py` module constructs a vertical trapezoidal decomposition for bounded, pairwise-disjoint, non-vertical segments with distinct endpoint x-coordinates. It builds a balanced x-decision tree and per-slab y-decision trees; query results are trapezoid records, with explicit original-segment boundary and outside-box results. Tests cover deterministic seeded permutations, cell interval invariants, boundary queries, invalid/crossing inputs and seeded query samples.

**Not complete:** the insertion permutation is randomized, but the current correctness-first reference rebuilds the entire decomposition after each insertion. It is not Seidel's local-update history DAG and does not claim expected (O(n\log n)) construction. Vertical segments, shared endpoints, intersections, unbounded subdivisions and face-label propagation are not supported. The optimized randomized incremental trapezoidal map remains an open compendium item. Test execution must be confirmed by CI before treating these authored tests as passing.
