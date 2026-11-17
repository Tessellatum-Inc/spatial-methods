# Lee local-statistics speckle filter

The Lee filter is an adaptive local estimator. It preserves values in
high-variance neighbourhoods and pulls values toward a local mean in
low-variance neighbourhoods. For centre observation z, local mean m,
observed local variance s² and assumed noise variance σ², define

\[
\sigma_x^2=\max(s^2-\sigma^2,0),\qquad
W=\frac{\sigma_x^2}{\max(s^2,\sigma^2)},\qquad
\hat z=m+W(z-m).
\]

The gain is small in homogeneous areas and approaches one where observed
variation is large relative to the noise model. This is an adaptive
smoothing estimator, not a universal denoiser.

## Assumptions and operational cautions

- The supplied noise variance is appropriate to the image scale and local
  noise process. The reference code does not estimate it.
- The implementation uses an odd square window, edge-replicated borders,
  sample variance and NaN-aware neighbourhood summaries.
- The included NumPy implementation is a scalar-intensity teaching baseline.
  Conventional SAR speckle is multiplicative; a calibrated intensity model,
  log-domain treatment, or distribution-aware estimator may be required.
- Directional Refined Lee, polarimetric covariance filtering, multi-looking,
  sensor-specific calibration and validation are separate methods.

## Reference implementation

See [the Python implementation](../../implementations/python/lee-speckle-filter/README.md).
The tests cover constant-field preservation, zero-noise behaviour, impulse
suppression, NoData preservation and parameter validation.
