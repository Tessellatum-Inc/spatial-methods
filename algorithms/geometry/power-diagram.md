# Weighted Voronoi power diagram

For sites p_i with additive weights w_i, the power distance is

\[
\pi_i(x)=\|x-p_i\|^2-w_i.
\]

The power cell of site i is the set of points where π_i is no greater than every competing site's power distance. Pairwise comparison cancels the quadratic terms, leaving a half-plane:

\[
2(p_j-p_i)^T x\le \|p_j\|^2-w_j-\|p_i\|^2+w_i.
\]

The implementation starts from a rectangular clipping window and intersects it with these half-planes using Sutherland–Hodgman clipping. It returns one polygon per input site; dominated sites may have empty cells.

## Scope and limits

This is a finite-site, rectangularly clipped 2D power diagram evaluated with floating-point arithmetic. It is not a multiplicatively weighted Voronoi diagram, order-k diagram, farthest-site diagram, segment Voronoi diagram or exact-predicate geometry kernel. Complexity is quadratic in site count times polygon clipping work; it is a correctness-oriented small-input baseline.

## Source
- Aurenhammer, F. (1987). Power diagrams: Properties, algorithms and applications. *SIAM Journal on Computing*, 16(1), 78–96. https://doi.org/10.1137/0216006.

Implementation: [Voronoi–Delaunay package](../../implementations/python/voronoi-delaunay/README.md).
