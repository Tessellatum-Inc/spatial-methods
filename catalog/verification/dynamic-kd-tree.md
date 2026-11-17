# Verification record: scapegoat-style dynamic k-d tree

## Implemented scope

- Stable monotonically increasing insertion IDs.
- Dynamic insertion with subtree size and active-count maintenance.
- Lazy deletion and subtree rebuilding when tombstones exceed the alpha threshold.
- Rebalancing when a child exceeds the configured alpha fraction.
- Exact nearest, k-nearest, radius and inclusive rectangle queries.
- Deterministic tie-breaking by stable ID.

## Tests

A seeded mixed insert/delete sequence compares all query families with
brute-force oracles after each mutation. Additional tests cover duplicate
coordinates, stable IDs, deletion of unknown IDs, empty trees and invalid
alpha/ID/coordinate inputs.

## Reference

The subtree-rebuilding idea is related to Galperin and Rivest's scapegoat trees (SODA 1993). The present k-d-tree adaptation uses a direct local balance/tombstone threshold and has no inherited complexity proof.

## Limits

Subtree rebuilds sort active points and can be O(m log² m). The implementation
does not claim worst-case logarithmic updates, persistence, concurrency,
disk-backed storage, high-dimensional efficiency or geodesic distance.
