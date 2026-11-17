# Spatial and multivariate spectral analysis

## Scope

This record covers a bounded set of spectral methods for gridded and multivariate spatial data: two-dimensional periodograms, empirical orthogonal functions (EOFs), univariate singular-spectrum analysis (SSA), maximum covariance analysis (MCA), canonical correlation analysis (CCA), and Welch cross-spectral coherence.

## Methods

- **2-D periodogram:** Fourier power on a regularly sampled rectangular field after mean removal and optional separable Hann taper. Frequency axes are expressed in inverse coordinate units from the supplied row and column spacing.
- **EOF:** SVD of a time-by-space anomaly matrix. Spatial modes are right singular vectors; principal component scores are left singular vectors scaled by singular values.
- **SSA:** SVD of the univariate trajectory matrix followed by anti-diagonal averaging of rank-one matrices to recover component series.
- **MCA:** SVD of the cross-covariance matrix between two time-aligned multivariate fields.
- **CCA:** SVD of a ridge-whitened cross-covariance matrix to obtain paired linear canonical variates.
- **Welch coherence:** Segment-averaged magnitude-squared cross-spectrum divided by the product of the two autospectra.

## Assumptions

Inputs are finite and regularly sampled. Gridded periodograms require known planar sample spacing; multivariate methods require time-aligned rows. EOF and MCA mode signs are arbitrary. CCA ridge regularisation changes the canonical objective and must be reported.

## Not covered

Multichannel MSSA, wavelet coherence, Hilbert–Huang transforms, spatially adaptive spectral estimation, causal spectral methods, missing-data imputation, irregular-grid spectral estimation and inferential confidence bands remain separate work.
