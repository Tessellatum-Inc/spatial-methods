# Source verification — Felzenszwalb–Huttenlocher Euclidean distance transform

## Identity and bibliography
Felzenszwalb, P. F. and Huttenlocher, D. P. (2012), “Distance Transforms of Sampled Functions,” *Theory of Computing*, 8, 415–428, DOI 10.4086/toc.2012.v008a019. The paper presents a linear-time one-dimensional lower-envelope transform for sampled functions and derives the exact Euclidean distance transform by separability.

## Technical claims
- A one-dimensional squared transform is the minimum of sampled costs plus a squared-distance parabola.
- The lower envelope can be represented by active parabola indices and their intersection coordinates.
- Applying the transform along each dimension yields an exact separable squared Euclidean transform; taking the square root gives Euclidean distances.
- For a fixed-dimensional regular grid, the algorithm is linear in the number of cells.

## Implementation/reproduction
Implemented: public 1-D sampled-function transform accepting finite values and positive infinity; 2-D binary target transform with anisotropic row/column spacing; two separable passes and square-root output. Tests compare 1-D output with brute-force minimisation and 2-D output with direct nearest-target distances over degenerate shapes and randomized masks. Tests also cover multiple targets, anisotropic spacing, empty rows, invalid costs and invalid spacing.

Not implemented: nearest-target indices, arbitrary-dimensional arrays, chamfer metrics, barrier-aware paths, cost surfaces, NoData policy, fast marching/Eikonal solvers or heat-method distances. Repository CI is required to establish passing status.

## Rights
Only mathematical definitions and bibliographic metadata are paraphrased; no source code, figures or datasets are reproduced.
