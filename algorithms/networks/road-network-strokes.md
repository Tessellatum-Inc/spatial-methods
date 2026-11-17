# Good-continuation road-network strokes

Stroke construction groups adjacent road segments into longer perceptually continuous chains. At each graph node, each incident edge is represented by the vector from the junction to its opposite endpoint. For each pair, calculate the deviation from a straight 180-degree continuation. Sort candidate pairs by increasing deviation and greedily pair edges while respecting a one-pair-per-edge constraint at each junction.

These local pairings define an edge-adjacency graph with degree at most two. Its components are traversed as open chains or closed cycles, producing a partition of the input edges.

The baseline assumes an undirected planar embedded graph with accurate junction segmentation and projected coordinates. It is sensitive to the angular threshold and local greedy choices; it does not solve a global matching objective. It does not implement road hierarchy, stroke simplification, topology-preserving map generalisation, dual-carriageway handling or grade-separation inference.
