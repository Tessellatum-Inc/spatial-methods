# Spherical polygon area

## Method

Convert latitude/longitude vertices to unit vectors. Triangulate the ring as a fan from its first vertex and sum signed spherical triangle excesses. For unit vectors a, b and c, the signed excess is 2 atan2(det(a,b,c), 1 + a·b + b·c + c·a). Multiply the absolute smaller-region excess by the square of the sphere radius. Interior-ring areas are subtracted.

## Assumptions

Coordinates are latitude/longitude in degrees. Consecutive edges follow minor great-circle arcs. The intended simple polygon must have an unambiguous smaller-than-hemisphere interpretation. The default radius is a mean-Earth sphere, not an ellipsoid.

## Limits

This method does not validate self-intersections or implement ellipsoidal geodesic area, spherical Voronoi/Delaunay, spherical wavelets, icosahedral grids or cubed-sphere discretisation. Use ellipsoidal geodesic polygon algorithms for survey-grade area.