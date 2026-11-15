# Minimum Noise Fraction (MNF)

## Purpose

MNF orders spectral components by signal-to-noise rather than by total variance alone. It is useful for reducing hyperspectral or multispectral data dimensionality while prioritising components with stronger signal relative to estimated noise.

## Method

Given signal covariance Cx and noise covariance Cn, the transform whitens noise and diagonalises the whitened signal covariance. Equivalently it solves a generalized symmetric eigenproblem. Components are ordered by descending eigenvalue. The eigenvectors/loadings depend on the selected noise covariance and regularisation.

## Implemented scope

The NumPy implementation accepts a pixel × row × band cube, an optional valid-pixel mask, and a supplied noise covariance or an adjacent-difference estimate. It returns scores, eigenvalues, loadings and covariance diagnostics. See [implementation](../../implementations/python/mnf-transform/README.md).

## Assumptions and cautions

The adjacent-difference estimator assumes locally smooth signal and stationary, spatially independent noise. Edges, texture, striping and correlated noise violate this assumption. Use sensor-calibrated or independently estimated noise covariance where possible. MNF eigenvalues are not PCA explained-variance ratios; eigenvalue regularisation and the noise model must be reported.
