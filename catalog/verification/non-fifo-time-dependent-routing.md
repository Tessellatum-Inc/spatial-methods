# Verification record: discrete non-FIFO earliest-arrival routing

## Implemented scope

- Finite integer time horizon and integer departure/travel-duration profiles.
- Non-FIFO edge profiles.
- Unrestricted one-tick waiting at every node with zero waiting cost.
- Time-expanded Dijkstra and reconstruction of node path, edge legs and waiting intervals.
- Explicit unreachable result and start-equals-goal behavior.

## Tests

Tests force a later faster departure on a non-FIFO edge, verify waiting at an intermediate node, compare with an independent exhaustive time-expanded reachability oracle, and cover unreachable, identity and invalid profile/horizon cases.

## Limits

No continuous-time profile functions, forbidden/limited waiting, waiting costs, time-dependent edge capacities, multi-criteria objectives or large-network acceleration. Exactness is relative to the discrete input profiles and finite horizon.
