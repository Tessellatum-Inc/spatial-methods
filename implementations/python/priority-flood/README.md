# Priority-Flood depression filling for a DEM

Priority-Flood raises cells inside depressions to the lowest spill elevation that connects them to the raster's valid boundary. This teaching implementation uses an eight-neighbour min-heap traversal.

It returns both the filled elevation grid and the fill-depth grid. Invalid/NoData cells remain NaN.

## Run

~~~bash
python -m pip install -r requirements.txt
python -m pytest -q
~~~

## Example

~~~python
import numpy as np
from priority_flood import priority_flood

dem = np.array([[5, 5, 5], [5, 1, 5], [5, 5, 5]], dtype=float)
filled, depth = priority_flood(dem)
~~~

## Contract and limits

- The DEM is a non-empty two-dimensional elevation grid.
- Eight-neighbour connectivity is used.
- Valid outer-edge cells and valid cells adjacent to NoData are treated as outlets/seeds.
- Each depression is raised to the minimum spill elevation reachable from those seeds.
- Invalid cells remain NaN; a valid mask or NoData sentinel may be supplied.
- Priority-Flood fills depressions; it does not breach them or preserve every real closed basin. Flat resolution is a separate companion operation in `flat_resolution.py` and should be applied only after the depression-conditioning policy is chosen.
- The boundary/NoData policy is a modelling decision. A clipped DEM boundary is not automatically a natural watershed outlet.
- This is a heap-based teaching implementation with O(n log n) time and O(n) memory for n valid cells.

Read the [canonical lesson](../../../algorithms/raster/priority-flood.md) and [intern walkthrough](implementation-walkthrough.md).

## Flat resolution

The companion `flat_resolution.py` module adds a small BFS-based gradient to
8-connected equal-elevation components that touch strictly lower terrain.
Every non-outlet cell has a lower BFS parent, giving a descending route toward
an outlet. The default epsilon uses the local floating-point spacing and is
guarded against crossing adjacent higher terrain; an explicit epsilon can be
provided.

```python
from flat_resolution import resolve_flats
resolved_dem = resolve_flats(filled_dem)
```

This is a routing perturbation, not depression filling or breaching. Flats
without a lower outlet are unchanged; unresolved closed basins still require
a separate sink policy.
