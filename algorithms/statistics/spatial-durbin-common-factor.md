# Spatial Durbin common-factor restriction test

Stable ID: `SA-STAT-SDM-COMMON-FACTOR` · Spatial econometrics specification testing

## Hypothesis

The spatial Durbin model is

[
y=ho Wy+Xeta+WXgamma+arepsilon.
]

The common-factor null is

[
H_0:quad gamma+hoeta=0.
]

Under this restriction,

[
(I-ho W)y=(I-ho W)Xeta+arepsilon,
]

which is a spatial-error model with (lambda=ho). The test therefore compares unrestricted SDM maximum likelihood against the nested SEM maximum likelihood.

## Likelihood-ratio statistic

[
LR=2{ell_{SDM}-ell_{SEM}} overset{a}{sim} chi^2_q,
]

where (q) is the number of independently identified columns of (WX) after projection on (X). A spatial lag of a constant under row-standardised weights is collinear with the constant and cannot identify a separate (gamma); it is excluded from (q). The implementation returns the estimated restrictions (hatgamma_j+hathohateta_j) for the retained columns.

## Python

```python
from spatial_durbin_common_factor import spatial_durbin_common_factor_test

result = spatial_durbin_common_factor_test(y, X, W)
print(result.statistic, result.degrees_of_freedom, result.p_value)
print(result.restriction_residuals)
```

## Assumptions and limitations

The reference implementation uses the package's concentrated Gaussian SDM and SEM maximum-likelihood estimators, with the same conservative norm-bounded spatial-parameter interval. The LR reference distribution is asymptotic and conditional on the supplied weights. It relies on correct likelihood specification and regular identification. Small samples, boundary estimates, weakly identified spatial covariates, or optimizer convergence problems can undermine the chi-square approximation. If the unrestricted numerical optimum is materially below the restricted likelihood, the routine raises rather than reporting a negative LR statistic.

This test is not a generic comparison of arbitrary SDM and SEM estimates: it specifically tests the common-factor restriction. Collinear (WX) columns are not separately identified and cannot contribute test degrees of freedom.

## References

- Burridge, P. (1981). Testing for a common factor in a spatial autoregressive model. *Environment and Planning A*, 13(7), 795–800.
- LeSage, J. and Pace, R. K. (2009). *Introduction to Spatial Econometrics*. CRC Press.
- [Concentrated spatial maximum likelihood implementation](../../implementations/python/spatial-econometrics/maximum_likelihood.py).
- [Spatial Durbin implementation](../../implementations/python/spatial-econometrics/spatial_durbin_2sls.py).
