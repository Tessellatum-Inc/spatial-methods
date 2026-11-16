# Coordinate transformation with explicit x/y axis order

This package wraps PROJ through pyproj to transform point coordinates between declared coordinate reference systems.

## Run

~~~bash
python -m pip install -r requirements.txt
python -m pytest -q
~~~

## Contract

- Input is a non-empty N×2 array.
- Source and target CRS may be EPSG identifiers, WKT or other pyproj-supported user inputs.
- always_xy is enabled: geographic coordinates are longitude, latitude; projected coordinates are easting, northing.
- Output coordinates use the target CRS units.
- Non-finite inputs or outputs and invalid transformations are rejected.
- The wrapper transforms points only; it does not reproject raster grids, geometries or datasets.

## Important limitations

A coordinate transformation is not merely a change of units. It can involve datum transformations, grid-shift files, area-of-use restrictions and coordinate epochs. The selected operation may depend on installed PROJ data and available transformation grids. This teaching wrapper does not expose operation selection, vertical transformations, dynamic reference frames, epoch metadata or accuracy budgets. Production work must record the full CRS definitions, selected operation, PROJ version and required grids.

Read the [canonical lesson](../../../algorithms/geodesy/crs-transformation.md) and [intern walkthrough](implementation-walkthrough.md).


## Ellipsoidal geodesic operations

The same package also exposes PROJ/Karney geodesic calculations:

- `geodesic_inverse`: forward/back azimuths and shortest ellipsoidal distance between matching longitude/latitude pairs.
- `geodesic_direct`: destination coordinates from starting points, azimuths and distances.
- `geodesic_polygon_area`: signed or unsigned ellipsoidal polygon area and perimeter.
- `geodesic_point_buffer`: sampled geodesic-radius ring, including antimeridian-crossing buffers.

The default ellipsoid is WGS 84. Pass a CRS or named ellipsoid explicitly when another reference ellipsoid is required. Distances are metres, azimuths are degrees clockwise from north, coordinates are longitude/latitude degrees, and polygon area is square metres.

~~~python
from transform import geodesic_inverse, geodesic_point_buffer

result = geodesic_inverse([[179.9, 0]], [[-179.9, 0]])
ring = geodesic_point_buffer((179.8, 0), 100_000, vertices=72)
print(result["distance_metres"])
~~~

The buffer is a sampled boundary, not an exact geometry overlay. These methods do not perform datum-epoch transformations, geoid height conversion, polygon topology repair or ellipsoidal raster warping.
