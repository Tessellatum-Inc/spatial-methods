# SLIC superpixels

Simple Linear Iterative Clustering (SLIC) groups nearby pixels using a
combined feature-space and spatial distance:

    D^2 = d_feature^2 + (m/S)^2 d_spatial^2

S is the nominal region spacing and m controls compactness. The reference
implementation uses regular grid seeds, local low-gradient seed adjustment,
bounded local assignment and iterative centre updates. Input feature vectors
are caller-supplied; CIELAB is a common choice for colour images.

The implementation does not enforce connected components and does not
include graph-based segmentation, multiresolution segmentation, MRF/CRF,
active contours or level sets. It is a scoped SLIC-style baseline, not a
complete segmentation suite. See the Python package for API and tests.
