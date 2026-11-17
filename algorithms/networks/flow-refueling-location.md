# Flow-refueling location model (FRLM)

The flow-refueling location model selects candidate refueling stations to
maximize the weight of origin-destination routes that can be completed by a
vehicle with finite range. A route is not served merely because it passes one
selected station: the selected stations must form a feasible sequence.

For route length L, vehicle range R and selected stations at ordered route
distances s_1,...,s_k, feasibility requires

    s_1 <= R
    s_(i+1) - s_i <= R
    L - s_k <= R

A route with L <= R is feasible without any station. The reference solver
uses caller-supplied route lengths and candidate-station positions, then
enumerates candidate-site subsets exactly. An empty candidate set is valid
when zero stations are selected. Numeric inputs must be finite; booleans and
integers too large for finite floating-point conversion are rejected. Seeded
randomized tests compare the solver with an independent subset and route-gap
oracle. It is exponential and intended for small instances and test oracles.

The implementation assumes fixed routes, full initial range, identical
vehicles, unlimited refueling and no detours. It does not model partial
charging, queues, station capacity, energy use by road grade or vehicle
heterogeneity.

Do not confuse FRLM with the flow-capturing location model (FCLM), which
counts a route when it encounters at least one selected facility.

See the Python reference package for route input format, solver and tests.
Reference: Kuby, M. J., & Lim, S. (2005). The flow-refueling location
problem for alternative-fuel vehicles. Socio-Economic Planning Sciences,
39(2), 125–145. https://doi.org/10.1016/j.seps.2004.03.001
