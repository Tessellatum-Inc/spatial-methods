# Broad-phase collision detection

Dependency-free 2-D axis-aligned bounding-box (AABB) reference methods:
sweep-and-prune, uniform spatial hashing and a median-split bounding-volume
hierarchy (BVH). All three return exact AABB overlap pairs; the hash and BVH
are broad-phase structures followed by an AABB narrow-phase check.

Run `python -m pip install -r requirements.txt && python -m pytest -q`.

Boxes use (xmin, ymin, xmax, ymax); touching edges/corners count as overlap.
Sweep-and-prune sorts on x and checks the active interval set. Spatial hashing
inserts each box into every touched grid cell; performance depends on cell
size and box-size distribution. The static BVH splits along the longest node
extent at the median centroid and is intended for repeated queries on an
unchanged box set. This is not continuous collision detection, polygon
intersection, 3-D collision, dynamic BVH maintenance or a physics engine.
