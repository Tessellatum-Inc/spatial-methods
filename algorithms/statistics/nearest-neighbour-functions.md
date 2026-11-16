# G, F and J nearest-neighbour functions

The three classical nearest-neighbour summaries describe different aspects of a planar point pattern:

- (G(r)), the nearest-neighbour distribution, is the empirical fraction of observed events whose nearest *other* event is within distance (r).
- (F(r)), the empty-space function, is the empirical fraction of independent test locations whose nearest event is within (r).
- (J(r)=(1-G(r))/(1-F(r))), where the denominator is positive.

The Python implementation accepts observed events, supplied empty-space test locations and radii. It computes Euclidean nearest distances, then evaluates the empirical CDFs with inclusive radius thresholds. Pairwise distance work is blockwise to bound temporary memory, but remains quadratic in event count and proportional to the product of test and event counts.

## Sampling and interpretation

For F to represent empty space in an observation window, test locations should be sampled uniformly and independently over that window. G uses the events themselves as query locations but excludes each event's self-distance; distinct coincident events remain valid zero-distance neighbours.

No edge correction, intensity estimation or simulation envelope is applied. Boundary effects can therefore bias interpretation, especially at larger radii. The J ratio is returned as NaN wherever the empirical (1-F(r)) denominator is zero. These empirical summaries should not be treated as a formal CSR test without a suitable null model and calibration.

See the [implementation and tests](../../implementations/python/ripley-k/README.md) and [verification record](../../catalog/verification/nearest-neighbour-functions.md).
