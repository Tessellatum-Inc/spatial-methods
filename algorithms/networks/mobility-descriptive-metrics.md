# Mobility metrics: radius of gyration, entropy and predictability

For ordered planar positions, radius of gyration is the square root of the weighted mean squared distance from the weighted centroid. Step lengths are Euclidean distances between consecutive positions; signed turning angles use the two-dimensional cross and dot products.

For a discrete sequence of visit labels, Shannon entropy H = -Σ pᵢ log pᵢ is reported in nats, with exp(H) as the effective number of states. Given an entropy value and a finite state count N, the maximum predictability bound is obtained by solving the Fano equality H = -Π log Π -(1-Π) log((1-Π)/(N-1)) over Π in [1/N,1].

The metrics are descriptive. Coordinate projection, visit-state definition, sampling interval and weighting must be documented. Entropy-based predictability is a theoretical upper bound, not a model validation result.
