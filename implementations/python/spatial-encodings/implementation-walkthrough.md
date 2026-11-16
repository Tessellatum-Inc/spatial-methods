# Implementation walkthrough: spatial encodings

## 1. Morton / Z-order

For each bit position i, copy xᵢ into output bit 2i and yᵢ into output bit 2i+1. Decoding extracts those positions. The implementation loops over the selected bit width, so both directions are O(b).

## 2. Hilbert distance

At each scale, inspect the x/y quadrant bits. The quadrant contributes one of 0, 1, 2 or 3 blocks of scale² cells to the distance. A conditional rotation/reflection puts the remaining subproblem into the canonical orientation. The inverse consumes base-4 digits from least significant to most significant and reconstructs coordinates.

The rotation is the delicate part: the scale passed to the transform is the current sub-square side, not the original grid side. Small-grid exhaustive round trips are therefore essential tests.

## 3. Geohash

Maintain latitude and longitude intervals. Alternate longitude then latitude. For each bit, compare the coordinate with the interval midpoint, retain the matching half and append 1 for the upper half or 0 for the lower half. Emit every five bits through the geohash alphabet. Decoding repeats the same interval refinement.

## 4. What a key does not do

A key gives an ordering or a cell identifier. It does not by itself implement exact range search, nearest-neighbour search, topology, equal-area measurement or geodesic distance. Those require additional query logic and an explicit coordinate model.
