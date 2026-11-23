# Moran eigenvector spatial filtering

NumPy implementation of Moran eigenvector extraction from a centered symmetric spatial weights matrix and a fixed-size OLS filter using caller-selected positive eigenvectors.

## Quick start

~~~python
import numpy as np
from moran_filter import moran_eigenvectors, moran_eigenvector_filter

n = 20
weights = np.zeros((n, n))
for i in range(n - 1):
    weights[i, i + 1] = weights[i + 1, i] = 1.0
basis = moran_eigenvectors(weights, n_components=3)
result = moran_eigenvector_filter(y, X, weights, n_components=3)
~~~

## Method

The basis is extracted from H W H, where H = I - 11'/n removes the intercept and W is a symmetric nonnegative spatial weights matrix. Positive eigenvalues are sorted descending; their orthonormal eigenvectors describe distinct positively autocorrelated spatial patterns. The regression adds a caller-selected number of these eigenvectors to an intercept and covariates.

## Scope and limitations

This is a fixed-size teaching baseline, not a full automatic eigenvector spatial filtering procedure. It does not select eigenvectors by residual Moran's I, AIC, p-values or a stepwise criterion; the user supplies the number. The basis uses intercept-only centering, not the general covariate projection M_X W M_X. W must be symmetric, nonnegative and have zero diagonal; row-standardized asymmetric matrices are rejected. No Spatial+, restricted spatial regression, GLM, SAR/CAR likelihood, uncertainty correction or inferential standard errors are implemented.
