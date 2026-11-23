# PCA implementation verification

The existing pca-transform package implements covariance PCA using the
symmetric sample-covariance eigensystem, descending eigenvalue order,
explained-variance ratios, optional standardization, a boolean valid-row mask
and projection into component space. Independent tests compare eigenvalues
and projected covariance against NumPy references, check masking and
standardization, and reject degenerate data and invalid component counts.

The package also implements a separate sensor-coefficient Tasseled Cap linear
transform. It is not PCA and must use coefficients appropriate to the sensor
and reflectance convention.

Not implemented: factor analysis, MNF/noise covariance whitening, robust PCA,
OAC-style geodemographic classification or spatially constrained PCA.
