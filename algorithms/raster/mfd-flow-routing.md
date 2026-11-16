# Multiple-flow-direction routing

MFD distributes each cell's flow among all strictly lower valid neighbours:

\[
w_{ij}=\frac{s_{ij}^{p}}{\sum_{k\in N_i,\ s_{ik}>0}s_{ik}^{p}},
\]

where \(s_{ij}\) is the downslope gradient to neighbour \(j\), and \(p>0\)
controls concentration. Larger \(p\) concentrates flow toward the steepest
receiver; smaller \(p\) spreads it more broadly.

The tested NumPy implementation in implementations/python/advanced-flow-routing
uses physical rectangular-cell distances, masks NoData cells and returns
explicit receiver proportions. Its accumulation routine uses a topological
graph traversal. It routes only to strictly lower cells; depression filling
and flat resolution remain separate preprocessing steps.

MFD is not interchangeable with D-infinity: MFD can have more than two
receivers per cell, while D-infinity uses a triangular-facet direction and at
most two adjacent receivers.
