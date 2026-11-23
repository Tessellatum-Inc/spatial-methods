# Laplacian and Taubin mesh smoothing

Implements uniform one-ring **Laplacian smoothing** and two-pass **Taubin smoothing** on triangular 3D meshes. Connectivity is unchanged. Optional boundary and explicit feature-vertex pinning are supported.

## Run
```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

## Example
```python
import numpy as np
from mesh_smoothing import laplacian_smooth, taubin_smooth
vertices = np.array([[0,0,0],[1,0,0],[0,1,0],[0,0,1]], dtype=float)
faces = np.array([[0,1,2],[0,1,3],[0,2,3],[1,2,3]])
smoothed = laplacian_smooth(vertices, faces, iterations=5, lam=0.3)
less_shrunken = taubin_smooth(vertices, faces, iterations=5, lam=0.3, mu=-0.32)
```

## Contract and limitations
Vertices must be finite (n,3) coordinates; faces must be valid (m,3) triangles. Repeated indices, out-of-range indices and edges incident to more than two faces are rejected. Each update is simultaneous. The implementation uses uniform graph weights, not cotangent-weighted Laplace–Beltrami operators. Ordinary Laplacian smoothing shrinks surfaces and rounds features. Taubin's negative pass counteracts much of that shrinkage but does not exactly preserve volume. It does not remesh, repair holes, or detect creases automatically.

Tests include a hand-calculated one-ring update, tetrahedron shrinkage, Taubin comparison, fixed/boundary vertices and invalid topology.
