"""Brovey component-substitution pan-sharpening reference implementation."""
import math

def _grid(values, label, nodata):
    if isinstance(values, (str, bytes)) or not isinstance(values, (list, tuple)) or not values:
        raise ValueError(f"{label} must be a non-empty 2-D sequence")
    if any(isinstance(row, (str, bytes)) or not isinstance(row, (list, tuple)) for row in values):
        raise ValueError(f"{label} rows must be sequences")
    width = len(values[0])
    if width == 0 or any(len(row) != width for row in values):
        raise ValueError(f"{label} must be rectangular")
    result = []
    for row in values:
        converted = []
        for value in row:
            missing = value is None
            if not missing and nodata is not None:
                missing = value == nodata
            if not missing and isinstance(value, (int, float)) and not isinstance(value, bool):
                missing = not math.isfinite(value)
            if missing:
                converted.append(None)
            elif isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
                raise ValueError(f"{label} valid values must be finite and non-negative")
            else:
                converted.append(float(value))
        result.append(converted)
    return result

def brovey_pansharpen(multispectral, panchromatic, *, nodata=None):
    """Sharpen co-registered multispectral bands using one high-resolution PAN grid.

    For N bands, output_i = input_i * PAN * N / sum(input bands).
    If any input at a pixel is missing, or the multispectral sum is zero,
    every output band at that pixel is None.
    """
    if isinstance(multispectral, (str, bytes)) or not isinstance(multispectral, (list, tuple)) or len(multispectral) < 2:
        raise ValueError("at least two multispectral bands are required")
    bands = [_grid(band, f"band {i}", nodata) for i, band in enumerate(multispectral)]
    pan = _grid(panchromatic, "panchromatic", nodata)
    height, width = len(pan), len(pan[0])
    if any(len(band) != height or len(band[0]) != width for band in bands):
        raise ValueError("all bands and panchromatic grid must have identical dimensions")
    outputs = [[[None for _ in range(width)] for _ in range(height)] for _ in bands]
    valid_mask = [[False for _ in range(width)] for _ in range(height)]
    band_count = len(bands)
    for row in range(height):
        for col in range(width):
            values = [band[row][col] for band in bands]
            p = pan[row][col]
            if p is None or any(value is None for value in values):
                continue
            total = math.fsum(values)
            if total <= 0:
                continue
            factor = band_count * p / total
            for index, value in enumerate(values):
                outputs[index][row][col] = value * factor
            valid_mask[row][col] = True
    return {"bands": outputs, "valid_mask": valid_mask}
