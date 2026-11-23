# Verification — geohash encoding

- Source: Section 19, page 40, location encoding systems row.
- Implemented: base-32 geohash encode, cell-bound decode and centre decode.
- Tests: known reference code, boundary coordinates, precision refinement,
  case-insensitive decode and invalid coordinates/precision/alphabet.
- Scope: WGS84 geohash only.
- Open: Open Location Code, H3, S2, what3words, geodesic neighbours and
  spatial database integration.
- Status: partial contribution to grouped source entry.
