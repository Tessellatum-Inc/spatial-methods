import numpy as np
import pytest
from hough_lines import hough_lines,hough_peaks

def test_vertical_line_peak():
    e=np.zeros((30,30),bool); e[:,12]=1
    acc,rhos,theta=hough_lines(e)
    peaks=hough_peaks(acc,rhos,theta,num_peaks=3,min_votes=20)
    assert peaks
    rho,ang,votes=peaks[0]
    assert abs(abs(rho)-12)<=1
    assert abs(ang)<.03  # theta is the normal angle; a vertical line has theta=0.
    assert votes>=29

def test_empty_edges():
    a,r,t=hough_lines(np.zeros((5,7)))
    assert a.sum()==0 and hough_peaks(a,r,t)==[]

def test_invalid():
    with pytest.raises(ValueError): hough_lines(np.ones((2,2)),rho_resolution=0)
