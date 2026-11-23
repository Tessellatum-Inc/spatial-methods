# Residual-based GNSS RAIM: global detection and single-fault exclusion baseline

## Problem and model

For one linearised navigation snapshot, write

`y = H x + e,  e ~ N(0, R)`

where `y` contains measurements, `H` is the supplied design matrix, `x` is the unknown state correction and `R` is a known positive-definite measurement covariance. The implementation does not build satellite geometry or produce a complete GNSS position from raw observables.

## Implemented baseline

1. Cholesky-whiten the observations and design matrix using `R = L Lᵀ`.
2. Solve the whitened least-squares problem and compute the weighted residual sum of squares `T = vᵀ R⁻¹ v`.
3. Under the no-fault Gaussian model and full-rank `H`, compare `T` with the upper chi-square quantile having `m - n` degrees of freedom.
4. If the global test alarms, delete each measurement in turn, refit the reduced system and test its residual statistic. The candidate tests use `alpha / m` (Bonferroni) as a conservative family-wise threshold level.
5. Report a measurement index only if exactly one deletion yields a passing subset test. Multiple passing candidates are ambiguous; none means the fault was not isolated.

## Assumptions and limitations

- The linearised model, measurement covariance and Gaussian error assumptions are correct.
- The covariance is known absolutely, not estimated from the same residuals.
- The design matrix has full column rank; every tested reduced design must remain full rank and redundant.
- Only one faulty measurement is hypothesised. Correlated faults, satellite-wide faults, constellation faults and multiple simultaneous faults are outside scope.
- The test is snapshot-based. It does not model temporal correlation, multipath, non-line-of-sight reception, spoofing, receiver faults or atmospheric residual structure.
- A unique deletion is a diagnostic candidate, not a proof of fault origin.
- This implementation does not calculate protection levels, integrity risk bounds, availability, continuity, fault slopes or certified aviation RAIM/ARAIM outputs.

## Relationship to adjacent methods

The global residual test is the conventional consistency check described in RAIM fundamentals. Leave-one-out refitting is a simple fault-exclusion baseline. It is not multiple-hypothesis solution separation, and it is not the same as the separate Baarda local data-snooping implementation in this repository.

## References

- ESA Navipedia. *RAIM Fundamentals* (2011), edited by GMV.
- Joerger, M., Chan, F.-C., & Pervan, B. (2014). Solution Separation Versus Residual-Based RAIM. *NAVIGATION*, 61(4), 273–291. DOI: 10.1002/navi.71.
- Brown, R. G. (1992). A baseline GPS RAIM scheme and a note on the equivalence of three RAIM methods. *NAVIGATION*, 39(3), 301–316.

No source code, text, figures or observation data are reproduced.
