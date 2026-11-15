# Laplacian and Taubin mesh smoothing

Mesh smoothing reduces high-frequency geometric variation by moving mesh vertices while retaining connectivity.

## Uniform Laplacian smoothing

For vertex $v_i$ with one-ring neighbours $N(i)$:

$$
v_i' = v_i + \lambda\left(\frac{1}{|N(i)|}\sum_{j\in N(i)}v_j-v_i\right).
$$

All vertices update simultaneously from the previous iteration. Positive lambda moves a free vertex toward its neighbour centroid. Repeated updates generally shrink closed surfaces and round sharp features.

## Taubin smoothing

Taubin smoothing applies two passes per iteration:

$$
v^{(1)}=(I+\lambda L)v^{(0)},\qquad
v^{(2)}=(I+\mu L)v^{(1)},
$$

where lambda is positive and mu is negative. The second pass counteracts much of the low-frequency shrinkage; it does not guarantee exact volume preservation.

## Applications and limits

Useful for cleaning noisy LiDAR-derived meshes, terrain surfaces, building meshes and reconstructed objects. Do not apply blindly to legally significant boundaries, sharp roof ridges, breaklines or engineering surfaces.

The [Python package](../../implementations/python/mesh-smoothing/README.md) implements uniform one-ring weights, optional boundary and feature pinning, and tests. Cotangent-weighted operators, crease detection, remeshing and repair are not included.

## Source mapping

Original compendium: Section 17, page 35, "Mesh processing". This record covers Laplacian and Taubin smoothing only. Remeshing, mesh repair, ball pivoting and half-edge/winged-edge/quad-edge structures remain separate backlog items. See the [verification ledger](../../catalog/verification/mesh-smoothing.md).
