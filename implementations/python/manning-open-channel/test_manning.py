import pytest
from manning import manning_discharge, manning_normal_depth

def test_rectangular_channel_discharge_matches_manning_equation():
    q = manning_discharge(1, 3, 0, 0.03, 0.001)
    area = 3
    radius = area / 5
    expected = (1/0.03) * area * radius**(2/3) * (0.001**0.5)
    assert q == pytest.approx(expected)

def test_trapezoidal_channel_area_and_wetted_perimeter_case():
    q = manning_discharge(2, 4, 1, 0.025, 0.002)
    area = 2*(4+2)
    perimeter = 4 + 4*(2**0.5)
    expected = (1/0.025)*area*(area/perimeter)**(2/3)*(0.002**0.5)
    assert q == pytest.approx(expected)

def test_normal_depth_inverts_discharge_for_rectangular_channel():
    expected_depth = 1.75
    q = manning_discharge(expected_depth, 5, 0, 0.03, 0.001)
    actual = manning_normal_depth(q, 5, 0, 0.03, 0.001)
    assert actual == pytest.approx(expected_depth, abs=1e-8)

def test_normal_depth_inverts_discharge_for_trapezoidal_channel():
    expected_depth = 2.3
    q = manning_discharge(expected_depth, 4, 1.5, 0.035, 0.004)
    actual = manning_normal_depth(q, 4, 1.5, 0.035, 0.004)
    assert actual == pytest.approx(expected_depth, abs=1e-8)

def test_zero_depth_and_zero_discharge():
    assert manning_discharge(0, 3, 0, 0.03, 0.001) == 0
    assert manning_normal_depth(0, 3, 0, 0.03, 0.001) == 0

def test_discharge_increases_with_depth():
    assert manning_discharge(2, 3, 0, 0.03, 0.001) > manning_discharge(1, 3, 0, 0.03, 0.001)

@pytest.mark.parametrize("args", [
    (-1, 3, 0, 0.03, 0.001),
    (1, 0, 0, 0.03, 0.001),
    (1, 3, -1, 0.03, 0.001),
    (1, 3, 0, 0, 0.001),
    (1, 3, 0, 0.03, -0.001),
])
def test_invalid_discharge_inputs_are_rejected(args):
    with pytest.raises(ValueError):
        manning_discharge(*args)

def test_invalid_normal_depth_controls_are_rejected():
    with pytest.raises(ValueError):
        manning_normal_depth(-1, 3, 0, 0.03, 0.001)
    with pytest.raises(ValueError):
        manning_normal_depth(1, 3, 0, 0.03, 0.001, tolerance=0)
    with pytest.raises(ValueError):
        manning_normal_depth(1, 3, 0, 0.03, 0.001, max_iterations=0)
