# Verification dossier: spatial spectral analysis

## Implemented scope

The package contains a 2-D periodogram, EOF analysis, univariate SSA, maximum covariance analysis, ridge-regularised CCA and Welch magnitude-squared coherence.

## Independent checks

Tests use a known sinusoidal spatial frequency, physical frequency spacing, constant-field zero power, full-rank EOF reconstruction and orthonormal modes, SSA reconstruction from all components, orthonormal MCA patterns, a perfectly linearly related CCA pair, and identical-signal Welch coherence. Invalid data, dimensions, windows, modes, and regularisation controls are also tested.

## Assumptions and exclusions

The methods assume finite regularly sampled inputs and common time alignment where required. They do not implement MSSA, wavelet coherence, Hilbert–Huang transforms, spatially adaptive spectra or uncertainty calibration. The source entry remains Partial because several named methods and its full bibliographic/technical review are still outstanding.
