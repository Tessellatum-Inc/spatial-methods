# Verification — raster components, flood fill and RLE

- Source: Section 4, page 6, connected components/flood fill/RLE/image pyramid row.
- Existing component labeling: 2-D 4/8 connectivity and 3-D 6/18/26 connectivity.
- Added: exact-value seed flood fill with 4/8 connectivity and validity barriers;
  lossless row-major RLE for finite numeric 2-D arrays, preserving shape/dtype; NaN-aware 2x2 box-reduction pyramids for 2-D and banded 3-D arrays.
- Tests: diagonal connectivity, invalid barriers/seeds, deterministic component
  labels, numeric/bool/float RLE round trips, single-run arrays, malformed RLE streams, odd-edge pyramid reductions, band-wise NoData averaging and invalid
  pyramid parameters.
- Open: Gaussian/Laplacian pyramids, tiled/parallel label reconciliation, optimized
  union-find/RLE labeling, bit packing and external raster format codecs.
- Status: partial contribution to grouped source entry.
