import numpy as np
import pytest
from vecchia import squared_exponential_covariance, vecchia_loglikelihood


def exact_loglik(y, covariance):
    sign, logdet = np.linalg.slogdet(covariance)
    assert sign > 0
    return -.5 * (len(y)*np.log(2*np.pi) + logdet + y @ np.linalg.solve(covariance, y))


def test_all_predecessors_reproduce_exact_gaussian_likelihood():
    x = np.linspace(0, 3, 12)[:, None]
    y = np.sin(x[:, 0]) + .1*np.cos(2*x[:, 0])
    K = squared_exponential_covariance(x, variance=1.3, length_scale=.8, nugget=.05)
    exact = exact_loglik(y, K)
    result = vecchia_loglikelihood(y, x, variance=1.3, length_scale=.8,
                                   nugget=.05, n_neighbors=len(y)-1, jitter=1e-12)
    assert result["loglikelihood"] == pytest.approx(exact, abs=1e-8)


def test_exact_likelihood_is_invariant_to_order():
    rng = np.random.default_rng(4)
    x = rng.uniform(size=(10, 2))
    y = rng.normal(size=10)
    order = rng.permutation(10)
    a = vecchia_loglikelihood(y, x, variance=1.0, length_scale=0.3, nugget=0.1,
                              n_neighbors=9, order=np.arange(10))
    b = vecchia_loglikelihood(y, x, variance=1.0, length_scale=0.3, nugget=0.1,
                              n_neighbors=9, order=order)
    assert a["loglikelihood"] == pytest.approx(b["loglikelihood"], abs=1e-8)


def test_sparse_neighbour_approximation_returns_finite_conditionals():
    x = np.linspace(0, 5, 30)[:, None]
    y = np.sin(x[:, 0])
    result = vecchia_loglikelihood(y, x, n_neighbors=4)
    assert np.isfinite(result["loglikelihood"])
    assert np.all(result["conditional_variances"] > 0)
    assert result["conditional_means"].shape == y.shape


@pytest.mark.parametrize("kwargs", [
    {"n_neighbors": 0}, {"variance": 0}, {"length_scale": -1},
    {"nugget": -1}, {"jitter": -1}, {"order": [0, 0, 1]},
])
def test_invalid_parameters_raise(kwargs):
    with pytest.raises(ValueError):
        vecchia_loglikelihood([0., 1., 2.], [[0.], [1.], [2.]], **kwargs)


def test_all_training_neighbours_match_exact_dense_gp_prediction():
    from vecchia import vecchia_predict
    rng=np.random.default_rng(29)
    x=rng.uniform(-1,1,size=(18,2)); y=np.sin(x[:,0])+0.3*x[:,1]
    xp=rng.uniform(-.8,.8,size=(5,2))
    variance,length_scale,nugget=1.4,.65,.07
    got=vecchia_predict(y,x,xp,variance=variance,length_scale=length_scale,
                        nugget=nugget,n_neighbors=len(y),jitter=0)
    k=squared_exponential_covariance(x,variance=variance,length_scale=length_scale,nugget=nugget)
    cross=variance*np.exp(-.5*np.sum((xp[:,None,:]-x[None,:,:])**2,axis=2)/length_scale**2)
    exact_mean=cross@np.linalg.solve(k,y)
    exact_var=variance+nugget-np.sum(cross*np.linalg.solve(k,cross.T).T,axis=1)
    np.testing.assert_allclose(got["predictive_mean"],exact_mean,atol=1e-9)
    np.testing.assert_allclose(got["predictive_variance"],exact_var,atol=1e-9)


def test_local_vecchia_prediction_uses_bounded_neighbour_sets():
    from vecchia import vecchia_predict
    x=np.linspace(0,5,40)[:,None];y=np.sin(x[:,0])
    result=vecchia_predict(y,x,[[.2],[2.3],[4.7]],n_neighbors=5)
    assert np.isfinite(result["predictive_mean"]).all()
    assert np.all(result["predictive_variance"]>0)
    assert all(len(ids)==5 for ids in result["neighbour_indices"])


@pytest.mark.parametrize("kwargs",[
    {"n_neighbors":0},{"variance":0},{"length_scale":-1},{"nugget":-1},
    {"jitter":-1},{"prediction_coordinates":[[float("nan")]]},
])
def test_vecchia_predict_rejects_invalid_inputs(kwargs):
    from vecchia import vecchia_predict
    prediction_coordinates = kwargs.pop("prediction_coordinates", [[.5]])
    with pytest.raises(ValueError):
        vecchia_predict([0.,1.,2.],[[0.],[1.],[2.]],prediction_coordinates,**kwargs)
