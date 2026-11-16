# Cascading overload failures in networks

## Method identity

Motter and Lai (2002) define node load as the number of shortest paths between node pairs that pass through a node. A node's capacity is set proportional to its load in the intact network:

\[ C_i=(1+\alpha)L_i^0,\qquad \alpha\geq0. \]

After an initial attack, shortest-path loads are recomputed. Nodes whose new load exceeds capacity fail; loads are recomputed again until no additional overload occurs. The process is a synchronous cascade model.

## Implemented baseline

The companion Python implementation uses unweighted undirected graphs, Brandes-style shortest-path betweenness, a configurable tolerance, synchronous overload rounds, and an optional round guard. It returns initial loads, capacities, failure rounds, surviving nodes and cascade size. Disconnected pairs contribute no shortest paths. The code uses unnormalized undirected node betweenness (divide ordered-source accumulation by two).

## Interpretation and limitations

This is a structural shortest-path load model, not a physical power-flow, hydraulic, passenger assignment or packet-routing simulator. It assumes all node-pair traffic is routed along shortest paths and that load redistributes instantaneously after each synchronous failure round. It does not model edge capacities, weighted/directed paths, demand matrices, partial rerouting, dynamic traffic, repair, stochastic component failure, protection systems or operator interventions. Results depend on topology and tolerance and should not be presented as real infrastructure failure probabilities.

## Reproducibility

Run `python -m pytest -q --import-mode=importlib` in `implementations/python/network-resilience`. The lab notebook uses a small synthetic graph.

## Primary reference

Motter, A. E., & Lai, Y.-C. (2002). Cascade-based attacks on complex networks. Physical Review E, 66(6), 065102(R). https://doi.org/10.1103/PhysRevE.66.065102.