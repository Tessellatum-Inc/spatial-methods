import math
import pytest
from stl import stl_decompose

def synthetic(n=120, period=12):
    return [0.04*t + 2.0*math.sin(2*math.pi*t/period) + 0.5*math.cos(4*math.pi*t/period) for t in range(n)]

def test_components_reconstruct_input():
    y = synthetic()
    result = stl_decompose(y, 12, seasonal_window=7, trend_window=21)
    rebuilt = [result["trend"][i] + result["seasonal"][i] + result["remainder"][i] for i in range(len(y))]
    assert rebuilt == pytest.approx(y)
    assert len(result["trend"]) == len(y)

def test_seasonal_component_is_centered_over_full_series():
    result = stl_decompose(synthetic(), 12, seasonal_window=7, trend_window=21)
    assert abs(sum(result["seasonal"]) / len(result["seasonal"])) < 0.1

def test_robust_mode_downweights_large_spike():
    y = synthetic(); y[61] += 35
    result = stl_decompose(y, 12, seasonal_window=7, trend_window=21, robust=True, outer_iterations=5)
    assert result["weights"][61] < 0.1
    assert all(0 <= w <= 1 for w in result["weights"])

@pytest.mark.parametrize("values,period", [([1], 2), ([1, 2, 3], 2), ([1, float("nan")] * 12, 2)])
def test_rejects_invalid_series(values, period):
    with pytest.raises(ValueError):
        stl_decompose(values, period)

def test_rejects_invalid_parameters():
    with pytest.raises(ValueError):
        stl_decompose(synthetic(), 12, seasonal_window=6)
    with pytest.raises(ValueError):
        stl_decompose(synthetic(), 1)
