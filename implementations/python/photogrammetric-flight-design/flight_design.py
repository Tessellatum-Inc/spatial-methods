"""Camera footprint, GSD and image-spacing calculations for survey planning."""
from __future__ import annotations
import math

def _positive(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be a finite positive number")
    return float(value)

def _overlap(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or not 0 <= value < 1:
        raise ValueError(f"{name} must be in [0, 1)")
    return float(value)

def ground_sample_distance(altitude, pixel_pitch, focal_length):
    """Return nadir GSD in the same length unit as pixel_pitch and altitude."""
    h = _positive(altitude, "altitude")
    p = _positive(pixel_pitch, "pixel_pitch")
    f = _positive(focal_length, "focal_length")
    return h * p / f

def ground_footprint(altitude, sensor_width, sensor_height, focal_length):
    """Return across-track and along-track nadir footprint dimensions."""
    h = _positive(altitude, "altitude")
    sw = _positive(sensor_width, "sensor_width")
    sh = _positive(sensor_height, "sensor_height")
    f = _positive(focal_length, "focal_length")
    return (h * sw / f, h * sh / f)

def image_spacing(altitude, sensor_width, sensor_height, focal_length, *, side_overlap, forward_overlap):
    """Return footprint and maximum image-center spacings for required overlaps."""
    width, height = ground_footprint(altitude, sensor_width, sensor_height, focal_length)
    side = _overlap(side_overlap, "side_overlap")
    forward = _overlap(forward_overlap, "forward_overlap")
    return {
        "footprint_width": width,
        "footprint_height": height,
        "line_spacing": width * (1.0 - side),
        "exposure_spacing": height * (1.0 - forward),
    }
