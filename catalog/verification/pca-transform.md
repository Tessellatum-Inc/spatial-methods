# PCA transform — verification ledger

## Scope
The implementation performs covariance or correlation PCA on a two-dimensional samples-by-bands matrix. It is not MNF and does not include raster I/O, spatial tiling, or streaming estimation.

## Verification evidence
- Tests compare eigenvalues with NumPy's independently exposed symmetric eigensolver and projected sample covariance with the diagonal eigenvalue matrix.
- Tests cover valid-row filtering, sample-standard-deviation scaling, constant-band rejection during standardization, invalid masks and component-count validation.
- Test suite has been authored but has not been executed in this environment. No passing CI run is claimed.

## Limitations
Eigenvector sign is indeterminate; exact component vectors should not be compared without sign alignment. Degenerate/tied eigenvalues allow rotations within their eigenspaces. MNF remains a separate backlog item.
