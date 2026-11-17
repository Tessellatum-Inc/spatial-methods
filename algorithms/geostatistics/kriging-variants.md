# Simple, ordinary and universal kriging

Kriging is a family of best linear unbiased prediction procedures whose
weights are derived from a covariance or variogram model. The mean/trend
assumption changes the system being solved.

- **Simple kriging** assumes a known mean. It solves the data covariance
  system directly and predicts the known mean plus a covariance-weighted
  residual.
- **Ordinary kriging** assumes an unknown constant mean. Its augmented
  system constrains weights to sum to one.
- **Universal kriging** assumes an unknown drift in a specified basis. This
  implementation uses an intercept and planar x/y terms, and constrains the
  weights to reproduce those basis functions at the target.

The implementation uses spherical, exponential and Gaussian covariance
families and returns predictions, conditional variances and weights. Nugget
and observation noise enter the sample covariance diagonal; the prediction
target is the latent field. A supplied covariance model is assumed valid.

This is a dense reference solver, not a variogram estimator or a scalable
kriging engine. It does not implement co-kriging, external drift covariates,
indicator/disjunctive kriging, block or area-to-point support, local
neighbourhood search, anisotropy estimation or parameter uncertainty.

## Runnable implementation

[NumPy implementation, tests and walkthrough](../../implementations/python/kriging-variants/README.md).

## References

- Goovaerts, P. (1997). *Geostatistics for Natural Resources Evaluation*.
  Oxford University Press.
- Chilès, J.-P., & Delfiner, P. (2012). *Geostatistics: Modeling Spatial
  Uncertainty*, 2nd ed. Wiley.
- Deutsch, C. V. (University of Alberta), [Geostatistics Formula Sheet](https://sites.ualberta.ca/~cdeutsch/Geostatistics%20Formula%20Sheet.pdf).


## External drift

A separate NumPy implementation adds caller-supplied external covariates to an intercept and solves the universal-kriging block system. It returns latent-field predictions, variances and weights. This covers external-drift kriging with known covariate values; it is not a complete regression-kriging workflow with a separately selected trend model or covariate uncertainty.
