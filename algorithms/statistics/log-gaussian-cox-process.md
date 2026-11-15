# Log-Gaussian Cox process

## Question

How can a point process represent spatially varying intensity where nearby locations tend to share high or low event rates?

## Model

A log-Gaussian Cox process (LGCP) is a Cox process driven by a random intensity field. Conditional on the field, events form an inhomogeneous Poisson process:

\[
X\mid\Lambda\sim\operatorname{PoissonProcess}(\Lambda(s)),
\qquad
\Lambda(s)=\exp\{Y(s)\}.
\]

Here \(Y(s)\) is a Gaussian random field. For a stationary construction, one possible covariance is the exponential model

\[
\operatorname{Cov}(Y(s),Y(t))
=\sigma^2\exp\left(-\frac{\lVert s-t\rVert}{a}\right).
\]

If the desired marginal mean event intensity is \(\lambda\), set
\(Y(s)=\log\lambda+Z(s)-\sigma^2/2\), where \(Z\) has mean zero and variance \(\sigma^2\). The subtraction of half the variance ensures \(E[\Lambda(s)]=\lambda\). Conditional Poisson variation is layered on top of the spatially correlated random intensity.

## Discretised simulation

The package implementation samples the Gaussian field at regular grid-cell centres using a dense covariance matrix and Cholesky factorisation. It treats the resulting intensity as piecewise constant within each cell, draws a conditional Poisson count per cell, then places events uniformly inside that cell.

This is an explicit grid approximation, not an exact continuous-field LGCP simulation. Dense Cholesky costs cubic time and quadratic memory in the number of cells; the teaching implementation therefore caps the grid at 225 cells. Grid resolution, covariance family and range should be sensitivity-tested. The implementation uses a stationary exponential covariance and a rectangular planar window.

Function: `simulate_log_gaussian_cox_process(window, mean_intensity, variance, correlation_range, nx=8, ny=8, seed=0)`.

## Interpretation

- \(\lambda\) controls the marginal mean event intensity.
- \(\sigma^2\) controls the variance of the latent log-intensity. At zero variance, the model reduces to a homogeneous Poisson process in distribution.
- \(a\) controls the spatial correlation range of the latent field.
- The latent field induces clustering even though events are conditionally Poisson and conditionally independent given the field.

## Limitations

This implementation is a small-grid simulator, not a fitted LGCP. It does not estimate covariance parameters, use SPDE/spectral approximations, handle irregular polygon windows, model covariates or perform goodness-of-fit inference. It should not be used for large grids: the dense covariance and Cholesky calculation are intentionally capped. For production inference, use a specialised spatial point-process or latent Gaussian modelling package.

## References

- Møller, J., Syversveen, A. R. and Waagepetersen, R. P. (1998). “Log Gaussian Cox processes.” *Scandinavian Journal of Statistics*, 25(3), 451–482. [DOI: 10.1111/1467-9469.00115](https://doi.org/10.1111/1467-9469.00115).
- Baddeley, A., Rubak, E. and Turner, R. *Spatial Point Patterns: Methodology and Applications with R*. See the spatstat documentation for LGCP model fitting and simulation.
