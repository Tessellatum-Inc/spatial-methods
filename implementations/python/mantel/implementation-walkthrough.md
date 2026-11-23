# Implementation walkthrough: Mantel tests

1. **Validate the matrix.** Check square shape, finite non-negative distances, symmetry and zero diagonal. Check that there are at least three observations.
2. **Extract each unordered pair once.** Use entries with i < j; the diagonal and mirrored lower triangle are redundant.
3. **Compute the statistic.** Simple Mantel uses Pearson correlation of upper triangles. Partial Mantel regresses each tested vector on the control vector and correlates the residuals.
4. **Preserve structure in permutations.** A permutation is an ordering of observation labels. For ordering pi, the relabelled entry is D[pi(i), pi(j)]. Apply it to both axes.
5. **Count extreme statistics.** The plus-one estimate is (k+1)/(B+1). A fixed seed makes examples reproducible.
6. **Interpret the null carefully.** A small p-value is conditional on exchangeability. Partial correlation removes only a linear relationship with the control-distance vector; it does not model an arbitrary spatial random field.
