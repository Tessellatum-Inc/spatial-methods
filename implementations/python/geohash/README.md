# Geohash location encoding

A dependency-free WGS84 geohash encoder/decoder. `encode(latitude,
longitude, precision)` returns a base-32 cell code; `decode_bounds(code)`
returns its south/north/west/east bounds; `decode(code)` returns the cell
centre. Precision is supported from 1 to 12 characters.

Run `python -m pip install -r requirements.txt && python -m pytest -q`.

Geohash is a hierarchical rectangular grid address, not a metric distance
system. Adjacent points can have very different strings across cell
boundaries, and equal string prefixes denote nested geographic rectangles.
This implementation covers geohash only: Open Location Code, H3, S2 and
what3words are different systems and are not implemented here. It does not
implement geodesic neighbour enumeration or database indexing.
