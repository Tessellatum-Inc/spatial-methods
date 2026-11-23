"""Empirical satellite-derived bathymetry and SeaWiFS OC4v4 chlorophyll."""
from __future__ import annotations
import math
from collections.abc import Sequence

OC4V4_COEFFICIENTS = (0.366, -3.067, 1.930, 0.649, -1.532)

def _vector(values, label):
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence) or len(values) == 0:
        raise ValueError(f"{label} must be a non-empty sequence")
    result = []
    for value in values:
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            raise ValueError(f"{label} must contain finite numeric values")
        result.append(float(value))
    return result

def stumpf_log_ratio(blue_reflectance, green_reflectance, n=1000.0):
    """Compute ln(n*blue Rrs) / ln(n*green Rrs) for positive reflectances."""
    blue = _vector(blue_reflectance, "blue_reflectance")
    green = _vector(green_reflectance, "green_reflectance")
    if len(blue) != len(green):
        raise ValueError("blue and green reflectance arrays must have equal length")
    if isinstance(n, bool) or not isinstance(n, (int, float)) or not math.isfinite(n) or n <= 0:
        raise ValueError("n must be finite and positive")
    ratios = []
    for b, g in zip(blue, green):
        if b <= 0 or g <= 0:
            raise ValueError("reflectances must be strictly positive")
        denominator = math.log(n * g)
        if denominator == 0:
            raise ValueError("green reflectance makes the log-ratio denominator zero")
        ratios.append(math.log(n * b) / denominator)
    return ratios

def fit_stumpf_bathymetry(blue_reflectance, green_reflectance, known_depths, n=1000.0):
    """Fit depth = slope * Stumpf log-ratio + intercept by ordinary least squares."""
    depths = _vector(known_depths, "known_depths")
    ratios = stumpf_log_ratio(blue_reflectance, green_reflectance, n=n)
    if len(ratios) != len(depths) or len(ratios) < 2:
        raise ValueError("at least two paired calibration observations are required")
    xbar = math.fsum(ratios) / len(ratios)
    ybar = math.fsum(depths) / len(depths)
    sxx = math.fsum((x - xbar) ** 2 for x in ratios)
    if sxx <= 0:
        raise ValueError("calibration log-ratio must vary")
    slope = math.fsum((x - xbar) * (y - ybar) for x, y in zip(ratios, depths)) / sxx
    intercept = ybar - slope * xbar
    return {"slope": slope, "intercept": intercept, "n": float(n),
            "calibration_count": len(depths)}

def predict_stumpf_bathymetry(blue_reflectance, green_reflectance, model):
    """Predict depths using a fitted slope/intercept model."""
    if not isinstance(model, dict) or "slope" not in model or "intercept" not in model or "n" not in model:
        raise ValueError("model must contain slope, intercept and n")
    slope, intercept = model["slope"], model["intercept"]
    if any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) for v in (slope, intercept)):
        raise ValueError("model coefficients must be finite")
    ratios = stumpf_log_ratio(blue_reflectance, green_reflectance, n=model["n"])
    return [slope * ratio + intercept for ratio in ratios]

def oc4v4_chlorophyll(r443, r490, r510, r555, coefficients=OC4V4_COEFFICIENTS):
    """Return SeaWiFS OC4v4 chlorophyll-a concentration in mg m-3.

    Uses log10(max(Rrs443,Rrs490,Rrs510)/Rrs555) and the published
    fourth-order SeaWiFS OC4v4 polynomial. Coefficients may be replaced only
    when a separately documented sensor/version calibration is intended.
    """
    bands = [_vector(v, name) for v, name in
             ((r443, "r443"), (r490, "r490"), (r510, "r510"), (r555, "r555"))]
    if len({len(v) for v in bands}) != 1:
        raise ValueError("all reflectance bands must have equal length")
    coeff = _vector(coefficients, "coefficients")
    if len(coeff) != 5:
        raise ValueError("OC4v4 requires five polynomial coefficients")
    result = []
    for b443, b490, b510, green in zip(*bands):
        if min(b443, b490, b510, green) <= 0:
            raise ValueError("remote-sensing reflectances must be strictly positive")
        x = math.log10(max(b443, b490, b510) / green)
        polynomial = coeff[4]
        for coefficient in reversed(coeff[:4]):
            polynomial = polynomial * x + coefficient
        result.append(10.0 ** polynomial)
    return result
