"""Compositional closure and log-ratio geometry."""
import math

def _row(values):
    if isinstance(values, (str, bytes)) or len(values) < 2:
        raise ValueError("a composition must contain at least two parts")
    row = []
    for value in values:
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
            raise ValueError("composition parts must be finite and non-negative")
        row.append(float(value))
    if math.fsum(row) <= 0:
        raise ValueError("composition must have positive total")
    return row

def closure(values):
    row = _row(values)
    total = math.fsum(row)
    return [value / total for value in row]

def multiplicative_zero_replacement(values, delta):
    row = closure(values)
    if isinstance(delta, bool) or not isinstance(delta, (int, float)) or not math.isfinite(delta) or delta <= 0:
        raise ValueError("delta must be finite and positive")
    zeros = sum(value == 0 for value in row)
    if zeros == 0:
        return row
    if zeros * delta >= 1:
        raise ValueError("total replacement mass must be less than one")
    nonzero_total = math.fsum(value for value in row if value > 0)
    scale = (1.0 - zeros * delta) / nonzero_total
    return [delta if value == 0 else value * scale for value in row]

def clr_transform(values, *, zero_replacement=None):
    row = _row(values)
    if any(value == 0 for value in row):
        if zero_replacement is None:
            raise ValueError("zero parts require an explicit zero_replacement")
        row = multiplicative_zero_replacement(row, zero_replacement)
    else:
        row = closure(row)
    logs = [math.log(value) for value in row]
    mean_log = math.fsum(logs) / len(logs)
    return [value - mean_log for value in logs]

def aitchison_distance(left, right, *, zero_replacement=None):
    if len(left) != len(right):
        raise ValueError("compositions must have the same number of parts")
    x = clr_transform(left, zero_replacement=zero_replacement)
    y = clr_transform(right, zero_replacement=zero_replacement)
    return math.sqrt(math.fsum((a - b) ** 2 for a, b in zip(x, y)))
