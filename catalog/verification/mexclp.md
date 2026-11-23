# Verification record: MEXCLP

## Implemented scope

- Exact small-instance enumeration of p unit placements with replacement.
- Expected coverage under a common independent busy fraction.
- Extension to independent site-specific busy fractions, with the probability all covering units are busy computed as their product.
- Demand weights, service threshold and deterministic lexicographic tie-breaking.

## Tests

Tests cover single and multiple coverage, heterogeneous busy probabilities, equivalence of a constant site-vector to the scalar formulation, deterministic ties, zero-unit and zero-busy limits, and invalid costs, weights, thresholds and busy fractions. CI status is tied to the commit containing the tests.

## Limits

The site-specific vector still assumes independent busy states. It is not the adjusted MEXCLP correction based on random sampling without replacement, nor a hypercube queueing model. It does not calculate busy probabilities from arrival rates, service times, dispatch policy or spatial interaction. Exact enumeration is intended for small candidate sets.

## Bibliography

- Daskin, M. S. (1983). A maximum expected covering location model: Formulation, properties and heuristic solution. *Transportation Science*, 17(1), 48–70. https://doi.org/10.1287/trsc.17.1.48
- Batta, R., Dolan, J. M., & Krishnamurthy, N. N. (1989). The maximal expected covering location problem: Revisited. *Transportation Science*, 23(4), 277–287. https://doi.org/10.1287/trsc.23.4.277

## Rights

Only mathematical definitions and bibliographic metadata are paraphrased; no source code, figures or datasets are reproduced.
