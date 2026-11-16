# Bayesian online change-point detection (BOCPD) baseline

A recursive run-length posterior for sequential observations under a **Gaussian likelihood with known fixed observation variance and an unknown segment mean**. Each segment mean has a Normal prior with configurable prior mean and precision-like concentration parameter. A constant hazard controls the prior probability of a change at each step.

The implementation returns the posterior probability of a change at each observation and the maximum-a-posteriori run length. It supports an optional run-length cap to bound memory.

This is not the full unknown-mean-and-variance Student-t BOCPD model, a general nonparametric detector, or a calibrated spatial/remote-sensing alert system. Hazard, observation variance and prior parameters materially affect results. Serial dependence, seasonality, missingness, multiple pixels and multiple-testing effects are not modelled.

Run tests from this directory:

```bash
python -m pytest -q
```
