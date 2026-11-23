# Stratified sampling allocation and estimation

Pure-Python reference methods for finite-population stratified simple random
sampling without replacement.

## Included methods

- **Neyman allocation:** allocates a fixed sample across strata in proportion
  to population size times pilot standard deviation when per-unit costs are
  equal. Integer allocation uses deterministic largest remainders, enforces
  at least one observation per stratum, and respects finite stratum capacity.
- **Stratified total and mean:** combines stratum sample means using known
  population sizes.
- **Variance estimation:** uses the finite-population correction and
  within-stratum sample standard deviations. Census strata contribute zero
  sampling variance.

## Use

```python
from stratified_sampling import neyman_allocation, stratified_total_estimate

allocation = neyman_allocation(
    population_sizes=[4000, 3500, 2500],
    standard_deviations=[12, 20, 8],
    sample_size=200,
)
# (70, 101, 29)

estimate = stratified_total_estimate(
    population_sizes=[4000, 3500, 2500],
    sample_sizes=allocation,
    sample_means=[36, 57, 23],
    sample_standard_deviations=[12, 20, 8],
)
print(estimate.total_estimate, estimate.total_variance_estimate)
```

## Assumptions and boundaries

- The frame is partitioned into mutually exclusive, exhaustive strata with
  known finite population sizes.
- Selection within each stratum is simple random sampling without replacement.
- Neyman allocation assumes equal per-unit costs and pilot standard
  deviations that are useful for planning.
- The variance estimator requires at least two observations in each
  non-census stratum.
- This package does not generate geographic sample locations, calculate
  inclusion probabilities for complex designs, handle nonresponse, cluster
  sampling, unequal costs, adaptive designs or spatially balanced probability
  designs.
- Sampling weights and design-based variance do not correct measurement bias
  or incomplete frames.

## Run tests

```bash
python -m pytest -q
```
