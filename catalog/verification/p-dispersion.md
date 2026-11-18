# Verification — exact p-dispersion

**Implementation:** [Python package](../../implementations/python/p-dispersion/README.md)  
**Walkthrough:** [enumerating max-min subsets](../../implementations/python/p-dispersion/implementation-walkthrough.md)

## Verified scope

- Exact selection of p distinct candidate indices by exhaustive subset enumeration.
- Maximise the minimum pairwise distance within the selected subset.
- Deterministic lexicographic tie handling.
- Input checks for square shape, finite/non-negative values, symmetry, zero diagonal and p bounds.

## Tests

- Known one-dimensional candidate set with an analytically checkable optimum.
- Square geometry with tied optimal diagonals.
- p equal to all candidates.
- Duplicate candidate locations and zero-distance pairs.
- Invalid matrix shapes, asymmetry, non-zero diagonal, non-finite/negative values and invalid p.

## Limits

This is an exact small-instance baseline with combinatorial enumeration. It does not include a scalable branch-and-bound, approximation algorithm, assignment model, capacity, uncertainty, equity or routing constraints. Metric validity and geographic interpretation are the responsibility of the distance-matrix producer.
