"""Connected-component labeling for boolean raster masks."""
from __future__ import annotations
from collections import deque
from typing import Sequence
import numpy as np

def connected_components(foreground: Sequence[Sequence[bool]]|np.ndarray, *, connectivity: int=8, valid: Sequence[Sequence[bool]]|np.ndarray|None=None) -> tuple[np.ndarray,dict[int,int]]:
    """Label foreground components in deterministic row-major discovery order.

    Label zero means background or invalid. A supplied valid mask marks cells
    participating in the analysis; invalid cells are barriers.
    """
    raw=np.asarray(foreground)
    if raw.ndim!=2 or raw.size==0:
        raise ValueError("foreground must be a non-empty 2D array")
    if not (np.issubdtype(raw.dtype,np.bool_) or np.issubdtype(raw.dtype,np.number)):
        raise ValueError("foreground must be boolean or numeric 0/1")
    if not np.isfinite(raw).all() or not np.isin(raw,[0,1]).all():
        raise ValueError("foreground must contain only finite boolean/0/1 values")
    mask=raw.astype(bool)
    if connectivity not in (4,8):
        raise ValueError("connectivity must be 4 or 8")
    if valid is None:
        valid_mask=np.ones(mask.shape,dtype=bool)
    else:
        raw_valid=np.asarray(valid)
        if raw_valid.ndim!=2 or raw_valid.shape!=mask.shape:
            raise ValueError("valid mask must have the same 2D shape as foreground")
        if not (np.issubdtype(raw_valid.dtype,np.bool_) or np.issubdtype(raw_valid.dtype,np.number)) or not np.isfinite(raw_valid).all() or not np.isin(raw_valid,[0,1]).all():
            raise ValueError("valid mask must contain only finite boolean/0/1 values")
        valid_mask=raw_valid.astype(bool)
    rows,cols=mask.shape
    labels=np.zeros(mask.shape,dtype=np.int32)
    if connectivity==4:
        offsets=((-1,0),(1,0),(0,-1),(0,1))
    else:
        offsets=tuple((dr,dc) for dr in (-1,0,1) for dc in (-1,0,1) if (dr,dc)!=(0,0))
    sizes={}
    next_label=0
    for r in range(rows):
        for c in range(cols):
            if not mask[r,c] or not valid_mask[r,c] or labels[r,c]!=0:
                continue
            next_label+=1
            labels[r,c]=next_label
            queue=deque([(r,c)])
            size=0
            while queue:
                cr,cc=queue.popleft()
                size+=1
                for dr,dc in offsets:
                    nr,nc=cr+dr,cc+dc
                    if 0<=nr<rows and 0<=nc<cols and mask[nr,nc] and valid_mask[nr,nc] and labels[nr,nc]==0:
                        labels[nr,nc]=next_label
                        queue.append((nr,nc))
            sizes[next_label]=size
    return labels,sizes


