# Spatial and image filtering baselines

NumPy-only reference implementations for five distinct filters:

- Gaussian smoothing: separable, unit-sum 1-D kernels, reflected boundaries.
- Laplacian: four-neighbour discrete second derivative; a response operator, not by itself an edge-preserving denoiser.
- Median: square-window rank filter with reflected boundaries.
- Bilateral: circular neighbourhood with spatial and intensity Gaussian weights; direct-loop computational cost.
- Perona-Malik anisotropic diffusion: explicit four-neighbour update with exponential or reciprocal conductance and the conservative 2-D stability restriction step <= 0.25.

Inputs are finite, non-empty 2-D numeric arrays. Parameters and boundary conventions are explicit. These are pedagogical baselines, not substitutes for optimized production image libraries. Total-variation denoising, non-local means, guided filtering, multiscale diffusion, calibrated noise models and spatially adaptive parameter selection are not included.

Run pytest -q in this directory.
