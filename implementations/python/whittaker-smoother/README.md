# Whittaker-Eilers smoothing

A NumPy reference implementation of penalized finite-difference smoothing for an ordered one-dimensional sequence. It solves a weighted least-squares system with a squared finite-difference penalty.

- The difference order controls the polynomial null space (for example, second differences preserve linear trends).
- Missing observations and zero-weight observations are omitted from the data-fit term.
- The index spacing is assumed uniform.
- Dense linear algebra makes this a clear small/medium reference implementation, not a sparse large-series solver.

Install NumPy and pytest, then run pytest -q. See the [algorithm note](../../../algorithms/interpolation/whittaker-smoother.md).
