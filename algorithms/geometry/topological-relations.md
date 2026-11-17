# DE-9IM and RCC-8 topological relations

Spatial topological relations describe how two geometries intersect without depending on their coordinate values or orientation. The Dimensionally Extended Nine-Intersection Model (DE-9IM) records the dimensions of intersections among the interior, boundary and exterior of two geometries.

## The nine-intersection matrix

For geometries A and B, the matrix is

\[
\begin{bmatrix}
I(A)\cap I(B) & I(A)\cap B(B) & I(A)\cap E(B)\\
B(A)\cap I(B) & B(A)\cap B(B) & B(A)\cap E(B)\\
E(A)\cap I(B) & E(A)\cap B(B) & E(A)\cap E(B)
\end{bmatrix}
\]

Each cell is encoded by the dimension of the intersection: F for empty, 0 for a point, 1 for a curve, 2 for an area, and T or * in pattern expressions for non-empty or any dimension. The exact matrix depends on geometry type and the geometry engine's topological model.

## RCC-8 for planar regions

The Region Connection Calculus RCC-8 defines eight mutually exclusive relations between regular closed regions:

- **DC** — disconnected: no points are shared.
- **EC** — externally connected: regions meet at their boundaries but interiors do not intersect.
- **PO** — partial overlap: interiors intersect, but neither region is contained in the other.
- **EQ** — equal regions.
- **TPP / TPPi** — tangential proper part and its inverse: one region is properly contained and shares boundary with the containing region.
- **NTPP / NTPPi** — non-tangential proper part and its inverse: one region is properly contained without boundary contact.

RCC-8 is a region calculus. The implementation therefore restricts this classifier to valid, non-empty Polygon and MultiPolygon inputs. It does not silently repair invalid geometry or reinterpret lines and points as regions.

## Implementation

The [spatial-topological-relations package](../../implementations/python/spatial-topological-relations/README.md) exposes Shapely/GEOS DE-9IM strings and classifies RCC-8 relations using polygon predicates and boundary intersection. The geometry engine supplies the underlying topology operations; this is a tested wrapper, not an independent computational-geometry kernel.

## Cardinal direction relations

DE-9IM and RCC-8 do not encode north/south/east/west. The package also provides a deliberately bounded 9-region relation based on axis-aligned minimum bounding rectangles. It reports the direction of B relative to A as N, NE, E, SE, S, SW, W, NW or OVERLAPPING. Bounding-box interval endpoints that touch are treated as directional separation. This is not a centroid-bearing model, a projection-based directional calculus or a complete qualitative spatial reasoning system.

## References

- Clementini, E., Di Felice, P., & van Oosterom, P. (1993). A small set of formal topological relationships suitable for end-user interaction. *Proceedings of the Third International Symposium on Large Spatial Databases*, 277–295.
- Egenhofer, M. J., & Franzosa, R. D. (1991). Point-set topological spatial relations. *International Journal of Geographical Information Systems*, 5(2), 161–174.
- Randell, D. A., Cui, Z., & Cohn, A. G. (1992). A spatial logic based on regions and connection. *Proceedings of KR'92*, 165–176.
- OGC Simple Feature Access: https://www.ogc.org/standards/sfa/
