# Positive and negative terrain openness

## Purpose

Terrain openness describes how much of the surrounding terrain horizon is open above and below a cell. Positive openness responds to enclosing ridges and positive relief; negative openness responds to enclosing valley sides and depressions. Both are reported as angles in degrees, with 90° representing a flat horizon under this implementation's convention.

## Algorithm

The implementation samples radial profiles at evenly spaced azimuths, bilinearly interpolates the DEM, and computes the maximum positive and maximum negative horizon angle along each ray. Positive openness is 90° minus the mean positive horizon angle; negative openness is 90° minus the mean magnitude of negative horizon angles. Horizontal distances and elevations must use compatible units.

Only cells with complete support to the declared maximum distance in every direction are evaluated. Borders and any ray crossing NoData are masked. The output is a local radial approximation and is sensitive to azimuth count, radial spacing and search distance.

## Scope

This is not the exact multi-scale geomorphon algorithm, a red-relief image-map renderer, sky-view factor, or solar radiation model. It does not account for earth curvature, vegetation, buildings or geodesic coordinates. Report the search distance and sampling parameters with every derived product.
