# N-FINDR endmember extraction

N-FINDR searches for a set of observed spectra whose simplex volume in a reduced spectral subspace is large. The method is commonly used to identify candidate endmembers under a linear mixture and pure-pixel model.

The reference implementation uses SVD subspace projection, seeded initialisation and iterative one-for-one vertex replacement by determinant-based simplex-volume improvement. It returns the selected spectra and pixel indices.

This direct implementation is computationally expensive and initialization-sensitive. It is not a noise-aware or accelerated variant. A large simplex does not prove that selected spectra are physically pure materials.
