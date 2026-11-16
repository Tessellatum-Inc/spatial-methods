# D-infinity and multiple-flow-direction routing

Two distinct multi-direction routing methods are implemented:

- D-infinity fits planar gradients across adjacent neighbour pairs and assigns
  flow to at most two bounding receivers.
- MFD distributes flow among every strictly lower valid neighbour in
  proportion to slope raised to a configurable exponent.

Both use north-up raster coordinates, rectangular cell spacing, NoData masks
and explicit receiver weights. D-infinity angles are radians counter-clockwise
from east. Flow accumulation propagates unit source contributions in
topological order and detects cycles.

This is a transparent NumPy teaching implementation. It does not fill
depressions, resolve flats, breach barriers or infer a CRS. Apply and document
appropriate preprocessing before interpreting a complete drainage network.
The facet method should be compared with a trusted GIS implementation before
operational use.

API: route_d_infinity, route_multiple_flow_direction, flow_accumulation.
Run pytest -q in this directory.
