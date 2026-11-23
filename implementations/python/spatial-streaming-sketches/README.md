# Streaming sketches for spatial data

Four dependency-free summaries for high-volume tile, feature and event streams:

- **HyperLogLog:** approximate distinct-key cardinality with mergeable registers.
- **Count-Min Sketch:** one-sided approximate frequency counts.
- **Bloom filter:** compact membership screening with possible false positives but no false negatives.
- **Reservoir sampling:** uniform fixed-size sample from a stream of unknown length.

## Example

```python
from streaming_sketches import HyperLogLog, CountMinSketch, BloomFilter, ReservoirSampler

tiles = HyperLogLog(precision=12)
frequencies = CountMinSketch(width=4096, depth=5, seed=42)
seen = BloomFilter(expected_items=100_000, false_positive_rate=0.01)
sample = ReservoirSampler(capacity=500, seed=42)

for tile_id in tile_id_stream:
    tiles.add(tile_id)
    frequencies.add(tile_id)
    if not seen.might_contain(tile_id):
        seen.add(tile_id)
    sample.add(tile_id)

print(tiles.estimate(), frequencies.estimate("tile/12/2048/1365"), len(sample.sample))
```

## Contracts and limits

Keys are strings or bytes and are hashed with BLAKE2b for deterministic behaviour. HyperLogLog estimates cardinality, not exact identities; merge requires equal precision. Count-Min estimates are upper bounds in the absence of deletions and use O(width*depth) counters. Bloom filters cannot delete keys and may return false positives. Reservoir sampling returns a uniform sample over the items observed so far; its seeded sequence is reproducible.

These structures summarise keys or event counts. They do not preserve geometry, ordering, timestamps or full records. Choose parameters from the expected stream size and acceptable error/memory budget; do not treat approximate counts as exact inventory totals.

## Run

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

See the [algorithm note](../../../algorithms/streaming/streaming-sketches.md) and [verification record](../../../catalog/verification/streaming-sketches.md).
