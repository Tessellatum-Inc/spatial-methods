# Spatial and multivariate spectral analysis

This package provides compact NumPy reference implementations for:

- two-dimensional periodograms of regularly sampled raster fields;
- empirical orthogonal functions (EOFs) from time-by-space matrices;
- univariate singular-spectrum analysis (SSA) with diagonal-averaged components;
- maximum covariance analysis (MCA) between time-aligned multivariate fields;
- ridge-regularised linear canonical correlation analysis (CCA);
- Welch magnitude-squared cross-spectral coherence.

## Data contracts

Raster periodograms assume a regular rectangular grid with known positive sample spacing. EOF and MCA inputs are rows of time samples and columns of spatial features. CCA inputs must share the same sample rows. SSA accepts one finite, regularly sampled univariate series. Welch coherence accepts equal-length finite vectors and numeric sampling frequency.

The functions do not infer missing values, regrid irregular samples, select trends or seasonal cycles, or convert geographic coordinates. EOF signs and paired-mode signs are arbitrary.

## Limits

These are transparent teaching baselines, not a complete spatial spectral-analysis suite. The package does not implement multichannel MSSA, wavelet coherence, Hilbert–Huang transforms, spectral-domain causal inference, spatially adaptive spectra, or uncertainty calibration. EOF, MCA and CCA are dense SVD/eigendecomposition methods and are intended for matrices that fit in memory.
