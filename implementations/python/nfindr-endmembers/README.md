# N-FINDR endmember extraction

Run `pytest -q`. The implementation projects spectra into a leading signal subspace and iteratively replaces candidate endmembers when a replacement increases the absolute determinant of the augmented simplex matrix. It returns observed endmember spectra, source pixel indices, final determinant and iteration count.

This is a direct, computationally expensive reference baseline: each update scans candidate pixels and recomputes a small determinant. It assumes a linear mixture model with pure pixels near the convex-hull vertices. Results depend on initialization, subspace dimension, noise and iteration limit. It is not a fast vectorized or fully noise-aware N-FINDR variant.
