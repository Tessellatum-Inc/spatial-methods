# Simple, ordinary and universal kriging

This package provides a small dense NumPy reference implementation of three
covariance-based kriging estimators:

- **Simple kriging:** known constant mean.
- **Ordinary kriging:** unknown constant mean, enforced by a sum-to-one
  constraint.
- **Universal kriging:** unknown planar drift
  `beta0 + beta_x*x + beta_y*y`, enforced by unbiasedness constraints.

All three use spherical, exponential or Gaussian covariance models. Nugget
and optional observation noise are added to the data covariance diagonal;
predictions target the latent field, whose marginal variance is the partial
sill. The output includes predictions, conditional variances and weights.

## Install and test

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

## Example

```python
from kriging_variants import kriging_predict

result = kriging_predict(
    [(0, 0), (1, 0), (0, 1), (1, 1)],
    [1.0, 2.0, 2.5, 3.2],
    [(0.5, 0.5)],
    drift="linear",
    model="exponential",
    nugget=0.05,
    partial_sill=1.0,
    range_=2.0,
)
print(result["prediction"], result["variance"])
```

## Sequential Gaussian simulation\n\n`sequential_gaussian_simulation` visits grid locations in seeded random order and samples each from its simple-kriging conditional Gaussian distribution given supplied observations and all earlier simulated cells. It preserves collocated exact observations when observation noise is zero. The known mean, covariance family and parameters are supplied. Observation noise applies only to measured values.\n\nThis is a small-grid reference implementation: each step solves a dense system whose size grows with the number of previously conditioned locations. It does not fit variograms, use local neighbourhoods, simulate indicator/multiple-point models or account for hyperparameter uncertainty.\n\n## Limits

The implementation is dense: the solve costs O(n^3) time and O(n^2) memory.
It uses a supplied covariance family and parameters; it does not fit a
variogram, estimate anisotropy, select local neighbourhoods, or propagate
parameter uncertainty. Universal kriging supports only a planar coordinate
drift, not arbitrary external covariates. Singular systems are rejected
rather than silently pseudo-inverted. Coordinates must be in meaningful
planar linear units.
