# Verification — broad-phase collision detection

- Source: Section 9, page 19, collision-detection row.
- Implemented: sweep-and-prune, uniform spatial hashing and median-split static
  AABB BVH, with a brute-force overlap oracle.
- Tests: edge/corner contact, disjoint boxes, multiple hash cell sizes,
  BVH queries, empty/singleton input and invalid geometry/parameters.
- Scope: exact AABB candidate pairs, not general geometry intersection.
- Open: dynamic BVH updates, 3-D volumes, continuous collision detection and
  narrow-phase polygon/mesh collision.
- Status: partial contribution to grouped source entry.
