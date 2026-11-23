# Empirical-line radiometric calibration

The empirical-line method fits a per-band affine relationship between image digital numbers and reference-target reflectance:

`reflectance = gain × DN + offset`

The reference implementation accepts paired `(samples, bands)` arrays (or one-dimensional single-band vectors), fits ordinary least-squares coefficients independently per band, and reports gain, offset, R-squared and RMSE. The resulting calibration can be applied to a single-band or matching multiband image. Reflectance is not clipped unless explicit bounds are supplied.

The method assumes representative reference targets with known reflectance and acquisition conditions sufficiently stable for the target measurements to describe the scene. Target selection, panel calibration, atmospheric stability, sensor linearity and independent validation remain the user's responsibility. This is an empirical calibration baseline, not a full atmospheric radiative-transfer correction.

See the [tested NumPy implementation](../../implementations/python/empirical-corrections/README.md), which shares its package with dark-object subtraction and terrain/relative normalization methods.
