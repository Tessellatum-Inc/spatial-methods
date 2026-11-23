# Iteratively reweighted multivariate alteration detection (IR-MAD)

## Purpose

IR-MAD compares two co-registered multispectral images and iteratively
identifies pixels whose paired spectral observations are consistent with a
no-change population. It is useful for relative radiometric normalization,
pseudo-invariant feature selection and unsupervised bitemporal change
screening.

## Canonical variates and MAD differences

For reference vector (X) and target vector (Y), canonical correlation
analysis finds linear combinations (a_i^T X) and (b_i^T Y) with maximal
paired correlation. The multivariate alteration-detection variates are

[
M_i = a_i^T(X-mu_X)-b_i^T(Y-mu_Y).
]

Under the idealized no-change model, the variance of the i-th MAD variate is
(2(1-ho_i)), where (ho_i) is its canonical correlation. A per-pixel
statistic is formed as

[
Q = sum_i rac{M_i^2}{2(1-ho_i)}.
]

Under the model assumptions, Q is compared with a chi-square distribution
with degrees of freedom equal to the number of canonical variates. Its
upper-tail probability becomes a weight for the next iteration. Stable
observations retain high weights; observations with large spectral alteration
are downweighted. Re-estimating weighted canonical correlations and weights
continues until convergence or an iteration limit.

## Implementation

The [NumPy/SciPy implementation](../../implementations/python/ir-mad/README.md)
supports different band counts between dates, boolean validity masks,
ridge-stabilized covariance whitening, configurable iteration/tolerance and
a minimum weight floor. It returns MAD variates, chi-square scores, weights,
canonical correlations and convergence diagnostics. The weight is a
model-based no-change score, not a calibrated posterior probability.

## Assumptions and failure modes

- Images must be co-registered and describe comparable spatial support.
- The scene must contain enough observations representative of no-change
  behaviour; pervasive change can corrupt the estimated canonical model.
- The method models linear cross-date relationships and global covariance.
- Clouds, shadows, misregistration, nonlinear sensor response and spatially
  varying atmospheric effects can create false change.
- Inputs are finite arrays; exclude invalid pixels through the validity mask.
- Ridge regularization stabilizes covariance inversion but does not cure
  rank-deficient or unrepresentative data.

IR-MAD is distinct from ordinary histogram matching and from the simpler
robust-difference PIF affine baseline: it explicitly estimates canonical
variates and iteratively reweights observations using the chi-square statistic.

## Reference

Nielsen, A. A., Conradsen, K. and Simpson, J. J. (1998). Multivariate
alteration detection (MAD) and MAF post-processing in multispectral,
bijective, image-to-image transformations. *Remote Sensing of Environment*,
64(1), 1–19. https://doi.org/10.1016/S0034-4257(97)001 ಸಮ
