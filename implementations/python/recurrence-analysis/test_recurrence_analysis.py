import numpy as np
import pytest
from recurrence_analysis import (largest_lyapunov_rosenstein, recurrence_plot, recurrence_quantification)


def test_recurrence_plot_exact_small_example():
    r=recurrence_plot([0,0,1,1],threshold=0)
    expected=np.array([[1,1,0,0],[1,1,0,0],[0,0,1,1],[0,0,1,1]],dtype=bool)
    np.testing.assert_array_equal(r,expected)


def test_euclidean_embedding_and_threshold():
    r=recurrence_plot([0,1,2,3,4],threshold=1.01,dimension=2,delay=1,metric="euclidean")
    assert r.shape==(4,4)
    assert np.all(np.diag(r))
    assert np.array_equal(r,r.T)


def test_rqa_reference_properties_for_two_constant_regimes():
    result=recurrence_quantification([0,0,0,1,1,1],threshold=0,
                                     theiler=0,min_diagonal=2,min_vertical=2)
    assert 0<result["recurrence_rate"]<=1
    assert 0<=result["determinism"]<=1
    assert result["max_diagonal_length"]>=2
    assert result["max_vertical_length"]>=2
    assert result["divergence"]==pytest.approx(1/result["max_diagonal_length"])
    assert result["recurrence_matrix"].shape==(6,6)
    assert not np.diag(result["recurrence_matrix"]).any()


def test_theiler_window_removes_near_diagonal_pairs():
    result=recurrence_quantification(np.arange(8.),threshold=0,theiler=2)
    assert result["recurrence_pairs"]==0
    assert result["recurrence_rate"]==0
    assert result["determinism"]==0


def test_invalid_inputs():
    with pytest.raises(ValueError): recurrence_plot([1,2],threshold=-1)
    with pytest.raises(ValueError): recurrence_plot([1,2],threshold=1,metric="manhattan")
    with pytest.raises(ValueError): recurrence_plot([1,2],threshold=1,dimension=3)
    with pytest.raises(ValueError): recurrence_quantification([1,2,3],threshold=1,theiler=-1)
    with pytest.raises(ValueError): recurrence_quantification([1,2,3],threshold=1,min_diagonal=1)


def test_rosenstein_largest_lyapunov_on_logistic_map():
    x=np.empty(5000,dtype=float)
    x[0]=0.213
    for i in range(1,len(x)):
        x[i]=4*x[i-1]*(1-x[i-1])
    result=largest_lyapunov_rosenstein(x,dimension=3,delay=1,theiler=10,
                                       max_horizon=12,fit_range=(1,6))
    assert 0.35<result["exponent"]<1.1
    assert result["anchor_indices"].size>100
    assert result["pair_counts"][1:6].min()>0


def test_rosenstein_rejects_invalid_fit_and_short_series():
    with pytest.raises(ValueError): largest_lyapunov_rosenstein([1,2,3],max_horizon=20)
    with pytest.raises(ValueError): largest_lyapunov_rosenstein(np.arange(100.),fit_range=(4,4))
    with pytest.raises(ValueError): largest_lyapunov_rosenstein(np.arange(100.),sampling_interval=0)
