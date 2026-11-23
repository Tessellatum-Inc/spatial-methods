# DEM void filling with local inverse-distance weighting

The reference method fills missing elevation cells from valid cells in a
bounded neighbourhood. For valid neighbours i at map distances d_i, it uses

    z_hat = sum(z_i / d_i^p) / sum(1 / d_i^p)

The caller controls neighbourhood radius, minimum neighbour count, distance
power, pixel dimensions and number of synchronous passes. Synchronous updates
avoid dependence on raster scan order. Existing values are preserved and an
explicit fill mask is returned; unresolved cells remain missing.

This is a generic IDW gap-fill baseline. It is not equivalent to
hydro-conditioning, stream burning, breakline-aware interpolation, DEM fusion
or bare-earth classification. It can smooth ridges and valleys and should be
validated before hydrological use. See the Python package for its API and
tests.
