# Ellipsoidal geodesic operations

## Why the ellipsoid matters

Longitude and latitude are angular coordinates, not planar coordinates. A Euclidean buffer or distance calculation on raw longitude/latitude values changes scale with latitude and mishandles the antimeridian. For many global and regional tasks, use geodesic calculations on an explicitly selected reference ellipsoid.

## Inverse geodesic problem

Given two geographic positions, the inverse problem returns the shortest ellipsoidal geodesic distance and endpoint azimuths. PROJ uses robust geodesic algorithms based on Karney's methods, including difficult near-antipodal configurations.

## Direct geodesic problem

Given a starting longitude/latitude, forward azimuth and distance, the direct problem returns the destination. Azimuths in this package are degrees clockwise from north; distances are metres.

## Polygon area and perimeter

The geodesic polygon calculation sums ellipsoidal edge contributions and returns signed area, unsigned area and perimeter. Ring orientation determines the signed convention. Large polygons, self-intersections and polygons whose intended interior is ambiguous need an explicit geometry convention; a raw ring does not decide which side of the globe is intended.

## Geodesic-radius point buffer

A geodesic point buffer samples equally spaced azimuths around the center and solves the direct problem for a fixed radius. The resulting longitude/latitude ring can cross the antimeridian; longitudes are normalized by PROJ. This is an approximation controlled by vertex count. It is not an exact analytic buffer, a topology-aware geometry operation or a guarantee of uniform planar polygon error.

## Implementation and coordinate contract

The [CRS transformation package](../../implementations/python/crs-transform/README.md) adds `geodesic_inverse`, `geodesic_direct`, `geodesic_polygon_area` and `geodesic_point_buffer`.

- Coordinates are longitude, latitude in degrees.
- Latitude must be in [-90, 90].
- Distances are metres; polygon areas are square metres.
- Azimuths are degrees clockwise from north.
- The default ellipsoid is WGS 84; another CRS or named ellipsoid can be supplied.
- Near-antipodal inverse calculations are delegated to PROJ's robust geodesic solver.
- Ellipsoidal surface calculations do not imply a vertical datum or height transformation.

## Tests and limitations

Tests cover known short dateline-crossing distances, near-antipodal inverse solutions, direct/inverse round trips, signed polygon area, and a sampled buffer crossing the antimeridian. The implementation does not cover geodesic polygon boolean operations, geodesic line intersections, ellipsoidal raster reprojection, dynamic datums or uncertainty propagation.

## References

- Karney, C. F. F. (2013). Algorithms for geodesics. *Journal of Geodesy*, 87, 43–55. https://doi.org/10.1007/s00190-012-0578-z
- PROJ documentation: Geodesic calculations, https://proj.org/en/stable/geodesic.html
