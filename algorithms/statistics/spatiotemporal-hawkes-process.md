# Spatiotemporal Hawkes point-process simulation

## Model

A Hawkes process is self-exciting: an event raises the conditional intensity of later events. This bounded implementation uses a constant background intensity and a separable triggering kernel with exponential temporal decay and isotropic Gaussian spatial displacement.

The branching representation is used. Immigrants arrive as a homogeneous Poisson process in the study window. Each event independently generates a Poisson number of offspring with mean branching ratio eta. Offspring delays are exponential with rate beta and spatial offsets are bivariate Gaussian with standard deviation sigma on each axis. The branching ratio is restricted to [0, 1), ensuring subcritical clusters.

## Implementation

The implementation is in [spatiotemporal_hawkes.py](../../implementations/python/point-process/spatiotemporal_hawkes.py). It returns chronologically ordered event times, locations, parent indices and generation numbers. A periodic (toroidal) boundary condition wraps offspring locations into the rectangle; this avoids edge loss but represents a periodic study region rather than a planar boundary. A maximum event count guards against accidental memory exhaustion.

This is a simulator only. It does not estimate parameters, implement power-law ETAS triggering, fit spatially varying background intensity, model marks or provide inference/diagnostics. The periodic boundary assumption must be appropriate for the intended synthetic experiment.

## Verification

Tests check seed reproducibility, temporal ordering, parent-child chronology and generation depth, the zero-branching Poisson limit, periodic spatial bounds, invalid parameters and the event safety limit.

## References

- Hawkes, A. G. (1971). Spectra of some self-exciting and mutually exciting point processes. *Biometrika*, 58(1), 83–90. https://doi.org/10.1093/biomet/58.1.83
- Ogata, Y. (1981). On Lewis' simulation method for point processes. *IEEE Transactions on Information Theory*, 27(1), 23–31. https://doi.org/10.1109/TIT.1981.1056305
- Bernabeu, A., Zhuang, J., & Mateu, J. (2025). Spatio-Temporal Hawkes Point Processes: A Review. *Journal of Agricultural, Biological and Environmental Statistics*, 30, 89–119. https://doi.org/10.1007/s13253-024-00653-7

## Rights

Only the published mathematical model and bibliographic metadata are paraphrased; no source code, figures or datasets are reproduced.
