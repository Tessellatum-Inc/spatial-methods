# Street address interpolation

A dependency-free reference implementation for interpolating address numbers along projected street polylines using cumulative line length. Same-parity ranges default to step-two numbering; mixed-parity ranges use consecutive integers. Caller-supplied address numbers are also supported. Optional left/right offsets place interpolated points beside the street using the local segment normal.

## Assumptions and limits

Coordinates must be projected planar x/y values in common linear units. The method assumes address numbers vary monotonically along the supplied polyline and are approximately proportional to cumulative street distance. It does not infer address ranges, choose the correct street side, assign numbers to building footprints, resolve intersections, parse local addressing conventions, or score address quality. Outputs are candidate interpolated locations, not verified addresses.

Run python -m pip install -r requirements.txt and python -m pytest -q.