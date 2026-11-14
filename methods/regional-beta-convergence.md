# Absolute and conditional beta-convergence

## Cross-sectional specification

A standard regional growth-convergence regression relates average log income growth to initial log income:

\[
\frac{1}{T}\log\left(\frac{y_{i,T}}{y_{i,0}}\right)
=\alpha+\beta\log(y_{i,0})+\gamma^T z_i+\epsilon_i.
\]

Without controls \(z_i\), this is an absolute beta-convergence specification. With controls it is conditional beta-convergence: regions are compared conditional on observed steady-state proxies. A negative \(\beta\) is consistent with initially poorer regions growing faster under the specified model. It is not proof of a causal mechanism or convergence of the entire income distribution.

The implied convergence speed per period is

\[
\lambda=-\frac{\log(1+\beta)}{T},
\]

when \(-1<\beta<0\). The corresponding half-life is \(\log(2)/\lambda\). These transformations are not meaningful for arbitrary coefficient values, so the implementation returns no speed or half-life when the estimated slope is nonnegative or at/below -1.

## Implemented baseline

The package fits ordinary least squares with an intercept and initial log income, optionally adding user-supplied controls. It returns coefficients, conventional OLS standard errors, HC1 heteroskedasticity-robust standard errors, residuals, R-squared, and convergence speed/half-life when defined.

## Spatial interpretation and limitations

This is a cross-sectional baseline, not a spatial econometric model. Regional growth residuals may be spatially autocorrelated, and ignoring that dependence can invalidate conventional inference or change the specification. Rey and Montouri (1999) demonstrate why spatial dependence matters in regional convergence analysis. A spatial lag/error model, spatial panel estimator, time-varying coefficient model, endogeneity strategy and robust inference for small samples are not implemented here. HC1 adjusts for heteroskedasticity only; it does not correct spatial dependence, serial correlation, omitted variables or endogenous initial income.

Report the spatial weights, diagnostics and model specification when moving beyond this baseline. Beta-convergence is distinct from sigma-convergence and from Markov distribution dynamics.

## Reproduction

Run from implementations/python/regional-dynamics:

~~~bash
python -m pytest -q --import-mode=importlib
~~~

## References

- Barro, R. J., & Sala-i-Martin, X. (1992). Convergence. *Journal of Political Economy*, 100(2), 223–251. DOI: 10.1086/261816.
- Rey, S. J., & Montouri, B. D. (1999). US regional income convergence: A spatial econometric perspective. *Regional Studies*, 33(2), 143–156. DOI: 10.1080/00343409950122945.
- Rey, S. J. (2001). Spatial Empirics for Economic Growth and Convergence. *Geographical Analysis*, 33(3), 195–214. DOI: 10.1111/j.1538-4632.2001.tb00444.x.

No source code, figures or datasets are reproduced.
