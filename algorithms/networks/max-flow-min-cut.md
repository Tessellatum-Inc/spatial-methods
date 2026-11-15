# Maximum flow and minimum cut

A flow network is a directed graph with a non-negative capacity on each arc. Given source s and sink t, maximum flow asks for the greatest feasible amount that can be sent from s to t while respecting arc capacities and flow conservation at intermediate vertices.

## Residual networks and augmenting paths

For each original arc, the residual network records how much additional flow can be sent forward and how much existing flow can be cancelled in reverse. An augmenting path is a source-to-sink path with positive residual capacity. Its bottleneck is the minimum residual capacity along that path. Augmenting by the bottleneck preserves feasibility and increases total flow.

Edmonds–Karp selects an augmenting path using breadth-first search, minimizing the number of arcs. Repeating until no augmenting path exists yields a maximum flow. Its worst-case complexity is O(VE²).

## Minimum cut

A cut partitions vertices into S and T with s in S and t in T. Its capacity is the sum of original capacities directed from S to T. The max-flow/min-cut theorem states that maximum-flow value equals minimum-cut capacity. After the final augmentation, vertices reachable from s in the residual network form the source side of a minimum cut.

## GIS applications

- Identify bottleneck links in road, transit, water and power networks.
- Model evacuation throughput under link-capacity constraints.
- Assess vulnerability by finding low-capacity cuts separating communities or facilities.
- Support network partitioning and infrastructure planning.

Capacity must be interpreted carefully. Road capacity, transit passenger throughput and water-pipe capacity are different quantities; shortest-path cost is not flow capacity.

## Implementation and evidence

The [Python implementation](../../implementations/python/max-flow-min-cut/README.md) provides Edmonds–Karp and minimum-cut extraction. Tests include the canonical six-vertex, 23-unit flow network and seeded random graphs checked against exhaustive enumeration of all s-t cuts. The independent cut oracle is exponential and is used only on small test graphs.

## Limitations

The teaching implementation uses floating-point capacities and is not a high-performance solver for massive networks. It does not cover multicommodity flow, lower/upper-bound circulation, min-cost flow or node-splitting capacity transformations.
