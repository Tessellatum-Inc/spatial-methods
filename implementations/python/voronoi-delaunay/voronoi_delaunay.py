"""Library-backed 2D Voronoi and Delaunay construction using SciPy/Qhull."""
from __future__ import annotations
from collections.abc import Sequence
from dataclasses import dataclass
import numpy as np
from scipy.spatial import Delaunay, Voronoi


@dataclass(frozen=True)
class TessellationResult:
    """The validated site coordinates and their SciPy tessellations."""
    points: np.ndarray
    voronoi: Voronoi
    delaunay: Delaunay


def build_tessellations(points: Sequence[Sequence[float]]) -> TessellationResult:
    """Build planar Voronoi and Delaunay structures for unique 2D sites.

    This validates the input contract and delegates construction to Qhull
    through SciPy. QhullError is allowed to propagate for numerical or
    combinatorial degeneracies that Qhull cannot resolve under its defaults.
    """
    coordinates = np.asarray(points, dtype=float)
    if coordinates.ndim != 2 or coordinates.shape[1] != 2:
        raise ValueError("points must be an n-by-2 coordinate array")
    if len(coordinates) < 3:
        raise ValueError("at least three points are required")
    if not np.isfinite(coordinates).all():
        raise ValueError("coordinates must be finite")
    if len(np.unique(coordinates, axis=0)) != len(coordinates):
        raise ValueError("duplicate site coordinates are not allowed")
    if np.linalg.matrix_rank(coordinates - coordinates[0]) < 2:
        raise ValueError("sites must not all be collinear")

    voronoi = Voronoi(coordinates)
    delaunay = Delaunay(coordinates)
    coordinates.setflags(write=False)
    return TessellationResult(coordinates, voronoi, delaunay)


@dataclass(frozen=True)
class AlphaShapeResult:
    """Triangle-union alpha shape and its oriented boundary edge set.

    Triangle indices refer to the immutable points array. Boundary edges are
    directed so that retained triangle interiors lie to their left.
    """
    points: np.ndarray
    max_circumradius: float
    triangles: tuple[tuple[int, int, int], ...]
    boundary_edges: tuple[tuple[int, int], ...]


def build_alpha_shape(
    points: Sequence[Sequence[float]], *, max_circumradius: float
) -> AlphaShapeResult:
    """Build the 2D triangle-union alpha shape from a Delaunay triangulation.

    The parameter is a length: retain each Delaunay triangle whose
    circumradius is <= max_circumradius. Boundary edges are those belonging
    to exactly one retained triangle. This returns the boundary of the
    retained 2D triangle union; isolated vertices/edges in the full alpha
    complex are intentionally not represented.
    """
    radius_limit = float(max_circumradius)
    if not np.isfinite(radius_limit) or radius_limit <= 0:
        raise ValueError("max_circumradius must be finite and positive")
    coordinates = np.asarray(points, dtype=float)
    if coordinates.ndim != 2 or coordinates.shape[1] != 2:
        raise ValueError("points must be an n-by-2 coordinate array")
    if len(coordinates) < 3:
        raise ValueError("at least three points are required")
    if not np.isfinite(coordinates).all():
        raise ValueError("coordinates must be finite")
    if len(np.unique(coordinates, axis=0)) != len(coordinates):
        raise ValueError("duplicate site coordinates are not allowed")
    if np.linalg.matrix_rank(coordinates - coordinates[0]) < 2:
        raise ValueError("sites must not all be collinear")

    triangulation = Delaunay(coordinates)
    retained: list[tuple[int, int, int]] = []
    edge_occurrences: dict[tuple[int, int], list[tuple[int, int]]] = {}
    for simplex in triangulation.simplices:
        i, j, k = (int(v) for v in simplex)
        a, b, c = coordinates[[i, j, k]]
        cross = float((b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0]))
        if cross == 0.0:
            continue
        ab = float(np.linalg.norm(a-b))
        bc = float(np.linalg.norm(b-c))
        ca = float(np.linalg.norm(c-a))
        circumradius = (ab * bc * ca) / (2.0 * abs(cross))
        if circumradius > radius_limit:
            continue
        if cross < 0:
            j, k = k, j
        triangle = (i, j, k)
        retained.append(triangle)
        for edge in ((i, j), (j, k), (k, i)):
            edge_occurrences.setdefault(tuple(sorted(edge)), []).append(edge)

    boundary = tuple(
        occurrences[0]
        for _, occurrences in sorted(edge_occurrences.items())
        if len(occurrences) == 1
    )
    coordinates.setflags(write=False)
    return AlphaShapeResult(
        points=coordinates,
        max_circumradius=radius_limit,
        triangles=tuple(retained),
        boundary_edges=boundary,
    )
