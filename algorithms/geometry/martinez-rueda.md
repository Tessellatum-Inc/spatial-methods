# Martinez–Rueda polygon clipping — implementation status

Implemented stages:

- X-ordered endpoint events and active x-overlap candidate set.
- Cross-source segment-intersection discovery and ordered segment splitting.
- Midpoint inside/outside classification of split fragments for intersection, union, difference and symmetric difference.
- Reversal of selected clip-boundary fragments for A-minus-B orientation.

The current implementation is still a staged baseline, not a complete Martinez–Rueda engine. Its active-set pair checks are quadratic in the worst case; it does not yet maintain the algorithm's neighbour-ordered sweep status or schedule only adjacent events. It returns selected directed fragments, not stitched polygon rings. Classification is limited to one simple shell ring per input; holes and multipart output assembly are outstanding. Collinear positive-length overlaps are rejected.

See [implementation and tests](../../implementations/python/martinez-rueda/README.md).