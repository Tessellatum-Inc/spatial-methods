# Spatial image filtering: smoothing, edge response and diffusion

This method family contains operators with different objectives; they are not interchangeable.

## Implemented reference methods

The NumPy package [spatial-image-filters](../implementations/python/spatial-image-filters/README.md) provides:

1. **Gaussian filter.** A separable discrete Gaussian kernel is normalized to unit sum and applied with reflected boundaries. It is a linear low-pass smoother.
2. **Four-neighbour Laplacian.** The stencil is [[0,1,0],[1,-4,1],[0,1,0]]. It approximates a second spatial derivative on a unit grid. Pixel spacing is not inferred; divide by squared cell size for a physical second derivative on a square grid.
3. **Median filter.** A square odd-width neighbourhood rank filter suppresses isolated impulses while retaining some sharp transitions.
4. **Bilateral filter.** A circular finite neighbourhood combines Gaussian spatial proximity and Gaussian intensity similarity. sigma_range is expressed in image intensity units.
5. **Perona-Malik diffusion.** An explicit four-neighbour update weights flux by exponential or reciprocal conductance. The implementation restricts the time step to 0.25 or less for a conservative 2-D explicit stability bound. It is a finite-step teaching solver, not a claim of convergence to a unique continuum solution.

## Scope and limits

All methods accept finite, non-empty 2-D arrays. Gaussian, Laplacian and median use reflected boundaries; diffusion uses replicated edge values. Bilateral uses reflected samples and circular support. Direct bilateral loops are intended for small arrays. The methods do not infer CRS, physical pixel spacing, sensor noise, or appropriate parameter values.

Total-variation denoising, non-local means, guided filtering, anisotropic tensor diffusion, multiscale methods, edge-aware adaptive parameter estimation and production acceleration remain open.

## Verification

Independent formula and invariant tests cover constant-field preservation, Gaussian symmetry, the Laplacian of a quadratic interior, a separately computed median-window oracle, bilateral edge preservation, diffusion variance reduction and invalid inputs. See the [verification record](../catalog/verification/spatial-image-filtering.md).
