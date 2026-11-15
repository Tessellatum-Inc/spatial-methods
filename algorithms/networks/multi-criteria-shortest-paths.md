# Pareto multi-criteria shortest paths

Stable ID: SA-NETWORK-PARETO-SHORTEST-PATHS · Draft 0.1 · Source compendium section 18

## Why one shortest path is not always enough

A route can be faster but longer, shorter but more energy-intensive, or safer but slower. Combining these criteria into a single weighted sum requires a preference choice and can hide valid trade-offs. A multi-criteria shortest-path algorithm returns the set of nondominated routes.

## Labels and dominance

Each edge has a nonnegative additive cost vector \(c_e\in\mathbb{R}_{\ge0}^m\). A path label stores its accumulated vector and path. Label a dominates label b when \(a_i\le b_i\) for every objective and at least one inequality is strict. Dominated labels at the same node can be discarded because every continuation adds the same nonnegative edge vector.

The implementation uses a lexicographically ordered priority queue and componentwise dominance pruning. It retains multiple labels per node, prevents repeated nodes in a path, and returns all nondominated source-to-target labels. Equal cost vectors retain the first discovered path. An optional per-node label cap raises an error rather than silently truncating the frontier.

## Correctness scope and complexity

For finite graphs with nonnegative additive edge costs, a Pareto-optimal route can be chosen simple: removing a cycle cannot increase any objective. The algorithm enumerates the nondominated labels under this model. The number of nondominated labels can grow exponentially in graph size, so this is an exact output-sensitive method, not a polynomial-time replacement for Dijkstra.

## Limitations

- No negative edge costs.
- No automatic scalar preference or final route selection.
- No turn restrictions, time-dependent costs, stochastic route choice or timetable integration unless represented explicitly in the state graph and edge vectors.
- No route diversity or skyline service beyond the returned Pareto frontier.
- Equal-cost alternative paths are deduplicated to one representative path.

## Implementation and tests

A tested Python baseline is available in the [shortest-path package](../../implementations/python/shortest-paths/README.md), with the [Pareto label-setting module](../../implementations/python/shortest-paths/pareto_paths.py) and `test_pareto_paths.py`. The [source-verification note](../../catalog/verification/multi-criteria-shortest-paths.md) records the identity, technical scope and limitations. Explore the [interactive Pareto routing lab](../../notebooks/pareto-multi-criteria-routing-lab.ipynb) to inspect trade-offs and apply preferences only after the nondominated frontier has been computed.

## Reference

Martins, E. Q. V. (1984). “On a multicriteria shortest path problem.” *European Journal of Operational Research*, 16(2), 236–245. https://doi.org/10.1016/0377-2217(84)90077-8.

## Exercises

1. Construct a graph where three routes are pairwise nondominated.
2. Show why a weighted sum can omit a Pareto-optimal route for a particular finite set of weights.
3. What happens to the frontier when one objective is removed?
4. Why does a nonnegative cycle never improve a path's cost vector?
