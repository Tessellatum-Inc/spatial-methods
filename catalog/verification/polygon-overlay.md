# Implementation verification — polygon Boolean overlay

## Implemented scope

The Python package exposes explicit intersection, union, difference and symmetric-difference operations for valid Shapely Polygon and MultiPolygon inputs. It delegates robust noding and overlay construction to GEOS through Shapely; it is a practical geometry-engine integration example, not a from-scratch Boolean clipping algorithm.

Optional fixed-precision grid reduction is passed to the GEOS overlay operation. The wrapper validates polygonal input type, emptiness, validity, operation name and grid-size constraints. Output dimensionality is preserved and reported rather than silently coerced to polygon output: edge-only intersections may be LineStrings and point-only intersections may be Points.

## Verification

Tests include hand-calculated rectangle areas; union/intersection and difference/intersection area identities; disjoint and contained polygons; holes and MultiPolygon inputs; edge and point touches; invalid input and operation rejection; precision-grid behavior; 500 seeded axis-aligned rectangle pairs against interval-arithmetic area formulas; and 250 seeded rotated-rectangle pairs checking symmetry and area-conservation identities.

## Limitations

The package inherits GEOS behavior and numerical policy. It does not implement a new overlay engine or promise exact arithmetic. Inputs must already be valid polygonal geometries; repair is a separate explicit workflow. CRS compatibility and planar units remain the caller's responsibility.

## Reproduction

From the package directory: `python -m pip install -r requirements.txt && python -m pytest -q`.

## Rights

The wrapper and tests are independently authored. Shapely and GEOS are third-party dependencies, not copied implementation source.
