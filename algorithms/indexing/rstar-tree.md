# R*-tree: overlap-aware indexing and forced reinsertion

An R*-tree is a height-balanced, disk-oriented spatial index whose bounding
rectangles organise objects into a hierarchy. Its insertion policy tries to
reduce overlap and coverage growth, since overlap determines how many sibling
subtrees a query must visit.

At each level, subtree selection considers area enlargement; immediately above
the leaves it gives priority to overlap enlargement. Overflow splitting first
chooses an axis by the sum of margins over legal distributions, then chooses a
distribution with low overlap and area. Unlike a basic R-tree split-only
strategy, an R*-tree can force-reinsert a fraction of entries when a non-root
node overflows. Entries farthest from the overflowing node's centre are
removed and reinserted at the same tree level. A level is reinserted at most
once during a top-level insertion, preventing reinsertion loops; a later
overflow at that level is resolved by splitting.

The [Python implementation](../../implementations/python/rstar-tree/README.md)
is an in-memory 2D teaching index for finite axis-aligned boxes. It implements
overlap-aware descent, R*-style split heuristics and level-preserving forced
reinsertion, with seeded brute-force query comparisons and structural checks
for equal leaf depth, parent links, bounding rectangles, minimum occupancy and
exactly-once record storage.

It is not a disk-page implementation or a complete production R*-tree.
Deletion uses condense-tree processing: underfilled nodes are detached and
their remaining entries or subtrees are reinserted at their original levels;
a one-child root is collapsed. Record IDs remain stable and deleted IDs are
not reused. Bulk loading, disk-page management, persistence and concurrency remain
outside scope. Best-first k-nearest search is also available for point-to-rectangle distance:
node MBR distances provide lower bounds, and the search stops only when the
next lower bound is strictly worse than the current kth candidate so stable
ID tie-breaking is preserved. The returned distance is to the indexed
rectangle, not an underlying arbitrary geometry. Envelope query results for
arbitrary geometries require a subsequent exact predicate test.
