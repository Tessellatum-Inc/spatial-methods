# Empirical atmospheric, terrain and relative radiometric corrections

## Dark-object subtraction

Dark-object subtraction estimates additive path radiance from a low percentile of valid image pixels in each band, then subtracts that estimate. This is an empirical haze-reduction heuristic, not a physical radiative-transfer solution and cannot replace 6S, MODTRAN, FLAASH or sensor-specific atmospheric processing.

## Terrain illumination correction

C-correction fits a per-band linear relation between reflectance and local illumination cosine, estimates C as intercept divided by slope, and applies rho_corrected = rho * (cos(solar zenith) + C) / (cos(incidence) + C). SCS+C estimates C per band by regressing reflectance divided by cosine of terrain slope against cosine of incidence, then applies rho_corrected = rho * (cos(slope) * cos(solar zenith) + C) / (cos(incidence) + C). It requires varying incidence cosines and non-vertical valid terrain. Minnaert correction applies rho_corrected = rho * (cos(solar zenith) / cos(incidence))^k, with k supplied by the caller. Both assume co-registration and a usable illumination model; neither is a BRDF solution.

## Histogram matching

For each band, histogram matching maps the empirical source quantiles to the corresponding reference-image quantiles using piecewise-linear interpolation. The mapping is univariate and clamps values beyond the fitted quantile range. It can harmonize marginal distributions but can also erase genuine distributional change; it is not radiometric calibration.

## Pseudo-invariant-feature normalization

The implemented PIF baseline scores each valid pixel by robustly scaled multiband difference between reference and target dates, selects the lowest-change fraction, and fits per-band ordinary least-squares affine maps from target to reference. It requires enough candidate pixels and non-constant target values. This is deliberately not labelled IR-MAD: canonical variates, iterative change-probability weighting and noise covariance estimation are not implemented.

## Tests, limitations and references

The [NumPy reference package](../../implementations/python/empirical-corrections/README.md) includes synthetic affine-recovery tests, explicit masks and invalid-input cases. All methods assume matching grids and compatible band definitions. They do not model spatially varying sensor response, BRDF, atmosphere, cloud/shadow contamination or uncertainty in selected invariant features.

- Schott et al. (1988), “Radiometric scene normalization using pseudo-invariant features,” *Remote Sensing of Environment*, 26(1), 1–16, [doi:10.1016/0034-4257(88)90001-1](https://doi.org/10.1016/0034-4257(88)90001-1).
- Hall et al. (1991), “Radiometric rectification: toward a common radiometric response among multidate, multisensor images,” *Remote Sensing of Environment*, 35(1), 11–27, [doi:10.1016/0034-4257(91)90084-8](https://doi.org/10.1016/0034-4257(91)90084-8).


## Empirical-line calibration

The empirical-line method fits a per-band affine relationship from paired image digital-number samples and reference-target reflectance samples:

`reflectance = gain × DN + offset`

The implementation accepts paired `(samples, bands)` arrays (or one-dimensional single-band vectors), estimates ordinary least-squares coefficients independently per band, and reports gain, offset, R-squared and RMSE. Apply the returned calibration to a single-band or matching multiband image. Values are not clipped by default; optional bounds must be explicitly requested.

The reference samples should represent targets with known reflectance and be measured under acquisition conditions representative of the scene. Target selection, panel calibration, atmospheric stability, sensor linearity and independent validation remain the user's responsibility. This is a practical empirical calibration baseline, not a substitute for radiative-transfer correction or sensor-specific processing.
