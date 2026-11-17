# Implementation verification — DE-9IM and RCC-8

## Scope

The package delegates geometry intersection and topological predicates to Shapely/GEOS. It exposes the DE-9IM relation string and an RCC-8 classifier for valid, non-empty Polygon and MultiPolygon inputs.

## Tests

Fixtures cover all eight RCC-8 relations: disconnected, externally connected, partial overlap, equality, tangential proper part and inverse, and non-tangential proper part and inverse. Tests also check the nine-character DE-9IM result, inverse symmetry for directional relations, invalid geometries, empty inputs, non-polygonal inputs and unsupported geometry types.

## Limitations

The package is a wrapper around GEOS predicates, not an independent topology kernel. RCC-8 classification is limited to planar polygonal regions. Cardinal-direction relations, qualitative direction calculi, geographic/geodesic semantics, 3D topological relations and formal verification against an independent topology oracle are not included. The source entry remains partial because its cardinal-direction family and source-level verification are outstanding.

## Reproduction

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```
