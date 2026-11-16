# Empirical atmospheric and terrain corrections

## Dark-object subtraction

Dark-object subtraction estimates additive path radiance from a low percentile of valid image pixels in each band, then subtracts that estimate. This is an empirical haze-reduction heuristic. It is not a physical radiative-transfer solution and cannot replace 6S, MODTRAN, FLAASH or sensor-specific atmospheric processing.

## C-correction

C-correction fits a per-band linear relation between reflectance and local illumination cosine, estimates C as intercept divided by slope, and applies rho_corrected = rho * (cos(solar zenith) + C) / (cos(incidence) + C). The baseline excludes invalid and near-zero illumination cells and rejects unstable or negative C estimates. It assumes co-registration and a usable linear fit.

## Minnaert correction

Minnaert correction applies rho_corrected = rho * (cos(solar zenith) / cos(incidence))^k. The exponent k is supplied by the caller, per band or scalar; it is not inferred from a single universal value. Non-illuminated cells are returned as NaN.

These are distinct correction families with different assumptions. They do not perform cloud masking, BRDF normalization, atmospheric gas/aerosol retrieval or full sensor calibration.
