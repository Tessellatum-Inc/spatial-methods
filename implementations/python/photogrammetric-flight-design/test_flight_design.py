import pytest
from flight_design import ground_sample_distance, ground_footprint, image_spacing

def test_ground_sample_distance_uses_nadir_scale():
    assert ground_sample_distance(120, 0.004, 0.035) == pytest.approx(13.7142857143)

def test_ground_footprint_scales_sensor_dimensions_by_height_over_focal_length():
    assert ground_footprint(100, 0.036, 0.024, 0.050) == pytest.approx((72.0, 48.0))

def test_image_spacing_respects_side_and_forward_overlap():
    result = image_spacing(100, 0.036, 0.024, 0.050, side_overlap=0.7, forward_overlap=0.8)
    assert result == pytest.approx({"footprint_width": 72.0, "footprint_height": 48.0, "line_spacing": 21.6, "exposure_spacing": 9.6})

@pytest.mark.parametrize("args", [(0, 0.004, 0.035), (100, 0, 0.035), (100, 0.004, 0), (float("nan"), 0.004, 0.035)])
def test_gsd_rejects_invalid_dimensions(args):
    with pytest.raises(ValueError):
        ground_sample_distance(*args)

@pytest.mark.parametrize("overlap", [-0.1, 1.0, float("nan"), True])
def test_image_spacing_rejects_invalid_overlap(overlap):
    with pytest.raises(ValueError):
        image_spacing(100, 0.036, 0.024, 0.050, side_overlap=overlap, forward_overlap=0.7)
