import numpy as np
import pytest
from morphology import dilation, erosion, opening, closing, morphological_gradient

def test_dilation_and_erosion_cross():
    a=np.zeros((5,5),bool); a[2,2]=1
    s=np.array([[0,1,0],[1,1,1],[0,1,0]],bool)
    assert dilation(a,s).sum()==5
    assert erosion(dilation(a,s),s)[2,2]

def test_opening_removes_isolated_pixel_and_closing_fills_hole():
    a=np.zeros((7,7),bool); a[1:6,1:6]=1; a[3,3]=0; a[0,0]=1
    opened=opening(a)
    assert not opened[0,0]
    closed=closing(a)
    assert closed[3,3]

def test_gradient_and_validation():
    a=np.zeros((5,5),bool); a[2,2]=1
    assert morphological_gradient(a).sum()>0
    with pytest.raises(ValueError): dilation(a,np.zeros((3,3),bool))
