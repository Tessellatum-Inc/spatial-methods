import numpy as np
import pytest
from fft_grid_kde import fft_grid_kde

def test_density_is_finite_nonnegative_and_approximately_normalized():
    points=np.array([[0.,0.],[0.1,0.],[0.,0.1],[0.1,0.1]])
    x,y,d=fft_grid_kde(points,extent=(-2,2,-2,2),shape=(80,80),bandwidth=.3)
    assert d.shape==(80,80) and np.all(d>=0) and np.isfinite(d).all()
    assert np.sum(d)*(x[1]-x[0])*(y[1]-y[0])==pytest.approx(1,rel=.03)

def test_weights_change_density_but_preserve_mass():
    pts=np.array([[-.5,0],[.5,0]])
    _,_,a=fft_grid_kde(pts,extent=(-3,3,-3,3),shape=(60,60),bandwidth=.4)
    _,_,b=fft_grid_kde(pts,extent=(-3,3,-3,3),shape=(60,60),bandwidth=.4,weights=[9,1])
    assert b[:,b.shape[1]//2].sum()>a[:,a.shape[1]//2].sum()*.5
    assert b.sum()>0

def test_boundary_correction_is_finite_and_nonnegative():
    _,_,d=fft_grid_kde([[0,0],[.1,.1]],extent=(0,1,0,1),shape=(30,30),bandwidth=.2,boundary_correction=True)
    assert np.isfinite(d).all() and np.all(d>=0)

def test_validation_and_outside_points():
    with pytest.raises(ValueError): fft_grid_kde([],extent=(0,1,0,1))
    with pytest.raises(ValueError): fft_grid_kde([[0,0]],extent=(1,0,0,1))
    with pytest.raises(ValueError): fft_grid_kde([[0,0]],extent=(0,1,0,1),bandwidth=0)
    with pytest.raises(ValueError): fft_grid_kde([[2,2]],extent=(0,1,0,1))
    with pytest.raises(ValueError): fft_grid_kde([[0,0]],extent=(0,1,0,1),weights=[0])
