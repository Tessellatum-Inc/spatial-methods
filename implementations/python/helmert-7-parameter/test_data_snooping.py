import numpy as np
import pytest
from data_snooping import adjust_and_snoop

def test_clean_line():
    x=np.arange(6.0); A=np.column_stack([np.ones(6),x]); y=2+3*x
    r=adjust_and_snoop(A,y)
    np.testing.assert_allclose(r["estimate"],[2,3],atol=1e-12)
    np.testing.assert_allclose(r["residuals"],0,atol=1e-12)
    assert r["global_degrees_of_freedom"]==4
    np.testing.assert_allclose(r["redundancy_numbers"].sum(),4,atol=1e-10)

def test_gross_error_is_largest_w():
    x=np.arange(8.0); A=np.column_stack([np.ones(8),x]); y=4+1.5*x
    y[5]+=12
    r=adjust_and_snoop(A,y,critical_value=2.5)
    assert r["largest_absolute_w_index"]==5
    assert 5 in r["suspect_indices"]
    assert abs(r["standardized_residuals"][5])>np.max(np.abs(np.delete(r["standardized_residuals"],5)))

def test_correlated_covariance():
    x=np.arange(5.0); A=np.column_stack([np.ones(5),x]); Q=np.eye(5)*2
    Q[0,1]=Q[1,0]=.25; y=1+2*x+np.array([.1,-.1,.05,-.05,0])
    r=adjust_and_snoop(A,y,covariance=Q,sigma0=.5)
    assert np.all(np.isfinite(r["standardized_residuals"]))
    assert r["parameter_covariance"].shape==(2,2)

@pytest.mark.parametrize("A,y",[
    ([[1,0],[1,1]],[1,2]), ([[1,1],[1,1],[1,1]],[1,2,3]),
    ([[1,0],[1,1],[1,2]],[1,2]), ([[1],[1],[1]],[1,2,float("nan")]),
])
def test_invalid_models(A,y):
    with pytest.raises(ValueError): adjust_and_snoop(A,y)

def test_invalid_covariance_and_threshold():
    A=np.column_stack([np.ones(3),np.arange(3.)]); y=np.array([1.,2.,3.])
    with pytest.raises(ValueError): adjust_and_snoop(A,y,covariance=np.ones((3,3)))
    with pytest.raises(ValueError): adjust_and_snoop(A,y,sigma0=0)
    with pytest.raises(ValueError): adjust_and_snoop(A,y,critical_value=-1)

def test_zero_redundancy_observations_have_undefined_local_w_statistic():
    # The first two observations uniquely determine both parameters; the
    # third carries all residual redundancy. This is valid, not a bad model.
    A=np.array([[1.,0.],[0.,1.],[0.,0.]])
    y=np.array([2.,3.,.5])
    r=adjust_and_snoop(A,y)
    assert np.isnan(r["standardized_residuals"][0])
    assert np.isnan(r["standardized_residuals"][1])
    assert np.isfinite(r["standardized_residuals"][2])
    np.testing.assert_allclose(r["redundancy_numbers"],[0.,0.,1.])

def test_pope_tau_flags_the_injected_gross_error_with_unknown_variance_factor():
    from data_snooping import pope_tau_test
    x=np.arange(9.0); A=np.column_stack([np.ones(9),x])
    y=3.0+1.25*x+np.array([.01,-.02,.01,0.,-.01,.02,-.01,.01,-.01])
    y[6]+=8.0
    result=pope_tau_test(A,y,significance_level=.05)
    assert result["status"]=="outlier_flagged"
    assert result["largest_absolute_tau_index"]==6
    assert 6 in result["flagged_indices"]
    assert result["degrees_of_freedom"]==7
    assert 0 < result["critical_tau"] < 1


def test_pope_tau_critical_value_is_student_t_transform():
    from scipy.stats import t as student_t
    from data_snooping import pope_tau_test
    x=np.arange(7.0); A=np.column_stack([np.ones(7),x])
    y=2.0+0.5*x+np.array([.1,-.1,.05,-.05,.02,-.02,0.])
    result=pope_tau_test(A,y,significance_level=.05)
    dof=5; m=7
    tcrit=student_t.ppf(1-.05/(2*m),dof-1)
    expected=np.sqrt(dof)*tcrit/np.sqrt(dof-1+tcrit**2)
    assert result["critical_tau"]==pytest.approx(expected)


def test_pope_tau_handles_perfect_fit_and_rejects_insufficient_redundancy():
    from data_snooping import pope_tau_test
    x=np.arange(5.0); A=np.column_stack([np.ones(5),x])
    exact=pope_tau_test(A,1+2*x)
    assert exact["status"]=="zero_residual_variance"
    assert exact["flagged_indices"]==[]
    with pytest.raises(ValueError):
        pope_tau_test(np.column_stack([np.ones(3),np.arange(3.)]),[1.,2.,3.])


def test_pope_tau_rejects_invalid_significance_level():
    from data_snooping import pope_tau_test
    x=np.arange(5.0); A=np.column_stack([np.ones(5),x])
    with pytest.raises(ValueError):
        pope_tau_test(A,1+2*x+[.1,0.,-.1,.05,-.05],significance_level=0.)
