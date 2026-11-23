# FFT-accelerated grid kernel density estimation

The algorithm bins weighted planar points to a regular grid, samples a truncated isotropic Gaussian kernel, and applies two-dimensional FFT convolution. The result is divided by total in-extent weight and cell area to produce density per square coordinate unit. Optional boundary correction divides by the discrete kernel mass supported inside the extent near each grid edge.

This is an approximate grid KDE: bandwidth, grid cell size, histogram binning and kernel truncation affect the result. It is not dual-tree KDE, an adaptive bandwidth method or a geodesic/network KDE. Coordinate units must be projected and meaningful for the chosen bandwidth.
