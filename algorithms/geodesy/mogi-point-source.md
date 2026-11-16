# Mogi point-source surface deformation

The Mogi model represents an isotropic point source at depth (d) in a homogeneous, isotropic elastic half-space. For horizontal offsets (x,y), volume change (Delta V), and Poisson ratio (
u), define

\[
R^2=x^2+y^2+d^2,\qquad
A=\frac{(1-\nu)\Delta V}{\pi R^3}.
\]

The surface displacement components are

\[
u_x=Ax,\qquad u_y=Ay,\qquad u_z=Ad.
\]

The sign of (Delta V) controls inflation versus deflation. Coordinates, depth and displacement share one length unit; volume change uses that unit cubed. The implementation accepts broadcastable observation coordinates and a horizontally offset source.

## Assumptions and limits

The Mogi source is a point approximation in an elastic half-space. It does not replace finite rectangular Okada dislocations, layered/heterogeneous media, topographic Green's functions, finite-fault inversion or viscoelastic time-dependent models. Source dimensions should be small relative to depth for the point approximation to be defensible.

## Verification

Tests cover the on-axis analytic displacement, radial symmetry, sign symmetry, linear volume scaling, broadcasting, an independent Cartesian equation oracle and parameter validation.

See the [implementation package](../../implementations/python/mogi-source/README.md).
