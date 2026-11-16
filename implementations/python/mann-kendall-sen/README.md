# Mann-Kendall and Sen trend methods

Dependency-free non-parametric trend summaries for an ordered numeric series.

The Mann-Kendall test counts positive and negative pairwise differences to
form S, applies the standard tie-corrected variance and continuity-corrected
normal approximation, and returns two-sided p-value and Kendall tau-b.
Sen's estimator is the median of all pairwise slopes; the intercept is the
median of value minus slope times time.

## Limits

The p-value is a normal approximation, not an exact small-sample permutation
test. Neither method corrects serial correlation, seasonality, missing
observations or multiple testing. For autocorrelated hydrological/climate
series, use an appropriate prewhitening or variance-correction procedure.
The pairwise slope calculation is O(n^2) in time and memory.

## Tests

    python -m pytest -q
