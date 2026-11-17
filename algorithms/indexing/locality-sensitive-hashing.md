# Locality-sensitive hashing with random hyperplanes

## Problem

Exact nearest-neighbour search compares a query with every indexed vector. Approximate nearest-neighbour (ANN) systems reduce the number of candidates examined, trading some recall for lower query work.

Locality-sensitive hashing (LSH) uses hash functions whose collision probability reflects a chosen similarity. For cosine similarity, random-hyperplane hashing maps a vector to the signs of its projections onto random directions.

## Random-hyperplane hash

For a random vector r drawn from an isotropic Gaussian, define

    h_r(x) = 1[rᵀx ≥ 0].

For non-zero vectors with angle θ, a single bit disagrees with probability θ/π, so it agrees with probability

    P[h_r(x) = h_r(y)] = 1 − θ/π.

Concatenate b independent bits to form a table key. Build L independent tables. A query gathers the union of rows in the matching bucket from each table, then reranks those candidates by exact cosine similarity.

## Implementation

The companion Python package creates Gaussian hyperplanes from a seeded generator, stores integer signatures in in-memory hash tables, deduplicates candidates and reranks them. Tests check deterministic construction, self-collision, validation and exact candidate scores.

## Complexity and trade-offs

For n vectors of dimension d, L tables and b bits per table, projection and indexing cost is approximately O(L n b d); storage is O(L n + L b d), excluding Python object overhead. Query projection costs O(L b d), plus candidate scoring O(c d) for c unique candidates.

More tables increase the chance that a similar vector collides somewhere, but also increase memory and duplicate candidate work. More bits per table reduce bucket sizes but can reduce recall. These parameters must be measured on the target distribution; they do not provide a universal recall or latency guarantee.

## Scope boundaries

This lesson covers random-hyperplane LSH for cosine similarity. It is not HNSW graph search, IVF-PQ vector quantization, ScaNN anisotropic vector quantization, or a spatially aware index. Euclidean, Jaccard and other metrics require different LSH families or transformations. A production evaluation should report recall@k against exact search, build time, query latency, memory, and sensitivity to data distribution and parameters.
