# Mann-Kendall and Sen trend methods

Dependency-free non-parametric trend summaries for ordered numeric series.

The standard Mann-Kendall test counts pairwise signs, applies the tie-corrected
variance and continuity-corrected normal approximation, and returns a
two-sided p-value and Kendall tau-b. Sen's estimator is the median of all
pairwise slopes; the intercept is the median of value minus slope times time.

## Seasonal methods

`seasonal_mann_kendall(values, seasons)` compares observations only within
matching season labels (for example, January with January). It sums the
within-season scores and tie-corrected variances before applying a
continuity-corrected normal approximation. `seasonal_sen_slope` takes the
median of pairwise slopes whose observations share a season label. Both
accept irregularly spaced time coordinates where applicable.

Season labels must be hashable and aligned with values. At least two
distinct seasons are required; seasonal Sen additionally requires at least
one season with two observations.

## Limits

P-values are normal approximations, not exact small-sample tests. Seasonal
Mann-Kendall does not correct dependence between seasons or serial
correlation within seasons. The standard test does not correct serial
correlation or seasonality. Neither method corrects missing-data mechanisms
or multiple testing. Assess dependence and sampling structure before
interpreting significance. Pairwise slope calculations are O(n²) in time
and memory.

## Tests

    python -m pytest -q
