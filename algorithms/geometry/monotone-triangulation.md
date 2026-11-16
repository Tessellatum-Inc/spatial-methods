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

The same Python module now also contains `partition_y_monotone`, a general
simple-polygon sweep that classifies start, end, split, merge and regular
vertices, maintains helper edges, and inserts partition diagonals. Its current
status structure is a Python list, so the implementation is O(n^2) worst case;
a balanced search tree is needed for the textbook O(n log n) bound. It requires
distinct vertex heights, rejects consecutive collinear event triples, and does not yet handle holes or horizontal event ties.
`triangulate_general` composes this partition with the stack triangulator.
