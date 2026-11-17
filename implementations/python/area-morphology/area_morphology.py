"""Small-raster grayscale area opening and closing by threshold components."""
from __future__ import annotations

from collections import deque
from typing import Iterable

import numpy as np


def _image(values: Iterable[Iterable[float]]) -> np.ndarray:
    image = np.asarray(values, dtype=float)
    if image.ndim != 2 or min(image.shape, default=0) < 1:
        raise ValueError("values must be a non-empty two-dimensional raster")
    if not np.all(np.isfinite(image)):
        raise ValueError("values must be finite")
    return image


def _offsets(connectivity: int) -> tuple[tuple[int, int], ...]:
    if connectivity == 4:
        return ((-1, 0), (1, 0), (0, -1), (0, 1))
    if connectivity == 8:
        return tuple((dr, dc) for dr in (-1, 0, 1) for dc in (-1, 0, 1) if (dr, dc) != (0, 0))
    raise ValueError("connectivity must be 4 or 8")


def area_opening(
    values: Iterable[Iterable[float]],
    *,
    min_area: int,
    connectivity: int = 4,
) -> np.ndarray:
    """Remove bright connected components smaller than min_area.

    This threshold-stack reference algorithm is exact for the chosen grid
    connectivity, but costs O(U * N), where U is the number of unique values.
    """
    image = _image(values)
    if isinstance(min_area, bool) or int(min_area) != min_area or min_area < 1:
        raise ValueError("min_area must be a positive integer")
    offsets = _offsets(connectivity)
    rows, cols = image.shape
    result = np.full(image.shape, np.min(image), dtype=float)
    for level in np.unique(image)[::-1]:
        active = image >= level
        visited = np.zeros(image.shape, dtype=bool)
        for row in range(rows):
            for col in range(cols):
                if not active[row, col] or visited[row, col]:
                    continue
                queue = deque([(row, col)])
                visited[row, col] = True
                component = []
                while queue:
                    r, c = queue.popleft()
                    component.append((r, c))
                    for dr, dc in offsets:
                        rr, cc = r + dr, c + dc
                        if 0 <= rr < rows and 0 <= cc < cols and active[rr, cc] and not visited[rr, cc]:
                            visited[rr, cc] = True
                            queue.append((rr, cc))
                if len(component) >= min_area:
                    for r, c in component:
                        if result[r, c] < level:
                            result[r, c] = level
    return result


def area_closing(
    values: Iterable[Iterable[float]],
    *,
    min_area: int,
    connectivity: int = 4,
) -> np.ndarray:
    """Fill dark connected components smaller than min_area."""
    return -area_opening(-_image(values), min_area=min_area, connectivity=connectivity)
