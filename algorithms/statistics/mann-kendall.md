# Mann–Kendall and seasonal Mann–Kendall tests

The Mann–Kendall test evaluates monotonic trend using the signed pairwise score

\[
S=\sum_{i<j}\operatorname{sign}(x_j-x_i).
\]

The null variance includes a correction for tied values. A continuity-corrected normal statistic gives a two-sided p-value. Kendall's tau is reported as (S/\binom{n}{2}).

The seasonal variant partitions observations by their position in a fixed-length cycle and compares only observations from the same season. It is suitable only when the sequence is correctly ordered into regular cycles.

## Interpretation and limits

These are rank-based trend tests, not trend-magnitude estimators; pair them with a slope estimator such as Theil–Sen. The normal approximation is used. Serial correlation can inflate false positives and is not corrected here. The methods do not identify structural breaks, handle arbitrary missing seasonal positions, adjust for multiple testing or establish causal drivers.

## Verification

Tests cover increasing/decreasing trends, ties and constant sequences, seasonal comparisons and invalid inputs.

See the [Theil–Sen implementation package](../../implementations/python/theil-sen/README.md).
