## Mesh-geodesic source check

- **MMP:** Mitchell, J. S. B., Mount, D. M., & Papadimitriou, C. H. (1987), “The Discrete Geodesic Problem,” *SIAM Journal on Computing* 16(4), 647–668, DOI 10.1137/0216045. The published SIAM record gives O(n² log n) time and O(n²) space for its stated formulation; distinguish this from an earlier abstract/preprint version with a different bound.
- **Chen–Han:** Chen, J., & Han, Y. (1990), “Shortest Paths on a Polyhedron,” SoCG, 360–369, DOI 10.1145/98524.98601. The proceedings version reports O(n²) time and linear space for its formulation; the expanded journal version appeared in 1996. Do not conflate those records.
- **Triangulated fast marching:** Kimmel, R., & Sethian, J. A. (1998), “Computing Geodesic Paths on Manifolds,” *PNAS* 95(15), 8431–8435, DOI 10.1073/pnas.95.15.8431. The paper extends fast marching to triangulated domains and reports O(M log M) complexity.
- **Implementation boundary:** the committed Python package is Dijkstra on the mesh edge graph only. It is not MMP, Chen–Han or continuous fast marching; edge-restricted paths generally overestimate continuous surface distances.
- **Rights:** citations and DOI links only; no paper text/figures copied.
- **Status:** bibliographic identity checked against publisher/primary records; edge-graph implementation and regression tests added; CI and independent review pending.
