"""Deterministic iterative inverse-distance DEM void filling."""
import math

def _prepare(grid, nodata):
    if isinstance(grid, (str, bytes)) or not isinstance(grid, (list, tuple)) or not grid:
        raise ValueError("grid must be a non-empty rectangular sequence")
    if any(isinstance(row, (str, bytes)) or not isinstance(row, (list, tuple)) for row in grid):
        raise ValueError("grid rows must be sequences")
    width = len(grid[0])
    if width == 0 or any(len(row) != width for row in grid):
        raise ValueError("grid must be rectangular and non-empty")
    result = []
    valid_count = 0
    for row in grid:
        out = []
        for value in row:
            missing = value is None
            if not missing and nodata is not None:
                missing = value == nodata
            if not missing and isinstance(value, (int, float)) and not isinstance(value, bool):
                missing = not math.isfinite(value)
            if missing:
                out.append(None)
            elif isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
                raise ValueError("valid DEM cells must be finite numeric values")
            else:
                out.append(float(value))
                valid_count += 1
        result.append(out)
    if valid_count == 0:
        raise ValueError("at least one valid elevation is required")
    return result, valid_count

def inverse_distance_void_fill(grid, *, nodata=None, max_radius=3,
                               min_neighbors=3, power=2.0,
                               pixel_size_x=1.0, pixel_size_y=1.0,
                               max_iterations=1):
    """Fill NoData cells using synchronous local inverse-distance weighting."""
    current, _ = _prepare(grid, nodata)
    if isinstance(max_radius, bool) or not isinstance(max_radius, int) or max_radius < 1:
        raise ValueError("max_radius must be a positive integer")
    if isinstance(min_neighbors, bool) or not isinstance(min_neighbors, int) or min_neighbors < 1:
        raise ValueError("min_neighbors must be a positive integer")
    if isinstance(max_iterations, bool) or not isinstance(max_iterations, int) or max_iterations < 1:
        raise ValueError("max_iterations must be a positive integer")
    for name, value in (("power", power), ("pixel_size_x", pixel_size_x), ("pixel_size_y", pixel_size_y)):
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0:
            raise ValueError(f"{name} must be finite and positive")
    height, width = len(current), len(current[0])
    for _ in range(max_iterations):
        updates = {}
        for row in range(height):
            for col in range(width):
                if current[row][col] is not None:
                    continue
                weighted_sum = 0.0
                weight_total = 0.0
                count = 0
                for rr in range(max(0, row-max_radius), min(height, row+max_radius+1)):
                    for cc in range(max(0, col-max_radius), min(width, col+max_radius+1)):
                        value = current[rr][cc]
                        if value is None:
                            continue
                        distance = math.hypot((cc-col)*pixel_size_x, (rr-row)*pixel_size_y)
                        if distance == 0 or distance > max_radius * max(pixel_size_x, pixel_size_y):
                            continue
                        weight = distance ** (-power)
                        weighted_sum += weight * value
                        weight_total += weight
                        count += 1
                if count >= min_neighbors and weight_total > 0:
                    updates[(row, col)] = weighted_sum / weight_total
        if not updates:
            break
        for (row, col), value in updates.items():
            current[row][col] = value
    filled_mask = [[grid[r][c] is None or (nodata is not None and grid[r][c] == nodata)
                    or (isinstance(grid[r][c], (int, float)) and not isinstance(grid[r][c], bool) and not math.isfinite(grid[r][c]))
                    for c in range(width)] for r in range(height)]
    return {"elevation": current, "filled_mask": filled_mask}
