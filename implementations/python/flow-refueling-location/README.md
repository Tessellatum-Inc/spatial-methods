# Flow-refueling location model (FRLM)

This exact small-instance solver selects p candidate stations to maximize the
weight of origin-destination routes that can be completed with a vehicle's
finite range.

## Route contract

Each route supplies:
- total route length;
- a mapping from candidate station ID to distance along that route;
- a non-negative flow weight supplied separately.

A vehicle starts with a full tank. It can reach the first selected station
within one range, travel between consecutive selected stations within one
range, and reach the destination from the last station within one range.
A route no longer than the vehicle range is feasible without a selected
station.

## Algorithm

The reference solver enumerates every p-site subset and checks route
feasibility. An empty candidate set is valid when p=0; it correctly serves
only routes no longer than the available range. Candidate IDs must otherwise
be unique and hashable, and numeric inputs must be finite. Complexity is exponential in candidate count:
O(binomial(m,p) times total route-station incidences). This is intended for
small instances, independent validation and benchmark oracles.

## Assumptions and limitations

Routes are fixed and ordered; station positions are known along each route.
The model assumes a full initial tank, identical vehicle range, unlimited
refueling at selected sites and no detours. It does not infer paths from a
road graph, model partial charging, station capacity, queues, heterogeneous
vehicles, charging time or energy consumption by grade/speed. It is a
simplified FRLM baseline, not a full electric-vehicle charging model.

The test suite includes a seeded exhaustive subset oracle over randomized
small instances, endpoint refuelling, empty candidate sets, and invalid or
non-finite input checks.

## Difference from FCLM

FCLM counts a path when it encounters at least one selected facility.
FRLM requires a feasible sequence of refueling stops under a range constraint.
The two objectives are not interchangeable.

## Run

    python -m pytest -q
