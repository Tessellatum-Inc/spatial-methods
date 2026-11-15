# Martinez–Rueda polygon clipping — implementation status

The repository now contains a first-stage sweep front end: x-ordered endpoint events, active x-overlap candidate testing, cross-source segment intersections and ordered segment fragments. It is not yet the complete Martinez–Rueda Boolean algorithm. Neighbour-only status scheduling, fill-transition classification, operation-specific edge selection and output-ring stitching remain outstanding. Collinear overlaps are rejected; hole semantics are not yet implemented.

See [implementation and tests](../../implementations/python/martinez-rueda/README.md).