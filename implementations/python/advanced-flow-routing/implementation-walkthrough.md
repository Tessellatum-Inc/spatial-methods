# D-infinity and MFD implementation walkthrough

D-infinity fits a planar gradient from the centre cell and two adjacent
neighbours. The negative gradient defines a continuous downslope angle. When
that angle falls inside the triangular facet, the flow is split linearly
between the bounding neighbour directions; otherwise the steeper descending
facet edge is selected.

MFD computes positive drop divided by physical neighbour distance for every
lower neighbour. The slopes are raised to an exponent and normalised. A larger
exponent concentrates flow on steep receivers; a smaller exponent spreads it.

Accumulation is a directed-acyclic-graph problem after strict downhill
receivers are established. Each valid cell starts with one unit. A topological
queue sends its accumulated amount to downstream cells using the edge weights.
Depression filling and flat resolution are separate methods and are not hidden
inside this implementation.
