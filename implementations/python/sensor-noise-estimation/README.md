# Robust sensor-noise estimation with Haar detail MAD

This package implements a small, reproducible baseline for estimating the standard deviation of approximately independent additive Gaussian noise in a single image band or each band of an image cube.

It computes orthonormal 2x2 Haar diagonal-detail coefficients and applies the median absolute deviation estimator:

` sigma_hat = median(abs(HH - median(HH))) / 0.67448975 `

```python
from noise_estimation import estimate_gaussian_noise, estimate_band_noise
sigma = estimate_gaussian_noise(image_2d)
band_sigmas = estimate_band_noise(image_hwb)
```

## Assumptions and limitations

The estimator assumes the finest-scale diagonal detail is dominated by approximately i.i.d. additive Gaussian noise, while the underlying signal is locally smooth/sparse in that detail band. Texture, fine edges, correlated noise, striping, quantisation, compression artefacts and signal-dependent noise (for example, Poisson noise) can bias it. It is not a complete sensor calibration model and does not estimate spatial covariance, read/shot-noise components, gain, offset or defective pixels. Odd trailing rows and columns are dropped rather than padded.

Run `pip install -r requirements.txt` and `pytest -q`.
