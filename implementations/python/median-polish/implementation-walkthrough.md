# Median polish — implementation walkthrough

1. Start with the median of all observed cells as the overall effect and subtract it from the table.
2. Calculate each row's median residual, add it to that row's effect and subtract it from the row.
3. Repeat for columns.
4. Recenter row and column effects by their medians, adding those shifts to the overall effect. This gives an identifiable additive decomposition.
5. Calculate the sum of absolute residuals and stop when its proportional reduction is less than eps or max_iterations is reached.
6. If na_rm=True, missing cells are skipped in medians and remain missing in residuals.
