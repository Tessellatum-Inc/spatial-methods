import numpy as np
import pytest
from fractional_cover import FractionalCoverTree

def test_tree_learns_piecewise_fractional_cover_response():
    X = np.arange(40, dtype=float).reshape(-1, 1)
    y = np.where(X[:, 0] < 12, 0.1, np.where(X[:, 0] < 27, 0.55, 0.9))
    pred = FractionalCoverTree(max_depth=3, min_samples_leaf=3).fit(X, y).predict(X)
    assert np.mean((pred-y)**2) < 1e-12
    assert np.all((pred >= 0) & (pred <= 1))

def test_leaf_size_limits_overfitting_and_prediction_is_leaf_mean():
    X = np.arange(6, dtype=float).reshape(-1, 1)
    y = np.array([0., .2, .4, .6, .8, 1.])
    model = FractionalCoverTree(max_depth=5, min_samples_leaf=3).fit(X, y)
    assert model.predict([[0.]])[0] == pytest.approx(np.mean(y[:3]))
    assert model.predict([[5.]])[0] == pytest.approx(np.mean(y[3:]))

def test_constant_target_stays_single_leaf():
    X = np.arange(8, dtype=float).reshape(-1, 1)
    y = np.full(8, .37)
    assert np.allclose(FractionalCoverTree().fit(X, y).predict(X), .37)

def test_multifeature_split_uses_predictive_band():
    x = np.linspace(0, 1, 30)
    X = np.column_stack([np.ones_like(x), x])
    assert np.mean((FractionalCoverTree(max_depth=4, min_samples_leaf=2).fit(X, x).predict(X)-x)**2) < .01

@pytest.mark.parametrize("X,y", [
    (np.ones(4), np.ones(4)), (np.ones((4,2)), np.ones((4,1))),
    (np.ones((4,2)), np.ones(3)), (np.array([[1.],[np.nan]]), np.array([.1,.2])),
    (np.ones((2,1)), np.array([-.1,.2])), (np.ones((2,1)), np.array([.2,1.1])),
])
def test_invalid_training_inputs_raise(X, y):
    with pytest.raises(ValueError):
        FractionalCoverTree().fit(X, y)

def test_predict_requires_fit_and_matching_shape():
    model = FractionalCoverTree()
    with pytest.raises(RuntimeError): model.predict([[0]])
    model.fit([[0], [1]], [0., 1.])
    with pytest.raises(ValueError): model.predict([[0, 1]])
