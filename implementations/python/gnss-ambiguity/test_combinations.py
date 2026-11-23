import pytest
from combinations import geometry_free, ionosphere_free, wide_lane

def test_geometry_free_is_frequency_independent_difference():
    assert geometry_free([20,21],[19,18])==[1,3]

def test_ionosphere_free_combination_cancels_first_order_term():
    f1,f2=1575.42e6,1227.60e6
    # Construct a common range plus dispersive terms proportional to 1/f^2.
    common=23_000_000.0; iono_constant=4.2e16
    a=[common+iono_constant/f1**2]
    b=[common+iono_constant/f2**2]
    result=ionosphere_free(a,b,f1,f2)
    assert result[0]==pytest.approx(common,abs=1e-7)

def test_wide_lane_is_difference_in_cycles():
    assert wide_lane([100.2,101.4],[98.1,99.0],10,8)==pytest.approx([2.1,2.4])

@pytest.mark.parametrize("args", [([1],[2],0,10),([1],[2],10,10),([1],[2],10,float("inf"))])
def test_ionosphere_free_rejects_invalid_frequencies(args):
    with pytest.raises(ValueError):
        ionosphere_free(*args)

def test_rejects_mismatched_or_nonfinite_observations():
    with pytest.raises(ValueError):
        geometry_free([1],[1,2])
    with pytest.raises(ValueError):
        wide_lane([1],[float("nan")],10,8)
