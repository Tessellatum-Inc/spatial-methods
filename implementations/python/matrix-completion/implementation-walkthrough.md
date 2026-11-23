# Soft-Impute implementation walkthrough

1. Mark observed and missing cells; reject an entirely missing matrix.
2. Initialize missing cells with the global mean of observed values.
3. Compute a compact singular-value decomposition of the current filled
   matrix.
4. Subtract the regularization threshold from singular values, floor at
   zero, and optionally truncate to a maximum rank.
5. Update missing cells from the low-rank reconstruction while clamping
   observed cells to their original values.
6. Stop when the relative change in missing cells is below tolerance or
   the iteration limit is reached.

The returned convergence flag is part of the output contract. The method
is a dense matrix baseline, not a complete spatiotemporal or tensor model.
