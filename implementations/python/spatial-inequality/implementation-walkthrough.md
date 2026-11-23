# Spatial inequality and segregation — implementation walkthrough

## 1. Inequality across area values
Weighted Gini compares all pairs of area values using population/exposure weights. The implementation sorts values and accumulates lower-value weighted totals, avoiding an explicit O(n²) pair loop. Theil T and Theil L use weighted logarithmic deviations from the weighted mean and are decomposable into within- and between-group components when a grouping is defined.

## 2. Spatial distribution entropy
Shannon entropy is computed from each area's share of the total population. The normalized value divides by log(number of supplied areas). It measures evenness across areas but does not use their map locations or adjacency.

## 3. Two-group segregation
The dissimilarity index compares the two groups' area-share distributions. Isolation and interaction weight each area's group composition by the probability that a randomly selected group-A member lives there.

## 4. Interpretation limits
These measures answer different questions and should not be collapsed into one segregation score. They do not capture clustering or distance decay. Group definitions, denominators, areal units and population weights materially affect interpretation.
