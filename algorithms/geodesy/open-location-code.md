# Open Location Code (Plus Codes)

Open Location Code encodes a latitude/longitude cell into a compact string
using a restricted alphabet. It is a location representation, not a postal
address and not a geocoder. A full code identifies a cell globally; a short
code omits leading context and must be recovered using a locality reference.

## Encoding structure

The first ten characters encode latitude/longitude in alternating pairs.
Their cell resolutions are 20°, 1°, 0.05°, 0.0025° and 0.000125°. Further
characters refine the cell using a 5-row by 4-column grid. The separator is
inserted after eight characters.

For each pair resolution r, the encoder selects

\[
i_\phi=\left\lfloor\frac{\phi+90}{r}\right\rfloor,\qquad
i_\lambda=\left\lfloor\frac{\lambda+180}{r}\right\rfloor
\]

then subtracts the selected cell offsets before processing the next level.
Coordinates at the north pole are nudged infinitesimally inside the final
cell because the latitude domain is half-open at +90°.

## Reference implementation

See [the Python implementation](../../implementations/python/open-location-code/README.md).
It implements full-code encode/decode and returns decoded cell bounds.
Short-code recovery and geocoding are intentionally excluded.

## Limits and responsible use

- The code represents a quantised cell, not an exact point.
- Cell dimensions are angular and vary in physical size with latitude.
- A Plus Code does not establish ownership, a building entrance, postal
  deliverability or legal address status.
- Do not infer an address or a person's identity from a code alone.
- For production interoperability, use and test against the official
  Open Location Code implementation and its versioned specification.
