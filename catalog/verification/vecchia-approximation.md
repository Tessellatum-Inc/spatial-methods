# Source verification — Vecchia likelihood and local prediction

## Identity and bibliography
- Vecchia, A. V. (1988). Estimation and model identification for continuous spatial processes. *Journal of the Royal Statistical Society: Series B*, 50(2), 297–312.
- Datta, A., Banerjee, S., Finley, A. O., & Gelfand, A. E. (2016). Hierarchical nearest-neighbor Gaussian process models for large geostatistical datasets. *Journal of the American Statistical Association*, 111(514), 800–812. DOI 10.1080/01621459.2015.1044091.

## Technical claims
- Vecchia approximations replace full predecessor conditioning with sparse local conditional sets.
- The local prediction routine applies Gaussian conditional mean/variance formulas to nearest observed neighbours; it is a conditional predictor, not a full hierarchical NNGP model.
- Using all training observations recovers the dense Gaussian-process conditional prediction.

## Implementation and tests
- Tests cover exact dense likelihood with all predecessors, ordering invariance, local likelihood outputs, exact dense prediction oracle, sparse neighbour selection and invalid inputs.

## Limits and rights
No joint predictive covariance over multiple prediction sites, parameter estimation, hierarchical Bayesian inference, nonstationary kernels, sparse precision solver or large-data benchmark is implemented. Original code and explanatory text; bibliographic metadata only.
