# Soft-Impute matrix completion

Soft-Impute estimates missing entries of a partially observed matrix by
repeated singular-value decomposition and soft-thresholding. The threshold
shrinks singular values, encouraging a low-rank reconstruction. Observed
entries are restored after every update.

The linked implementation initializes missing cells with the observed
global mean, supports an optional rank cap, and reports convergence
diagnostics. It is a dense matrix baseline. Tensor completion, spatial
regularization, uncertainty quantification and deep inpainting are
different methods and are not included.
