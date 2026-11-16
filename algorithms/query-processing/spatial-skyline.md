# Spatial skyline queries

## Problem

A nearest-neighbour query returns the single closest object. A spatial skyline query instead returns objects that represent meaningful trade-offs between proximity to a query location and other attributes such as cost, capacity, quality or risk.

For object i at location x_i, query location q, and attributes a_i1,...,a_ik, define the criterion vector

[
z_i=(|x_i-q|^2,;s_1a_{i1},ldots,s_ka_{ik}),
]

where s_j=1 when attribute j is minimised and s_j=-1 when it is maximised. Squared distance preserves Euclidean distance ordering without a square root.

## Dominance and skyline

Object i dominates object j when z_i is no worse on every criterion and strictly better on at least one. The spatial skyline is the set of objects not dominated by any other object. This is a Pareto frontier, not a weighted score: it avoids choosing arbitrary exchange rates between distance, price, quality or other attributes.

## Block-nested-loop algorithm

The reference implementation processes objects in input order and maintains a current skyline:

1. Compare the candidate with every current skyline object.
2. If any incumbent dominates it, discard the candidate.
3. Otherwise remove incumbents dominated by the candidate and insert it.
4. Return surviving original indices in input order.

For n objects and k total criteria, worst-case time is O(n²k). Working memory is O(sk), where s is the current skyline size. Skyline size can approach the full dataset when criteria conflict.

## Input and interpretation

- Locations are finite 2D coordinates in one projected Cartesian CRS and linear unit.
- The query location is a finite 2D coordinate.
- Attributes are a finite N-by-K numeric matrix.
- Distance is always minimised; attribute directions are explicit.
- Equal criterion vectors do not strictly dominate one another, so tied objects are all returned.
- Results depend on the query point, selected attributes, units and optimisation direction.

The current package is a transparent exact baseline. R-tree filtering, branch-and-bound, partitioned skyline algorithms, network distance, textual relevance and approximate skyline semantics are not implemented.

## Verification

Tests cover trade-offs, dominated objects, attribute maximisation, query-location sensitivity, ties, empty and singleton inputs, invalid values, and seeded comparison against an independent pairwise dominance oracle.

## Reference

Sharifzadeh, M. and Shahabi, C. (2006). “The spatial skyline queries.” *Proceedings of the 32nd International Conference on Very Large Data Bases (VLDB)*.

See the [runnable package](../../implementations/python/spatial-skyline/README.md).
