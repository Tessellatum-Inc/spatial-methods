# Implementation verification — planar point location

This record covers two distinct structures in `implementations/python/point-location`. Their contracts and complexity claims must not be conflated.

## 1. Static slab locator

### Implemented scope

The `SlabPointLocator` preprocesses a restricted planar subdivision into vertical x-slabs. Each slab stores ordered boundary-edge crossings and the face occupying each interval. Queries use binary search over x-events and crossing groups. Queries on event lines use a boundary-aware fallback. The supported model includes valid polygon faces with exterior and hole rings, pairwise interior-disjoint face interiors, explicit boundary results and an outside/unbounded result.

### Verification evidence

Tests cover inside/outside/boundary queries, adjacent faces and shared edges, holes, vertical edges and event-line queries, invalid open rings, non-finite query values and overlapping-face rejection. Seeded tests compare 2,000 queries against a rectangle-membership oracle across 36 randomly sized disjoint faces and check every shared seam in a 5-by-5 adjacent-face grid. Regression tests cover points on either side of vertical edges and points within the configured event-line tolerance.

### Complexity and limitations

The straightforward construction scans edges for every slab, so preprocessing and storage can be O(n²) in the worst case. Strictly interior slab queries use O(log n) comparisons; event-line queries fall back to a boundary scan and are O(n) in the number of edges. The package assumes valid closed ring topology and non-crossing boundaries; it does not validate arbitrary planar subdivisions. It uses floating-point edge interpolation and a configurable epsilon.

## 2. Randomized trapezoidal decomposition with persistent history DAG

### Implemented scope

The `randomized_trapezoidal_map.py` module provides a bounded randomized incremental trapezoidal-decomposition prototype for finite, pairwise-disjoint, non-vertical segments in general position inside a finite rectangular bounding box.

The implementation:
- validates segment geometry and rejects vertical, zero-length, crossing, touching and out-of-box inputs outside its supported contract;
- inserts segments in a seeded random permutation;
- maintains trapezoid-cell snapshots using corridor replacement, retaining endpoint caps and coalescing compatible lower/upper fragments;
- records added and removed cells for each replacement and checks reciprocal left/right neighbour relationships and full-domain coverage;
- updates a persistent search-history DAG by replacing removed trapezoid leaves with endpoint x-decisions and segment y-decisions while preserving untouched branches;
- answers public point-location queries by traversing the persistent history DAG, returning a trapezoid, `BOUNDARY` for an original segment, or `None` outside the bounding box;
- retains a rebuilt slab decomposition as a differential reference oracle.

### Verification evidence

Package tests cover deterministic seeded insertion order, trapezoid vertical intervals, original-segment boundary results, outside-box results, deterministic handling of artificial vertical walls, invalid and unsupported segment sets, and seeded randomized query comparisons. They also exercise the persistent history query against the independently rebuilt slab locator and validate corridor replacement invariants, neighbour reciprocity and domain coverage.

The tests are registered through the `implementations/python/point-location` package in `scripts/python-ci-packages.json`. Their authored presence is not itself proof of a passing CI run; use the exact-head GitHub Actions result before claiming execution success.

### Complexity and limitations

This is a correctness-oriented research/teaching prototype, not a claim of a complete optimised Seidel implementation. The insertion process still rebuilds global decomposition and neighbour information in parts of its workflow; neighbour maintenance is not fully local. The history DAG is updated persistently and used for public queries, but no proven expected O(n log n) construction bound or worst-case query bound is claimed.

Vertical segments, shared endpoints, intersecting segments, unbounded subdivisions, arbitrary planar arrangements and face-label propagation are outside the supported contract. The slab oracle is independent at the query-structure level but shares the same validated segment input and geometric model; it is not an external library or published benchmark oracle.

## Reproduction

From the package directory:

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```
