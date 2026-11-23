# Spatial encodings: Morton, Hilbert and Geohash

Dependency-free reference implementations for three spatial key encodings named in the source compendium.

## Included algorithms

- **Morton / Z-order:** interleaves the bits of two non-negative integer grid coordinates. It is simple and cheap, but its locality is weaker and more orientation-sensitive than a Hilbert curve.
- **Hilbert curve:** maps a cell in a square power-of-two integer grid to a one-dimensional distance. The inverse is included. Nearby cells tend to remain close in the ordering, but this is not a guarantee for every pair.
- **Geohash:** alternately bisects longitude and latitude intervals and emits five-bit groups in a base-32 alphabet. Decoding returns the represented latitude and longitude bounds, not merely a centre point.

## Run

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

## Examples

```python
from spatial_encodings import (
    morton_encode, morton_decode,
    hilbert_encode, hilbert_decode,
    geohash_encode, geohash_decode,
)

key = morton_encode(12, 9, bits=8)
assert morton_decode(key, bits=8) == (12, 9)

distance = hilbert_encode(12, 9, bits=8)
assert hilbert_decode(distance, bits=8) == (12, 9)

cell = geohash_encode(-1.286, 36.817, precision=8)
lat_bounds, lon_bounds = geohash_decode(cell)
```

## Contracts and limitations

- Morton and Hilbert operate on integer grid coordinates. Choose the grid extent, origin, projection and quantisation policy before converting real coordinates.
- Both integer encoders support 1–32 bits per axis and reject out-of-range coordinates.
- Geohash accepts WGS84 longitude/latitude in degrees and precision 1–12 characters. It does not wrap longitudes outside [-180, 180].
- Geohash cells are rectangular in angular coordinates; their physical dimensions vary with latitude. They are not equal-area cells.
- This package does **not** implement H3, S2, HEALPix or a quadkey tile pyramid. Those are distinct systems with separate indexing, topology and/or projection contracts.
- These are transparent reference implementations, not database index integrations or a benchmarked large-scale spatial storage engine.

## Related material

- [Spatial encoding algorithm notes](../../../algorithms/indexing/spatial-encodings.md)
- [Source inventory: original pages 1–5](../../../source-inventory/pages-01-05.md)
