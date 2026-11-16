# Mann-Kendall trend test and Sen's slope

The Mann-Kendall statistic is the sum of signs of all pairwise temporal
differences:

    S = sum_{i<j} sign(x_j - x_i)

Its variance includes a correction for tied values. The reference method
uses a continuity-corrected normal approximation for the two-sided p-value
and reports Kendall tau-b. Sen's slope is the median of pairwise slopes:

    beta = median((x_j - x_i) / (t_j - t_i))

The implementation accepts an optional strictly increasing time coordinate
and reports a median intercept.

The p-value is not an exact test and does not correct serial correlation,
seasonality, missingness or multiple testing. These effects matter for
environmental time series. See the Python package for tests and usage.
