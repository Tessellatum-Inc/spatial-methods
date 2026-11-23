# Maximum flow and minimum cut

A dependency-free Dinic implementation for directed capacitated networks. It uses level graphs and blocking flows, and returns a maximum flow, per-input-arc flow values, the residual-reachable source side and a minimum s-t cut. Parallel and antiparallel arcs are represented independently.

## Run

~~~bash
python -m pip install -r requirements.txt
python -m pytest -q
~~~

## Complexity and assumptions

Dinic's general worst-case bound is O(V²E); stronger bounds apply to restricted network classes. Capacities must be finite and non-negative. The graph is directed; no undirected-edge shorthand is applied. Self-loops are rejected. The routine is a teaching/reference implementation and does not include capacity scaling, push-relabel, min-cost flow, lower bounds, multi-commodity flow or dynamic updates.
