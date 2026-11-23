# Source verification — pole of inaccessibility / Polylabel

## Identity

The pole of inaccessibility is the point inside a polygon with maximum distance to its boundary. The Polylabel best-first cell subdivision algorithm is documented by Mapbox as an approximate method with a user-controlled precision parameter.

## Implemented scope

The package implements signed point-to-polygon-boundary distance for an exterior ring and optional holes, followed by best-first square-cell subdivision. A cell's upper bound is its centre distance plus the half-diagonal. The search prunes cells that cannot improve the current best beyond the requested precision.

## Limitations

The input polygon must be valid and planar. Ring topology is not validated or repaired. The result is approximate within the specified absolute coordinate-unit precision; it is not an exact largest-empty-circle solution for arbitrary site sets or domains. A maximum-cell guard prevents unbounded refinement.

## Rights

The method is independently implemented from the published algorithm description; no source code or figures are reproduced.
