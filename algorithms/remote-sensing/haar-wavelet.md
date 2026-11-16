# 2-D Haar wavelet transform

## Purpose

Wavelet transforms represent imagery at multiple spatial scales and orientations. They separate a coarse approximation from horizontal, vertical and diagonal detail coefficients and are useful in multiscale analysis, compression and denoising workflows.

## Implemented scope

The reference implementation performs orthonormal, critically sampled 2-D Haar (Daubechies-1) decomposition and exact inverse reconstruction, recursively decomposing the approximation subband. Each level requires even dimensions. See [implementation](../../implementations/python/haar-wavelet/README.md).

## Limitations

This is not a general wavelet family implementation and does not include coefficient thresholding, wavelet packets, boundary extension or arbitrary odd-sized input handling. Coefficient orientation and scaling conventions are explicitly defined in the source.
