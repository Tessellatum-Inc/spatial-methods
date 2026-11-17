# Verification record: binary mathematical morphology

## Scope
NumPy reference implementations: erosion, dilation, opening, closing, hit-or-miss, geodesic reconstruction and 4-/8-connected components.

## Independent checks
- Explicit false-padding boundary contract is tested on all-foreground and single-pixel rasters.
- Opening and closing idempotence are tested on a mixed raster.
- Monotonicity and erosion/dilation duality are checked on seeded random masks.
- Hit-or-miss is checked against a hand-constructed cross template.
- Reconstruction is checked against the independently specified marker-connected mask component, including invalid marker and iteration-limit cases.
- Component counts and sizes are checked for diagonal pixels under both connectivity conventions.
- Invalid dimensionality, empty arrays, empty structures and invalid connectivity are rejected.

## Reproduction
From implementations/python/binary-morphology:
~~~bash
python -m pip install -r requirements.txt
python -m pytest -q
~~~

These are source-level test claims; CI execution must pass before this record can be treated as release verification. No external source code or imagery is reproduced.

- Zhang-Suen thinning is checked for foreground-subset preservation, reduction of a solid region, idempotence on the converged skeleton, preservation of a one-pixel line, 8-connected component count and explicit iteration-limit failure.
