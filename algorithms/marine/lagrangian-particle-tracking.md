# Lagrangian particle advection and connectivity

## Steady-field particle advection

For a steady two-dimensional velocity field ((u(x,y),v(x,y))), particle position satisfies

\[
\frac{dx}{dt}=u(x,y),\qquad \frac{dy}{dt}=v(x,y).
\]

The implementation evaluates the velocity by bilinear interpolation on a rectilinear grid and advances particles with the classical fourth-order Runge–Kutta scheme. Particles leaving the interpolation domain become inactive; their later trajectory coordinates are NaN.

## Regional connectivity

Given particle release region (i), destination region (j), and optional particle weight (w_p), the connectivity count is

\[
C_{ij}=\sum_{p\in(i,j)}w_p.
\]

The row probability divides (C_{ij}) by all released weight in source region (i), including particles with no assigned destination. Lost/unassigned mass is reported separately, so assigned probabilities need not sum to one.

## Assumptions and limits

This is a steady 2D deterministic advection kernel. It does not implement time-varying velocity fields, stochastic diffusion, vertical transport, beaching, decay, boundary reflection, hydrodynamic feedback, uncertainty ensembles, or protected-area optimisation. Production ocean drift requires validated forcing, land/coast handling, temporal interpolation and particle-state processes.

## Verification

Tests compare constant velocity against the exact linear trajectory, a linear rotational field against its analytic solution, connectivity aggregation against direct counts, and domain exit/input validation.

See the [implementation package](../../implementations/python/lagrangian-connectivity/README.md).
