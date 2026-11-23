# Fully Constrained Least Squares (FCLS) unmixing

## Purpose

Linear spectral unmixing estimates per-pixel material fractions from a set of endmember spectra. FCLS enforces nonnegative abundances that sum to one.

## Implemented scope

The SciPy reference solves one constrained least-squares problem per pixel using SLSQP and returns abundance fractions, reconstructed spectra, RMSE and convergence flags. See [implementation](../../implementations/python/fcls-unmixing/README.md).

## Assumptions and cautions

The endmember matrix must be spectrally aligned with the input cube. The linear mixture and sum-to-one assumptions may fail with shade or unmodelled materials. Inspect solver flags and residuals. This is not spatially regularised unmixing.
