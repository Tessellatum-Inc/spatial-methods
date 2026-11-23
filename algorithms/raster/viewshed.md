# Raster viewshed and cumulative visibility

## Purpose

A viewshed marks raster cells with an unobstructed line of sight from an observer. A cumulative viewshed sums visibility across multiple observer locations and is useful for exploratory placement and exposure analysis.

## Reference implementation

The Python implementation is in [viewshed.py](../../implementations/python/terrain-derivatives/viewshed.py). It traces a centre-to-centre Bresenham path from the observer to each target and compares the apparent elevation angle of every intervening cell with the target angle. Observer and target heights are independently configurable.

Optional curvature correction subtracts the tangent-plane drop d²(1-k)/(2R), where R is the supplied Earth radius and k is a refraction coefficient. Leave earth_radius unset for planar analysis. Elevations, heights, cell dimensions and Earth radius must use consistent linear units.

## NoData and limits

The observer must be finite. A target is visible only if its own elevation and every traversed intermediate cell are finite; a NoData obstruction makes the result False rather than assuming open terrain. This conservative policy conflates blocked and indeterminate cells in the Boolean output.

The algorithm is a discrete teaching baseline. It does not implement R3, R2, XDraw, exact continuous ray/surface intersection, sub-cell observers, directional radar propagation, Fresnel clearance, vegetation/building surface models or time-varying obstructions. Runtime is approximately O(N × L), where N is the number of targets and L is average ray length. Cumulative viewshed repeats the calculation per observer.
