import pytest
from slic import slic_superpixels

def test_two_colour_regions_receive_distinct_superpixel_labels():
    image = [[[0.0] if col < 4 else [100.0] for col in range(8)] for row in range(8)]
    result = slic_superpixels(image, region_size=4, compactness=1, max_iterations=10)
    labels = result["labels"]
    assert labels[3][1] != labels[3][6]
    assert all(0 <= value < len(result["centres"]) for row in labels for value in row)

def test_output_dimensions_match_input_and_centres_are_finite():
    image = [[[float(row), float(col), 0.5] for col in range(7)] for row in range(5)]
    result = slic_superpixels(image, region_size=3)
    assert len(result["labels"]) == 5
    assert all(len(row) == 7 for row in result["labels"])
    assert all(all(value == value for value in centre) for centre in result["centres"])

def test_result_is_deterministic():
    image = [[[float((row+col)%3), float(col)] for col in range(9)] for row in range(7)]
    a = slic_superpixels(image, region_size=3, compactness=5)
    b = slic_superpixels(image, region_size=3, compactness=5)
    assert a == b

def test_region_size_larger_than_image_creates_one_cluster():
    result = slic_superpixels([[[1.0],[2.0]],[[3.0],[4.0]]], region_size=10)
    assert len(result["centres"]) == 1
    assert set(value for row in result["labels"] for value in row) == {0}

@pytest.mark.parametrize("kwargs", [
    {"region_size": 0}, {"compactness": 0}, {"max_iterations": 0}, {"tolerance": -1}
])
def test_invalid_parameters_are_rejected(kwargs):
    with pytest.raises(ValueError):
        slic_superpixels([[[1.0],[2.0]],[[3.0],[4.0]]], **kwargs)

@pytest.mark.parametrize("image", [
    [], [[[]]], [[[1.0],[2.0,3.0]]], [[[float("nan")]]], [[[True]]], [[[1.0]],[[2.0],[3.0]]]
])
def test_invalid_feature_images_are_rejected(image):
    with pytest.raises(ValueError):
        slic_superpixels(image)
