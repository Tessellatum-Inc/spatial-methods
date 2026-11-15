# Martinez–Rueda sweep-line front end (partial)

Implements x-ordered endpoint events, an active x-overlap set, proper cross-source segment intersection discovery and ordered segment splitting. The active status tests all x-overlapping pairs on insertion, so worst-case work is quadratic; it is not yet Martinez–Rueda's full neighbour-updating sweep. Fill-transition classification, Boolean result-edge selection and ring stitching are not implemented. Collinear overlaps are rejected; holes and ring roles are not yet interpreted.

Run `python -m pytest -q` in this directory.