# Raster cut-and-fill volume

## Purpose

Cut-and-fill analysis estimates the volume difference between an existing terrain surface and a proposed design surface. It is commonly used for earthworks quantities, grading comparisons and reservoir or excavation scenarios.

## Cellwise calculation

For existing elevation \(z_i\) and design elevation \(d_i\):

\[
c_i=\max(z_i-d_i,0),\qquad f_i=\max(d_i-z_i,0).
\]

For constant rectangular cell dimensions \(\Delta x,\Delta y\), cell area is \(A_c=\Delta x\Delta y\). Total cut and fill volumes are

\[
V_c=A_c\sum_i c_i,\qquad V_f=A_c\sum_i f_i.
\]

The net cut volume is \(V_c-V_f\).

## Implementation contract

The cut_fill_volume function accepts two same-shaped 2D arrays, horizontal cell dimensions and an optional Boolean validity mask. It returns cut-depth and fill-depth rasters, total cut and fill volumes, net cut volume, cell area and valid-cell count. Cells with non-finite values in either surface are excluded and receive NaN in both depth outputs.

Both surfaces must already be aligned and expressed in compatible vertical units. For example, metre elevations and metre cell dimensions produce cubic metres.

## Limitations

This direct raster method does not reproject or resample either surface, correct vertical datums, account for material swell/shrinkage, apply construction tolerances, or infer missing terrain. Variable-area cells require per-cell area weighting rather than one constant cell area. Results depend on DEM/design resolution and alignment.

## Verification

Tests cover mixed cut/fill cells, rectangular cell areas, identical surfaces, NoData and mask handling, shape validation and invalid cell dimensions.
