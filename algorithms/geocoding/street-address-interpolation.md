# Street address interpolation along street segments

## Method

Given an ordered projected street polyline and a monotonic start/end address range, compute each address's normalized fraction along the range. Convert that fraction to cumulative polyline distance, locate the containing segment and linearly interpolate within it. Same-parity ranges default to increments of two; mixed-parity ranges use increments of one. Optional left/right offsets use the local segment normal.

## Assumptions

The address range increases or decreases monotonically along the supplied line, and address spacing is approximately proportional to cumulative street length. Coordinates must be projected planar values in common linear units. Side is relative to the direction of the input polyline.

## Limits

This creates candidate interpolated locations, not verified addresses. It does not infer address ranges, resolve local numbering conventions, assign numbers to building footprints, identify the correct street side, handle intersections or provide quality scores.