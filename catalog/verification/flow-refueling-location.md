# Source verification — flow-refueling location model

## Identity and distinction

The flow-refueling location problem (FRLP/FRLM) is distinct from the flow-capturing location model (FCLM). FCLM counts a route when it passes at least one selected facility. FRLM requires a feasible sequence of refuelling stops so that every segment from the origin, between selected stops, and to the destination is within vehicle range.

Primary reference:
- Kuby, M. J., & Lim, S. (2005). The flow-refueling location problem for alternative-fuel vehicles. *Socio-Economic Planning Sciences*, 39(2), 125–145. https://doi.org/10.1016/j.seps.2004.03.001

This is the canonical citation used by the algorithm record. Publisher metadata and project-level redistribution rights are separate review dimensions and are not claimed complete here.

## Mathematical contract

For a fixed route of length L, vehicle range R > 0, and selected stations at ordered route positions 0 <= s1 <= ... <= sk <= L, every consecutive gap must be at most R, including the origin and destination gaps. A route with L <= R needs no selected station. A selected station at either route endpoint is permitted.

The exact reference implementation accepts fixed route IDs and lengths, candidate-station positions along each route, matching non-negative route weights, a unique candidate-site sequence, a station budget p, and one common vehicle range. It enumerates every p-site subset and maximizes the sum of weights for feasible routes. Ties retain the first subset in caller candidate order.

## Independent validation

The package tests include hand-calculated feasible and infeasible multi-stop examples, an independently written exhaustive subset oracle, and seeded randomized small instances comparing all candidate subsets with a separate route-gap predicate. They also cover zero-length and short routes, zero station budget and an empty candidate set, endpoint stations, exact-range gaps, mismatched route/weight keys, duplicate candidates, out-of-route positions, negative weights, invalid budgets and ranges, booleans, NaN, infinities, non-iterable candidate inputs and integers too large to convert to finite floating point.

The randomized oracle constructs the ordered origin/station/destination boundary sequence and checks each consecutive gap. It does not call the implementation's internal feasibility function.

## Implementation boundary

This is an exact exponential-time small-instance baseline, not a scalable production solver. It assumes fixed routes, caller-supplied station positions, full initial range, identical vehicles, unlimited refuelling and no detours. It does not solve road-network path generation, partial charging, station capacity, queues, heterogeneous fleets, grade/speed-dependent energy use, charging schedules or trajectory map matching. No approximation ratio or scalability claim is made.

The grouped source row also includes trajectory-derived charging demand and other charging-infrastructure methods; this record verifies only the FRLM component. The remaining methods require separate child records and validation.

## Rights

Only the mathematical model and bibliographic metadata are summarized. No source prose, figures, code or datasets are reproduced. Permission to redistribute the original compendium and transcription remains unresolved.
