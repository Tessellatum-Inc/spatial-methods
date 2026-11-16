# Spatial information theory

Implements Shannon, Renyi and Tsallis entropies for nonnegative weights, categorical raster entropy with masks, normalized ordinal-pattern permutation entropy, sample entropy, and adjacency-weighted spatial conditional entropy and mutual information.

Sample entropy uses Chebyshev template matching and a caller-declared tolerance convention. Spatial measures are computed over directed positive-weight edges, with self-edges excluded; they are descriptive and do not establish causal information flow.
