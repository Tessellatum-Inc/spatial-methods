# Hydrographic sounding-point geometry and local Jacobian

**Status:** Curated geometric method with dependency-free reference implementation  
**Scope:** One rigid-body transform from a navigation reference point to a sounding point, plus a local small-attitude-error Jacobian.

## 1. Coordinate model

Let navigation-frame coordinates be denoted by subscript (n), and body-frame coordinates by subscript (b). Let (mathbf{R}_{n\leftarrow b}) map body-frame vectors into navigation axes. For navigation reference-point position (mathbf{r}_n), body-frame lever arm (oldsymbol{\ell}_b), and acoustic vector (mathbf{s}_b),

\[
\mathbf{p}_n=\mathbf{r}_n+
\mathbf{R}_{n\leftarrow b}(\boldsymbol{\ell}_b+\mathbf{s}_b).
\]

The lever arm points from the navigation reference point to the acoustic origin. The acoustic vector points from the acoustic origin to the detected seabed point. All linear quantities must use the same unit. The body and navigation axes, handedness, rotation order, timestamps and reference points must be declared by the project.

## 2. Left-multiplicative attitude perturbation

Define an infinitesimal attitude perturbation in navigation axes by

\[
\mathbf{R}'=
\exp([\delta\boldsymbol{\theta}_n]_\times)
\mathbf{R},
\]

where ([\mathbf{a}]_\times) is the skew-symmetric matrix satisfying
([\mathbf{a}]_\times\mathbf{b}=\mathbf{a}\times\mathbf{b}). Let
\(mathbf{v}_n=\mathbf{R}(\boldsymbol{\ell}_b+\mathbf{s}_b)\).
To first order,

\[
\delta\mathbf{p}_n
\approx
\delta\mathbf{r}_n
+
[\delta\boldsymbol{\theta}_n]_\times\mathbf{v}_n
+
\mathbf{R}\,\delta\boldsymbol{\ell}_b
+
\mathbf{R}\,\delta\mathbf{s}_b.
\]

Using (\delta\boldsymbol{\theta}\times\mathbf{v}
=-[\mathbf{v}]_\times\delta\boldsymbol{\theta}), the Jacobian for
input order
([\mathbf{r}_n,\delta\boldsymbol{\theta}_n,
\boldsymbol{\ell}_b,\mathbf{s}_b]) is

\[
\mathbf{J}=
\begin{bmatrix}
\mathbf{I}&-[\mathbf{v}_n]_\times&\mathbf{R}&\mathbf{R}
\end{bmatrix}.
\]

Attitude columns are per radian. This sign and frame convention is not
interchangeable with a right-multiplicative body-frame perturbation. A
different convention requires a different Jacobian.

## 3. Covariance use

Given a joint covariance matrix for the 12 ordered inputs, including all
cross-covariances, propagate it using

\[
\mathbf{C}_{pp}\approx\mathbf{J}\mathbf{C}_{xx}\mathbf{J}^{T}.
\]

The same shared lever-arm or attitude parameter can correlate multiple
soundings. For a batch of pings, do not treat a shared calibration parameter
as a fresh independent draw for every sounding.

## 4. Implementation and verification

The companion [Python implementation](../../implementations/python/hydrographic-sounding-geometry/README.md):
- validates a finite proper orthonormal rotation matrix;
- computes the navigation-frame sounding point;
- returns the 3 by 12 Jacobian in the stated input order;
- tests identity and rotated geometry;
- checks attitude derivatives against finite differences using the same
  left-multiplicative convention;
- rejects malformed vectors and invalid rotations.

## 5. Limits

This is one rigid transform, not a complete vessel/sensor chain. Real systems
may require GNSS-antenna-to-IMU, IMU-to-transducer, array alignment, timing,
heave, draft, squat, ray tracing, beamforming, bottom detection, geodetic
transformation and vertical-reference stages. Their derivatives and joint
covariances must be included in the full model. This method does not estimate
calibration parameters or supply instrument uncertainty values.
