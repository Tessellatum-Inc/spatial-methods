# Implementation verification — STR-packed R-tree

## Scope

Immutable 2D STR bulk-loaded R-tree over closed axis-aligned bounding boxes. Input-order indices are preserved. This package returns envelope candidates; it does not store polygon topology or replace exact geometry predicates.

## Implemented queries

- Closed-box intersection query, including boundary touching.
- Exact k-nearest rectangle query by Euclidean point-to-box distance.
- Deterministic result ordering by distance and original input index.
- Empty-tree and k=0 behavior, plus validation of malformed boxes, query points and k.

## Differential tests

- Range query: 300 seeded boxes, 60 seeded query windows, five node capacities; each result is compared to a brute-force closed-box intersection scan.
- Nearest query: 240 seeded boxes, 100 seeded query points, k from 0 to 20; each result is compared to a brute-force full sort by point-to-box distance and original index.
- Fixed tests cover equal-distance ties, boundary touches, empty trees, and invalid inputs.

## Complexity

STR construction repeatedly sorts each level and packs groups; it is a static bulk loader. Range query prunes disjoint node envelopes. Nearest query uses a min-heap of unexplored nodes and a bounded max-heap of the best k entries. Candidate maintenance is O(log k) per visited entry and result storage is O(k), but worst-case traversal remains O(n) when node envelopes overlap heavily or provide weak lower bounds.

## Reproduction

From this directory:

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```
