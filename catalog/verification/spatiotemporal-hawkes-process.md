# Verification record: spatiotemporal Hawkes simulation

## Implemented scope

- Constant-background immigrant Poisson process in a rectangular spatial window and finite time horizon.
- Branching/cluster simulation with Poisson offspring count and subcritical branching ratio.
- Exponential temporal offspring delay and isotropic Gaussian spatial displacement.
- Periodic (toroidal) spatial boundary condition and chronological parent-index remapping.

## Tests

Tests cover deterministic seeding, sorted event times, valid parent chronology and generation increments, zero-branching Poisson limit, periodic coordinate bounds, invalid parameters and maximum-event protection. CI status is tied to the commit containing the tests.

## Limits

This is a bounded simulator, not an estimator. It assumes constant background intensity, separable exponential/Gaussian triggering, no marks, and periodic spatial boundaries. It is not an ETAS power-law model, does not handle spatially varying background rates, and does not provide likelihood, parameter inference or residual diagnostics.

## Bibliography

- Hawkes, A. G. (1971). Spectra of some self-exciting and mutually exciting point processes. *Biometrika*, 58(1), 83–90. https://doi.org/10.1093/biomet/58.1.83
- Ogata, Y. (1981). On Lewis' simulation method for point processes. *IEEE Transactions on Information Theory*, 27(1), 23–31. https://doi.org/10.1109/TIT.1981.1056305
- Bernabeu, A., Zhuang, J., & Mateu, J. (2025). Spatio-Temporal Hawkes Point Processes: A Review. *Journal of Agricultural, Biological and Environmental Statistics*, 30, 89–119. https://doi.org/10.1007/s13253-024-00653-7
