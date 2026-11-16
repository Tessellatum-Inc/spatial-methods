# Empirical optical and relative radiometric normalization

This package implements seven scoped methods:

- Percentile-based dark-object subtraction for a simple additive path-radiance estimate.
- Per-band C-correction from a fitted reflectance–illumination relation.
- SCS+C topographic correction using a slope-adjusted illumination regression.
- Minnaert terrain correction with a caller-supplied exponent.
- Per-band empirical-quantile histogram matching to a reference image.
- Pseudo-invariant-feature (PIF) normalization: robustly rank candidate stable pixels by multiband date difference, then fit per-band affine target-to-reference corrections.
- Empirical-line calibration: fit per-band DN-to-reflectance gain and offset from paired reference-target samples, then apply them to imagery.

## Run

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

All image methods require matching, co-registered arrays. Inputs are finite numeric 2D or (rows, columns, bands) arrays; optional masks select valid spatial pixels. Histogram matching uses corresponding empirical quantiles and clamps extrapolation to the end quantiles. PIF normalization selects a configurable lowest-change fraction (at least max(3, bands + 1) pixels) and fits ordinary least-squares affine corrections. Empirical-line fitting accepts paired sample matrices (samples, bands), reports per-band gain, offset, R-squared and RMSE, and applies the calibration to matching single- or multiband images. Reflectance is left unclipped unless bounds are explicitly supplied.

SCS+C estimates its per-band C parameter by regressing reflectance divided by cosine of terrain slope against cosine of incidence; it requires varying illumination and non-vertical valid terrain. The correction assumes accurate co-registered slope/aspect and solar geometry. These are empirical baselines, not sensor physics. Histogram matching can remove genuine temporal distribution shifts. PIF selection can fail when real change dominates the scene or when illumination/sensor differences are spatially complex. PIF normalization is not IR-MAD: it does not estimate canonical variates or posterior change probabilities. Empirical-line calibration depends on representative reference targets with known reflectance and stable illumination during acquisition; it does not solve atmospheric effects or sensor nonlinearity. None of these methods replaces full radiative-transfer atmospheric correction, BRDF normalization, cloud masking or independent validation.
