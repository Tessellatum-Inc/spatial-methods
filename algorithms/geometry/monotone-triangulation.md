# Y-monotone polygon triangulation

A y-monotone polygon intersects every horizontal line in either an empty set
or one connected interval. Its vertices form two chains from the topmost to
the bottommost vertex. Sorting vertices from top to bottom and maintaining a
stack allows the triangulation to be constructed without repeatedly searching
the entire polygon for ears.

The implementation in [Python](../../implementations/python/monotone-triangulation/README.md)
uses exact rational orientation predicates and validates a simple, strictly
y-monotone ring before triangulating. It deliberately rejects equal vertex
heights in this first version: horizontal edges and tied events need a
consistent symbolic ordering and should not be resolved by arbitrary x-order
alone.

For a polygon with n vertices, the result contains n-2 triangles and n-3
internal diagonals. Exact area conservation and positive triangle orientation
are checked at runtime. These checks do not replace independent overlap and
edge-incidence verification.

This is a triangulator for polygons that are already y-monotone. It is not the
monotone partition algorithm for arbitrary simple polygons; that sweep-line
partition remains a separate implementation target.
