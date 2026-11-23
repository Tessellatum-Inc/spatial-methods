# Implementation verification — G, F and J nearest-neighbour functions

The implementation computes:
- G from each observed event's nearest other event distance;
- F from each supplied test location's nearest observed event distance;
- J as the ratio (1-G)/(1-F), with NaN when the denominator is zero.

Verification uses an independent nested-loop Euclidean-distance oracle, including seeded patterns of different event and test-sample sizes. Additional cases cover duplicate events, inclusive radius ties, zero denominators and invalid inputs.

The implementation is uncorrected and planar. It does not generate the F test sample, estimate intensity, correct window-edge bias or perform CSR simulation inference. For a meaningful F estimate, callers must provide independent uniform test locations in the observation window.

Reproduce from implementations/python/ripley-k with `python -m pytest -q`.
