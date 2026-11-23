import math
import pytest
from time_aligned_sensor_chain import time_aligned_sensor_chain_sounding_point_and_jacobian as solve
I=[[1,0,0],[0,1,0],[0,0,1]]
RZ=[[0,-1,0],[1,0,0],[0,0,1]]
def args(**kw):
 d=dict(ping_time=5.,time_offset_s=0.,navigation_time_0=0.,navigation_time_1=10.,
 gnss_position_0_navigation=[0,0,0],gnss_position_1_navigation=[10,0,0],
 imu_to_navigation_rotation_0=I,imu_to_navigation_rotation_1=I,
 imu_to_gnss_lever_arm_imu=[0,0,0],imu_to_transducer_lever_arm_imu=[0,0,0],
 imu_to_transducer_rotation=I,acoustic_vector_transducer=[0,0,-2])
 d.update(kw);return solve(**d)
def test_linear_position_and_time_sensitivity():
 o=args()
 assert o["evaluation_time"]==5
 assert o["interpolation_fraction"]==pytest.approx(.5)
 assert o["point_navigation"]==pytest.approx([5,0,-2])
 assert o["time_offset_sensitivity"]==pytest.approx([1,0,0])
def test_rotation_follows_shortest_so3_geodesic():
 o=args(imu_to_navigation_rotation_1=RZ,acoustic_vector_transducer=[1,0,0],
        gnss_position_0_navigation=[0,0,0],gnss_position_1_navigation=[0,0,0])
 assert o["point_navigation"]==pytest.approx([math.sqrt(.5),math.sqrt(.5),0])
def test_time_column_matches_finite_difference():
 base=args(time_offset_s=.2);eps=1e-5
 later=args(time_offset_s=.2+eps)["point_navigation"]
 numeric=[(later[i]-base["point_navigation"][i])/eps for i in range(3)]
 assert numeric==pytest.approx(base["time_offset_sensitivity"],abs=1e-7)
def test_combined_translation_and_rotation_time_derivative():
 kw=dict(imu_to_navigation_rotation_1=RZ,acoustic_vector_transducer=[1,0,0],
         gnss_position_0_navigation=[0,0,0],gnss_position_1_navigation=[10,0,0])
 base=args(time_offset_s=.2,**kw);eps=1e-6
 p=args(time_offset_s=.2+eps,**kw)["point_navigation"]
 numeric=[(p[i]-base["point_navigation"][i])/eps for i in range(3)]
 assert numeric==pytest.approx(base["time_offset_sensitivity"],abs=2e-6)
def test_rejects_extrapolation_and_bad_time_order():
 with pytest.raises(ValueError):args(time_offset_s=6)
 with pytest.raises(ValueError):args(navigation_time_0=10,navigation_time_1=0)
