# Verification record: distance-band Moran correlogram

## Implemented scope

- Symmetric binary adjacency constructed independently for each Euclidean distance band.
- Half-open bands, with the final upper edge included.
- Global Moran's I, link count and randomisation expectation for each band.
- Optional row-standardised weights; isolates remain zero rows.
- Optional shared random-labelling permutations across bands.
- Two-sided pseudo p-values and single-step max-statistic family-wise adjustment.

## Tests

Tests compare the first distance band with standalone global Moran's I,
check link counts and empty bands, exercise row standardisation, compare
single-band permutation inference with the existing global Moran
permutation oracle, check reproducibility and maxT conservativeness, and
reject invalid band/permutation inputs.

## Limits

No simultaneous confidence envelope, adaptive band selection, edge
correction or non-Euclidean distance support. The maxT adjustment is based
on standardized permutation departures and is a single-step family-wise
procedure; it is not a step-down Westfall–Young method.
