# HMM map matching

Map matching infers a plausible road-network path from noisy, sparse position observations. Independent nearest-road snapping is unstable near parallel roads, intersections and grade-separated crossings. A Hidden Markov Model treats candidate road positions as hidden states.

For observation z_t and candidate c_t, an isotropic Gaussian emission model scores lateral offset d:

`P(z_t|c_t) ∝ exp(-d²/(2σ²))`.

A transition model compares observed displacement with legal network distance D(c_(t-1),c_t):

`P(c_t|c_(t-1)) ∝ exp(-|D - observed_displacement|/β)`.

Viterbi maximises the sum of log emission and transition likelihoods over the whole trace.

## Runnable implementation

The [map-matching package](../../implementations/python/map-matching/README.md) implements polyline candidate projection and Viterbi decoding. It requires a caller-supplied network-distance function so road topology, one-way rules, turn restrictions and unreachable pairs are not silently approximated by Euclidean distance.

## Assumptions and limitations

- Coordinates and distances use a suitable projected metric CRS.
- The transition metric must be non-negative, or positive infinity for unreachable pairs.
- Emission errors are isotropic Gaussian; heading, speed, sampling interval and anisotropic GPS error are not modelled.
- Candidate search is a linear scan over all road segments; use a spatial index at scale.
- Educational reference, not a production matcher for raw GPS or global geographic coordinates.

## References

- Newson, P. and Krumm, J. (2009), [Hidden Markov map matching through noise and sparseness](https://doi.org/10.1145/1653771.1653818), ACM SIGSPATIAL.
- [OSRM map matching API](https://project-osrm.org/docs/v5.24.0/api/#match-service).

**Scope:** candidate projection, distance-based HMM emissions/transitions and Viterbi decoding are implemented. Network construction and scalable candidate indexing remain external.
