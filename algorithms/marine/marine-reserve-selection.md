# Marine reserve selection

A conservation-planning problem can select a subset of planning zones to represent biodiversity features while controlling acquisition cost and fragmentation. Let (x_j\in\{0,1\}) indicate whether zone (j) is selected, (a_{jk}) its amount of feature (k), (c_j) its cost, and (T_k) the target for feature (k).

The reference objective is

\[
\min_x\;\sum_j c_jx_j
+\lambda\sum_{(i,j)\in E}b_{ij}|x_i-x_j|
+\rho\sum_k\left[\max\left(T_k-\sum_j a_{jk}x_j,0\right)\right]^2.
\]

The first term is acquisition cost, the second penalizes selected/unselected boundaries, and the third penalizes representation shortfalls. The implementation uses seeded single-zone simulated annealing, starting with all zones selected and retaining the best solution encountered.

## Limits

This is a Marxan-style teaching baseline, not full Marxan or Zonation. It omits separation targets, zone status, connectivity constraints, feature-specific penalty functions, irreplaceability, uncertainty, multiple planning scenarios and global optimality guarantees. Benthic habitat classification and multibeam backscatter calibration are separate tasks.

## Verification

Tests compare the objective to a direct numeric oracle, exercise a small target-covering case and confirm infeasible targets are reported explicitly.

See the [implementation package](../../implementations/python/marine-reserve-selection/README.md).
