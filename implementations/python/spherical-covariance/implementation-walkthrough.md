# Intern walkthrough: a valid isotropic covariance on the sphere

## 1. Why this implementation exists

A planar covariance formula is not automatically valid when distance is replaced by great-circle distance. On the two-sphere, isotropic covariance functions have a spherical spectral representation. We use a finite Legendre series with non-negative coefficients so the validity condition is built into the model.

## 2. Understand the inputs

There are two input routes:

- `latlon_to_unit_vectors` converts latitude/longitude degrees to unit Cartesian XYZ coordinates.
- `spherical_covariance_matrix` accepts only unit vectors on the unit sphere and checks their norms.

The covariance function itself takes angular separation in radians, not kilometres or metres.

## 3. Install and test

~~~bash
python -m pip install -r requirements.txt
python -m pytest -q
~~~

Run from this directory. The test suite checks coordinate conversion, broadcasting, invalid coordinates, coefficient constraints, angular-distance bounds, matrix symmetry, diagonal variance, positive-semidefinite examples, duplicate sites and antipodal locations.

## 4. Trace the Legendre recurrence

The first two polynomials are (P_0(x)=1) and (P_1(x)=x). Higher degrees follow:

\[
P_\ell(x)=\frac{(2\ell-1)xP_{\ell-1}(x)-(\ell-1)P_{\ell-2}(x)}{\ell}.
\]

The implementation accumulates (b_\ell P_\ell(\cos\theta)) as it advances. It does not need to store every polynomial surface or add SciPy as a dependency.

## 5. Build the matrix

For unit vectors (u_i,u_j), the dot product is (cos\theta_{ij}=u_i^T u_j). Small floating-point excursions outside [-1, 1] are clipped before applying arccos. The resulting angular distances are passed to the Legendre-series evaluator.

## 6. Validate responsibly

The theorem requires non-negative coefficients. Tests additionally inspect symmetry, the diagonal, and numerical eigenvalues for selected site sets. These tests can catch coding mistakes; they do not replace the mathematical condition.

## 7. Experiments

1. Use only (b_0). Explain why every location pair has the same covariance.
2. Add a degree-one coefficient and compare nearby and antipodal sites.
3. Move coefficient mass from low to high degrees. Describe how the angular covariance curve changes.
4. Duplicate a location and inspect the repeated matrix rows.
5. Compare the spherical result with the Euclidean Gaussian kernel composed with angular distance. Treat any negative eigenvalues as a warning, not as a universal counterexample theorem.

## 8. Boundaries

This is a scalar, isotropic, stationary covariance on the perfect two-sphere. It is not an ellipsoidal geodesy library, a fitted model, a full Gaussian-process engine or a network covariance implementation.


## 9. Intrinsic Fréchet mean

The intrinsic mean minimizes the average squared great-circle angle. The implementation starts from the sample medoid, maps observations into the tangent plane with the sphere's logarithm map, averages tangent vectors and moves along the exponential map. This is a local iterative procedure. Antipodes are cut-locus singularities because the shortest geodesic direction is not unique; the function raises rather than inventing a direction.

## 10. Spherical k-means

Spherical k-means assigns each unit vector to the centroid with greatest dot product. Each centroid is the normalized resultant vector of its members. Seeded k-means++ initialization spreads starting directions; the algorithm can still converge to a local optimum. Empty or degenerate clusters are reseeded and should be inspected.

## 11. von Mises–Fisher models

For unit vector x, mean direction mu and concentration kappa, the 3-D vMF density is proportional to exp(kappa * dot(x, mu)). Its normalization is evaluated using a log-sinh identity to avoid overflow at large concentration. At zero concentration it becomes uniform over the sphere.

The finite-mixture EM routine alternates posterior responsibilities and updates component proportions, normalized resultant directions and concentration estimates. It is a local maximum-likelihood fit; compare multiple seeds and inspect component collapse and effective membership. Spherical KDE evaluates a weighted mixture of vMF kernels, not a planar Gaussian KDE.

## 12. Experiments and limitations

1. Compare the normalized arithmetic mean with the intrinsic Fréchet mean on a broad cluster.
2. Rotate every vector by the same 3-D rotation and verify that the Fréchet mean rotates with the data.
3. Increase vMF concentration and observe the density sharpen around its mean direction.
4. Fit mixtures with several seeds and compare log likelihoods.
5. Integrate the vMF density numerically over solid angle; do not use a flat latitude-longitude grid without its cosine-latitude area factor.

The methods operate on the perfect unit sphere. They do not implement ellipsoidal geodesics, directional regression, spherical splines or spherical Gaussian-process prediction.
