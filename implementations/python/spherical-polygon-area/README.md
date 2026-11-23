# Spherical polygon area

NumPy reference implementation of spherical polygon area from latitude/longitude rings in degrees. It converts vertices to unit vectors and sums signed spherical excesses of a fan triangulation. Optional interior rings are subtracted. The default radius is the mean Earth radius in metres; choose another radius and unit when appropriate.

## Assumptions and limitations

Rings must be simple and should represent an unambiguous region smaller than a hemisphere. Edges follow minor great-circle arcs. Antipodal consecutive vertices are rejected. The function does not compute ellipsoidal geodesic area, validate self-intersections, infer ring orientation semantics, or implement spherical Voronoi/Delaunay, spherical wavelets, or cubed-sphere/icosahedral grids. For high-accuracy geodesy use an ellipsoidal geodesic polygon algorithm.

Run python -m pip install -r requirements.txt and python -m pytest -q.