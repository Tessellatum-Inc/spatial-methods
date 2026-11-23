import math
import pytest
from sounding_geometry_uncertainty import sounding_point_and_jacobian


I = [[1,0,0],[0,1,0],[0,0,1]]


def test_identity_geometry_and_jacobian_blocks():
    out = sounding_point_and_jacobian([10,20,30], I, [1,2,3], [4,5,6])
    assert out["point_navigation"] == pytest.approx([15,27,39])
    j = out["jacobian"]
    assert [row[:3] for row in j] == [[1,0,0],[0,1,0],[0,0,1]]
    assert [row[6:9] for row in j] == I
    assert [row[9:12] for row in j] == I
    # -[v]x, where v=(5,7,9)
    assert [row[3:6] for row in j] == [[0,9,-7],[-9,0,5],[7,-5,0]]


def test_rotation_matrix_maps_body_vector_to_navigation():
    r = [[0,-1,0],[1,0,0],[0,0,1]]
    out = sounding_point_and_jacobian([0,0,0], r, [1,0,0], [0,2,0])
    assert out["point_navigation"] == pytest.approx([-2,1,0])
    assert [row[6:9] for row in out["jacobian"]] == r


def _exp_rotation(delta):
    angle = math.sqrt(sum(x*x for x in delta))
    if angle == 0:
        return I
    x,y,z = [v/angle for v in delta]
    c,s,t = math.cos(angle),math.sin(angle),1-math.cos(angle)
    return [
        [t*x*x+c, t*x*y-s*z, t*x*z+s*y],
        [t*x*y+s*z, t*y*y+c, t*y*z-s*x],
        [t*x*z-s*y, t*y*z+s*x, t*z*z+c],
    ]


def test_attitude_jacobian_matches_left_perturbation_finite_difference():
    r = [[0,-1,0],[1,0,0],[0,0,1]]
    nav, lever, acoustic = [3,4,5], [0.4,-0.2,1.1], [2.0,0.5,-8.0]
    base = sounding_point_and_jacobian(nav, r, lever, acoustic)
    eps = 1e-7
    for axis in range(3):
        d = [0.0,0.0,0.0]
        d[axis] = eps
        perturbed_rotation = _exp_rotation(d)
        rotated = [[sum(perturbed_rotation[i][k]*r[k][j] for k in range(3))
                    for j in range(3)] for i in range(3)]
        p = sounding_point_and_jacobian(nav, rotated, lever, acoustic)["point_navigation"]
        numerical = [(p[i]-base["point_navigation"][i])/eps for i in range(3)]
        analytic = [base["jacobian"][i][3+axis] for i in range(3)]
        assert numerical == pytest.approx(analytic, abs=2e-6)


@pytest.mark.parametrize("rotation", [
    [[1,0,0],[0,1,0],[0,0,-1]],  # reflection
    [[1,0.1,0],[0,1,0],[0,0,1]], # non-orthogonal
    [[1,0],[0,1]],               # wrong shape
])
def test_rejects_invalid_rotation(rotation):
    with pytest.raises(ValueError):
        sounding_point_and_jacobian([0,0,0], rotation, [0,0,0], [0,0,1])


def test_rejects_invalid_vectors_and_tolerance():
    with pytest.raises(ValueError):
        sounding_point_and_jacobian([0,0], I, [0,0,0], [0,0,1])
    with pytest.raises(ValueError):
        sounding_point_and_jacobian([0,0,0], I, [0,0,0], [0,0,float("nan")])
    with pytest.raises(ValueError):
        sounding_point_and_jacobian([0,0,0], I, [0,0,0], [0,0,1], 0)
