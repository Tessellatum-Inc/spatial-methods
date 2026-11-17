# Verification — empirical spatial-extremes dependence

**Status:** Partial implementation of the source-listed spatial extremes family.

## Implemented

- Pairwise empirical F-madogram from block maxima.
- Average-rank handling for ties and pairwise-complete handling of NaN.
- Pairwise sample counts and optional Euclidean coordinate distances.
- Pairwise extremal-coefficient transform under the max-stable relationship.
- Input validation for dimensions, infinities, minimum pair counts and coordinates.

## Independent checks

- Perfectly comonotone synthetic series provide the exact oracle nu_F=0 and theta=1.
- Independent random series are checked against the asymptotic independence values nu_F=1/6 and theta=2 with finite-sample tolerances.
- Missing-data counts, symmetry, ties and coordinate-distance calculations are tested separately.

Run from this package directory: python -m pytest -q.

## Not covered

Marginal GEV/Gumbel estimation, Brown–Resnick or other max-stable process fitting, spatial copulas, likelihood/composite-likelihood inference, confidence intervals, bootstrap uncertainty, spatial prediction and extremal-coefficient variogram fitting.
