import math
import pytest
from lucas_kanade import lucas_kanade_dense

def gaussian_image(rows=25, cols=25, shift_x=0.0):
    return [[math.exp(-((j-shift_x-12)**2 + (i-12)**2)/30.0) for j in range(cols)] for i in range(rows)]

def test_dense_flow_recovers_small_horizontal_translation():
    first = gaussian_image()
    second = gaussian_image(shift_x=0.25)
    flow = lucas_kanade_dense(first, second, window_radius=3)
    values = [flow["u"][i][j] for i in range(8,17) for j in range(8,17) if flow["valid"][i][j]]
    assert len(values) > 20
    assert sum(values)/len(values) == pytest.approx(0.25, abs=0.12)

def test_identical_images_have_near_zero_flow():
    image = gaussian_image()
    flow = lucas_kanade_dense(image, image, window_radius=3)
    values = [flow["u"][i][j] for i in range(8,17) for j in range(8,17) if flow["valid"][i][j]]
    assert values
    assert max(abs(v) for v in values) < 1e-8

def test_flat_region_is_marked_invalid():
    flow = lucas_kanade_dense([[1]*7 for _ in range(7)], [[1]*7 for _ in range(7)])
    assert not any(value for row in flow["valid"] for value in row)

def test_rejects_mismatched_images_and_invalid_window():
    with pytest.raises(ValueError):
        lucas_kanade_dense([[1,2]], [[1]])
    with pytest.raises(ValueError):
        lucas_kanade_dense([[1,2],[3,4]], [[1,2],[3,4]], window_radius=0)
