# Hydrographic sounding geometry and local Jacobian

A dependency-free implementation of the rigid-body transform from a navigation
reference point to an acoustic sounding point, plus its first-order Jacobian.

## Model and conventions

\[
\mathbf{p}_n=\mathbf{r}_n+
\mathbf{R}_{n\leftarrow b}(\boldsymbol{\ell}_b+\mathbf{s}_b).
\]

The body-frame lever arm \(\boldsymbol{\ell}_b\) runs from the navigation
reference point to the acoustic origin. The body-frame acoustic vector
\(\mathbf{s}_b\) runs from the acoustic origin to the seabed detection.
\(\mathbf{R}_{n\leftarrow b}\) maps body-frame vectors into navigation axes.

The attitude perturbation is left-multiplicative and expressed in navigation
axes: \(\mathbf{R}'=\exp([\delta\boldsymbol{\theta}_n]_\times)\mathbf{R}\).
With \(\mathbf{v}=\mathbf{R}(\boldsymbol{\ell}_b+\mathbf{s}_b)\), the
Jacobian for input order
\([\mathbf{r}_n,\delta\boldsymbol{\theta}_n,\boldsymbol{\ell}_b,\mathbf{s}_b]\)
is

\[
\mathbf{J}=
\begin{bmatrix}
\mathbf{I}&-[\mathbf{v}]_\times&\mathbf{R}&\mathbf{R}
\end{bmatrix}.
\]

The output position is in navigation-frame linear units; attitude derivatives
are per radian. Pass this 3 by 12 Jacobian and a covariance matrix ordered
identically to the generic `covariance_propagation` function to obtain a
first-order sounding-point covariance.

## Run

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

## Scope and limits

The routine validates that the supplied matrix is a proper rotation and
returns the point and local Jacobian. It does not estimate the rotation,
calibration, lever arm, covariance or acoustic vector. It assumes a single
rigid transform and the stated perturbation convention. It does not include
GNSS-to-IMU-to-transducer multi-stage lever-arm geometry, time synchronisation,
heave/draft/squat, sound-speed ray tracing, beamforming, bottom detection,
geodetic projection, vertical datum reduction or surface interpolation.

This is a geometry derivative, not a full TPU model. Input covariance must
represent the actual joint uncertainty and cross-correlations in the stated
order. Verify frame conventions and derivatives against the project's sensor
documentation before operational use.
