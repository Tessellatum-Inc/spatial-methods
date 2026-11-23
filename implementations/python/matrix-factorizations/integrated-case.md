# Integrated spatial case: control transformation and terrain estimation

This case connects four factorization roles in one synthetic workflow:

1. **Pivoted LU** estimates the two affine coordinate equations from three non-collinear control pairs.
2. **QR** fits a terrain plane by ordinary least squares (OLS), without forming normal equations.
3. **Cholesky** whitens observations under an explicitly assumed correlated-error covariance, after which QR solves the generalized least-squares (GLS) problem.
4. **SVD** diagnoses numerical rank and conditioning of the whitened design matrix.

The transformed sample coordinates feed the terrain model; the same elevation observations are then fitted under two different stochastic assumptions. This is a method-selection exercise, not four disconnected demonstrations.

## Run

From this directory:

```bash
python -m pip install -r requirements.txt
python integrated_case.py
python -m unittest -v
```

The script prints the affine parameters, OLS and GLS plane coefficients, residual summaries, singular values, condition numbers and the explicit numerical-rank tolerance.

## Model and assumptions

The local control coordinates and mapped coordinates are invented dimensionless values. Three non-collinear points exactly determine a 2-D affine transformation; there is no redundancy, outlier detection or independent check point. The sample coordinates are synthetic. Elevation is generated from a plane plus a fixed error vector so the run is deterministic.

The GLS covariance is an assumed AR(1)-style matrix with standard deviation 0.03 and correlation parameter 0.45, ordered by the sample sequence. This ordering is part of the model: it is not a spatial covariance derived from distances, a variogram fit, or a measured sensor process. Cholesky whitening requires the covariance to be symmetric positive definite. A different or misspecified covariance can change the GLS estimate and its interpretation.

## Reading the diagnostics

- The affine control condition number describes the chosen control design in its stated coordinate scale. It is not a universal quality score; coordinate centring and scaling affect it.
- OLS and GLS residual RMS values are in the synthetic elevation units. A smaller raw RMS does not by itself make one estimator statistically preferable.
- The whitened residual norm is evaluated after applying the assumed covariance factor.
- SVD singular values and numerical rank are computed on the whitened design. The tolerance is `machine epsilon × max(matrix dimensions) × largest singular value`. Other tolerances may be appropriate for other scales and error models.
- Full column rank establishes algebraic estimability for this design under the selected numerical threshold; it does not establish precise parameters or a valid physical model.

## Boundaries

This is not a geodetic adjustment, a field-survey workflow, a terrain product, an instrument calibration, or evidence of positional/elevation accuracy. It does not estimate the covariance parameters, handle robust outliers, model spatially varying terrain, propagate control uncertainty, validate a CRS, or provide independent survey checks. It is an instructional integration of standard NumPy/SciPy routines.

For isolated method demonstrations, see [the factorization companion](README.md). For the underlying theory, see [matrix factorizations](../../../foundations/linear-algebra/matrix-factorizations-lu-qr-cholesky-svd.md) and [covariance matrices](../../../foundations/linear-algebra/covariance-matrices-and-multivariate-structure.md).

## Teaching companion

Use the [practical exercise and worked solution](integrated-case-exercise.md) for learner tasks, interpretation questions and a marking guide.
