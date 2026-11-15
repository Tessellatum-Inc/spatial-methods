import pytest
from mantel import mantel_test, partial_mantel_test
X=[[0,1,2,3],[1,0,1,2],[2,1,0,1],[3,2,1,0]]
Y=[[0,2,4,6],[2,0,2,4],[4,2,0,2],[6,4,2,0]]
Z=[[0,3,1,4],[3,0,2,1],[1,2,0,3],[4,1,3,0]]

def test_simple_perfect_and_reproducible():
    a=mantel_test(X,Y,permutations=99,seed=42)
    assert a==mantel_test(X,Y,permutations=99,seed=42)
    assert a["statistic"]==pytest.approx(1.0)
    assert 0<a["p_value"]<=1

def test_partial_statistic():
    r=partial_mantel_test(X,Y,Z,permutations=49,seed=7)
    assert -1<=r["statistic"]<=1 and 0<r["p_value"]<=1

@pytest.mark.parametrize("bad",[
 [[0,1],[1,0]], [[1,1,2],[1,0,1],[2,1,0]],
 [[0,1,2],[2,0,1],[2,1,0]], [[0,-1,2],[-1,0,1],[2,1,0]],
 [[0,1,float("nan")],[1,0,1],[float("nan"),1,0]]
])
def test_invalid_matrix(bad):
    with pytest.raises(ValueError): mantel_test(bad,bad)

def test_mismatched_dimensions():
    with pytest.raises(ValueError): mantel_test(X,[[0,1,2],[1,0,1],[2,1,0]])

@pytest.mark.parametrize("kwargs",[{"permutations":0},{"permutations":-1},{"alternative":"bad"}])
def test_invalid_options(kwargs):
    with pytest.raises(ValueError): mantel_test(X,Y,**kwargs)

def test_constant_upper_triangle_rejected():
    a=[[0,1,1],[1,0,1],[1,1,0]]
    with pytest.raises(ValueError): mantel_test(a,a)
