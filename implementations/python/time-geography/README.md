# Time-geography potential path areas

This package implements the constant-speed Euclidean potential path area (PPA) and a time-slice description of a space-time prism.

For an origin O, destination D, travel-speed bound v and available duration T, the spatial projection of feasible locations satisfies d(O,p) + d(p,D) <= vT. When feasible, this is an ellipse with foci O and D, semi-major axis vT/2 and semi-minor axis sqrt((vT/2)^2 - (d(O,D)/2)^2). A helper evaluates point membership directly from the distance-sum inequality. A prism time slice is represented as the intersection of a disk reachable from the origin and a disk from which the destination remains reachable.

## Run

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

## Assumptions and limits

Coordinates are projected planar x/y values in a common linear unit; speed is coordinate units per time unit. Travel is at constant isotropic speed in unobstructed Euclidean space. The method ignores barriers, street networks, mode changes, time-dependent speeds, activity duration, uncertainty and population-based activity-space estimation. The slice API returns the two-disk intersection description, not a polygonized geometry.
