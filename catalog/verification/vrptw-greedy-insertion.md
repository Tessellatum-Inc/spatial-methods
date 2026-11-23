# Verification record: greedy VRPTW insertion

## Scope

The package implements a deterministic Euclidean greedy construction for a single-depot, homogeneous-capacity VRPTW. It checks capacity, customer service-start windows, waiting, service durations and return to the depot by its closing time. It returns schedules and an explicit unserved-customer list.

## Evidence in the repository

- Tests cover feasible multi-route construction, capacity limits, waiting and service-time propagation, depot return, vehicle limits, infeasible windows and invalid controls.
- The implementation uses deterministic incremental closed-route distance and customer-index tie breaking.
- The existing `routing-heuristics` package is already included in the checked-in Python CI manifest.

## Limits of this verification

This is a greedy constructive baseline, not an exact or competitive VRPTW solver. It does not backtrack, repair routes, model road-network travel times, heterogeneous fleets, breaks, pickup-and-delivery precedence, stochastic travel, ALNS or branch-and-price. No standard benchmark comparison or optimality gap is reported. The grouped source entry remains partial.

## Status

Implementation and focused tests are present. The current GitHub Actions run must pass before CI verification can be recorded; the source entry is not fully verified.
