# Broad-phase collision detection with AABBs

Broad-phase collision detection quickly rejects object pairs whose bounding
volumes cannot overlap. An exact narrow-phase geometry test is still required
when the objects are not themselves axis-aligned rectangles.

This reference package implements three 2-D methods:

1. **Sweep and prune:** sort boxes by minimum x, retain boxes whose maximum x
   still reaches the current box, then test y-interval overlap.
2. **Uniform spatial hash:** insert each box into all grid cells it touches,
   deduplicate candidate pairs and apply an AABB overlap test. Cell size trades
   bucket occupancy against replication.
3. **Bounding-volume hierarchy:** build a median-split static AABB tree and
   query it for each box. This suits repeated queries over a fixed dataset.

The convention is inclusive overlap: edge or corner contact counts as a
candidate. The implementations return original input indices and deterministic
unordered pairs. Tests compare all methods against brute-force AABB overlap.

Limitations include static 2-D boxes, no continuous-time collision detection,
no polygon/mesh narrow phase and no dynamic tree updates. See the tested
[Python package](../../implementations/python/collision-broadphase/README.md).
