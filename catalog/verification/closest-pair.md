# Verification record: closest pair

## Implementation

- **Code:** `implementations/python/closest-pair/closest_pair.py`
- **Tests:** `implementations/python/closest-pair/test_closest_pair.py`
- **Algorithm:** divide and conquer with x/y presorting and a y-ordered split strip
- **Claimed complexity:** O(n log n) time; the transparent recursive implementation allocates O(n log n) temporary list/set storage across levels
- **Numerics:** finite binary floating-point coordinates; no exact predicates

## Verification design

The test suite compares computed distances against an independent quadratic pairwise oracle over seeded random clouds for sizes 2 through 89, eight clouds per size. It also covers duplicate coordinates, collinear points, negative coordinates, deterministic repeated calls and invalid inputs.

The test suite is committed, but its execution status must be taken from the GitHub Actions run for the commit containing it. Do not treat the presence of tests as evidence that they passed.
