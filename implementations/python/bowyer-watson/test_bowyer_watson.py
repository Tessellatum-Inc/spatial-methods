import pytest
from bowyer_watson import triangulate, edges, _incircle


def test_three_sites_form_one_ccw_triangle():
    pts = [(0,0),(2,0),(0,2)]
    tris = triangulate(pts)
    assert len(tris) == 1
    a,b,c = (pts[i] for i in tris[0])
    assert (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]) > 0


def test_square_has_two_triangles_and_five_edges():
    tris = triangulate([(0,0),(1,0),(1,1),(0,1)])
    assert len(tris) == 2
    assert len(edges(tris)) == 5


def test_interior_point_is_used():
    pts = [(0,0),(4,0),(4,4),(0,4),(2,2)]
    tris = triangulate(pts)
    assert {v for t in tris for v in t} == set(range(len(pts)))


def test_empty_circumcircle_property_for_general_position_fixture():
    pts = [(0,0),(5,0),(4,4),(0,3),(1.2,1.1),(2.8,2.1),(3.4,.7)]
    for tri in triangulate(pts):
        a,b,c = (pts[i] for i in tri)
        d = 2*(a[0]*(b[1]-c[1])+b[0]*(c[1]-a[1])+c[0]*(a[1]-b[1]))
        ux = ((a[0]**2+a[1]**2)*(b[1]-c[1])+(b[0]**2+b[1]**2)*(c[1]-a[1])+(c[0]**2+c[1]**2)*(a[1]-b[1]))/d
        uy = ((a[0]**2+a[1]**2)*(c[0]-b[0])+(b[0]**2+b[1]**2)*(a[0]-c[0])+(c[0]**2+c[1]**2)*(b[0]-a[0]))/d
        r2 = (ux-a[0])**2+(uy-a[1])**2
        for i,p in enumerate(pts):
            if i not in tri:
                assert (ux-p[0])**2+(uy-p[1])**2 >= r2-1e-9


def test_seeded_random_cloud_has_planar_triangle_count():
    import random
    rng = random.Random(7)
    pts = [(rng.random(),rng.random()) for _ in range(30)]
    tris = triangulate(pts)
    hull = _hull_count(pts)
    assert len(tris) == 2*len(pts)-2-hull


def _hull_count(points):
    pts = sorted(points)
    def cross(o,a,b):
        return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    lo=[]
    for p in pts:
        while len(lo)>=2 and cross(lo[-2],lo[-1],p)<=0: lo.pop()
        lo.append(p)
    hi=[]
    for p in reversed(pts):
        while len(hi)>=2 and cross(hi[-2],hi[-1],p)<=0: hi.pop()
        hi.append(p)
    return len(lo[:-1]+hi[:-1])


@pytest.mark.parametrize("bad", [[(0,0),(1,1)],[(0,0),(1,1),(2,2)],
                                  [(0,0),(1,0),(0,1),(0,0)],
                                  [(0,0),(1,0),(0,float("nan"))],
                                  [(0,0,1),(1,0,1),(0,1,1)]])
def test_invalid_inputs_are_rejected(bad):
    with pytest.raises(ValueError):
        triangulate(bad)


def test_incircle_sign_for_ccw_triangle():
    assert _incircle((0,0),(2,0),(0,2),(.5,.5)) > 0
    assert _incircle((0,0),(2,0),(0,2),(3,3)) < 0


def test_triangulation_is_translation_invariant():
    points = [(0,0),(5,0),(4,4),(0,3),(1.2,1.1),(2.8,2.1),(3.4,.7)]
    shifted = [(x+1e9,y-1e9) for x,y in points]
    assert triangulate(points) == triangulate(shifted)


def test_small_coordinate_scale_is_not_swallowed_by_absolute_tolerance():
    points = [(0,0),(5e-8,0),(4e-8,4e-8),(0,3e-8),
              (1.2e-8,1.1e-8),(2.8e-8,2.1e-8),(3.4e-8,.7e-8)]
    assert len(triangulate(points)) == len(triangulate(
        [(x*1e8,y*1e8) for x,y in points]))
