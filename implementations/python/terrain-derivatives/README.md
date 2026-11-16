# Horn 3×3 slope and aspect

This package estimates local terrain slope and downslope aspect from a regular elevation grid using Horn's 3×3 finite-difference operator.

## Install and test

~~~bash
python -m pip install -r requirements.txt
python -m pytest -q
~~~

## Contract

- Input is a 2D elevation array; finite values are valid and NaN marks NoData.
- Horizontal cell spacings are positive and in the same linear unit.
- z_factor converts elevation units into the horizontal unit; default 1 assumes matching units.
- Slope is returned in degrees and percent rise.
- Aspect is clockwise from north, points downslope, and lies in [0, 360). Flat cells have NaN aspect.
- The outer border is NaN because a complete 3×3 neighbourhood is required. Any window containing NoData is also NaN.
- The method assumes a regular grid in a suitable projected coordinate system. It does not reproject, resample, smooth or condition the DEM.

See the [canonical lesson](../../../algorithms/raster/slope-aspect.md) and [intern walkthrough](implementation-walkthrough.md).

## Local hillshade

The package also includes [hillshade_from_slope_aspect](hillshade.py), which converts slope and downslope aspect into normalized local illumination using a declared sun azimuth and altitude. It assigns flat cells illumination equal to the sine of sun altitude. It does not cast terrain shadows or model atmospheric scattering, multidirectional illumination or solar radiation. See [hillshade.md](../../../algorithms/raster/hillshade.md) and the tests in test_hillshade.py.

## Topographic wetness index

The companion terrain_indices module calculates the conventional logarithmic TWI from supplied specific catchment area (metres) and slope (degrees). It requires an explicit positive slope floor for flats and masks invalid/non-positive areas. This is a terrain index, not a soil-moisture model. See [the canonical lesson](../../../algorithms/raster/topographic-wetness-index.md).


## Zevenbergen–Thorne slope and aspect

The companion `zevenbergen_thorne_slope_aspect` function uses central differences from the four cardinal neighbours rather than Horn's weighted 3×3 directional sums. It returns the same three arrays and follows the same units, border and strict NoData contract. The two estimators agree on planar surfaces but can differ on curved or noisy terrain because their neighbourhood weights differ. This is a first-derivative implementation only; it does not yet calculate profile or plan curvature.


## Profile and plan curvature

`terrain_curvature` estimates signed profile and plan curvature from central first and second differences on a 3×3 neighbourhood. Profile curvature is measured along the steepest-slope direction; plan curvature is measured across it. Both outputs use inverse horizontal units, require positive cell spacing and a positive vertical conversion factor, and return NaN at borders, in any window containing NoData, and on flat cells where aspect/curvature directions are undefined. This is a local finite-difference teaching baseline. The companion `multiscale_terrain_curvature` applies separable Gaussian smoothing at one or more map-unit scales before calculating the same profile and plan curvature measures. It requires a fully finite DEM and uses reflective padding; scale, resolution and boundary policy must be reported. Geographic-grid correction and geomorphon classification remain outside scope.


## Topographic position index (TPI)

The topographic_position_index function calculates focal TPI as the centre elevation minus the mean elevation in an odd-sized square window (including the centre). It uses integral images for O(rows × columns) work regardless of window size. The outer half-window border is always NoData. Non-finite cells are omitted from the local mean, with min_valid_fraction controlling the minimum share of valid cells required; the centre must be valid. Positive values are locally elevated (ridge-like), negative values locally depressed (valley-like), and values near zero are locally similar to the neighbourhood. TPI is scale-dependent: window size, terrain resolution and study area affect interpretation. It is not a landform classifier by itself.


## Riley terrain ruggedness index (TRI)

The riley_terrain_ruggedness_index function implements the eight-neighbour Riley form: the square root of the sum of squared elevation differences from the centre cell to its eight immediate neighbours. It requires a complete finite 3×3 neighbourhood and returns NaN at borders or around NoData. z_factor converts vertical values before differencing. This is not the alternative mean absolute-difference TRI variant; the formula must be stated when comparing products.


## Hypsometric curve and integral

The hypsometric_curve function summarizes the elevation distribution of a basin or other raster region. It returns unique normalized elevation thresholds in descending order, the fraction of valid cells at or above each threshold, and the hypsometric integral (mean normalized elevation). A Boolean valid_mask can select the basin cells; non-finite elevations are always excluded. It assumes equal-area raster cells, so it is appropriate for a regular projected grid, not an unprojected geographic raster with varying cell area. A zero-relief region has no defined normalized curve and is rejected. The integral is a descriptive elevation-distribution summary, not a direct measure of basin age or geomorphic stage.


## Cut-and-fill volume

The cut_fill_volume function compares aligned existing and design elevation surfaces. Existing terrain above design is cut; existing terrain below design is fill. It returns cellwise depth rasters and total volumes using the supplied rectangular cell dimensions. Both surfaces must share a vertical unit compatible with horizontal cell units for the resulting volume to be meaningful. Non-finite cells and an optional Boolean valid_mask are excluded. This is a direct raster difference calculation: it does not align grids, transform coordinate systems, account for compaction/bulking, or model construction tolerances.


## Multidirectional hillshade

The multidirectional_hillshade function averages equally weighted local hillshade values from multiple sun azimuths at a shared altitude. Its default four azimuths are 225°, 270°, 315° and 360°. This reduces the directional bias of a single illumination direction but remains a local reflectance-style visualization: it does not calculate cast shadows, diffuse sky light, atmospheric effects or solar irradiance. Missing derivative cells remain NoData; flat cells use the single-direction flat-surface illumination in each component.
