# Raster fractal diagnostics

NumPy baselines for three raster-based scale diagnostics:

- **Box-counting dimension:** threshold a raster into occupied/unoccupied cells, count occupied boxes at multiple integer scales, and regress log count on log inverse scale. Edge boxes are retained rather than silently cropped.
- **Gliding-box lacunarity:** compute the binary occupancy mass in every valid sliding window using an integral image, then report E[M²] / E[M]². An empty support returns an undefined lacunarity.
- **Hurst scaling estimate:** pool horizontal and vertical empirical semivariances at supplied integer lags and regress log semivariance on log lag; H is half the fitted slope.

## Run

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

## Assumptions and limitations

Inputs are finite, equally spaced 2-D raster grids. Box-counting and lacunarity use a strict value > threshold binary support; they do not infer an optimal threshold. Box counts use one grid origin, so estimates can depend on alignment and selected scales. The Hurst estimate assumes an approximately isotropic power-law variogram over the selected lags; anisotropy, trends, measurement noise and finite-domain effects can bias it. This is not multifractal spectrum estimation, a formal uncertainty interval, or a scale-space/MAUP analysis. Use multiple origins, threshold sensitivity, directional variograms and surrogate tests for defensible research conclusions.
