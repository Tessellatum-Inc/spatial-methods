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


def _rgb_to_hsi(red, green, blue):
    total = red + green + blue
    intensity = total / 3.0
    if total <= 0:
        return intensity, 0.0, 0.0
    minimum = min(red, green, blue)
    saturation = 1.0 - 3.0 * minimum / total
    denominator = math.sqrt((red-green)**2 + (red-blue)*(green-blue))
    if denominator <= 1e-15:
        hue = 0.0
    else:
        numerator = 0.5 * ((red-green) + (red-blue))
        angle = math.acos(max(-1.0, min(1.0, numerator / denominator)))
        hue = angle if blue <= green else 2.0 * math.pi - angle
    return intensity, saturation, hue

def _hsi_to_rgb(intensity, saturation, hue):
    sector = 2.0 * math.pi / 3.0
    hue = hue % (2.0 * math.pi)
    if hue < sector:
        blue = intensity * (1.0 - saturation)
        red = intensity * (1.0 + saturation * math.cos(hue) / math.cos(math.pi/3.0 - hue))
        green = 3.0 * intensity - red - blue
    elif hue < 2.0 * sector:
        h = hue - sector
        red = intensity * (1.0 - saturation)
        green = intensity * (1.0 + saturation * math.cos(h) / math.cos(math.pi/3.0 - h))
        blue = 3.0 * intensity - red - green
    else:
        h = hue - 2.0 * sector
        green = intensity * (1.0 - saturation)
        blue = intensity * (1.0 + saturation * math.cos(h) / math.cos(math.pi/3.0 - h))
        red = 3.0 * intensity - green - blue
    return red, green, blue

def ihs_pansharpen(red, green, blue, panchromatic, *, nodata=None):
    """Replace RGB HSI intensity with PAN and transform back to RGB.

    Inputs must be co-registered, same-sized, non-negative grids in a common
    radiometric scale. Missing/non-finite values mask the output pixel.
    """
    bands = [_grid(values, name, nodata) for values, name in
             ((red, "red"), (green, "green"), (blue, "blue"))]
    pan = _grid(panchromatic, "panchromatic", nodata)
    height, width = len(pan), len(pan[0])
    if any(len(band) != height or len(band[0]) != width for band in bands):
        raise ValueError("RGB bands and panchromatic grid must have identical dimensions")
    outputs = [[[None for _ in range(width)] for _ in range(height)] for _ in range(3)]
    valid_mask = [[False for _ in range(width)] for _ in range(height)]
    for row in range(height):
        for col in range(width):
            values = [band[row][col] for band in bands]
            intensity = pan[row][col]
            if intensity is None or any(value is None for value in values):
                continue
            _old_intensity, saturation, hue = _rgb_to_hsi(*values)
            sharpened = _hsi_to_rgb(intensity, saturation, hue)
            for index, value in enumerate(sharpened):
                outputs[index][row][col] = value
            valid_mask[row][col] = True
    return {"bands": outputs, "valid_mask": valid_mask}
