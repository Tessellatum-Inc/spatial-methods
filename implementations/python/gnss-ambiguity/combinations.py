"""Dual-frequency GNSS linear combinations of observables in metres."""
from __future__ import annotations
from math import isfinite

def _check(f1,f2):
    f1=float(f1);f2=float(f2)
    if not isfinite(f1) or not isfinite(f2) or f1<=0 or f2<=0 or f1==f2:
        raise ValueError("frequencies must be finite, positive and distinct")
    return f1,f2

def geometry_free(first, second):
    """Return L1-L2 (or P1-P2) in metres; inputs must share units."""
    a=[float(v) for v in first];b=[float(v) for v in second]
    if len(a)!=len(b) or not a:
        raise ValueError("observable sequences must have equal non-zero length")
    if any(not isfinite(v) for v in a+b):
        raise ValueError("observables must be finite")
    return [x-y for x,y in zip(a,b)]

def ionosphere_free(first, second, frequency_1, frequency_2):
    """First-order ionosphere-free combination of two range observables (metres)."""
    f1,f2=_check(frequency_1,frequency_2)
    a=[float(v) for v in first];b=[float(v) for v in second]
    if len(a)!=len(b) or not a:
        raise ValueError("observable sequences must have equal non-zero length")
    if any(not isfinite(v) for v in a+b):
        raise ValueError("observables must be finite")
    f1sq,f2sq=f1*f1,f2*f2
    denominator=f1sq-f2sq
    return [(f1sq*x-f2sq*y)/denominator for x,y in zip(a,b)]

def wide_lane(first_cycles, second_cycles, frequency_1, frequency_2):
    """Wide-lane phase combination N_W=L1-L2 in cycles (not range metres)."""
    f1,f2=_check(frequency_1,frequency_2)
    a=[float(v) for v in first_cycles];b=[float(v) for v in second_cycles]
    if len(a)!=len(b) or not a:
        raise ValueError("phase sequences must have equal non-zero length")
    if any(not isfinite(v) for v in a+b):
        raise ValueError("phase cycles must be finite")
    return [x-y for x,y in zip(a,b)]

def melbourne_wubbena(first_phase_cycles, second_phase_cycles,
                      first_code_metres, second_code_metres,
                      frequency_1, frequency_2, speed_of_light=299792458.0):
    """Return Melbourne-Wubbena wide-lane observable in wide-lane cycles.

    Carrier phases are in cycles; code pseudoranges are in metres. The
    combination is (L1-L2) - ((f1-f2)/c) * (f1*P1+f2*P2)/(f1+f2).
    Receiver/satellite hardware biases remain; code noise and multipath can
    be substantial. This is an observable, not an ambiguity-fixed solution.
    """
    f1, f2 = _check(frequency_1, frequency_2)
    c = float(speed_of_light)
    if not isfinite(c) or c <= 0:
        raise ValueError("speed_of_light must be finite and positive")
    l1 = [float(v) for v in first_phase_cycles]
    l2 = [float(v) for v in second_phase_cycles]
    p1 = [float(v) for v in first_code_metres]
    p2 = [float(v) for v in second_code_metres]
    if not l1 or not (len(l1) == len(l2) == len(p1) == len(p2)):
        raise ValueError("all observable sequences must have equal non-zero length")
    if any(not isfinite(v) for v in l1 + l2 + p1 + p2):
        raise ValueError("observables must be finite")
    code_narrow_lane = [(f1*a + f2*b)/(f1+f2) for a,b in zip(p1,p2)]
    return [(a-b) - ((f1-f2)/c)*pn
            for a,b,pn in zip(l1,l2,code_narrow_lane)]
