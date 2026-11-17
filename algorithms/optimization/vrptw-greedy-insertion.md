# Vehicle routing with time windows: greedy feasible insertion

## Problem

The vehicle-routing problem with time windows (VRPTW) assigns customers to vehicle routes while respecting vehicle capacity and customer service windows. A route must also return to its depot within the depot's operating window. This makes route order a scheduling decision as well as a distance decision.

For customer i, let demand be q_i, service duration s_i, and time window [a_i,b_i]. If a vehicle reaches i at time t_i, service begins at max(t_i,a_i), and the next departure occurs after service. Feasibility requires the service-start time not to exceed b_i and the accumulated route load not to exceed capacity.

## Greedy construction

The companion implementation starts each route at the depot's opening time. At the current stop, it evaluates every unserved customer and retains candidates that satisfy:

1. remaining vehicle capacity;
2. the candidate's service-start window, allowing waiting;
3. the ability to return from that candidate to the depot before depot closing.

Among feasible candidates, it chooses the smallest incremental closed-route distance, breaking ties by customer index. It repeats until no feasible customer can be appended, closes the route, and starts another vehicle if the vehicle limit permits.

Each stop records arrival, service-start and departure times. The result explicitly reports customers left unserved rather than silently dropping them.

## Assumptions and limitations

- Distances are symmetric Euclidean distances between planar coordinates in one consistent linear unit. This is not road-network travel time.
- Demands are non-negative and indivisible; all vehicles share one capacity.
- Time windows constrain service start, waiting is allowed, and service durations are deterministic.
- The depot has one opening/closing window. Vehicles start no earlier than depot opening and must return by depot closing.
- The construction is deterministic and greedy. It does not backtrack, repair an earlier route, or guarantee that all feasible customers will be served.
- Fleet heterogeneity, multiple depots, time-dependent travel, breaks, driver rules, pickup-and-delivery precedence, split deliveries, stochastic travel, ALNS and exact branch-and-price are outside scope.

## Complexity

For each appended customer, the baseline scans the remaining unserved customers and computes a constant amount of distance and schedule information. Across n customers this gives O(n²) candidate evaluations in the straightforward implementation, excluding coordinate parsing. The transparent scan is intended for teaching and small instances, not large dispatch workloads.

## Validation

Tests cover capacity, inclusive service windows, waiting, service durations, depot return feasibility, vehicle limits, deterministic route construction and explicit unserved-customer reporting. A production solver should additionally compare route feasibility and objective quality against an exact or trusted VRPTW benchmark on standard instance sets.
