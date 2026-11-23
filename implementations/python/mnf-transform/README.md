# Minimum Noise Fraction (MNF)

Install requirements and run `pytest -q`. Input is a finite rows × columns × bands cube. The routine centres valid pixels, whitens by the supplied or estimated noise covariance, diagonalises the whitened signal covariance, and returns descending MNF eigenvalues, band loadings and pixel scores. A boolean mask leaves invalid scores as NaN.

The adjacent-difference noise estimator pools horizontal and vertical differences and divides their sample covariance by two. This assumes adjacent signal is locally smooth and noise is stationary and independent between pixels; edges, texture, striping and spatially correlated noise can bias it. Prefer a sensor- or scene-calibrated noise covariance when available. Eigenvalue flooring regularises singular/near-singular noise covariance. MNF eigenvalues are not ordinary PCA explained-variance ratios and should not be interpreted as such.
