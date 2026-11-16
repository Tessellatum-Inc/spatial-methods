# InSAR orbital-ramp correction and SBAS inversion

## Orbital ramp removal

An unwrapped interferometric phase image may contain a broad spatial ramp. The reference implementation fits a first-order plane or second-order polynomial surface by least squares over valid pixels and subtracts it. It does not identify atmospheric phase screens or DEM-correlated error.

## Small-baseline network inversion

For an interferogram between acquisitions (i) and (j), the sign convention is

\[
\Delta_{ij}=d_j-d_i.
\]

With a reference acquisition fixed to zero, each pixel is solved by weighted least squares over its available interferograms. Pixels whose available network does not have full rank are returned as NoData. The solution estimates relative acquisition displacement in the same units as the input interferograms.

## Limits

This is a core linear inversion kernel, not a complete InSAR workflow. It assumes consistently unwrapped interferograms and does not perform phase unwrapping, atmospheric correction, coherence weighting, DEM-error correction, temporal regularization, GNSS integration or 3D velocity decomposition.

## Verification

Tests recover known planar and quadratic ramps and synthetic acquisition displacement series, exercise weighting, masked pixels and rank-deficient networks, and validate the input graph.

See the [implementation package](../../implementations/python/insar-time-series/README.md).
