# D8 and multiple-flow-direction routing on a raster DEM

The D8 method assigns each valid raster cell to the steepest downslope neighbour among its eight adjacent cells. Direction codes follow the ESRI power-of-two convention:

| Direction | Code |
|---|---:|
| East | 1 |
| South-east | 2 |
| South | 4 |
| South-west | 8 |
| West | 16 |
| North-west | 32 |
| North | 64 |
| North-east | 128 |

The implementation uses strict downslope movement. A valid cell with no lower valid neighbour is coded 0 (sink/flat); an invalid or NoData cell is coded -1.

## Multiple flow direction (MFD)

The companion module implements a power-law MFD variant. Each cell distributes its contribution to every strictly lower valid neighbour in proportion to the neighbour slope raised to an exponent. The default exponent is 1.1; larger values concentrate more flow toward the steepest downslope neighbours. Fractions are stored in the channel order E, SE, S, SW, W, NW, N, NE.

Use the weights with the topological accumulation routine:

~~~python
from mfd_flow import mfd_flow_weights, mfd_flow_accumulation

weights = mfd_flow_weights(dem, exponent=1.1, cell_size=(10, 20))
accumulation = mfd_flow_accumulation(dem, weights)
~~~

The accumulation starts each valid cell with one unit by default (cell counts). Pass a raster of cell areas as initial_contribution to accumulate physical area. Invalid cells are NaN in the accumulation output. Strictly downhill routing makes the graph acyclic; the implementation uses a Kahn topological traversal.

This is a bounded Freeman/Holmgren-style power-law MFD implementation, not D-infinity, Qin's adaptive MFD, a contour-length-corrected variant, or a depression-filling method. Flats and pits remain sinks.

## Run

~~~bash
python -m pip install -r requirements.txt
python -m pytest -q
~~~

## Example

~~~python
import numpy as np
from d8_flow import d8_flow_direction

dem = np.array([[9, 8, 7], [8, 7, 6], [7, 6, 5]], dtype=float)
directions = d8_flow_direction(dem, cell_size=(10, 20))
~~~

## Contract and limits

- The DEM is a two-dimensional elevation grid.
- Cell size is supplied as (row spacing, column spacing), in horizontal map units; elevations must use compatible vertical units.
- The selected neighbour maximises elevation drop divided by centre-to-centre distance.
- Ties follow the documented direction iteration order.
- Flat areas and pits are not resolved or breached; they receive code 0 if no strictly lower neighbour exists.
- Invalid cells receive -1 and are not considered as neighbours.
- D8 is single-direction routing. The companion MFD implementation supports divergent routing and accumulation, but neither method fills depressions, resolves flats, builds stream networks or delineates watersheds.
- The algorithm is sensitive to grid resolution, DEM noise and the selected treatment of flats and sinks.

Read the [D8 lesson](../../../algorithms/raster/d8-flow-direction.md), [MFD lesson](../../../algorithms/raster/mfd-flow-routing.md) and [intern walkthrough](implementation-walkthrough.md).
