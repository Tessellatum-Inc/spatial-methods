# FFT-accelerated grid KDE

Implements a binned planar Gaussian kernel-density estimate. Weighted points are accumulated to a regular grid, convolved with a truncated discrete Gaussian using FFT convolution, and scaled to density per coordinate-area. Optional boundary correction divides by kernel support fraction near grid edges. Accuracy depends on grid resolution, binning and bandwidth; this is not an exact dual-tree KDE or an adaptive-bandwidth estimator. Points outside the supplied extent are excluded.
