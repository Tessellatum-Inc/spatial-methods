# Mann-Kendall trend test, seasonal Mann-Kendall and Sen's slope

The Mann-Kendall statistic is the sum of signs of all pairwise temporal
differences:

    S = sum_{i<j} sign(x_j - x_i)

Its variance includes a correction for tied values. The reference method
uses a continuity-corrected normal approximation for the two-sided p-value
and reports Kendall tau-b. Sen's slope is the median of pairwise slopes:

    beta = median((x_j - x_i) / (t_j - t_i))

The implementation accepts an optional strictly increasing time coordinate
and reports a median intercept.

## Seasonal Mann-Kendall

For seasonal observations, compare only pairs that share a season label.
Compute each season's Mann-Kendall score and tie-corrected variance, then sum
the scores and variances across seasons. Apply the continuity-corrected
normal approximation to the combined statistic. The seasonal Sen estimator
takes the median of slopes formed only by within-season pairs.

This implementation does not correct serial correlation within seasons,
dependence between seasons, missingness mechanisms or multiple testing. Its
p-value is not an exact small-sample test. Assess dependence and sampling
structure before interpreting significance.

See the dependency-free Python package for tests and usage.
