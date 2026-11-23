# Open Location Code (Plus Codes)

A dependency-free reference implementation of full Open Location Code encoding
and decoding for WGS84 coordinates.

## Run

Install with pip install -r requirements.txt, then run pytest -q.

## Contract

- Accepts finite latitude in [-90, 90] and finite longitude (normalised to
  [-180, 180)).
- Encodes full codes with 10–15 alphabet characters and the separator at
  position eight.
- Decodes full codes to south, west, north and east cell bounds.
- Does not resolve short codes, recover locality context, perform address
  lookup, or provide a geocoder.
- This is a compact teaching baseline; verify interoperability against the
  official Open Location Code library before operational use.

The alphabet and pair/grid resolutions follow the Open Location Code format.
