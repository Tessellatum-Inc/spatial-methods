# Isotropic covariance on the two-sphere

This package constructs valid isotropic covariance functions on the unit two-sphere (S^2) using a finite Schoenberg/Legendre series. It is a spherical counterpart to the Euclidean examples, not a planar kernel with a new distance pasted in.

## The construction

For angular separation (	hetain[0,pi]),

\[
C(\theta)=\sum_{\ell=0}^{L} b_\ell P_\ell(\cos\theta),
\qquad b_\ell\geq 0.
\]

Here (P_\ell) is the Legendre polynomial of degree (ell). Non-negative coefficients make this a valid isotropic covariance on (S^2); the marginal variance is (C(0)=\sum_\ell b_\ell). The finite series is a truncated spectral construction, not a fit to observations.

## Run

~~~bash
python -m pip install -r requirements.txt
python -m pytest -q
~~~

~~~python
from spherical_covariance import (
    latlon_to_unit_vectors,
    spherical_covariance_matrix,
)

sites = latlon_to_unit_vectors([0, 20, -35], [0, 90, 140])
C = spherical_covariance_matrix(sites, [1.0, 0.5, 0.2, 0.1])
print(C)
~~~

## Coordinate contract

- Input geographic coordinates are latitude and longitude in degrees, converted to unit XYZ vectors on a perfect sphere.
- Alternatively, supply unit XYZ vectors directly. The function checks their norms.
- Angular distance is the central angle on the unit sphere, in radians, derived from the dot product.
- This is not an ellipsoidal geodesic calculation. It does not model a reference ellipsoid, geoid, datum epoch or physical distance in metres.
- Longitude is restricted to [-180, 180] degrees; latitude to [-90, 90].
- The dense matrix is intended for small teaching examples.
- The coefficients are non-negative and finite; no coefficient-fitting or Bayesian inference is included.
- This package does not implement vector-valued fields, non-isotropic spherical fields, space-time covariance, or spherical Gaussian-process prediction.

The implementation uses the Legendre three-term recurrence and NumPy only. Its finite-dimensional eigenvalue checks are useful tests, but the validity claim comes from the non-negative Legendre-series construction, not from numerical checks on a handful of site sets.

See the [method lesson](../../../methods/isotropic-covariance-on-the-sphere.md) and [intern walkthrough](implementation-walkthrough.md).


## Spherical statistics

The companion `spherical_statistics.py` module provides:

- Great-circle angular distances between unit vectors.
- An intrinsic Fréchet/Karcher mean on S2, with medoid initialization and explicit rejection of antipodal cut-locus cases.
- Spherical k-means with seeded spherical k-means++ initialization.
- The normalized three-dimensional von Mises–Fisher (vMF) density.
- EM fitting of finite vMF mixtures, with component directions, concentrations, proportions and responsibilities.
- Weighted spherical KDE as a mixture of vMF kernels with common concentration.

~~~python
from spherical_statistics import (
    frechet_mean_sphere, spherical_kmeans, spherical_vmf_kde,
    von_mises_fisher_density, von_mises_fisher_mixture,
)

mean = frechet_mean_sphere(unit_vectors)
clusters = spherical_kmeans(unit_vectors, 4, seed=7)
mixture = von_mises_fisher_mixture(unit_vectors, 4, seed=7)
density = spherical_vmf_kde(query_vectors, unit_vectors, concentration=12)
~~~

All locations are unit XYZ vectors. Fréchet iteration and k-means/mixture fitting are local numerical methods. Use multiple initial seeds for mixtures, inspect convergence, and avoid interpreting an intrinsic mean across antipodal/cut-locus configurations as unique. vMF density is per unit solid angle on the unit sphere, not per unit ellipsoidal surface area.

The tests are in `test_spherical_statistics.py`; the [spherical statistics walkthrough](implementation-walkthrough.md) explains the algorithms and limitations.
