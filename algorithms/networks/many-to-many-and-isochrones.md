# Many-to-many shortest paths and network isochrones

## Many-to-many shortest paths

Given source set S and target set T, the many-to-many query returns a shortest path and cost for every requested pair. A transparent baseline runs one single-source Dijkstra search per source, then reconstructs the requested target paths from each predecessor tree.

For |S| sources, the search work is approximately |S| repetitions of Dijkstra. This is useful as a reference implementation and for small query batches, but it is not a high-performance many-to-many routing index. Large road networks may need shared preprocessing, contraction hierarchies, customizable route planning, or transit-specific algorithms.

The implementation supports directed graphs and finite non-negative edge weights. Unreachable pairs return no path and infinite cost.

## Network isochrones

For source s and budget B, an isochrone is the set of network nodes whose shortest-path cost from s is at most B. The implementation uses a cutoff Dijkstra search and returns:
- shortest costs for all reached nodes;
- predecessor links for reconstructing paths;
- directed frontier arcs from reached nodes whose traversal would exceed the budget.

The result is a graph-based reachability region, not a polygon. Polygonizing an isochrone requires an additional geometric representation and a choice about how to interpolate between network edges.

## Complexity and limitations

The baseline is output-sensitive repeated Dijkstra. It does not implement contraction hierarchies, hub labels, transit routing, time-dependent edge costs, turn-expanded state, stochastic travel times or polygonization. It treats edge weights as static additive costs and includes nodes exactly on the budget boundary.

## Implementation

See the [tested Python reference package](../../implementations/python/shortest-paths/README.md) and [network query tests](../../implementations/python/shortest-paths/test_network_queries.py).

## Source

The methods correspond to the Section 1 source entries for shortest paths and for service areas/isochrones and many-to-many routing on pages 1–2 of the [preserved source transcription](../../source-inventory/pages-01-05.md).
