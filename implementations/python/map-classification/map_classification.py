"""Reference classification breaks for ordered numeric map values."""
from bisect import bisect_left
import math


def _validated(values, k):
    data = [float(x) for x in values]
    if not data or any(not math.isfinite(x) for x in data):
        raise ValueError("values must be a non-empty finite sequence")
    if not isinstance(k, int) or isinstance(k, bool) or k < 1:
        raise ValueError("k must be a positive integer")
    return sorted(data)


def equal_interval_breaks(values, k):
    """Return k+1 equally spaced inclusive class boundaries."""
    data = _validated(values, k)
    lo, hi = data[0], data[-1]
    return [lo + (hi-lo)*i/k for i in range(k+1)]


def quantile_breaks(values, k):
    """Return linearly interpolated empirical quantile boundaries."""
    data = _validated(values, k)
    n = len(data)
    result = []
    for i in range(k+1):
        pos = (n-1)*i/k
        low = int(math.floor(pos))
        high = int(math.ceil(pos))
        fraction = pos-low
        result.append(data[low]*(1-fraction)+data[high]*fraction)
    return result


def jenks_natural_breaks(values, k):
    """Exact Fisher-Jenks 1-D within-class SSE minimization, O(k*n²) time."""
    data = _validated(values, k)
    if k > len(set(data)):
        raise ValueError("Jenks class count cannot exceed the number of distinct values")
    n = len(data)
    lower = [[0]*(k+1) for _ in range(n+1)]
    variance = [[float("inf")]*(k+1) for _ in range(n+1)]
    for j in range(1, k+1):
        variance[0][j] = 0.0
    for end in range(1, n+1):
        s1 = s2 = weight = 0.0
        for width in range(1, end+1):
            start = end-width+1
            x = data[start-1]
            weight += 1
            s1 += x
            s2 += x*x
            within = s2-s1*s1/weight
            previous = start-1
            if previous:
                for classes in range(2, k+1):
                    candidate = within+variance[previous][classes-1]
                    if candidate < variance[end][classes]:
                        lower[end][classes] = start
                        variance[end][classes] = candidate
            else:
                lower[end][1] = 1
                variance[end][1] = within
        lower[end][1] = 1
    breaks = [0.0]*(k+1)
    breaks[0], breaks[k] = data[0], data[-1]
    classes, end = k, n
    while classes > 1:
        start = lower[end][classes]
        if start < 1:
            raise RuntimeError("failed to recover optimal class boundaries")
        breaks[classes-1] = data[start-2]
        end = start-1
        classes -= 1
    return breaks


def classify(values, breaks):
    """Assign values to classes; interior upper bounds belong to lower class."""
    if len(breaks) < 2 or any(not math.isfinite(float(x)) for x in breaks):
        raise ValueError("breaks must contain at least two finite boundaries")
    if any(breaks[i] > breaks[i+1] for i in range(len(breaks)-1)):
        raise ValueError("breaks must be non-decreasing")
    result = []
    for value in values:
        x = float(value)
        if not math.isfinite(x) or x < breaks[0] or x > breaks[-1]:
            raise ValueError("each value must be finite and within break range")
        result.append(bisect_left(breaks[1:], x))
    return result
