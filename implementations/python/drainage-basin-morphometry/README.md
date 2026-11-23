# Drainage-basin morphometry

Dependency-free formulas for basin shape, relief and drainage-network structure from supplied measurements.

## Inputs and units

Supply basin area, perimeter, basin length, relief, channel lengths and stream counts keyed by positive stream order (normally Strahler). All linear measurements must share a unit; area must use its square. The package cannot verify unit consistency.

## Measures

- Form factor: A / Lb².
- Elongation ratio: 2√(A/π) / Lb.
- Circularity ratio: 4πA / P².
- Compactness coefficient: P / (2√(πA)).
- Drainage density: total channel length / A.
- Stream frequency: total stream count / A.
- Drainage texture: total stream count / P.
- Bifurcation ratio: Nu / N(u+1), only for adjacent orders with a positive denominator.
- Relief ratio: relief / basin length.
- Ruggedness number: drainage density × relief.

Measurement conventions vary. Report basin-length and perimeter methods, channel initiation threshold, ordering rule, map scale and units.

## Scope

No basin delineation, channel extraction, stream ordering, unit conversion, uncertainty estimation or geomorphic interpretation is included. Run tests with python -m pytest -q.
