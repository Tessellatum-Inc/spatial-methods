# Gabor filter bank

Generates zero-mean, unit-L2 Gabor kernels and applies them to 2-D images using reflected boundaries. A bank returns absolute response magnitudes for every requested frequency/orientation pair. Frequencies are cycles per pixel and must lie in (0, 0.5].

Gabor filters are orientation- and frequency-selective texture/edge operators. Kernel size is controlled by sigma and the truncation radius. This is a direct NumPy implementation intended for reproducibility and small-to-medium arrays; large-scale use should use FFT or optimized convolution. It does not perform automatic scale selection or feature normalization.

```python
from gabor_filters import gabor_bank
responses = gabor_bank(image, frequencies=[.08,.16,.24],
                       orientations=[0, .785, 1.571, 2.356])
```

Run `pytest -q` in this directory.
