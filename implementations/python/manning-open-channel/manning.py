"""Manning uniform open-channel flow and normal-depth inversion."""
import math

def _parameters(bottom_width, side_slope, roughness, energy_slope):
    for name, value in (("bottom_width", bottom_width), ("roughness", roughness), ("energy_slope", energy_slope)):
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0:
            raise ValueError(f"{name} must be finite and positive")
    if isinstance(side_slope, bool) or not isinstance(side_slope, (int, float)) or not math.isfinite(side_slope) or side_slope < 0:
        raise ValueError("side_slope must be finite and non-negative")
    return float(bottom_width), float(side_slope), float(roughness), float(energy_slope)

def manning_discharge(depth, bottom_width, side_slope, roughness, energy_slope):
    """Compute steady uniform-flow discharge for a trapezoidal channel.

    side_slope is horizontal:vertical (z:1). Uses SI-compatible Manning
    units when geometry is metres, slope is dimensionless and n is SI.
    """
    b, z, n, slope = _parameters(bottom_width, side_slope, roughness, energy_slope)
    if isinstance(depth, bool) or not isinstance(depth, (int, float)) or not math.isfinite(depth) or depth < 0:
        raise ValueError("depth must be finite and non-negative")
    y = float(depth)
    if y == 0:
        return 0.0
    area = y * (b + z*y)
    perimeter = b + 2*y*math.hypot(1.0, z)
    hydraulic_radius = area / perimeter
    return (1.0/n) * area * hydraulic_radius**(2.0/3.0) * math.sqrt(slope)

def manning_normal_depth(discharge, bottom_width, side_slope, roughness,
                         energy_slope, *, tolerance=1e-9, max_iterations=200):
    """Invert Manning's equation for normal depth using bracketed bisection."""
    b, z, n, slope = _parameters(bottom_width, side_slope, roughness, energy_slope)
    if isinstance(discharge, bool) or not isinstance(discharge, (int, float)) or not math.isfinite(discharge) or discharge < 0:
        raise ValueError("discharge must be finite and non-negative")
    if isinstance(tolerance, bool) or not isinstance(tolerance, (int, float)) or not math.isfinite(tolerance) or tolerance <= 0:
        raise ValueError("tolerance must be finite and positive")
    if isinstance(max_iterations, bool) or not isinstance(max_iterations, int) or max_iterations < 1:
        raise ValueError("max_iterations must be a positive integer")
    target = float(discharge)
    if target == 0:
        return 0.0
    low, high = 0.0, max(1.0, b)
    for _ in range(100):
        if manning_discharge(high, b, z, n, slope) >= target:
            break
        high *= 2
    else:
        raise ValueError("could not bracket normal depth")
    for _ in range(max_iterations):
        middle = (low + high) / 2
        value = manning_discharge(middle, b, z, n, slope)
        if value < target:
            low = middle
        else:
            high = middle
        if high - low <= tolerance:
            return (low + high) / 2
    return (low + high) / 2
