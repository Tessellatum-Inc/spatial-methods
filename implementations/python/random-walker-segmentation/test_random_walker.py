import numpy as np
import pytest

from random_walker import random_walker


def test_two_region_image_respects_seeds_and_propagates_labels():
    image = np.zeros((5, 7), dtype=float)
    image[:, 4:] = 10.0
    seeds = np.zeros((5, 7), dtype=int)
    seeds[2, 0] = 1
    seeds[2, 6] = 2
    result = random_walker(image, seeds, beta=2.0)
    assert np.all(result["labels"][:, :3] == 1)
    assert np.all(result["labels"][:, 4:] == 2)
    assert result["labels"][2, 0] == 1 and result["labels"][2, 6] == 2
    np.testing.assert_allclose(result["probabilities"].sum(axis=2), 1.0)


def test_beta_zero_gives_linear_harmonic_probabilities_on_a_line():
    image = np.zeros((1, 5), dtype=float)
    seeds = np.array([[1, 0, 0, 0, 2]])
    result = random_walker(image, seeds, beta=0)
    np.testing.assert_allclose(result["probabilities"][0, :, 0], [1, 0.75, 0.5, 0.25, 0], atol=1e-10)
    np.testing.assert_allclose(result["probabilities"][0, :, 1], [0, 0.25, 0.5, 0.75, 1], atol=1e-10)


def test_multichannel_feature_distance_and_class_label_order():
    image = np.zeros((3, 3, 2), dtype=float)
    seeds = np.zeros((3, 3), dtype=int)
    seeds[0, 0] = 7
    seeds[2, 2] = 3
    result = random_walker(image, seeds)
    np.testing.assert_array_equal(result["class_labels"], [3, 7])
    np.testing.assert_array_equal(result["labels"][seeds > 0], seeds[seeds > 0])


def test_all_seeded_image_returns_exact_one_hot_probabilities():
    image = np.zeros((2, 2))
    seeds = np.array([[1, 1], [2, 2]])
    result = random_walker(image, seeds)
    assert np.all(result["probabilities"].max(axis=2) == 1)


@pytest.mark.parametrize("image,seeds,beta", [
    (np.ones((2, 2)), np.zeros((2, 2), dtype=int), 1),
    (np.ones((2, 2)), np.ones((2, 2), dtype=int), 1),
    (np.ones((2, 2)), np.array([[1, 0], [0, -1]]), 1),
    (np.ones((2, 2)), np.array([[1, 0], [0, 2]]), -1),
    (np.array([[1, np.nan], [1, 1]]), np.array([[1, 0], [0, 2]]), 1),
])
def test_invalid_images_seeds_and_controls_are_rejected(image, seeds, beta):
    with pytest.raises(ValueError):
        random_walker(image, seeds, beta=beta)


def test_rejects_misaligned_seed_grid():
    with pytest.raises(ValueError):
        random_walker(np.ones((3, 3)), np.ones((2, 2), dtype=int))
