# Raster box-counting, lacunarity and Hurst diagnostics

For a binary raster support, box-counting dimension is estimated from the slope of log occupied-box count against log inverse box width. Partial edge boxes are included. This is a finite-scale estimator, not a proof of an asymptotic fractal dimension.

Gliding-box lacunarity uses the occupancy mass M of each sliding window of fixed width and reports E[M²]/E[M]². It captures variation in gap/cluster structure at the chosen scale; zero-occupancy support has no defined ratio.

For a scalar raster, the Hurst baseline pools horizontal and vertical semivariances at each lag h and fits log gamma(h) = c + 2H log h. The estimate is descriptive and depends on a power-law scaling interval and approximate isotropy.

These methods do not implement multifractal spectra, scale-space theory, formal MAUP sensitivity experiments, directional/anisotropic H estimation, confidence intervals or robust multi-origin box-counting. Raster spacing must be uniform and known; the Hurst estimate is not invariant to trends or arbitrary preprocessing.
