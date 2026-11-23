# Spatial lag 2SLS: instrument the endogenous spatial lag

Stable ID: `SA-STAT-SPATIAL-LAG-2SLS` · Source compendium section 2 · Teaching estimator

## Why ordinary least squares is not enough

The spatial lag model is:

[
y=ho Wy+Xeta+arepsilon
]

The lagged response (Wy) is endogenous: the reduced form feeds disturbances and outcomes across the network, so (Wy) is generally correlated with (arepsilon). Ordinary least squares therefore does not generally provide consistent estimates of (ho) and (eta).

## Instrumental-variable idea

Rearrange the model's reduced form:

[
E[ymid X]=(I-ho W)^{-1}Xeta
=Xeta+ho WXeta+ho^2W^2Xeta+cdots
]

This motivates using exogenous covariates and their spatial lags as instruments for (Wy). A common teaching instrument set is (Z=[X,WX]), with higher-order lags considered when justified and relevant.

Let (Q=[Wy,X]) be the structural regressor matrix and (P_Z=Z(Z'Z)^{-1}Z') the projection onto the instrument space. The two-stage least-squares estimate is:

[
hat	heta_{2SLS}=(Q'P_ZQ)^{-1}Q'P_Zy
]

where the first element of (hat	heta) estimates (ho), and the remaining elements estimate (eta).

## What the repository implementation does

The dense NumPy baseline constructs instruments as (X,WX,ldots,W^qX), with the maximum spatial-lag order controlled by `instrument_orders`. It removes linearly dependent instrument columns in stable order, which avoids duplicating an intercept when row-standardised weights map the constant column back to itself.

It then projects the structural regressors and response onto the instrument space and solves the 2SLS least-squares system. The implementation deliberately does not report standard errors.

## Assumptions and limitations

- (X) must be exogenous.
- The selected spatial lags of (X) must be valid instruments: correlated with (Wy), but uncorrelated with the structural disturbance.
- Instrument relevance and rank must be checked; the code rejects an underidentified projected design.
- Instrument validity is a substantive assumption, not something this implementation proves.
- The baseline assumes the specified spatial lag model and does not correct for spatially autocorrelated errors.
- It does not implement Kelejian–Prucha heteroskedasticity-robust GMM, weak-instrument diagnostics, finite-sample corrections or coefficient uncertainty.
- Dense matrices are intended for small teaching cases.

## Reproducible synthetic example

~~~python
import numpy as np
from spatial_2sls import spatial_lag_2sls

rng = np.random.default_rng(2026)
n = 80
W = np.zeros((n, n))
for i in range(n - 1):
    W[i, i + 1] = W[i + 1, i] = 1
W = W / W.sum(axis=1, keepdims=True)
x = np.column_stack([np.ones(n), rng.normal(size=n)])
rho = 0.3
beta = np.array([1.2, 0.8])
epsilon = rng.normal(scale=0.15, size=n)
y = np.linalg.solve(np.eye(n) - rho * W, x @ beta + epsilon)

fit = spatial_lag_2sls(y, x, W, instrument_orders=1)
print("rho:", fit.rho)
print("beta:", fit.beta)
~~~

The generated values are synthetic and are used to test recovery under the stated data-generating process. Real applications require a defensible instrument argument and diagnostics beyond coefficient recovery.

## References

- Anselin, L. (2003). “Spatial Econometrics.” In *A Companion to Theoretical Econometrics*, Chapter 14, especially the discussion of the reduced form and spatial two-stage least squares. [Chapter PDF](https://web.pdx.edu/~crkl/WISE/SEAUG/papers/anselin01_CTE14.pdf).
- Kelejian, H. H. and Prucha, I. R. (1998). “A generalized spatial two-stage least squares procedure for estimating a spatial autoregressive model with autoregressive disturbances.” *Journal of Real Estate Finance and Economics*, 17, 99–121.
- [Spatial Data Science: Spatial Econometrics Models](https://r-spatial.org/book/17-Econometrics.html).

## Repository implementation

- [Spatial econometrics package](../../implementations/python/spatial-econometrics/README.md)
- [2SLS source](../../implementations/python/spatial-econometrics/spatial_2sls.py)
- [Tests](../../implementations/python/spatial-econometrics/test_spatial_econometrics.py)
