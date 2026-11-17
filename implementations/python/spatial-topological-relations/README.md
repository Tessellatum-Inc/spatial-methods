# DE-9IM and RCC-8 topological relations

A Shapely/GEOS-backed teaching wrapper for the nine-intersection matrix and RCC-8 relations between planar polygonal regions.

## Run

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

## Contract

- `de9im(a, b)` returns the geometry engine's nine-character DE-9IM string for valid, non-empty Shapely geometries.
- `rcc8(a, b)` classifies one of DC, EC, PO, EQ, TPP, NTPP, TPPi or NTPPi for valid, non-empty Polygon or MultiPolygon inputs.
- Inputs must share a planar coordinate space and compatible precision semantics.
- Invalid geometries are rejected rather than repaired.
- Cardinal-direction calculi, 3D relations and geographic/geodesic semantics are not implemented.

The geometry predicates and matrix are supplied by GEOS through Shapely. This package is not an independent topology kernel.

## Tests

Fixtures cover all eight RCC-8 relations, inverse pairs, the DE-9IM string shape and invalid, empty and non-region inputs. These tests validate the wrapper contract, not the independent correctness of GEOS itself.
