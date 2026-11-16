# Fay–Herriot area-level small-area estimation

Install and test with python -m pip install -r requirements.txt && python -m pytest -q.

The implementation fits the area-level Gaussian model y = X beta + u + e. Direct estimates have known sampling variances; independent area random effects have an unknown common variance. Regression coefficients are estimated by generalized least squares and the between-area variance by ML or REML. The returned empirical-Bayes estimate shrinks each direct estimate toward its regression mean according to its sampling variance.

The returned conditional random-effect variance conditions on fitted parameters. It is not a complete frequentist MSE estimator because it omits uncertainty from estimating beta and the variance component. The model assumes independent Gaussian area effects and known sampling variances. No survey design correction, unit-level model, Horvitz–Thompson estimator, MRP or spatially structured random effect is included.
