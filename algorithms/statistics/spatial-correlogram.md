# Distance-band Moran correlogram

The Moran correlogram describes how global spatial autocorrelation changes
across distance scales. This implementation builds a symmetric binary graph
for each non-overlapping Euclidean distance band and calculates global
Moran's I for each band. It reports the number of linked pairs and the
randomisation expectation `-1/(n-1)`. The last band includes its upper edge;
earlier bands are half-open. Empty bands are reported with a null statistic.

The optional row-standardisation changes the weight matrix but does not
change the reported randomisation expectation. Coordinates must be planar
and use consistent linear units. This is a descriptive statistic: it does
not provide permutation p-values, simultaneous confidence envelopes,
multiple-testing adjustment or a correction for spatially estimated
distance scales.

Code and tests: [global-morans-i package](../../implementations/python/global-morans-i/README.md).
