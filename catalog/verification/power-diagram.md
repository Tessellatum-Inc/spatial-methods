# Source verification — weighted Voronoi power diagram

## Identity and bibliography
- Aurenhammer, F. (1987). “Power diagrams: Properties, algorithms and applications.” *SIAM Journal on Computing*, 16(1), 78–96. DOI 10.1137/0216006.

## Technical claims
- Additive squared-distance weights produce linear pairwise bisector half-planes.
- A power cell is the intersection of the clipping region with all pairwise half-planes.
- A site can have an empty clipped cell when dominated by competitors.

## Implementation and tests
- NumPy implementation using Sutherland–Hodgman half-plane clipping.
- Tests cover the unweighted midpoint bisector, a hand-computed weighted boundary, single-site coverage, empty dominated cells, area partition and invalid inputs.

## Limits and rights
2D finite sites, rectangular clipping bounds and floating-point arithmetic only. No multiplicative weights, order-k, farthest-site, segment Voronoi or exact predicates. Original code and explanatory text; bibliographic metadata only.
