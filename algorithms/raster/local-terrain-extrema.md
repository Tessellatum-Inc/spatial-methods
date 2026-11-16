# Local terrain extrema

## Purpose

Detect local raster peaks and pits over a square neighbourhood. The routine requires a complete finite neighbourhood and supports a minimum prominence threshold.

## Contract

detect_local_extrema(elevation, window_size=3, min_prominence=0.0) returns two Boolean arrays: local maxima and local minima. The window must be odd and at least 3. Prominence is the difference between the candidate and the most extreme neighbour. Flat windows are not classified as either extrema. A border of half-window width remains false; any window containing NoData is rejected.

Plateau boundaries can produce multiple candidate cells. The function does not label connected plateaus, estimate topographic prominence along drainage saddles, or classify landforms.

## Complexity

The implementation uses NumPy sliding-window views and reductions. Runtime is proportional to the number of output cells times the window area.

## Implementation

See the terrain-indices implementation and unit tests.