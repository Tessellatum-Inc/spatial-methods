# Distance-band Moran correlogram

The Moran correlogram describes how global spatial autocorrelation changes
across distance scales. This implementation builds a symmetric binary graph
for each non-overlapping Euclidean distance band and calculates global
Moran's I for each band. It reports link counts and the randomisation
expectation -1/(n-1). The last band includes its upper edge; earlier bands
are half-open. Empty bands are reported with a null statistic.

Optional random-labelling permutations use the same shuffled value vector
across all bands in each replicate. The method reports two-sided pseudo
p-values centred on the randomisation expectation and a single-step
max-statistic family-wise adjusted p-value based on standardized departures
from each band's permutation distribution. Bands with zero permutation
standard deviation have no standardized maxT result. The optional
row-standardisation changes the weight matrix but not the randomisation
expectation.

Coordinates must be planar and use consistent linear units. The method does
not provide a simultaneous confidence envelope, adapt distance bands, correct
edge effects, or support non-Euclidean distance.

Code and tests: [global-morans-i package](../../implementations/python/global-morans-i/README.md).
