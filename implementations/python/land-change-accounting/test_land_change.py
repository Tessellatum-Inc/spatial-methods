import numpy as np
import pytest
from land_change import intensity_analysis,land_change_accounting,transition_matrix

def test_transition_matrix_counts():
    labels,m=transition_matrix(np.array([[1,1,2],[2,2,1]]),np.array([[1,2,2],[1,2,1]]),classes=[1,2])
    assert labels==[1,2];np.testing.assert_array_equal(m,[[2,1],[1,2]])
def test_gain_loss_net_swap_and_disagreement():
    a=np.array([[1,1,2,2]]);b=np.array([[1,2,1,1]]);r=land_change_accounting(a,b,classes=[1,2])
    np.testing.assert_allclose(r["from_area"],[2,2]);np.testing.assert_allclose(r["to_area"],[3,1])
    np.testing.assert_allclose(r["gains"],[2,1]);np.testing.assert_allclose(r["losses"],[1,2])
    np.testing.assert_allclose(r["net_change"],[1,-1]);np.testing.assert_allclose(r["swap"],[2,2])
    assert r["total_disagreement"]==pytest.approx(.75) and r["quantity_disagreement"]==pytest.approx(.25) and r["allocation_disagreement"]==pytest.approx(.5)
def test_mask_and_intensity():
    a=np.array([[1,1],[2,2]]);b=np.array([[1,2],[2,1]])
    assert int(transition_matrix(a,b,mask=np.array([[True,False],[True,True]]))[1].sum())==3
    r=intensity_analysis(np.array([[1,1,2,2]]),np.array([[1,2,1,1]]),years=2,classes=[1,2])
    assert r["interval_intensity"]==pytest.approx(.375)
    np.testing.assert_allclose(r["gain_intensity"],[.5,.25]);np.testing.assert_allclose(r["loss_intensity"],[.25,.5])
def test_numeric_nodata_is_excluded():
    a=np.array([[1.,np.nan,2.]]);b=np.array([[1.,1.,1.]])
    labels,m=transition_matrix(a,b,classes=[1.,2.])
    assert int(m.sum())==2
def test_validation():
    with pytest.raises(ValueError): transition_matrix([1,2],[1])
    with pytest.raises(ValueError): transition_matrix([1,2],[1,2],classes=[1])
    with pytest.raises(ValueError): intensity_analysis([1],[1],years=0)
