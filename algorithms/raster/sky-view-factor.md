# Radial horizon sky-view factor

Stable ID: `SA-RASTER-SKY-VIEW-FACTOR` · Draft 0.1 · Source compendium section 4, page 6

## Purpose

The sky-view factor (SVF) approximates the fraction of the sky hemisphere visible from a terrain cell. Valleys and enclosed depressions have lower values than exposed ridges and flat terrain. It is used as a terrain exposure descriptor and as one input to some microclimate and radiation workflows; it is not itself a complete radiation or temperature model.

## Radial horizon approximation

For each target cell, cast (A) rays at evenly spaced azimuths. Along ray (a), sample terrain elevations (z_{a,j}) at horizontal distances (d_j). The elevation angle of a sample relative to the target elevation (z_0) is

[
	heta_{a,j}=	an^{-1}left(rac{z_{a,j}-z_0}{d_j}ight).
]

The horizon angle is the maximum positive angle along that ray:

[
h_a=maxleft(0,max_j	heta_{a,j}ight).
]

The implemented approximation is

[
SVFapproxrac{1}{A}sum_{a=1}^{A}cos^2(h_a).
]

It returns values between zero and one. A flat unobstructed surface has SVF 1. Terrain that blocks a large part of the sky has a smaller value.

## Implementation contract

The Python baseline is `sky_view_factor` in [terrain_indices.py](../../implementations/python/terrain-derivatives/terrain_indices.py). It uses bilinear elevation sampling along each ray, explicit cell dimensions, a maximum search distance, a configurable azimuth count and optional radial sample spacing. A cell is only evaluated if every ray is supported all the way to the maximum distance. Rays that exit the raster or encounter NoData invalidate that cell; no unobserved horizon is silently treated as open sky.

This is a radial azimuth-sampling approximation. It does not integrate exact solid angle over the hemisphere, calculate cast shadows through time, model atmospheric scattering, or replace a physically based solar-radiation model. Results depend on azimuth count, radial spacing, search distance, DEM resolution and boundary policy. Runtime is proportional to the number of cells multiplied by the number of azimuths and radial samples.

## Tests and interpretation

The tests verify the unit sky-view factor on flat terrain, reduced sky visibility inside an enclosing elevated surface, rectangular cell spacing, and strict NoData/boundary support. Use a projected grid with consistent horizontal units. Increase azimuth count and reduce radial sample spacing to test numerical sensitivity; report both settings with the output.

## Further work

Exact hemispherical integration, adaptive horizon sampling, multi-scale openness, directional openness, viewshed algorithms and solar-radiation models are distinct extensions and should not be represented as completed by this baseline.
