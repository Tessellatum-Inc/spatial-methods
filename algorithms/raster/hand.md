# Height Above Nearest Drainage (HAND)

HAND measures the vertical elevation difference between a raster cell and the
first drainage cell encountered by following its downstream flow path. It is
useful for terrain normalisation, floodplain screening and relating landscape
positions to a drainage network.

For a valid cell i, let d(i) be the first stream cell reached by repeatedly
following the D8 receiver function. Then

\[
HAND(i)=z(i)-z(d(i)).
\]

Stream cells have HAND zero. A cell whose path reaches a sink, raster edge or
NoData before reaching the mapped stream network has no drainage target and
is returned as NoData/None by this implementation.

The Python package uses iterative path compression over the single-receiver
D8 graph. It checks that receiver links are strictly downhill and rejects
cycles, while avoiding recursive traversal for large rasters. The stream mask
is an explicit input: stream extraction threshold and DEM conditioning are
separate modelling decisions.

This is a terrain metric, not a hydraulic model. It does not simulate water
surface elevation, channel stage, flood depth or inundation extent. The
result is sensitive to DEM resolution, vertical datum, D8 routing and the
definition of the drainage network.

## Reference

Rennó, C. D., Nobre, A. D., Cuartas, L. A., Soares, J. V., Hodnett, M. G.,
Tomasella, J., &amp; Waterloo, M. J. (2008). HAND, a new terrain descriptor using
SRTM-DEM: Mapping terra-firme rainforest environments in Amazonia. Remote
Sensing of Environment, 112(9), 3469–3481.
