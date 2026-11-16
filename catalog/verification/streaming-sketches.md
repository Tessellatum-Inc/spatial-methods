# Verification record: spatial streaming sketches

## Implemented algorithms

- HyperLogLog cardinality estimation with small-range correction and same-precision merge.
- Count-Min Sketch with deterministic row hashes and non-negative weighted updates.
- Bloom filter with parameter-derived bit and hash counts, no false negatives and expected false positives.
- Algorithm R reservoir sampling with a fixed-capacity sample and reproducible seed.

## Tests

Synthetic deterministic tests cover cardinality estimation and merge, Count-Min no-underestimate behaviour, Bloom membership and observed false-positive rate, and reservoir size/reproducibility. Validation rejects invalid dimensions, probabilities, capacities and unsupported key types.

## Limits

These are sketches, not exact databases. They do not retain geometry, time ordering or source records. Count-Min has no deletion support; Bloom has no deletion support; HLL returns estimates; reservoir sampling is only representative of the observed stream.
