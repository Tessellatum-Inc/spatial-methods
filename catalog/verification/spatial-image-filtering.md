# Verification — spatial image filtering

**Status:** Partial implementation; this record verifies the scoped reference methods, not the complete filtering family.

## Implemented

- Separable Gaussian smoothing with normalized kernels and reflected boundaries.
- Four-neighbour discrete Laplacian response.
- Square-window median filter.
- Circular-support bilateral filter with Gaussian spatial and range weights.
- Explicit Perona-Malik diffusion with exponential and reciprocal conductance.

## Independent checks

Tests include constant-field invariants, Gaussian symmetry and impulse response, the analytic interior Laplacian of x²+y², an independent nested-loop median-window oracle, bilateral suppression across a sharp step, diffusion variance reduction, and malformed-input checks.

Run from the package directory: python -m pytest -q

## Not covered

Total variation, non-local means, guided filtering, tensor diffusion, multiscale filtering, adaptive parameter selection, sensor-specific noise models, physical-grid calibration and optimized large-raster execution.
