# Triangle-mesh edge shortest paths

A transparent Dijkstra baseline on the **edge graph** of a triangular mesh. Edge weights are 3D Euclidean lengths; output is a vertex path and accumulated edge length.

This is useful for graph-routing baselines, topology checks and comparison experiments. It is **not** MMP, Chen–Han or fast marching on a triangulated surface. Since paths are restricted to mesh edges, the result is generally an upper bound on the continuous surface-geodesic distance (assuming the mesh edges lie on the represented surface). Mesh refinement may improve the approximation, but convergence depends on mesh quality and geometry.

Run:

```bash
python -m pytest -q
```

The code validates triangular faces and vertex indices, handles disconnected components, and uses a binary heap. Complexity is O((V+E) log V) for the edge graph. It does not interpolate paths through triangle interiors, support edge costs beyond Euclidean length, or implement continuous wavefront propagation.
