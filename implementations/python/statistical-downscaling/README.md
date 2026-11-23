# Statistical downscaling baselines

This package contains two distinct statistical correction methods.

- **Empirical quantile mapping** estimates calibration-period model and
  observed quantiles, then maps simulated values through the empirical
  quantile relationship. The mapping is linearly interpolated between knots
  and held constant outside the calibration range.
- **Delta change** applies the modelled future change to the observed
  historical mean, additively or multiplicatively.

## Install and test

    python -m pip install -r requirements.txt
    python -m pytest -q

## Important limits

These are transparent statistical baselines, not a full climate downscaling
system. Quantile mapping assumes a stationary calibration-period bias
relationship and may not preserve trends or physical dependencies.
Delta change adjusts means but does not correct distribution shape.
Neither method performs spatial disaggregation, BCSD workflows, analog
selection, dynamical downscaling or multivariate dependence correction.
