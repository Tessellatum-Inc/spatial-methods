"""Muskingum hydrologic channel routing."""
import math

def muskingum_coefficients(time_step, storage_time, weighting_factor):
    """Return stable Muskingum C0, C1, C2 coefficients."""
    for name, value in (("time_step", time_step), ("storage_time", storage_time)):
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0:
            raise ValueError(f"{name} must be finite and positive")
    if isinstance(weighting_factor, bool) or not isinstance(weighting_factor, (int, float)) or not math.isfinite(weighting_factor) or not 0 <= weighting_factor <= 0.5:
        raise ValueError("weighting_factor must be finite and in [0, 0.5]")
    dt, k, x = float(time_step), float(storage_time), float(weighting_factor)
    if dt < 2*k*x or dt > 2*k*(1-x):
        raise ValueError("time_step violates non-negative Muskingum coefficient stability bounds")
    denominator = k*(1-x) + dt/2
    c0 = (dt/2 - k*x) / denominator
    c1 = (dt/2 + k*x) / denominator
    c2 = (k*(1-x) - dt/2) / denominator
    return {"c0": c0, "c1": c1, "c2": c2}

def muskingum_route(inflow, time_step, storage_time, weighting_factor,
                    initial_outflow=None):
    """Route an equally spaced non-negative inflow hydrograph.

    The first output is the supplied initial_outflow (or inflow[0] when
    omitted). Subsequent values use O[t] = C0 I[t] + C1 I[t-1] + C2 O[t-1].
    Storage is reported as K * (X I + (1-X) O).
    """
    if isinstance(inflow, (str, bytes)) or not isinstance(inflow, (list, tuple)) or not inflow:
        raise ValueError("inflow must be a non-empty sequence")
    values = []
    for value in inflow:
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
            raise ValueError("inflow values must be finite and non-negative")
        values.append(float(value))
    coefficients = muskingum_coefficients(time_step, storage_time, weighting_factor)
    if initial_outflow is None:
        initial = values[0]
    elif isinstance(initial_outflow, bool) or not isinstance(initial_outflow, (int, float)) or not math.isfinite(initial_outflow) or initial_outflow < 0:
        raise ValueError("initial_outflow must be finite and non-negative")
    else:
        initial = float(initial_outflow)
    outflow = [initial]
    c0, c1, c2 = coefficients["c0"], coefficients["c1"], coefficients["c2"]
    for index in range(1, len(values)):
        outflow.append(c0*values[index] + c1*values[index-1] + c2*outflow[-1])
    k, x = float(storage_time), float(weighting_factor)
    storage = [k*(x*i + (1-x)*o) for i, o in zip(values, outflow)]
    return {"outflow": outflow, "storage": storage, "coefficients": coefficients}
