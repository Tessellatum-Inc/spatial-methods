# Streaming sketches for spatial data

Spatial platforms often receive more tile IDs, feature IDs and event keys than can be retained in memory. Streaming sketches trade exactness or record retention for bounded memory and predictable update cost.

## Four distinct summaries

| Structure | Question answered | Guarantee / limitation |
|---|---|---|
| HyperLogLog | How many distinct keys have appeared? | Approximate cardinality; mergeable registers; relative standard error about 1.04/sqrt(m) |
| Count-Min Sketch | How frequent is this key? | One-sided estimate (never below the true frequency for non-negative updates); collisions overestimate |
| Bloom filter | Might this key have appeared? | No false negatives after insertion; false positives are possible; no deletion |
| Reservoir sampling | What uniform sample can represent this stream? | Every observed item has equal inclusion probability k/n after n items |

## Update rules

### HyperLogLog

Hash a key to a register index and a leading-zero rank. Each register stores the maximum rank observed. The estimate uses the harmonic mean of (2^{-M_j}), with small-cardinality linear counting correction. Independent sketches with the same precision merge by taking register-wise maxima.

### Count-Min Sketch

Use d independent row hashes into a width-w table. An update increments one counter per row; a query returns the minimum of the corresponding counters. For non-negative updates, collisions can only increase the estimate. Memory is O(wd).

### Bloom filter

For expected n keys and target false-positive probability p, choose approximately (m=-nln(p)/(ln 2)^2) bits and (k=(m/n)ln 2) hash probes. The implementation uses double hashing to derive k bit positions from one digest. It is a membership prefilter, not a replacement for an authoritative key store.

### Reservoir sampling

For the t-th observed item, retain it while the reservoir is not full. Thereafter draw a uniform integer in [0,t); replace a reservoir slot only when the draw is below k. After n items, each item has inclusion probability k/n.

## Spatial uses

- Estimate unique tiles, parcels or road segments encountered in a stream.
- Approximate hot tile or feature frequencies for monitoring and workload balancing.
- Screen likely-seen tile IDs before expensive lookups.
- Retain a reproducible sample of incoming GPS events or image chips for quality review.

The sketches do not preserve geometry, event order or full attributes. Store exact records separately when auditability or exact counts are required.

## Verification

Tests cover empty and large-cardinality HyperLogLog estimates, sketch merging, Count-Min's no-underestimate property, Bloom no-false-negative behaviour and observed false-positive rate, and deterministic bounded reservoir sampling. The tests use synthetic string keys and fixed seeds.

## References

- Flajolet, P. et al. (2007). HyperLogLog: the analysis of a near-optimal cardinality estimation algorithm. *Discrete Mathematics & Theoretical Computer Science*.
- Cormode, G. and Muthukrishnan, S. (2005). An improved data stream summary: the Count-Min Sketch and its applications. *Journal of Algorithms*.
- Bloom, B. H. (1970). Space/time trade-offs in hash coding with allowable errors. *Communications of the ACM*.
- Vitter, J. S. (1985). Random sampling with a reservoir. *ACM Transactions on Mathematical Software*.

See the [tested Python package](../../implementations/python/spatial-streaming-sketches/README.md).
