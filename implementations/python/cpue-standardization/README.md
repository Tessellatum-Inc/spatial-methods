# CPUE standardization

Install and test with `python -m pip install -r requirements.txt && python -m pytest -q`.

`fit_cpue_model` fits an effort-offset log-linear model for non-negative integer catch using either a Poisson or NB2 likelihood. The log of effort enters as a fixed offset, so coefficients describe catch rate conditional on effort. The standardized index is predicted catch at unit effort and the sample mean covariate vector. `predict_cpue` applies the fitted model to new covariates and effort.

This is a GLM-like baseline, not a GAM or VAST implementation. It has no smooth terms, spatiotemporal random effects, zero inflation, vessel effects, catchability changes, stock dynamics, survey design correction or fishing-effort allocation. Optimizer convergence and model diagnostics should be checked; the reported index is conditional on the supplied covariates and model form.
