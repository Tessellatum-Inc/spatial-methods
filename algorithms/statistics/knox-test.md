# Knox space-time interaction test

The Knox test examines whether events that are close in space also tend to be close in time. For each unordered event pair, it flags a spatially close pair when distance is no greater than (d_s), and a temporally close pair when absolute time separation is no greater than (d_t). The observed statistic is the number of pairs satisfying both conditions.

The reference implementation holds locations fixed and permutes event times. Its one-sided Monte Carlo p-value is

\[
p=\frac{1+\sum_{b=1}^{B} I(K_b\ge K_{obs})}{B+1},
\]

where (K_b) is the close-pair count in permutation (b). The plus-one correction avoids a zero Monte Carlo p-value.

## Assumptions and limitations

The permutation null assumes temporal labels are exchangeable over fixed event locations. This can be inappropriate under strong temporal trends, varying observation effort, inhomogeneous risk populations or repeated-event dependence. The test does not identify a causal mechanism and does not adjust automatically for selecting thresholds after inspecting the data. Distances are planar; project coordinates into a suitable metric CRS first.

## Verification

Tests cover a constructed clustered event pattern, deterministic permutation reproducibility and invalid dimensions/thresholds.

See the [implementation package](../../implementations/python/knox-test/README.md).
