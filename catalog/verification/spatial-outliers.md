# Verification — spatial outlier diagnostics

**Status:** Partial; the tests verify the scoped descriptive baselines only.

## Coverage

- Global population Z scores, including constant-column behaviour.
- Spatial scatterplot inputs against a hand-computed row-standardised lag.
- All-pairs variogram cloud distances and semivariances against a three-point analytic example.
- Brute-force LOF on a compact cluster with an isolated point and on a uniform square.
- Gaussian distance-weighted local scores on a synthetic local spike.
- Invalid dimensions, mismatched lengths, invalid weights, k and radius.

Run with `python -m pytest -q` from the package directory.

## Not verified / not implemented

No calibrated p-values, isolation forest, formal variogram-cloud test, automatic neighbourhood or bandwidth selection, CRS transformations, edge correction, spatial multiple-testing control, or large-data performance guarantees are claimed.
