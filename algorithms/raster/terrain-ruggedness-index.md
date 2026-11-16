# Riley terrain ruggedness index (TRI)

## Definition

For a raster cell \(i\) and its eight immediate neighbours \(N_8(i)\), the Riley terrain ruggedness index is

\[
\operatorname{TRI}_i =
\sqrt{\sum_{j\in N_8(i)}(z_j-z_i)^2}.
\]

It measures local elevation variability, in the elevation unit. A flat 3×3 neighbourhood has TRI zero; larger values indicate greater local relief.

## Implementation

The Python function riley_terrain_ruggedness_index uses the eight cells in a 3×3 neighbourhood. It requires every cell in that neighbourhood to be finite and returns NaN at the outer border or wherever NoData occurs in the neighbourhood. The optional positive z_factor is applied to vertical differences.

## Important distinction

“TRI” is also used for other formulas, including mean absolute elevation difference and related normalizations. This implementation is specifically the Riley square-root-of-sum-of-squares definition. Values from different definitions, neighbourhood sizes, cell resolutions or vertical units are not directly interchangeable.

## Verification

Tests cover the exact eight-neighbour formula, flat terrain, vertical scaling, NoData propagation and invalid scale values.
