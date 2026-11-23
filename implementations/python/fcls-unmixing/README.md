# Fully Constrained Least Squares (FCLS)

Install requirements and run `pytest -q`. The implementation solves a per-pixel constrained least-squares problem with nonnegative abundances and a sum-to-one equality constraint using SciPy SLSQP. It returns abundance fractions, reconstructed spectra, per-pixel RMSE and solver success flags.

The linear mixture model is assumed. The sum-to-one constraint is appropriate when the selected endmembers explain the full mixture and data are appropriately calibrated; it may be inappropriate with shade, unmodelled materials or additive effects unless those are represented in the model. Inspect convergence flags and residuals; do not silently treat failed pixels as reliable. This baseline solves pixels independently and is not a spatially regularised unmixing method.
