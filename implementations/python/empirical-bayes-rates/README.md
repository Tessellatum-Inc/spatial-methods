# Empirical Bayes rate smoothing

A dependency-free implementation of Roger Marshall's moment-based global and local shrinkage estimators for Poisson disease/mortality rates.

## Quick start

~~~python
from empirical_bayes import global_empirical_bayes, local_empirical_bayes
counts = [2, 8, 20, 5]
person_years = [1000, 1000, 1000, 1000]
global_result = global_empirical_bayes(counts, person_years)
neighbors = [[0, 1], [0, 1, 2], [1, 2, 3], [2, 3]]
local_result = local_empirical_bayes(counts, person_years, neighbors)
~~~

## Model and estimator

For area i, counts follow a conditionally independent Poisson model with mean exposure times unknown rate. The pooled rate estimates the common prior mean m. A population-weighted rate variance S² estimates total marginal variation; subtract the expected Poisson sampling component to estimate between-area variance A:

- m = sum(y_i) / sum(e_i)
- crude rate x_i = y_i / e_i
- S² = sum(e_i (x_i - m)²) / sum(e_i)
- A = max(0, S² - m / mean(e_i))
- C_i = A / (A + m/e_i)
- estimate = m + C_i (x_i - m)

The local estimator repeats the same moment calculation within each caller-supplied neighbourhood and shrinks the focal area's rate toward that local pooled rate.

## Assumptions and limitations

Counts are nonnegative integers, exposures strictly positive, and areas conditionally independent under the sampling model. Global shrinkage ignores geography and is invariant to area order. Local shrinkage depends on the supplied neighbourhood graph and a local homogeneity assumption. This package does not construct contiguity, fit covariates, adjust age structure, model spatially correlated random effects, calculate posterior intervals or provide a full disease-mapping model. It is not a cluster significance test.
