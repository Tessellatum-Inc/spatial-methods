# Source verification — k-medoids, CLARA and CLARANS

## Identity

PAM k-medoids and CLARA are established partitioning clustering methods.
The source entry groups them with k-means, CLARANS and constrained/equal-size
variants; those are separate methods and are not implied by this implementation.

## Implemented scope

The package implements deterministic PAM BUILD/SWAP over a symmetric
precomputed dissimilarity matrix, a Euclidean distance-matrix helper, and
CLARA sampling with full-data scoring. Medoids are observed row indices.
Input-order tie breaking makes the teaching baseline reproducible.

## Independent tests

Tests include separated clusters, a small brute-force objective oracle,
medoid membership, direct objective recomputation, k=n, deterministic
repeated runs, invalid matrices and controls, CLARA reproducibility, and
full-sample agreement with PAM's objective, CLARANS repeatability and\nfull-data objective recomputation.

## Limitations

Dense O(n²) dissimilarity storage is required. PAM is intended for modest
datasets; CLARA reduces sample search but this implementation still retains
the full matrix for full-data scoring. No contiguity, capacity, balance,
equal-size, CLARANS or automatic-k constraints are implemented.

## Rights

The implementation is independently written from the published algorithm
descriptions. No source code, text or figures are reproduced.
