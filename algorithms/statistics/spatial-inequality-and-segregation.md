# Spatial inequality and segregation measures

This lesson implements a bounded group of area-level measures:

- weighted Gini inequality across area values;
- Theil T and Theil L (mean log deviation);
- Shannon entropy of population shares across areas;
- Duncan-Duncan two-group dissimilarity;
- group-A isolation and interaction exposure indices.

These measures describe different aspects of inequality and segregation. The [implementation](../../implementations/python/spatial-inequality/README.md) makes weights, denominators, zero handling and limits explicit.

## Important distinction

The weighted Gini and Shannon area entropy in this package do not use distances or adjacency. Dissimilarity measures evenness; isolation and interaction measure potential within-area exposure. None measures spatial clustering or distance decay. These are not interchangeable indicators.

## References

Duncan and Duncan (1955); Massey and Denton (1988); Shannon (1948); Theil (1967).
