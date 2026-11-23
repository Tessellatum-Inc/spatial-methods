import math
import pytest
from sensor_chain_geometry import sensor_chain_sounding_point_and_jacobian
I=[[1,0,0],[0,1,0],[0,0,1]]
def exp(d):
 a=math.sqrt(sum(x*x for x in d))
 if a==0:return I
 x,y,z=[v/a for v in d];c=math.cos(a);s=math.sin(a);t=1-c
 return [[t*x*x+c,t*x*y-s*z,t*x*z+s*y],[t*x*y+s*z,t*y*y+c,t*y*z-s*x],[t*x*z-s*y,t*y*z+s*x,t*z*z+c]]
def mm(a,b):return [[sum(a[i][k]*b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
def calc(R=I,Q=I,a=(1,2,.5),b=(.2,-.1,1),s=(2,.5,-8)):
 return sensor_chain_sounding_point_and_jacobian([100,200,30],R,a,b,Q,s)
def test_identity_and_signs():
 o=calc();assert o["point_navigation"]==pytest.approx([101.2,198.4,22.5])
 assert [x[6:9] for x in o["jacobian"]]==[[-1,0,0],[0,-1,0],[0,0,-1]]
 assert [x[9:12] for x in o["jacobian"]]==I
 assert [x[15:18] for x in o["jacobian"]]==I
def test_composed_rotations():
 R=[[0,-1,0],[1,0,0],[0,0,1]];Q=[[1,0,0],[0,0,-1],[0,1,0]]
 assert calc(R,Q)["point_navigation"]==pytest.approx([94.1,201.2,31])
@pytest.mark.parametrize("block,axis",[(3,0),(6,0),(9,1),(12,2),(15,1)])
def test_jacobian_blocks_finite_difference(block,axis):
 R=[[0,-1,0],[1,0,0],[0,0,1]];Q=[[1,0,0],[0,0,-1],[0,1,0]]
 base=calc(R,Q); eps=1e-7
 vals={"R":R,"Q":Q,"a":[1,2,.5],"b":[.2,-.1,1],"s":[2,.5,-8]}
 key={3:"R",6:"a",9:"b",12:"Q",15:"s"}[block];v=vals[key]
 if key in ("R","Q"):
  d=[0.,0.,0.];d[axis]=eps; vals[key]=mm(exp(d),v)
 else: vals[key]=v[:];vals[key][axis]+=eps
 p=sensor_chain_sounding_point_and_jacobian([100,200,30],vals["R"],vals["a"],vals["b"],vals["Q"],vals["s"])["point_navigation"]
 numeric=[(p[i]-base["point_navigation"][i])/eps for i in range(3)]
 analytic=[base["jacobian"][i][block+axis] for i in range(3)]
 assert numeric==pytest.approx(analytic,abs=3e-6)
def test_reject_invalid_rotation_nonfinite_and_tolerance():
 bad=[[1,0,0],[0,1,0],[0,0,-1]]
 with pytest.raises(ValueError):calc(R=bad)
 with pytest.raises(ValueError):sensor_chain_sounding_point_and_jacobian([0,0,float("nan")],I,[0,0,0],[0,0,0],I,[0,0,1])
 with pytest.raises(ValueError):sensor_chain_sounding_point_and_jacobian([0,0,0],I,[0,0,0],[0,0,0],I,[0,0,1],0)
