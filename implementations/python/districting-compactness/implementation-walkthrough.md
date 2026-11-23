# Districting compactness walkthrough

1. Remove an optional repeated closing vertex and validate finite 2D
   coordinates with at least three distinct vertices.
2. Compute planar area by the shoelace formula and perimeter by summing
   Euclidean segment lengths.
3. Compute the minimum enclosing circle of all boundary vertices using a
   deterministic incremental support-set algorithm.
4. Evaluate Polsby–Popper, Reock and Schwartzberg from area, perimeter and
   enclosing-circle radius.

The implementation assumes a simple exterior ring in a projected CRS.
It does not interpret holes or multipart boundaries, and it does not
encode districting fairness constraints.
