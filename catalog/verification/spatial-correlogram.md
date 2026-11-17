# Verification record: distance-band Moran correlogram

## Implemented scope

- Symmetric binary adjacency constructed independently for each Euclidean distance band.
- Half-open bands, with the final upper edge included.
- Global Moran's I, link count and randomisation expectation for each band.
- Optional row-standardised weights; isolates remain zero rows.
- Empty bands return a null statistic.

## Tests

Tests compare the first distance band with the standalone global Moran's I statistic, check band-specific link counts, exercise row standardisation and empty bands, and reject misaligned, non-finite and invalid band inputs.

## Limits

No permutation inference, simultaneous envelope, multiple-testing correction, adaptive band selection, edge correction or non-Euclidean distance support. This record verifies the descriptive baseline only.
