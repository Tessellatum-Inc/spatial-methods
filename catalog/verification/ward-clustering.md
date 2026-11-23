# Ward clustering implementation verification

Implemented: exact greedy Ward merge objective for finite Euclidean vectors;
linkage matrix with cluster IDs, sqrt(2 Delta-SSE) height and cluster size;
deterministic tie breaking; flat k-cluster tree cutting.

Independent tests check a hand-computed three-point hierarchy, a separated
four-point partition, deterministic zero-distance ties, singleton handling
and malformed inputs.

Not implemented: Ward linkage on arbitrary dissimilarities, accelerated
nearest-neighbour-chain search, other linkage methods or spatial contiguity.
