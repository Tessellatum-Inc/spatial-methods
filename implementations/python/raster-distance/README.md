# Euclidean raster distance transform

This package implements the exact centre-to-centre Euclidean distance transform from first principles using the Felzenszwalb–Huttenlocher lower-envelope algorithm. A separable pair of one-dimensional passes gives O(HW) time for an H-by-W grid.

## Run

~~~bash
python -m pip install -r requirements.txt
python -m pytest -q
~~~

## Example

~~~python
import numpy as np
from raster_distance import distance_to_targets

targets = np.zeros((5, 5), dtype=bool)
targets[2, 2] = True
distance = distance_to_targets(targets, cell_size=(10, 20))
print(distance[2, 3])  # 20 map units
~~~

## Grid contract

- The input is a two-dimensional mask; True marks target cells.
- Cell spacing is (row_spacing, column_spacing) in map units.
- Distances are measured between cell centres, not to cell edges.
- At least one target cell is required.
- The output has the same shape and uses floating-point map units.
- The operation is Euclidean and ignores barriers, cost surfaces and connectivity. It is not a least-cost path.
- NoData handling must be designed by the caller. Invalid cells are not automatically excluded from distance measurement.
- The implementation uses the lower envelope of parabolas in each one-dimensional pass; it is not a chamfer approximation or a SciPy wrapper.

Read the [canonical lesson](../../../algorithms/raster/euclidean-distance-transform.md) and [intern walkthrough](implementation-walkthrough.md).
