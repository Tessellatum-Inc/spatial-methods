# Geodesics on triangular meshes: exact surface paths versus edge-graph paths

A geodesic is a shortest path constrained to a surface. For a triangulated polyhedral surface, the continuous path may cross triangle interiors; restricting the path to mesh edges changes the problem.

## Edge-graph baseline implemented here

The Python package constructs an undirected graph whose nodes are mesh vertices and whose edges are triangle edges weighted by their 3D Euclidean lengths. Dijkstra's algorithm then solves

\[
d(v)=\min_{(u,v)\in E}\{d(u)+\|p_u-p_v\|_2\}.
\]

With a binary heap, the graph solve is \(O((V+E)\log V)\). The returned route is an edge-constrained path. It is not generally the shortest path over the triangle surface: the continuous geodesic can cut across face interiors and therefore be shorter. For a valid embedded mesh with Euclidean edge weights, the edge path provides an upper bound on the continuous surface distance between its vertices.

See the [tested Python package](../implementations/python/mesh-geodesics/README.md) for input validation, disconnected-component handling, distances and path reconstruction.

## Research algorithms in the source inventory

- **Mitchell–Mount–Papadimitriou (MMP):** an exact continuous-Dijkstra approach. It propagates windows over edges to represent shortest-path distance functions to points in face interiors. The original published SIAM Journal on Computing paper gives an \(O(n^2\log n)\)-time, \(O(n^2)\)-space bound in its stated surface-complexity parameter.
- **Chen–Han (CH):** an exact single-source approach based on a different unfolding/propagation organization. The 1990 SoCG paper reports \(O(n^2)\) time and linear space for its stated formulation. Its full journal version appeared later.
- **Fast marching on triangulated domains:** numerical solution of the Eikonal equation, extended from orthogonal grids to triangulated manifolds. Kimmel and Sethian report \(O(M\log M)\) complexity for their triangulated-domain method. It is a numerical method, not the same algorithm as exact window propagation.

The current package does **not** implement MMP, Chen–Han or triangulated fast marching. It is a graph baseline to test mesh topology and establish a measurable approximation reference before implementing continuous methods.

## Practical evaluation

Compare edge-graph distances against a trusted exact or high-quality continuous solver on meshes with varied resolution, aspect ratios, curvature, boundaries and non-convexity. Report absolute and relative distance error, path length, runtime, memory and sensitivity to remeshing. Do not infer convergence from one regular planar mesh.

## Sources

- Mitchell, J. S. B., Mount, D. M., & Papadimitriou, C. H. (1987). “The Discrete Geodesic Problem.” *SIAM Journal on Computing*, 16(4), 647–668. DOI: [10.1137/0216045](https://doi.org/10.1137/0216045).
- Chen, J., & Han, Y. (1990). “Shortest Paths on a Polyhedron.” *Proceedings of the Sixth Annual Symposium on Computational Geometry*, 360–369. DOI: [10.1145/98524.98601](https://doi.org/10.1145/98524.98601).
- Kimmel, R., & Sethian, J. A. (1998). “Computing Geodesic Paths on Manifolds.” *Proceedings of the National Academy of Sciences*, 95(15), 8431–8435. DOI: [10.1073/pnas.95.15.8431](https://doi.org/10.1073/pnas.95.15.8431).

Only bibliographic metadata and links are included; no paper text or figures are reproduced.
