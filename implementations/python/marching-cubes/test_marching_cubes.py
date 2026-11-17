import numpy as np
import pytest
from marching_cubes import extract_isosurface


def test_extracts_closed_sphere_surface_with_expected_radius():
    axis = np.linspace(-1.2, 1.2, 31)
    x, y, z = np.meshgrid(axis, axis, axis, indexing="ij")
    volume = 0.75**2 - (x*x + y*y + z*z)
    mesh = extract_isosurface(volume, 0, spacing=(axis[1]-axis[0],)*3,
                              origin=(axis[0],)*3)
    vertices, faces = mesh["vertices"], mesh["faces"]
    assert vertices.shape[1] == 3 and faces.shape[1] == 3
    assert len(vertices) > 100 and len(faces) > 100
    radius = np.linalg.norm(vertices, axis=1)
    assert np.mean(np.abs(radius-.75)) < .01
    assert np.all(np.isfinite(mesh["normals"]))


def test_anisotropic_spacing_and_origin_are_applied():
    volume = np.zeros((5, 5, 5))
    volume[2:, :, :] = 1
    mesh = extract_isosurface(volume, .5, spacing=(2, 3, 4), origin=(10, 20, 30))
    assert np.allclose(mesh["vertices"][:, 0], 14)
    assert np.all(mesh["vertices"][:, 1] >= 20)
    assert np.all(mesh["vertices"][:, 2] >= 30)


@pytest.mark.parametrize("volume,level", [
    (np.ones((3, 3, 3)), .5),
    (np.zeros((3, 3)), 0),
    (np.full((3, 3, 3), np.nan), 0),
])
def test_invalid_volume_or_level_raises(volume, level):
    with pytest.raises(ValueError):
        extract_isosurface(volume, level)


def test_invalid_geometry_controls_raise():
    volume = np.indices((3, 3, 3))[0].astype(float)
    with pytest.raises(ValueError):
        extract_isosurface(volume, 1, spacing=(1, 0, 1))
    with pytest.raises(ValueError):
        extract_isosurface(volume, 1, step_size=0)
