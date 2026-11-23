# Neyman allocation and stratified estimation

## Purpose

Stratified sampling divides a finite target population into non-overlapping
strata, selects a probability sample within each stratum, and combines the
stratum estimates using known population sizes. It is useful when meaningful
subgroups differ in variability or when estimates are required for each
subgroup as well as for the population total.

## Equal-cost Neyman allocation

For a fixed total sample size (n), stratum population size (N_h), and
planning standard deviation (S_h), the continuous equal-cost allocation is

\[
n_h^*=n\frac{N_hS_h}{\sum_{k=1}^{H}N_kS_k}.
\]

This allocation minimises the variance of the stratified total under the
usual stratified simple-random-sampling assumptions when per-unit costs are
equal and the (S_h) values are suitable planning estimates. Integer
allocations require rounding; the reference implementation uses a
deterministic largest-remainder rule, enforces at least one observation per
stratum, and caps allocations at the finite stratum population.

If every planning standard deviation is zero, the implementation falls back
to proportional allocation by (N_h). This is an operational fallback, not
evidence that the population is truly constant.

## Estimation

For realised stratum sample mean \(\bar y_h\), the estimated population
total is

\[
\widehat T_{st}=\sum_{h=1}^{H}N_h\bar y_h,
\]

and the estimated population mean is

\[
\widehat{\bar Y}_{st}=\frac{\widehat T_{st}}{N},
\qquad N=\sum_{h=1}^{H}N_h.
\]

For independent simple random samples without replacement within strata,
the estimated variance of the total is

\[
\widehat{\operatorname{Var}}(\widehat T_{st})
=\sum_{h=1}^{H}N_h^2
\left(1-\frac{n_h}{N_h}\right)
\frac{s_h^2}{n_h}.
\]

The finite-population correction is zero for a census stratum. A non-census
stratum requires at least two observations to estimate its sample variance.

## Worked synthetic example

For (N=(4000,3500,2500)), (S=(12,20,8)), and (n=200), the unrounded
allocations are approximately ((69.57,101.45,28.99)). The deterministic
integer allocation is ((70,101,29)). If the corresponding synthetic sample
means are ((36,57,23)), then

\[
\widehat T_{st}=4000(36)+3500(57)+2500(23)=401000.
\]

These values are synthetic teaching inputs, not field observations.

## Limitations

- A complete, correctly stratified sampling frame is required.
- The formula assumes equal per-unit costs; unequal costs require a different
  allocation derivation.
- Spatial clustering, unequal inclusion probabilities, nonresponse,
  measurement error and spatial dependence require additional treatment.
- This design is for design-based population estimation. Space-filling
  designs for simulator inputs or prediction are different objectives.
- A large sample does not repair an incomplete frame or biased measurement.

## Implementation

The standard-library reference implementation is in
[implementations/python/stratified-sampling](../../implementations/python/stratified-sampling/README.md).
The [spatial observation and sampling exercise](../../collection/spatial-observation-sampling-exercise.md)
provides a longer design exercise and field-planning discussion.

## References

- Neyman, J. (1934). On the two different aspects of the representative
  method: The method of stratified sampling and the method of purposive
  selection. *Journal of the Royal Statistical Society*, 97(4), 558–625.
- Cochran, W. G. (1977). *Sampling Techniques* (3rd ed.). Wiley.
