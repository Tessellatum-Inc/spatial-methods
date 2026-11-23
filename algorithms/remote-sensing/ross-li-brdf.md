# RossThick-LiSparseR BRDF normalization

The kernel-driven model represents reflectance as an isotropic term plus
Ross-Thick volumetric and Li-Sparse-Reciprocal geometric kernels. The
implementation fits the three coefficients by per-band ordinary least
squares over multi-angle observations, then scales each observation to a
specified reference geometry using the ratio of fitted model values.

## Interface

- ross_li_kernels(solar_zenith, view_zenith, relative_azimuth, ...) returns
  volumetric and geometric kernels.
- fit_ross_li_brdf(reflectance, solar_zenith, view_zenith, relative_azimuth,
  reference_solar_zenith=..., ...) returns normalized reflectance,
  coefficients, R-squared and RMSE.

Angles are radians; observations are rows and spectral bands are columns.
The design matrix must have rank three.

## Assumptions and limits

This is a kernel-model baseline, not the complete operational MODIS MCD43
processing chain. It does not perform atmospheric correction, cloud screening,
temporal weighting, quality-flag filtering or uncertainty estimation. Shape
ratios should be justified for the target canopy and sensor. BRDF normalization
is distinct from C-correction, SCS+C and Minnaert terrain correction.
