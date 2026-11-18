# Estimating additive Gaussian image noise with Haar detail MAD

## Why estimate noise?

Noise estimates inform image-quality assessment, denoising strength and uncertainty reporting. A single number is only meaningful after stating the assumed noise model and the image content used to estimate it.

## Haar diagonal detail

For each non-overlapping 2x2 block with values `a, b, c, d`, the orthonormal diagonal-detail coefficient is

`HH = (a - b - c + d) / 2`.

The squared sum of the four weights is one. Therefore independent, equal-variance pixel noise with variance sigma-squared remains variance sigma-squared in this coefficient band.

For approximately white additive Gaussian noise, use the robust median absolute deviation:

` sigma_hat = median(abs(HH - median(HH))) / 0.67448975 `

The divisor is the median absolute deviation of a standard normal distribution. The median makes the scale estimate less sensitive to a minority of large coefficients than a standard deviation.

## Implemented baseline

The repository includes a [NumPy implementation](../../implementations/python/sensor-noise-estimation/README.md), tests with seeded synthetic Gaussian noise and smooth trends, per-band estimates and a [verification record](../../catalog/verification/sensor-noise-estimation.md).

## Assumptions and cautions

The finest-scale diagonal detail should be dominated by noise rather than real texture or edges. Fine spatial texture can inflate the estimate. Correlated noise, periodic striping, quantisation, compression artefacts and signal-dependent noise violate the simple model. This method estimates one marginal sigma per band; it does not estimate a spatial covariance, cross-band covariance, gain/offset or full sensor noise model. It is not a substitute for calibration metadata or laboratory characterisation.

## References

- Donoho, D. L. and Johnstone, I. M. (1994). Ideal spatial adaptation by wavelet shrinkage. *Biometrika*, 81(3), 425–455. https://doi.org/10.1093/biomet/81.3.425
- Mallat, S. (2009). *A Wavelet Tour of Signal Processing: The Sparse Way*, 3rd ed. Academic Press.
