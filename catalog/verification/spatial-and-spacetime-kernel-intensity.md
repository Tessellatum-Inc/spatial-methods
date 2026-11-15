# Source verification — spatial and space-time kernel intensity

## Identity and bibliography
- Diggle, P. J. (1985), “A kernel method for smoothing point process data,” *Journal of the Royal Statistical Society: Series C (Applied Statistics)*, 34(2), 138–147.
- Baddeley, Rubak & Turner (2015), *Spatial Point Patterns: Methodology and Applications with R*.

## Technical claims
- Spatial point-process intensity is an expected event count per unit area, distinct from a probability density normalized to one.
- A fixed-bandwidth Gaussian estimator sums a normalized kernel contribution per event.
- A separable space-time kernel multiplies spatial and temporal kernels, giving units per area per time.
- Uncorrected kernels lose mass beyond study-window boundaries and can bias estimates near edges.

## Implementation/reproduction
Implemented: fixed-bandwidth planar Gaussian spatial intensity and separable space-time intensity with optional nonnegative event weights. Tests are authored for normalization at the kernel centre, event-count scaling, weight scaling, space-time factorization and invalid inputs.

Not implemented: edge correction, adaptive bandwidths, anisotropy, network kernels, Voronoi/Delaunay estimators, prospective hotspot inference, bandwidth selection or uncertainty estimates. Test files are not evidence of a passing repository test run.

## Rights
Original explanatory text and bibliographic metadata only; no source figures, code or datasets reproduced.
