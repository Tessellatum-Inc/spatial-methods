# Piecewise-constant inhomogeneous Poisson process simulation

An inhomogeneous Poisson process has a spatially varying first-order intensity
\(\lambda(s)\). For a supplied rectangular grid of cellwise-constant
intensities, each cell count is an independent Poisson random variable with
mean \(\lambda_j |A_j|\), and event locations conditional on each count
are independent uniform points within that cell.

The implementation accepts a non-negative intensity raster in events per
squared coordinate unit and a rectangular window. It partitions the window
into equal-sized cells, samples independent Poisson counts and then samples
uniform event locations inside each cell. The result is exact for this
piecewise-constant intensity model, not an approximation to an internally
fitted continuous intensity surface.

## Limits

No intensity estimation, kernel bandwidth selection, covariate model,
log-Gaussian Cox dependence, irregular observation window or inferential
procedure is included. Cells are independent by construction; spatial
dependence beyond the deterministic intensity surface is absent.

## Runnable implementation

[Point-process package, tests and model documentation](../../implementations/python/point-process/README.md).

## References

- Baddeley, A., Rubak, E., & Turner, R. (2015). *Spatial Point Patterns:
  Methodology and Applications with R*. Chapman & Hall/CRC.
- Møller, J., & Waagepetersen, R. P. (2004). *Statistical Inference and
  Simulation for Spatial Point Processes*. Chapman & Hall/CRC.
