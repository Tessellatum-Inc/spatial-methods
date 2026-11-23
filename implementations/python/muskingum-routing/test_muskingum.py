import pytest
from muskingum import muskingum_coefficients, muskingum_route

def test_coefficients_are_nonnegative_and_sum_to_one():
    coeff = muskingum_coefficients(2, 4, 0.2)
    assert min(coeff.values()) >= 0
    assert sum(coeff.values()) == pytest.approx(1)

def test_constant_inflow_remains_constant_at_steady_state():
    result = muskingum_route([5, 5, 5, 5], 2, 4, 0.2)
    assert result["outflow"] == pytest.approx([5, 5, 5, 5])

def test_routing_recurrence_matches_independent_calculation():
    result = muskingum_route([0, 10, 10, 0], 2, 4, 0.2, initial_outflow=0)
    c = result["coefficients"]
    expected = [0]
    for i in range(1, 4):
        expected.append(c["c0"]*[0,10,10,0][i] + c["c1"]*[0,10,10,0][i-1] + c["c2"]*expected[-1])
    assert result["outflow"] == pytest.approx(expected)

def test_storage_uses_muskingum_storage_relation():
    inflow = [1, 3, 5]
    result = muskingum_route(inflow, 2, 4, 0.2)
    expected = [4*(0.2*i + 0.8*o) for i, o in zip(inflow, result["outflow"])]
    assert result["storage"] == pytest.approx(expected)

def test_initial_outflow_is_respected():
    result = muskingum_route([2, 2], 2, 4, 0.2, initial_outflow=1)
    assert result["outflow"][0] == 1

@pytest.mark.parametrize("dt,k,x", [(0,4,0.2), (2,0,0.2), (1,4,0.2), (9,4,0.2), (2,4,0.6)])
def test_unstable_or_invalid_parameters_are_rejected(dt,k,x):
    with pytest.raises(ValueError):
        muskingum_coefficients(dt,k,x)

@pytest.mark.parametrize("flow", [[], [-1,2], [1,float("nan")], [True,2], [1,float("inf")]])
def test_invalid_inflow_is_rejected(flow):
    with pytest.raises(ValueError):
        muskingum_route(flow, 2, 4, 0.2)

def test_invalid_initial_outflow_is_rejected():
    with pytest.raises(ValueError):
        muskingum_route([1,2], 2, 4, 0.2, initial_outflow=-1)
