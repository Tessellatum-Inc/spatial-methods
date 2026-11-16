# Empirical optical and relative radiometric normalization

This package implements five scoped methods:

- Percentile-based dark-object subtraction for a simple additive path-radiance estimate.
- Per-band C-correction from a fitted reflectance–illumination relation.
- Minnaert terrain correction with a caller-supplied exponent.
- Per-band empirical-quantile histogram matching to a reference image.
- Pseudo-invariant-feature (PIF) normalization: robustly rank candidate stable pixels by multiband date difference, then fit per-band affine target-to-reference corrections.

## Run

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

All image methods require matching, co-registered arrays. Inputs are finite numeric 2D or (rows, columns, bands) arrays; optional masks select valid spatial pixels. Histogram matching uses corresponding empirical quantiles and clamps extrapolation to the end quantiles. PIF normalization selects a configurable lowest-change fraction (at least max(3, bands + 1) pixels) and fits ordinary least-squares affine corrections.

These are empirical baselines, not sensor physics. Histogram matching can remove genuine temporal distribution shifts. PIF selection can fail when real change dominates the scene or when illumination/sensor differences are spatially complex. PIF normalization is not IR-MAD: it does not estimate canonical variates or posterior change probabilities. None of these methods replaces atmospheric correction, BRDF normalization, cloud masking, radiometric calibration or independent validation.
