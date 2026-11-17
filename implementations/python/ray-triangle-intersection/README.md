# Möller–Trumbore ray/triangle intersection

A dependency-free reference implementation of the Möller–Trumbore ray/triangle test. It returns the ray parameter, barycentric weights and Cartesian intersection point.

## Run

    python -m pip install -r requirements.txt
    python -m pytest -q

## Input and numerical contract

- Coordinates are finite Cartesian 3D values in one consistent frame and unit.
- The ray is o + t*d. The parameter t is Euclidean distance only if d is unit length.
- Default policy is two-sided intersection; back-face culling is opt-in.
- Edges and vertices are included within the configurable tolerance.
- Degenerate triangles and near-parallel ray/triangle pairs return no hit.
- This floating-point teaching implementation is not an exact/adaptive geometric predicate.

Do not pass longitude/latitude directly as Cartesian 3D coordinates. Transform vertices and rays into an appropriate local/projected 3D engineering frame first. CRS transformation, ellipsoidal geometry and acceleration structures are outside scope.
