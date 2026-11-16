# Spatial encodings: Morton, Hilbert and Geohash

The source compendium groups Z-order (Morton), Hilbert, Geohash, H3, S2, quadkeys and HEALPix under space-filling curves and grids. They are related indexing tools, not interchangeable encodings.

## Morton / Z-order

For integer coordinates x and y, write each in binary and interleave the bits:

`x = x₂x₁x₀`, `y = y₂y₁y₀` gives `code = y₂x₂y₁x₁y₀x₀` when the most-significant bit is written first.

The implementation places x in even bit positions and y in odd bit positions. Encoding and decoding are O(b) for b bits per axis. Morton keys are inexpensive and can support sort-based spatial partitioning, but adjacent keys may represent cells that are not immediate neighbours.

## Hilbert curve

The Hilbert mapping recursively rotates and reflects quadrants so that consecutive indices visit edge-adjacent cells. The implementation uses the standard iterative xy-to-distance and distance-to-xy transforms on a `2^b × 2^b` integer grid. Both directions take O(b) time and O(1) auxiliary space.

A Hilbert key can improve locality in bulk loading and partitioning, but it does not replace a spatial predicate: a one-dimensional key interval is not generally an exact answer to a two-dimensional range query.

## Geohash

Geohash alternates binary subdivision of longitude and latitude intervals, starting with longitude. Every five bits become one base-32 character. Decoding yields a bounding rectangle. Precision increases resolution, but cell dimensions vary by latitude and geohash adjacency has boundary artefacts.

## Implementation boundary

The tested reference package implements Morton, Hilbert and Geohash. H3, S2 and HEALPix are hierarchical global grid systems with different cell geometry and topology; quadkeys encode a Web Mercator tile pyramid. They remain separate implementation/research items rather than being claimed as covered by these functions.

## Source

The original source entry is on page 1 of the supplied *Spatial Analysis Algorithms: Complete Compendium*: `Space-filling curves and grids: Z-order (Morton), Hilbert, Geohash, H3, S2, quadkeys, HEALPix`. See [the preserved transcription](../../source-inventory/pages-01-05.md#page-1-of-47).
