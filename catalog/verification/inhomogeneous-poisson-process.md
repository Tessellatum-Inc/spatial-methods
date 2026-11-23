# Verification record: piecewise-constant inhomogeneous Poisson simulation

## Implemented scope

- A finite non-negative 2D intensity grid over a rectangular planar window.
- Independent Poisson counts per cell with mean intensity times cell area.
- Uniform within-cell event locations.
- Seeded reproducibility and zero-intensity handling.

## Tests

Tests check deterministic seeded output, cell containment, zero-intensity
behaviour, invalid grids/windows/seeds, and the expected total count against
the integrated grid intensity over repeated independent seeds.

## Limits

Exactness is conditional on the piecewise-constant grid model. No intensity
estimation, continuous kernel surface, covariate regression, irregular
window or spatial interaction is included.
