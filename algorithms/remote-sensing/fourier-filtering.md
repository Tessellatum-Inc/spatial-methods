# Fourier transforms and frequency-domain filtering

## Purpose

The two-dimensional discrete Fourier transform represents an image as spatial frequencies. Low-pass filters suppress rapid spatial variation; high-pass filters emphasize edges and fine texture; band-pass filters isolate a frequency range.

## Mathematical form

For an image x[m,n], the 2-D DFT is the sum over rows and columns of x[m,n] exp(-2 pi i (um/M + vn/N)). The inverse transform reconstructs the image. The implementation centres zero frequency for filter design.

## Implemented scope

The NumPy reference provides forward/inverse transforms and radial ideal, Gaussian and Butterworth low-pass, high-pass and band-pass transfer functions. Cutoff units are cycles per pixel. See [implementation](../../implementations/python/fourier-filtering/README.md), including its synthetic vertical-stripe recovery test.

## Assumptions and limitations

The DFT treats the image as periodically extended. Discontinuities at image boundaries can cause spectral leakage; tapering/windowing may help but changes the signal. Ideal filters have sharp frequency cutoffs and can cause ringing. The package now also provides user-guided conjugate-symmetric notch rejection for known periodic components and a scoped periodic destriping helper. The caller supplies the frequency peak(s); automatic peak discovery, deconvolution, phase correlation and geospatial NoData interpolation remain outside scope.
