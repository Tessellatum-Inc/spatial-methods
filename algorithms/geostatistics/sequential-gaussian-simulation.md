# Sequential Gaussian simulation

Sequential Gaussian simulation (SGS) generates conditional realizations of a
Gaussian random field at a set of unsampled locations. A simulation order is
chosen, and each new location is sampled from its conditional Gaussian
distribution given the original observations and all previously simulated
values. The implementation uses simple kriging with a supplied known mean
and a stationary spherical, exponential or Gaussian covariance model.

The small-grid reference implementation rebuilds and solves the dense
conditioning covariance matrix at every step. It preserves exact collocated
observations when observation noise is zero and can include independent
measurement noise on the supplied observations. The random seed fixes the
simulation order and draws.

This implementation does not estimate a variogram, choose local
neighbourhoods, model non-Gaussian variables, or implement indicator,
multiple-point, object-based or p-field simulation. It is computationally
expensive as the grid grows and should be treated as a transparent teaching
baseline rather than a large-area simulator.

## Runnable implementation

[Simple/ordinary/universal kriging and SGS package](../../implementations/python/kriging-variants/README.md).

## References

- Goovaerts, P. (1997). *Geostatistics for Natural Resources Evaluation*.
  Oxford University Press.
- Chilès, J.-P., & Delfiner, P. (2012). *Geostatistics: Modeling Spatial
  Uncertainty*, 2nd ed. Wiley.
