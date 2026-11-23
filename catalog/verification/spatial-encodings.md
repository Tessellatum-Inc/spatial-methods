# Verification record: Morton, Hilbert and Geohash

## Source identity

- Compendium: *Spatial Analysis Algorithms: Complete Compendium*
- Original location: section 1, Spatial indexing and query processing, page 1
- Preserved transcription: [pages 1–5](../../source-inventory/pages-01-05.md)
- Source wording: Z-order (Morton), Hilbert, Geohash, H3, S2, quadkeys, HEALPix

## Scope implemented

- Morton/Z-order encode and decode for two integer grid coordinates.
- Hilbert xy-to-distance and distance-to-xy transforms on a square power-of-two grid.
- Geohash encode and decode to latitude/longitude bounds.

## Verification performed in code

The test suite checks:
- exhaustive bijection/round trips on small grids;
- seeded round trips at 10, 16, 24 and 32 bits;
- geohash reference string `ezs42` for (42.6, -5.6) at precision 5;
- decoded bounds contain the original coordinate;
- precision narrows both coordinate intervals;
- invalid widths, coordinates, distances and geohash inputs are rejected.

## Claims not made

H3, S2, HEALPix and quadkeys are not implemented by this package. The package is not a production spatial database index and does not benchmark large-scale workloads. The source-entry row remains **partial** until each named family has its own identity, technical and rights review.

## Reproduction

From `implementations/python/spatial-encodings`:

```bash
python -m pip install pytest
python -m pytest -q
```
