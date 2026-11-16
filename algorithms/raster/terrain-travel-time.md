# Directional terrain travel-time models

The symmetric raster cost-distance algorithm assigns one cost per cell and averages endpoint costs. Terrain travel time is directional: the cost of moving uphill is not generally the same as moving downhill. This module supplies three rule-based travel models and a multi-source raster Dijkstra solver.

## Tobler hiking function

For signed slope grade S = rise/run, Tobler's function estimates walking speed:

[
v(S)=6exp(-3.5|S+0.05|)quad	ext{km/h}.
]

The speed maximum occurs at a 5% downhill grade. For a directed edge of horizontal length L metres and elevation change dz, S=dz/L and travel time is L divided by the resulting speed. Reversing the edge changes the sign of S and can change travel time.

## Naismith's rule

The implementation uses one hour per 5 km horizontal distance plus one hour per 600 m ascent:

[
t_N = rac{D_{km}}{5}+rac{H_{up,m}}{600}quad	ext{hours}.
]

Downhill distance receives no extra adjustment in this base rule.

## Langmuir descent correction

The Langmuir variant adds a descent correction to Naismith's base time:

- descent angle below 5°: no correction;
- 5–12°: subtract 10 minutes per 300 m descent;
- above 12°: add 10 minutes per 300 m descent.

The raster implementation applies this rule to each directed neighbour edge using that edge's average slope angle. This is a coarse discretisation and is resolution-sensitive; the rule's discontinuity at 12° should be treated as an empirical heuristic, not a physical law.

## Raster Dijkstra

Each finite elevation cell is a node. Four- or eight-neighbour moves are available; rectangular cell sizes determine horizontal step length. Edge travel time is directional and non-negative. Multi-source Dijkstra accumulates the minimum travel time in seconds. Non-finite elevation cells are barriers, unreachable valid cells remain infinity, and source cells start at zero. Diagonal corner cutting can be prohibited.

## Limits

These rules are planning heuristics for an average walker. They do not model trail surface, vegetation, load, fatigue, weather, fitness, path networks, navigation or safety. The raster solution is constrained by grid resolution and connectivity. It does not produce backlink rasters, path geometries, turn penalties, a continuous Eikonal solution or a calibrated energy-expenditure model.

## Verification

Tests cover the Tobler speed curve and directionality, Naismith base rates, Langmuir corrections, raster directional asymmetry, NoData barriers, multiple sources and parameter validation.

## References

- Tobler, W. (1993). *Three presentations on geographical analysis and modeling*. NCGIA Technical Report 93-1.
- Naismith, W. W. (1892). *Excursions*. Scottish Mountaineering Club Journal.
- Langmuir, E. (1984). *Mountaincraft and Leadership*. The Mountaineers.

See the [cost-distance package](../../implementations/python/cost-distance/README.md).
