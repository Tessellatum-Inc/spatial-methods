# Geohash: hierarchical rectangular location encoding

Geohash recursively bisects longitude and latitude intervals, interleaving
longitude and latitude bits, then encodes each five-bit group with a 32-symbol
alphabet. The first bit splits longitude; the next splits latitude; the
sequence alternates. Each additional character refines the rectangular cell
by five binary subdivisions.

For a point (latitude, longitude), the encoder returns a string at a chosen
precision. Decoding recovers the cell bounds rather than the original exact
coordinate. The centre of those bounds is a representative coordinate. The
cell is not a circle, and its physical width varies with latitude.

The tested implementation validates WGS84 coordinate ranges, supports
precision 1–12, accepts uppercase input during decoding, and exposes both
cell bounds and centre. It is a location-code primitive, not a replacement
for geodesic distance calculations or a full spatial index.

Geohash is only one member of the source entry's family. Open Location Code,
H3, S2 and three-word addressing use different encodings and require separate
implementations and validation. See the
[Python package](../../implementations/python/geohash/README.md).
