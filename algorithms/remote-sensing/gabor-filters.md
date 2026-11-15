# Gabor filters

A 2-D Gabor kernel is a sinusoidal carrier modulated by a Gaussian envelope. Varying carrier frequency and orientation produces a filter bank responsive to local texture and oriented structure.

See [the NumPy implementation](../../implementations/python/gabor-filters/README.md). Kernels are zero-mean and unit-L2 normalized; response magnitude is returned for each frequency/orientation pair. Frequency is expressed in cycles per pixel.

The current implementation is a direct convolution baseline. It does not perform automatic scale selection or normalized feature aggregation.
