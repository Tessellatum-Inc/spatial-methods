# Spatial intensity estimation baselines

This directory contains Gaussian kernel estimators for planar point-event intensity and a separable space-time extension.

## Spatial intensity

For events s(i) and query location s, the estimator sums a normalized bivariate Gaussian kernel over events:

lambda_hat(s) = sum_i [ exp(-||s-s(i)||²/(2h²)) / (2 pi h²) ].

Optional nonnegative event weights represent event multiplicity or exposure weights. The output is an intensity (events per squared coordinate unit), not a probability density normalized to integrate to one.

## Space-time intensity

The space-time estimator multiplies the planar Gaussian kernel by a univariate Gaussian time kernel. Its units are events per squared coordinate unit per time unit. Spatial and temporal bandwidths must be specified in the units of the projected coordinates and event-time variable.

Run tests from this directory with: python -m pytest -q

## Limitations

These are fixed-bandwidth product-kernel teaching estimators. They do not implement edge correction, adaptive bandwidths, anisotropy, bandwidth selection, directional/network kernels, Delaunay-based estimators, prospective hotspot inference, significance testing or uncertainty intervals. A separate Voronoi module provides a bounded-window inverse-cell-area baseline, without boundary correction. Near boundaries, uncorrected kernels lose mass outside the observation window and can bias intensity downward. Use a projected metric coordinate system; longitude/latitude degrees are not planar distance units. Time zones, irregular observation exposure and censoring require explicit treatment.


## Voronoi intensity

The `voronoi_intensity.py` module constructs bounded rectangular-window Voronoi cells by half-plane clipping and returns inverse cell-area intensity estimates. It checks that the clipped cells partition the window. Boundary correction, resample-smoothing and Delaunay-based estimators remain open. See the [Voronoi intensity lesson](../../../methods/voronoi-point-intensity.md) and [lab notebook](../../../notebooks/voronoi-point-intensity-lab.ipynb).
