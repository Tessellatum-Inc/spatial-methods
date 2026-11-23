# Source verification — spatial inequality and segregation measures

## Identity and bibliography
The two-group dissimilarity measure is associated with Duncan and Duncan (1955), “A Methodological Analysis of Segregation Indexes,” *American Sociological Review*, 20(2), 210–217, DOI 10.2307/2088328. Massey and Denton (1988), “The Dimensions of Residential Segregation,” *Social Forces*, 67(2), 281–315, DOI 10.1093/sf/67.2.281, classify segregation measures into evenness, exposure, concentration, centralization and clustering. Shannon (1948) establishes the entropy measure; Theil (1967) develops entropy-based economic inequality measures.

## Technical claims
Weighted Gini summarizes pairwise inequality in area values. Theil T and L are entropy-based inequality indices. Shannon entropy of area population shares measures evenness across the supplied areas. The dissimilarity index compares group-specific area shares; isolation and interaction are group-A-weighted averages of the within-area group proportions.

## Implementation and reproduction
Implemented: weighted Gini, Theil T, Theil L, Shannon area entropy, two-group dissimilarity, and two-group isolation/interaction. Tests check known values, equality, scale invariance, zero handling, the two-group exposure identity and invalid inputs.

Not implemented: distance-weighted spatial Gini, Moran-based inequality, multigroup entropy decomposition, concentration, centralization, clustering, proximity or distance-decay segregation. Repository CI is required to establish committed tests pass in its target environment.

## Rights
Definitions and equations are independently typeset and paraphrased. No publisher or government source code or figures are reproduced.
