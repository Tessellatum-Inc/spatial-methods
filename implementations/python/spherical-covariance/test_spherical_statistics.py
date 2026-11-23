import numpy as np
import pytest

from spherical_statistics import (
    angular_distance, frechet_mean_sphere, spherical_kmeans,
    spherical_vmf_kde, von_mises_fisher_density, von_mises_fisher_mixture,
)


def unit(lon, lat=0.0):
    lon, lat = np.deg2rad(lon), np.deg2rad(lat)
    return np.array([np.cos(lat)*np.cos(lon), np.cos(lat)*np.sin(lon), np.sin(lat)])


def test_angular_distance_wraparound_and_antipodes():
    assert angular_distance(unit(359), unit(1)) == pytest.approx(np.deg2rad(2))
    assert angular_distance(unit(0), unit(180)) == pytest.approx(np.pi)


def test_frechet_mean_recovers_tight_cluster_and_reports_objective():
    points = np.array([unit(-2), unit(-1), unit(0), unit(1), unit(2)])
    result = frechet_mean_sphere(points)
    assert angular_distance(result["mean"], unit(0)) < 1e-8
    assert result["mean_squared_geodesic_distance"] == pytest.approx(
        np.mean(np.deg2rad([-2, -1, 0, 1, 2])**2), abs=1e-8
    )
    assert result["converged"]


def test_frechet_mean_is_rotation_equivariant():
    points = np.array([unit(-4, 10), unit(-2, 11), unit(1, 9), unit(3, 10)])
    result = frechet_mean_sphere(points)["mean"]
    angle = 0.7
    rotation = np.array([[np.cos(angle), -np.sin(angle), 0],
                         [np.sin(angle), np.cos(angle), 0],
                         [0, 0, 1]])
    rotated = frechet_mean_sphere(points @ rotation.T)["mean"]
    assert angular_distance(rotated, rotation @ result) < 1e-7


def test_frechet_mean_rejects_antipodal_cut_locus():
    with pytest.raises(ValueError, match="antipodal"):
        frechet_mean_sphere([unit(0), unit(180)])


def test_spherical_kmeans_separates_two_directional_clusters():
    points = np.array([unit(-4), unit(-3), unit(-2), unit(80), unit(81), unit(82)])
    result = spherical_kmeans(points, 2, seed=4)
    assert len(set(result["labels"][:3])) == 1
    assert len(set(result["labels"][3:])) == 1
    assert result["labels"][0] != result["labels"][3]
    assert result["objective"] < 0.01
    assert result["converged"]


def test_spherical_kmeans_is_deterministic_for_fixed_seed():
    points = np.array([unit(a, b) for a, b in [(-20, 0), (-18, 1), (30, 0), (32, -1)]])
    a = spherical_kmeans(points, 2, seed=12)
    b = spherical_kmeans(points, 2, seed=12)
    np.testing.assert_array_equal(a["labels"], b["labels"])
    np.testing.assert_allclose(a["centers"], b["centers"])


def test_vmf_density_is_normalized_and_uniform_at_zero_concentration():
    lon = np.linspace(-np.pi, np.pi, 500)
    lat = np.linspace(-np.pi/2, np.pi/2, 250)
    llon, llat = np.meshgrid(lon, lat)
    points = np.column_stack((np.cos(llat).ravel()*np.cos(llon).ravel(),
                              np.cos(llat).ravel()*np.sin(llon).ravel(),
                              np.sin(llat).ravel()))
    density = von_mises_fisher_density(points, unit(0), 0)
    assert density == pytest.approx(np.full(len(points), 1/(4*np.pi)))
    concentrated = von_mises_fisher_density(points, unit(0), 3)
    integral = np.sum(concentrated.reshape(len(lat), len(lon)) *
                      np.cos(llat) * (lon[1]-lon[0]) * (lat[1]-lat[0]))
    assert integral == pytest.approx(1.0, abs=0.01)


def test_vmf_large_concentration_does_not_overflow():
    value = von_mises_fisher_density([unit(0), unit(90)], unit(0), 1000)
    assert np.isfinite(value).all()
    assert value[0] > value[1]


def test_spherical_vmf_kde_is_normalized_weighted_mixture():
    samples = np.array([unit(-10), unit(10)])
    values = spherical_vmf_kde([unit(0), unit(90)], samples,
                               concentration=4, weights=[1, 3])
    expected = (von_mises_fisher_density([unit(0), unit(90)], samples[0], 4) +
                3*von_mises_fisher_density([unit(0), unit(90)], samples[1], 4))/4
    np.testing.assert_allclose(values, expected)


@pytest.mark.parametrize("bad", [[], [[0, 0, 0]], [[1, 0]], [[1, np.nan, 0]]])
def test_spherical_vector_validation(bad):
    with pytest.raises(ValueError):
        frechet_mean_sphere(bad)


def test_spherical_kmeans_and_density_validate_parameters():
    with pytest.raises(ValueError, match="n_clusters"):
        spherical_kmeans([unit(0), unit(1)], 3)
    with pytest.raises(ValueError, match="concentration"):
        von_mises_fisher_density([unit(0)], unit(0), -1)
    with pytest.raises(ValueError, match="weights"):
        spherical_vmf_kde([unit(0)], [unit(0)], concentration=2, weights=[0])


def test_vmf_mixture_recovers_separated_directional_modes():
    rng = np.random.default_rng(23)
    east = np.array([unit(a) for a in rng.normal(-25, 3, 80)])
    west = np.array([unit(a) for a in rng.normal(55, 4, 90)])
    points = np.vstack((east, west))
    result = von_mises_fisher_mixture(points, 2, seed=8, max_iterations=200)
    assert result["responsibilities"].shape == (170, 2)
    assert result["weights"].sum() == pytest.approx(1.0)
    assert np.all(result["concentrations"] >= 0)
    assert result["log_likelihood"] > -500
    labels = result["labels"]
    assert max(np.mean(labels[:80] == labels[0]),
               np.mean(labels[:80] != labels[0])) > 0.9
    assert max(np.mean(labels[80:] == labels[80]),
               np.mean(labels[80:] != labels[80])) > 0.9


def test_vmf_mixture_rejects_invalid_component_count():
    with pytest.raises(ValueError, match="n_components"):
        von_mises_fisher_mixture([unit(0), unit(1)], 3)
