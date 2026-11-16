# Verification record: classification breaks

## Implemented

Geometric interval, standard-deviation, box-plot, head/tail, Dalenius–Hodges and exact one-dimensional ckmeans break calculations. Each returns ordered boundaries under a documented input contract.

## Tests

Formula and invariant tests cover positivity, observed-range clipping, quartiles/Tukey fences, heavy-tail recursion, histogram-based break ordering, constant data and invalid parameters. The ckmeans dynamic program is compared with exhaustive partition enumeration for small samples.

## Not implemented

“Maximum breaks” and “pretty breaks” remain unresolved names; they require source identity verification. Map symbolisation, class-count selection, multivariate classification and spatially constrained classification are outside this package.