def connected_components_3d(
    foreground: Sequence[Sequence[Sequence[bool]]] | np.ndarray, *,
    connectivity: int = 26,
    valid: Sequence[Sequence[Sequence[bool]]] | np.ndarray | None = None,
) -> tuple[np.ndarray, dict[int, int]]:
    """Label 3-D foreground voxels using 6-, 18- or 26-neighbour connectivity.

    Labels are assigned in deterministic z/y/x discovery order. Zero denotes
    background or invalid voxels; invalid voxels are barriers. This is a
    breadth-first reference implementation, not a parallel or tiled labeler.
    """
    raw = np.asarray(foreground)
    if raw.ndim != 3 or raw.size == 0:
        raise ValueError("foreground must be a non-empty 3D array")
    if not (np.issubdtype(raw.dtype, np.bool_) or np.issubdtype(raw.dtype, np.number)):
        raise ValueError("foreground must be boolean or numeric 0/1")
    if not np.isfinite(raw).all() or not np.isin(raw, [0, 1]).all():
        raise ValueError("foreground must contain only finite boolean/0/1 values")
    mask = raw.astype(bool)
    if connectivity not in (6, 18, 26):
        raise ValueError("connectivity must be 6, 18 or 26")
    if valid is None:
        valid_mask = np.ones(mask.shape, dtype=bool)
    else:
        raw_valid = np.asarray(valid)
        if raw_valid.ndim != 3 or raw_valid.shape != mask.shape:
            raise ValueError("valid mask must have the same 3D shape as foreground")
        if (not (np.issubdtype(raw_valid.dtype, np.bool_) or np.issubdtype(raw_valid.dtype, np.number))
                or not np.isfinite(raw_valid).all() or not np.isin(raw_valid, [0, 1]).all()):
            raise ValueError("valid mask must contain only finite boolean/0/1 values")
        valid_mask = raw_valid.astype(bool)
    offsets = []
    for dz in (-1, 0, 1):
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                order = abs(dz) + abs(dy) + abs(dx)
                if order == 0:
                    continue
                if connectivity == 6 and order != 1:
                    continue
                if connectivity == 18 and order == 3:
                    continue
                offsets.append((dz, dy, dx))
    depth, rows, cols = mask.shape
    labels = np.zeros(mask.shape, dtype=np.int32)
    sizes = {}
    next_label = 0
    for z in range(depth):
        for y in range(rows):
            for x in range(cols):
                if not mask[z, y, x] or not valid_mask[z, y, x] or labels[z, y, x] != 0:
                    continue
                next_label += 1
                labels[z, y, x] = next_label
                queue = deque([(z, y, x)])
                size = 0
                while queue:
                    cz, cy, cx = queue.popleft()
                    size += 1
                    for dz, dy, dx in offsets:
                        nz, ny, nx = cz + dz, cy + dy, cx + dx
                        if (0 <= nz < depth and 0 <= ny < rows and 0 <= nx < cols
                                and mask[nz, ny, nx] and valid_mask[nz, ny, nx]
                                and labels[nz, ny, nx] == 0):
                            labels[nz, ny, nx] = next_label
                            queue.append((nz, ny, nx))
                sizes[next_label] = size
    return labels, sizes


def flood_fill(
    raster: Sequence[Sequence[object]] | np.ndarray,
    seed: tuple[int, int],
    *,
    connectivity: int = 4,
    valid: Sequence[Sequence[bool]] | np.ndarray | None = None,
) -> np.ndarray:
    """Return the exact-value region connected to seed; invalid cells are barriers."""
    data = np.asarray(raster)
    if data.ndim != 2 or data.size == 0:
        raise ValueError("raster must be a non-empty 2D array")
    if data.dtype.kind not in "biuf":
        raise ValueError("raster values must be boolean, integer or real numeric")
    if not np.isfinite(data).all():
        raise ValueError("raster values must be finite")
    if connectivity not in (4, 8):
        raise ValueError("connectivity must be 4 or 8")
    if len(seed) != 2 or any(isinstance(v, bool) or not isinstance(v, (int, np.integer)) for v in seed):
        raise ValueError("seed must contain two integer indices")
    sr, sc = map(int, seed)
    rows, cols = data.shape
    if not (0 <= sr < rows and 0 <= sc < cols):
        raise ValueError("seed lies outside raster bounds")
    if valid is None:
        valid_mask = np.ones(data.shape, dtype=bool)
    else:
        raw_valid = np.asarray(valid)
        if raw_valid.shape != data.shape or raw_valid.dtype.kind not in "biu" or not np.isin(raw_valid, [0, 1]).all():
            raise ValueError("valid mask must be a same-shape boolean/0/1 array")
        valid_mask = raw_valid.astype(bool)
    result = np.zeros(data.shape, dtype=bool)
    if not valid_mask[sr, sc]:
        return result
    target = data[sr, sc]
    offsets = ((-1,0),(1,0),(0,-1),(0,1)) if connectivity == 4 else tuple(
        (dr,dc) for dr in (-1,0,1) for dc in (-1,0,1) if (dr,dc)!=(0,0)
    )
    queue = deque([(sr, sc)])
    result[sr, sc] = True
    while queue:
        r, c = queue.popleft()
        for dr, dc in offsets:
            nr, nc = r+dr, c+dc
            if (0 <= nr < rows and 0 <= nc < cols and valid_mask[nr,nc]
                    and not result[nr,nc] and data[nr,nc] == target):
                result[nr,nc] = True
                queue.append((nr,nc))
    return result


