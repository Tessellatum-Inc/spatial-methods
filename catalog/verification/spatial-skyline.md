# Verification record: spatial skyline

## Implemented scope

The package implements an exact block-nested-loop spatial skyline over squared Euclidean distance to a query point and caller-selected numeric attributes. Attribute columns can be minimised or maximised independently. Equal criterion vectors are retained.

## Tests

Tests cover dominance and trade-offs, direction reversal, query-location sensitivity, ties, empty/singleton inputs, invalid dimensions and non-finite values, and seeded comparisons with an independent pairwise oracle.

## Limits

The baseline is O(n²k) in the worst case. No spatial index, textual relevance, network distance, uncertainty model or approximate skyline is implemented. Planar CRS and compatible units are required.
