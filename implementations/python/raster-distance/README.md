# Euclidean raster distance transform

This package implements both an exact centre-to-centre Euclidean distance transform using the Felzenszwalb–Huttenlocher lower-envelope algorithm and an eight-neighbour chamfer graph-distance transform. The exact transform uses separable one-dimensional passes in O(HW); the chamfer reference uses two directional raster scans.

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


## Eight-neighbour chamfer distance

`chamfer_distance_to_targets` computes shortest-path distance on the raster's eight-neighbour graph. Horizontal and vertical moves cost their respective cell spacing; diagonal moves cost the hypotenuse of the two spacings. Forward and reverse raster scans compute the obstacle-free graph metric. This is not the exact continuous Euclidean transform: for offsets such as (2, 1), the chamfer path is longer than the straight-line distance. It also does not support barriers; use a graph-search cost-distance method when obstacles or variable costs matter.