def run_length_encode(raster: Sequence[Sequence[object]] | np.ndarray) -> dict:
    """Losslessly encode a finite numeric 2-D raster as row-major value/count runs."""
    data = np.asarray(raster)
    if data.ndim != 2 or data.size == 0:
        raise ValueError("raster must be a non-empty 2D array")
    if data.dtype.kind not in "biuf" or not np.isfinite(data).all():
        raise ValueError("raster must contain finite boolean or numeric values")
    flat = data.ravel(order="C")
    runs = []
    value, count = flat[0].item(), 1
    for item in flat[1:]:
        current = item.item()
        if current == value:
            count += 1
        else:
            runs.append((value, count))
            value, count = current, 1
    runs.append((value, count))
    return {"shape": tuple(data.shape), "dtype": data.dtype.str, "runs": runs}


def run_length_decode(encoded: dict) -> np.ndarray:
    """Decode the value/count representation returned by run_length_encode."""
    if not isinstance(encoded, dict) or set(encoded) != {"shape", "dtype", "runs"}:
        raise ValueError("encoded data must contain shape, dtype and runs")
    shape = encoded["shape"]
    if (not isinstance(shape, (tuple, list)) or len(shape) != 2
            or any(isinstance(v, bool) or not isinstance(v, int) or v < 1 for v in shape)):
        raise ValueError("shape must contain two positive integer dimensions")
    try:
        dtype = np.dtype(encoded["dtype"])
    except (TypeError, ValueError):
        raise ValueError("invalid dtype") from None
    if dtype.kind not in "biuf":
        raise ValueError("only finite boolean or numeric dtypes are supported")
    runs = encoded["runs"]
    if not isinstance(runs, (tuple, list)) or not runs:
        raise ValueError("runs must be a non-empty sequence")
    values, total = [], 0
    for run in runs:
        if not isinstance(run, (tuple, list)) or len(run) != 2:
            raise ValueError("each run must be (value, positive_count)")
        value, count = run
        if isinstance(count, bool) or not isinstance(count, int) or count < 1:
            raise ValueError("run counts must be positive integers")
        try:
            cast = np.asarray(value, dtype=dtype).item()
        except (TypeError, ValueError, OverflowError):
            raise ValueError("run value cannot be represented by dtype") from None
        if not np.isfinite(cast):
            raise ValueError("run values must be finite")
        values.extend([cast] * count)
        total += count
    if total != shape[0] * shape[1]:
        raise ValueError("run counts do not match encoded shape")
    return np.asarray(values, dtype=dtype).reshape(tuple(shape), order="C")


def build_box_pyramid(
    raster: Sequence[Sequence[object]] | np.ndarray,
    *,
    levels: int,
) -> list[np.ndarray]:
    """Build a spatial box-reduction pyramid; NaNs are ignored in each 2x2 mean.

    Accepts a 2-D single-band array or 3-D (rows, columns, bands) array.
    The original array is copied as float64; each next level has ceil-half
    spatial dimensions. The number of returned levels includes the original.
    """
    data = np.asarray(raster, dtype=np.float64)
    if data.ndim not in (2, 3) or data.size == 0:
        raise ValueError("raster must be a non-empty 2D or 3D array")
    if np.isinf(data).any():
        raise ValueError("raster cannot contain infinite values")
    if isinstance(levels, bool) or not isinstance(levels, int) or levels < 1:
        raise ValueError("levels must be a positive integer")
    pyramid = [data.copy()]
    for _ in range(levels - 1):
        current = pyramid[-1]
        rows, cols = current.shape[:2]
        out_shape = ((rows + 1)//2, (cols + 1)//2) + current.shape[2:]
        reduced = np.full(out_shape, np.nan, dtype=np.float64)
        for r in range(out_shape[0]):
            for c in range(out_shape[1]):
                block = current[2*r:min(2*r+2, rows), 2*c:min(2*c+2, cols)]
                if current.ndim == 2:
                    valid_values = block[np.isfinite(block)]
                    if valid_values.size:
                        reduced[r,c] = valid_values.mean()
                else:
                    for band in range(current.shape[2]):
                        values = block[:,:,band]
                        valid_values = values[np.isfinite(values)]
                        if valid_values.size:
                            reduced[r,c,band] = valid_values.mean()
        pyramid.append(reduced)
        if reduced.shape[:2] == (1,1):
            break
    return pyramid
