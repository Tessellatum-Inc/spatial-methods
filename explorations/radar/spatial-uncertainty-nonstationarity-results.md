# Nonstationarity and informative-missingness stress test

## Status

Simulation and automated validation workflow have been added. Numerical results are pending the GitHub Actions run and must be appended from the produced artifact; no coverage conclusion is made in this design note.

## Question

Do the three experimental uncertainty candidates retain useful coverage when the spatial field is nonstationary, or when eligibility depends on the values being measured?

## Design

- Grid: 24 × 24.
- Replications: 80 per scenario.
- Seed: 20261203.
- Candidate methods: moving-window bootstrap, product-Bartlett spatial HAC, and complete-grid spatial subsampling where supported.
- Shared field realizations are passed to each candidate within a scenario.
- HAC bandwidths: 3 and 6 cells in both directions.
- Moving-window and subsampling widths: 4 and 6 cells.
- Moving-window bootstrap: 200 replicates per realization.
- Coverage target: the finite full-grid mean for each generated realization, not the observed eligible-cell mean.
- Monte Carlo uncertainty: 95% Wilson intervals.

## Scenarios

1. **Smooth mean gradient:** deterministic column gradient plus independent noise. The gradient is centered over the grid.
2. **Variance gradient:** independent noise with a column-varying scale; each realized field is recentered to have a zero finite-grid mean.
3. **Abrupt mean boundary:** two regions with opposite means plus independent noise, with zero expected full-grid mean.
4. **Informative high-value missingness:** a spatially correlated Gaussian field in which the upper 22% of values are removed using a value-dependent eligibility rule.

The first three scenarios isolate nonstationary mean or variance structure without adding spatially correlated noise. The fourth combines spatial dependence and informative selection. It is intentionally a severe stress test.

## Interpretation guardrails

- The value-dependent mask changes the observed-data distribution. The estimators in this experiment do not correct for selection; their intervals are still judged against the full-grid mean. Bias and coverage loss are therefore expected possibilities, not surprising implementation failures.
- Subsampling is specified for complete grids and should explicitly refuse the irregular informative-missingness case.
- A small simulation and a small tuning grid cannot establish nominal coverage.
- No candidate should be selected by the best observed coverage.
- These mean-estimator results do not validate intervals for the Nairobi matched-strata, equal-block contrast estimand.

## Reproducibility

- Script: [simulate_spatial_uncertainty_nonstationarity.py](simulate_spatial_uncertainty_nonstationarity.py)
- Workflow: [spatial-uncertainty-nonstationarity-validation.yml](../../.github/workflows/spatial-uncertainty-nonstationarity-validation.yml)
- Artifact expected: `spatial-uncertainty-nonstationarity`

## Results

Pending automated run. Replace this section with the artifact-backed coverage, Wilson intervals, interval widths, estimate bias and eligible-cell counts after the workflow completes.
