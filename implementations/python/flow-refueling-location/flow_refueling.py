"""Exact small-instance flow-refueling location model."""
from __future__ import annotations
import math
from collections.abc import Mapping
from itertools import combinations

def _finite(value, label):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError("value must be finite numeric")
    return float(value)
