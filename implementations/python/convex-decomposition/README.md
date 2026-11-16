# Convex decomposition by triangulation and greedy merging

This package triangulates one simple polygon ring with the repository's exact-predicate ear-clipping implementation, then greedily merges adjacent pieces whenever the merged boundary remains convex.

## Run the tests

```bash
python -m pip install -r requirements.txt
PYTHONPATH=../ear-clipping python -m pytest -q
```

## Scope

- One simple, non-degenerate polygon ring; no holes or self-intersections.
- Exact rational predicates through `fractions.Fraction`.
- The output is a set of convex pieces whose areas sum exactly to the input area.
- Greedy merge order affects the partition. The result is not guaranteed to use the fewest possible pieces.
- This is a teaching baseline, not a complexity-optimized or certified Hertel–Mehlhorn implementation.

The initial triangulation uses the current ear-clipping package, whose transparent implementation has an (O(n^3)) worst-case bound. The merge pass also uses straightforward repeated pair scans. Do not attribute the linear-time bound of a specialized Hertel–Mehlhorn post-processing algorithm to this package.


## Merge-candidate maintenance

The greedy merge stage now indexes piece ownership by undirected boundary edge and processes candidate pairs from a work queue. When two pieces merge, only the new piece's edge-neighbours are added to the queue; the implementation no longer rescans every pair of current pieces after every successful merge. This reduces unnecessary candidate comparisons on partitions with many triangles. It remains a greedy triangulate-and-merge teaching baseline, not the optimized Hertel–Mehlhorn algorithm and not a minimum-piece partition.


## Hertel–Mehlhorn-style diagonal removal

The module also exposes `hertel_mehlhorn_decompose(vertices)`. It starts from the same ear-clipping triangulation, freezes the initial internal-diagonal set, and considers each original diagonal once. A diagonal is removed only when its two current incident pieces have a convex union. This is a distinct single-pass variant from `convex_decompose`, whose work queue may revisit newly exposed adjacencies.

This is an executable diagonal-removal baseline, not a certified reproduction of every implementation detail or complexity guarantee in the published Hertel–Mehlhorn algorithm. The repository's ear-clipping seed is O(n^3) in the worst case, and the current merge predicates are not the specialized linear-time post-processing implementation. No minimum-piece guarantee is claimed.
