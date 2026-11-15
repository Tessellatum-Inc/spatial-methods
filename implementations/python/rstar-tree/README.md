# Mutable 2D R*-tree

Dependency-free incremental in-memory bounding-box index. Insertion uses
R*-tree-style overlap-enlargement subtree selection near leaves, margin-based
split-axis selection, overlap/area split distribution, and forced reinsertion.
On overflow, the farthest 30% (subject to minimum fill) are removed and
reinserted at their original tree level, at most once per level in one
top-level insertion. Stable integer record IDs are preserved.

Queries return IDs whose closed axis-aligned envelopes intersect the query.
Duplicate and zero-area boxes are retained. Use suitable planar coordinate
units and refine envelope candidates with exact geometry predicates when
indexing non-rectangular objects.

Deletion is supported by condense-tree processing: underfilled nodes are
removed, their remaining entries/subtrees are reinserted at their original
levels, and a one-child root is collapsed. Record IDs are stable; deleting an
unknown or already deleted ID returns False. This is still not a full
production R*-tree: bulk loading, kNN, disk pages, persistence, concurrency
and robust exact arithmetic are not implemented. Split and query operations use floating-point bounds.

Run `pytest -q` from this directory.
