# Implementation verification — polygon Boolean overlay

## Implemented scope

The Python package exposes explicit intersection, union, difference and symmetric-difference operations for valid Shapely Polygon and MultiPolygon inputs. It delegates robust noding and overlay construction to GEOS through Shapely; it is a practical geometry-engine integration example, not a from-scratch Boolean clipping algorithm.

Optional fixed-precision grid reduction is passed to the GEOS overlay operation. The wrapper validates polygonal input type, emptiness, validity, operation name and grid-size constraints. Output dimensionality is preserved and reported rather than silently coerced to polygon output: edge-only intersections may be LineStrings and point-only intersections may be Points.

A separate C# example now exercises Clipper2's general polygon Boolean API on a concave U-shaped subject and a horizontal bar. The regression expects two disconnected intersection components and checks intersection, difference and union areas (18, 54 and 90 square units), including the subject partition identity. This is library-backed Clipper2 verification, not a from-scratch Vatti implementation.

## Verification

Python tests include hand-calculated rectangle areas; union/intersection and difference/intersection area identities; disjoint and contained polygons; holes and MultiPolygon inputs; edge and point touches; invalid input and operation rejection; precision-grid behavior; 500 seeded axis-aligned rectangle pairs against interval-arithmetic area formulas; and 250 seeded rotated-rectangle pairs checking symmetry and area-conservation identities.

The C# CI executable checks positive and negative offsets, collapse under over-contraction, concave Boolean intersection with disconnected output, and area conservation across intersection and difference.

## Limitations

The Python package inherits GEOS behavior and numerical policy. It does not implement a new overlay engine or promise exact arithmetic. Inputs must already be valid polygonal geometries; repair is a separate explicit workflow. CRS compatibility and planar units remain the caller's responsibility.

The Clipper2 example delegates the Boolean engine to the pinned NuGet package (2.0.0). It currently verifies simple non-self-intersecting rings with the NonZero fill rule. It does not establish support for every Vatti degeneracy, self-intersecting input, all fill rules or all hole-nesting configurations. Vatti's original scanbeam algorithm remains a distinct from-scratch implementation gap.

## Reproduction

Python: from the package directory, run `python -m pip install -r requirements.txt && python -m pytest -q`.

C#: run `dotnet run --project implementations/clipper2-csharp/Clipper2Example.csproj`.

## Rights

The wrapper and tests are independently authored. Shapely/GEOS and Clipper2 are third-party dependencies, not copied implementation source.


## Collection-level cascaded union

A collection-level wrapper was added to the existing polygon-overlay package. It rejects empty collections, invalid geometries and unsupported non-polygonal inputs, and delegates to Shapely 2.1.2 / GEOS `union_all`. Tests cover overlapping polygons, equivalence to repeated binary union on a small fixture, disjoint components, hole preservation and invalid input.

This verifies the wrapper's contract only. It does not independently verify GEOS's internal cascaded-union tree, complexity guarantees or robustness claims. The source entry remains partial pending source identity/claim review and a decision on whether a standalone teaching implementation is required.
