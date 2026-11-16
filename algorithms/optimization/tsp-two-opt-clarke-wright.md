# TSP 2-opt and Clarke–Wright CVRP heuristics

## 2-opt for the travelling salesperson problem

Given a closed tour and two non-adjacent edges (a,b) and (c,d), 2-opt removes
those edges and reconnects (a,c) and (b,d), reversing the intervening segment.
For symmetric Euclidean costs, accept the exchange when the new edge sum is
strictly smaller. Repeating until no improving exchange remains yields a
2-opt local optimum, not a globally optimal TSP tour.

The reference implementation fixes the first point at index zero and uses
deterministic first-improvement scanning. Its worst-case work per pass is
quadratic in the number of tour vertices.

## Clarke–Wright savings for capacitated VRP

For customers i and j and depot 0, the savings score is
s(i,j)=d(0,i)+d(0,j)-d(i,j). Start with one depot-customer-depot route per
customer, sort savings descending, then merge routes when i and j are current
route endpoints and the merged load respects capacity. The implementation
uses the parallel variant and deterministic tie-breaking.

The method produces a feasible heuristic solution when each individual
demand fits capacity. It does not prove optimality. This baseline assumes a
single depot, symmetric planar Euclidean costs, homogeneous vehicles,
indivisible demands and no time windows or precedence constraints.

See [the Python package](../../implementations/python/routing-heuristics/README.md)
for tests and a runnable example.
