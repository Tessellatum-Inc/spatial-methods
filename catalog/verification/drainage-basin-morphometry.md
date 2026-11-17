# Verification — drainage-basin morphometry

**Status:** Partial; formula-level descriptive measures are implemented and tested.

Coverage: shape ratios (form factor, elongation, circularity, compactness); network ratios (drainage density, stream frequency, drainage texture, bifurcation); relief ratio and ruggedness. Tests use hand-calculated formula oracles, zero-relief/empty-network cases and invalid-input checks.

Run python -m pytest -q from this package directory.

Not covered: basin delineation, perimeter measurement, channel extraction, Strahler ordering, unit conversion, uncertainty estimation or geomorphic interpretation.
