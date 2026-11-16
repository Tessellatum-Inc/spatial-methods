"""Mann-Kendall trend test and Sen's median slope estimator."""
import math
from statistics import median

def _values(values, label):
    if isinstance(values, (str, bytes)) or not isinstance(values, (list, tuple)) or len(values) < 2:
        raise ValueError(f"{label} must contain at least two observations")
    result = []
    for value in values:
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            raise ValueError(f"{label} must contain finite numeric values")
        result.append(float(value))
    return result

def _times(times, count):
    if times is None:
        return [float(i) for i in range(count)]
    result = _values(times, "times")
    if len(result) != count:
        raise ValueError("times and values must have equal length")
    if any(b <= a for a,b in zip(result,result[1:])):
        raise ValueError("times must be strictly increasing")
    return result

def mann_kendall(values):
    """Return S, tie-corrected variance, continuity-corrected Z, p and tau-b.

    The two-sided p-value uses the normal approximation. Serial correlation
    and seasonal structure are not corrected.
    """
    y = _values(values, "values")
    n = len(y)
    score = 0
    for i in range(n-1):
        for j in range(i+1,n):
            score += (y[j] > y[i]) - (y[j] < y[i])
    tie_counts = {}
    for value in y:
        tie_counts[value] = tie_counts.get(value,0) + 1
    tie_term = sum(t*(t-1)*(2*t+5) for t in tie_counts.values() if t > 1)
    variance = (n*(n-1)*(2*n+5) - tie_term) / 18.0
    if variance <= 0:
        z = 0.0
        p_value = 1.0
    elif score > 0:
        z = (score-1.0) / math.sqrt(variance)
        p_value = math.erfc(abs(z)/math.sqrt(2.0))
    elif score < 0:
        z = (score+1.0) / math.sqrt(variance)
        p_value = math.erfc(abs(z)/math.sqrt(2.0))
    else:
        z = 0.0
        p_value = 1.0
    pairs = n*(n-1)/2.0
    tied_pairs = sum(t*(t-1)/2.0 for t in tie_counts.values())
    denominator = math.sqrt(pairs*(pairs-tied_pairs))
    tau = score/denominator if denominator else 0.0
    return {"s": score, "variance_s": variance, "z": z,
            "p_value_two_sided": p_value, "tau_b": tau}

def sen_slope(values, times=None):
    """Return Sen's median pairwise slope and median intercept."""
    y = _values(values, "values")
    x = _times(times, len(y))
    slopes = [(y[j]-y[i])/(x[j]-x[i])
              for i in range(len(y)-1) for j in range(i+1,len(y))]
    slope = median(slopes)
    intercept = median([value-slope*time for time,value in zip(x,y)])
    return {"slope": slope, "intercept": intercept, "pair_count": len(slopes)}
