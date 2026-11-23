# Weighted head-banging spatial smoother

A dependency-free implementation of the weighted two-dimensional head-banging smoother for values observed at projected planar locations.

## Quick start

~~~python
from head_bang import head_bang
points = [(0,0), (-1,0), (1,0), (0,1), (0,-1)]
rates = [1.0, 2.0, 9.0, 3.0, 4.0]
weights = [100, 80, 120, 90, 110]
result = head_bang(points, rates, weights, n_neighbors=4)
print(result["smoothed_values"])
~~~

For each target, nearly collinear triples are formed from its nearest neighbours. Weighted medians of the lower and higher endpoint values form low and high screens. The target is updated by a weighted median of the two screens and its current value. Screen weights are the sums of selected endpoint weights; the target's weight is multiplied by the number of triples.

Defaults: 30 nearest neighbours, 45-degree deviation from a straight line, about two-thirds as many triples as neighbours, and at most 10 synchronous iterations.

## Assumptions and limitations

Coordinates must be projected planar coordinates. Weights are strictly positive caller-defined reliability/population weights. Neighbourhoods are Euclidean k-nearest neighbours, not polygon contiguity. Locations with no qualifying triples are left unchanged; this is a conservative fallback, not the full Head-Bang software's special corner-point rules. No age adjustment, uncertainty, risk model or automatic parameter optimization is included.
