# Iteratively reweighted MAD (IR-MAD)

A NumPy/SciPy reference implementation of iteratively reweighted multivariate
alteration detection for co-registered bitemporal imagery.

## Method

1. Estimate weighted means and covariance matrices for each date.
2. Whiten the two covariance matrices and solve the canonical-correlation
   problem by singular value decomposition.
3. Difference paired canonical variates to form MAD variates.
4. Standardize squared MAD variates using their canonical-correlation-derived
   variances and calculate a chi-square statistic.
5. Convert the chi-square upper-tail probability to a no-change weight and
   repeat until weights stabilize or the iteration limit is reached.

The implementation supports different band counts between dates, a spatial
boolean validity mask, covariance ridge regularization, and explicit
convergence controls. It returns per-pixel MAD variates, chi-square scores,
no-change weights, canonical correlations, coefficients, means and convergence
diagnostics. Invalid-mask pixels are NaN in spatial outputs.

## Run

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

## Interpretation and limits

Low weights/high chi-square values indicate pixels inconsistent with the
estimated no-change population; they are not calibrated change probabilities.
IR-MAD is unsupervised and depends on a sufficiently large, representative
no-change population. Strong scene-wide change, poor co-registration,
nonlinear sensor differences, cloud contamination and severe outliers can
destabilize the canonical model. Inputs must be finite; mask unusable pixels
rather than encoding NoData as NaN. This implementation is a global
linear-covariance baseline, not a spatially regularized or operational
atmospheric-normalization pipeline.
