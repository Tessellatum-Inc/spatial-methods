# Non-FIFO time-dependent routing with unrestricted waiting

A time-dependent edge is non-FIFO when entering it later can produce an
earlier arrival. Ordinary label-setting time-dependent Dijkstra assumes FIFO
arrival functions; applying it unchanged to a non-FIFO profile can discard a
later, faster departure.

This reference implementation solves a bounded discrete-time version. Each
directed edge has a finite mapping from integer departure ticks to
non-negative integer travel durations. The expanded graph contains states
(node, tick), one-tick waiting transitions at every node, and travel
transitions wherever an edge profile defines a departure. Dijkstra on this
finite non-negative graph finds the earliest reachable arrival within the
requested horizon and reconstructs both traversed edges and waiting intervals.

The implementation is exact for the caller-supplied integer departure
profiles, unrestricted zero-cost waiting and finite horizon. Its state count
is O(|V|H), where H is the number of time ticks in the horizon, and its
relaxation work also depends on outgoing edge counts. It is not a continuous
time solver, a restricted-waiting algorithm or a large-network speedup.

Code and tests: [road-routing package](../../implementations/python/road-routing/README.md).

## Reference

Orda, A., & Rom, R. (1990). Shortest-path and minimum-delay algorithms in
networks with time-dependent edge-length. *Journal of the ACM*, 37(3),
607–625. https://doi.org/10.1145/79147.214078.
