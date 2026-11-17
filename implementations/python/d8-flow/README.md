# D8 flow direction on a raster DEM

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
- This is D8 flow direction only. It does not calculate flow accumulation, stream networks, watershed boundaries or depression filling.
- The algorithm is sensitive to grid resolution, DEM noise and the selected treatment of flats and sinks.

Read the [canonical lesson](../../../algorithms/raster/d8-flow-direction.md) and [intern walkthrough](implementation-walkthrough.md).

## Multiple-flow-direction routing

The companion `mfd_flow.py` module implements a power-law multiple-flow-direction (MFD) variant. `mfd_flow_weights` splits flow among strictly lower neighbours using slope-to-the-exponent weights; `mfd_flow_accumulation` routes contributions through the resulting acyclic graph with a topological traversal. It supports rectangular cell spacing, masks, NoData and raster-valued initial contributions. Run the same test command above to exercise both D8 and MFD. This is not D-infinity and does not resolve flats or fill depressions. See the [MFD lesson](../../../algorithms/raster/mfd-flow-routing.md) and [interactive lab](../../../notebooks/mfd-flow-routing-lab.ipynb).


## D-infinity (D∞) routing

The companion `dinf_flow.py` module fits a planar slope to each triangular
facet in the 3×3 neighbourhood. It selects the steepest valid facet; when the
downslope aspect falls inside a facet, flow is split between its two
neighbouring cells according to angular position. Available edge slopes
provide a fallback beside NoData and raster boundaries. The output uses the
same E, SE, S, SW, W, NW, N, NE channel order and shape as the MFD weights,
so it can be passed to the existing `mfd_flow_accumulation` routine for
topological accumulation. This is a D-infinity facet method, not the
power-law MFD rule. Flats and depressions are not conditioned.


The D-infinity facet method has a separate [verification record](../../../catalog/verification/d-infinity-flow-routing.md), including its analytic and randomized invariants and known comparison gaps.

## D8 stream ordering: Strahler and Shreve

The companion stream_order.py module computes Strahler order and Shreve magnitude for a supplied Boolean channel mask and ESRI-coded D8 directions. It requires every in-grid downstream receiver of a channel cell to also be in the channel mask; channel links may terminate at code 0 or leave the raster. It rejects NoData stream cells and directed cycles. Non-channel cells are NaN. This is network ordering only: it does not extract a channel mask or condition the DEM. See the [stream-order lesson](../../../algorithms/raster/stream-order.md).
