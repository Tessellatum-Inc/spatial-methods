# Point in polygon with Python

This tutorial asks a simple question: given a point and a boundary, is the point inside, outside or exactly on the edge?

It implements the ray-crossing (even–odd) method for one simple polygon ring and reports boundary points separately.

## Set up

Use Python 3.10 or newer.

```bash
python -m venv .venv
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Run it

```bash
python point_in_polygon.py
```

Expected output:

```text
(2, 2) inside
(5, 2) outside
(4, 2) boundary
```

## Run the tests

```bash
python -m pytest -q
```

The test suite covers inside, outside, edge, vertex, concavity, a ray passing through a concave vertex, and both open and explicitly closed ring representations.

## Follow the code

1. Start with `PointLocation`: the result has three states, not just True or False.
2. Read `_on_segment`: boundary is checked before counting crossings.
3. Read `locate_point`: each edge is checked once and a crossing toggles the parity.
4. Change the point coordinates and predict the classification before running the tests.

## Step-by-step implementation walkthrough

Read [how the implementation works](implementation-walkthrough.md) for ring normalisation, boundary detection, half-open scanline crossings and parity toggling.

## Important limits

- This is a teaching implementation for a single simple ring.
- It does not support holes, multipolygons or self-intersecting rings.
- The original `locate_point` and `locate_point_winding` functions use floating-point arithmetic and exact equality; they are pedagogical, not robust predicates.
- The additional `locate_point_exact`, `winding_number_exact` and `locate_point_winding_exact` functions convert finite decimal coordinates to `Fraction` and use division-free exact orientation signs. They avoid floating-point predicate sign errors for the supplied decimal representations, at higher computational cost.
- It uses planar x/y coordinates; it does not transform CRS or interpret longitude/latitude.
- Production systems should use a geometry library with documented topology and boundary semantics.

## Checked environment

- Python 3.13.5
- pytest 9.0.2

The 12 tests passed in the recorded environment. Run them again in your own environment before using the code in a project.


## Winding-number implementation

The module also exposes `winding_number(point, ring)` and `locate_point_winding(point, ring)`. These implement the signed crossing-count method and the nonzero winding fill rule. The scalar winding function raises on boundary points because the winding number is undefined there; the three-way classifier reports boundary separately. For simple rings, seeded randomized tests compare the winding classifier against the independent even-odd ray-crossing implementation. Both are O(n) in the number of ring edges.


## Exact-rational predicate variants

For data where floating-point boundary classification is unacceptable, use `locate_point_exact(point, ring)` or `locate_point_winding_exact(point, ring)`. Both preserve a separate `BOUNDARY` result and use exact rational orientation tests without calculating ray/edge intersection coordinates. `winding_number_exact` returns the signed integer winding count and raises when the query is on the boundary. The exact variants are still scoped to one simple planar ring: they do not validate ring simplicity, model holes or multipolygons, or resolve application-specific fill rules for self-intersecting paths. Fraction arithmetic can be slower and use more memory than floating-point predicates.
