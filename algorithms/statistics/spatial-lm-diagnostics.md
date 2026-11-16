# Spatial LM diagnostics: lag or error dependence?

Stable ID: `SA-STAT-SPATIAL-LM-DIAGNOSTICS` · Source compendium section 2 · Teaching implementation

## Why diagnose spatial dependence after OLS?

A conventional linear regression assumes that, conditional on the included predictors, the unexplained component has the required independence structure. Spatial data can violate that assumption in different ways.

- **Spatial lag dependence** places interaction in the response: neighbouring outcomes help determine the outcome at each location.
- **Spatial error dependence** places spatial structure in the disturbance: omitted or unobserved influences are spatially correlated.

These are different models, not two labels for the same residual pattern. Anselin's spatial econometrics review distinguishes substantive dependence in the response from nuisance dependence in the error process.

## The two classic score tests

Fit the null OLS model:

[
y=Xeta+e,qquad hatsigma^2=e'e/n
]

Let (W) be the supplied spatial weights matrix, with zero diagonal. Define:

[
T=operatorname{tr}(W'W+W^2)
]

The classic LM-error statistic is:

[
LM_{	ext{error}}=
rac{(e'We/hatsigma^2)^2}{T}
]

For the lag test, let (M=I-X(X'X)^{-1}X'). Then:

[
D=rac{(WXhateta)'M(WXhateta)}{hatsigma^2}+T
]

[
LM_{	ext{lag}}=
rac{(e'Wy/hatsigma^2)^2}{D}
]

Under their respective null hypotheses and regularity conditions, each classic statistic is asymptotically (chi^2_1).

## Interpretation and limitations

Each classic test asks whether the OLS null is locally inconsistent with one specified spatial alternative. The classic tests can both respond to the other form of dependence. Robust Bera-Yoon score tests adjust for the competing alternative. Define the scores \(d_\rho=e'Wy/\hat\sigma^2\), \(d_\lambda=e'We/\hat\sigma^2\), and retain \(D\) and \(T\) above. Then the robust lag test is

\[
RLM_{lag}=\frac{(d_\rho-d_\lambda)^2}{D-T}
\]

while the robust error test is

\[
RLM_{error}=\frac{(d_\lambda-(T/D)d_\rho)^2}{T(1-T/D)}.
\]

Each is asymptotically chi-square with one degree of freedom under its null. If \(D-T\) is numerically zero, the implementation returns both robust results as unavailable rather than dividing by a degenerate adjustment term. Do not mechanically select a model from the largest statistic.

The tests do not estimate a spatial lag or error model. In particular, OLS is generally inconsistent for a model with a spatially lagged dependent variable because (Wy) is endogenous. Use a maintained spatial econometrics package for SAR/SEM estimation, robust diagnostics, uncertainty estimates and model comparison.

The implementation:
- estimates the null OLS coefficients by least squares;
- calculates both classic and robust Bera-Yoon LM-lag/LM-error statistics;
- uses the maximum-likelihood residual variance (e'e/n) in the score formulas;
- accepts finite non-negative weights as supplied and does not standardise them;
- reports one-degree-of-freedom asymptotic chi-square upper-tail p-values;
- uses dense NumPy matrices and is intended for small teaching examples.

## Reproducible Python example

~~~python
import numpy as np
from diagnostics import spatial_lm_diagnostics

x = np.column_stack([np.ones(5), [0., 1., 2., 3., 4.]])
y = [1.0, 2.1, 2.8, 4.2, 4.9]
w = np.zeros((5, 5))
for i in range(4):
    w[i, i + 1] = w[i + 1, i] = 1.0

result = spatial_lm_diagnostics(y, x, w)
print("LM lag:", result.lm_lag)
print("LM error:", result.lm_error)
print("Robust LM lag:", result.robust_lm_lag)
print("Robust LM error:", result.robust_lm_error)
~~~

## References

- Anselin, L. (2003). “Spatial Econometrics.” In *A Companion to Theoretical Econometrics*, Chapter 14. Equations 14.31–14.32 give the classic LM-error and LM-lag tests and explain their asymptotic chi-square reference. [Chapter PDF](https://web.pdx.edu/~crkl/WISE/SEAUG/papers/anselin01_CTE14.pdf).
- Anselin, L. (1988). “Lagrange multiplier test diagnostics for spatial dependence and spatial heterogeneity.” *Geographical Analysis*, 20, 1–17.
- Anselin, L., Bera, A., Florax, R. and Yoon, M. (1996). “Simple diagnostic tests for spatial dependence.” *Regional Science and Urban Economics*, 26, 77–104.
- [Spatial Data Science: Spatial Econometrics Models](https://r-spatial.org/book/17-Econometrics.html), for current model definitions and the broader SAR, SEM, SDM, SDEM and SAC family.

## Repository implementation

- [Implementation package](../../implementations/python/spatial-econometrics/README.md)
- [Diagnostic source](../../implementations/python/spatial-econometrics/diagnostics.py)
- [Tests](../../implementations/python/spatial-econometrics/test_spatial_econometrics.py)

This is a classic and robust LM teaching implementation, not a production estimator or a complete specification-testing suite.
