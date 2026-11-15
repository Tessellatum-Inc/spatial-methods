# Intern walkthrough: D8 flow direction

## 1. Start with the elevation grid

Each cell stores an elevation. D8 examines the eight adjacent cells around a valid cell. Row indices increase southward and column indices increase eastward in this teaching convention.

## 2. Calculate slope to each neighbour

For a candidate neighbour at row/column offset $(\Delta r,\Delta c)$:

$$
s=\frac{z_0-z_1}{\sqrt{(\Delta r\,s_r)^2+(\Delta c\,s_c)^2}}
$$

where $s_r$ and $s_c$ are row and column cell spacing. Only strictly positive slopes are eligible.

## 3. Choose the steepest descent

The neighbour with the largest positive slope receives the flow. The code maps directions to the ESRI power-of-two codes and uses a fixed iteration order to resolve equal slopes reproducibly.

## 4. Handle cells without a lower neighbour

A valid cell with no lower valid neighbour receives code 0. This can represent a flat or a pit in this simple implementation. Invalid or NoData cells receive -1 and are not considered as neighbours.

## 5. Understand what is not solved

Real DEM conditioning often needs explicit flat resolution, depression filling or breaching, and treatment of artefacts. This implementation does none of those. It also does not calculate flow accumulation, stream extraction or watershed boundaries.

## 6. Check the units

Horizontal cell spacing and elevation values must use compatible units for slope comparisons. If horizontal coordinates are metres and elevations are feet, convert before running the algorithm. Document the DEM CRS, vertical datum and NoData policy.

## 7. Compare multiple-flow-direction routing

D8 sends all contribution to one steepest neighbour. The companion MFD variant in mfd_flow.py computes a positive slope gradient to every strictly lower valid neighbour. It raises each slope to a positive convergence exponent and normalises the values to fractions that sum to one.

The exponent controls concentration. A larger exponent places more of the cell's contribution on the steepest neighbour; a smaller exponent spreads it more evenly. The eight fraction channels follow E, SE, S, SW, W, NW, N, NE.

Flow accumulation validates that each positive fraction points to a valid, strictly lower neighbour. This makes the routing graph acyclic. Kahn's topological traversal processes upstream cells before their receivers and conserves initial contributions at terminal sinks. By default each cell contributes one unit; pass cell-area values to accumulate area.

This is a bounded power-law MFD variant. It does not implement D-infinity, adaptive MFD, contour-length correction, flat resolution or depression filling.
