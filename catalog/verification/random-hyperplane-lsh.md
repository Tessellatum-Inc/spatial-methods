# Verification record: random-hyperplane LSH

## Scope

The package implements a static multi-table random-hyperplane locality-sensitive hash for cosine similarity. It returns the union of matching buckets and reranks only those candidates using exact cosine similarity.

## Evidence in the repository

- Seeded projection generation and candidate ordering are deterministic.
- Tests cover candidate deduplication, self-collision, exact similarity values for returned candidates, invalid dimensions, non-finite and zero vectors, query shape, top-k validation and large finite values.
- The implementation is registered in `scripts/python-ci-packages.json`; the sharded CI runner creates an isolated environment for the package.

## Limits of this verification

Candidate discovery is approximate and may miss the true nearest neighbour. No recall@k benchmark, exact-search differential study over a representative corpus, latency profile, memory profile or high-dimensional scaling claim is supplied. HNSW, IVF-PQ and ScaNN are not covered. Source identity, bibliography and rights review for the grouped compendium entry remain open.

## Status

Implementation and focused tests are present. The current GitHub Actions run must pass before CI verification can be recorded; the source entry remains partial, not fully verified.
