# Poisson pseudo-maximum likelihood for gravity models

## Model and motivation

A gravity-style conditional mean is multiplicative:

\[ E[y_i\mid x_i]=\exp(o_i+x_i^\top\beta), \]

where outcomes are nonnegative and the offset is known. PPML estimates the conditional mean directly. Unlike OLS on log outcomes, it retains zero observations and avoids the log-linearization problem under heteroskedasticity identified by Santos Silva and Tenreyro (2006).

## Implemented baseline

The NumPy routine uses Newton/IRLS scoring, step halving, an optional known offset and an HC0 sandwich covariance estimate. Include an intercept explicitly if desired. The pseudo-log-likelihood omits the parameter-independent log-factorial term. For logged continuous predictors, coefficients are elasticities; indicator coefficients are semi-elasticities.

## Scope and limitations

This is a small cross-sectional estimator, not a production structural-gravity workflow. It does not absorb exporter/importer/pair/time fixed effects, cluster standard errors, detect and remove separated observations, or implement high-dimensional fixed-effect algorithms. Separation, severe collinearity or poor scaling can prevent convergence. HC0 does not replace clustering when dyadic or panel dependence is present.

## Reproducibility

Run `python -m pytest -q --import-mode=importlib` in `implementations/python/regional-dynamics`. The lab uses synthetic bilateral flows and is not a reproduction of published trade tables.

## Primary references

- Santos Silva, J. M. C. and Tenreyro, S. (2006). The Log of Gravity. Review of Economics and Statistics, 88(4), 641–658. https://doi.org/10.1162/rest.88.4.641.
- Santos Silva, J. M. C. and Tenreyro, S. (2022). The Log of Gravity at 15. Portuguese Economic Journal, 21, 423–437. https://doi.org/10.1007/S10258-021-00203-w.

## Related spatial-interaction specifications

The [constrained gravity-flow family](../algorithms/spatial-interaction/gravity-flow-models.md) implements unconstrained, production-constrained, attraction-constrained and doubly constrained allocation, plus an exponential-cost entropy-maximising variant solved by iterative proportional fitting. This is an aggregate flow-allocation baseline, distinct from the cross-sectional PPML regression above. Negative-binomial estimation, high-dimensional fixed effects, competing-destination and intervening-opportunity variants remain open.
