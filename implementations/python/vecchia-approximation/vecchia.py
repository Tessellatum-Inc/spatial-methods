"""Vecchia nearest-neighbour approximation to a zero-mean Gaussian process."""
from __future__ import annotations
import numpy as np


def squared_exponential_covariance(coordinates, *, variance=1.0, length_scale=1.0, nugget=0.0):
    """Build an isotropic squared-exponential covariance matrix."""
    x = np.asarray(coordinates, dtype=float)
    if x.ndim != 2 or x.shape[0] == 0 or x.shape[1] == 0 or not np.all(np.isfinite(x)):
        raise ValueError("coordinates must be a nonempty finite 2-D array")
    if not np.isfinite(variance) or variance <= 0:
        raise ValueError("variance must be finite and positive")
    if not np.isfinite(length_scale) or length_scale <= 0:
        raise ValueError("length_scale must be finite and positive")
    if not np.isfinite(nugget) or nugget < 0:
        raise ValueError("nugget must be finite and nonnegative")
    delta = x[:, None, :] - x[None, :, :]
    d2 = np.sum(delta * delta, axis=-1)
    covariance = variance * np.exp(-0.5 * d2 / (length_scale * length_scale))
    covariance.flat[::len(x) + 1] += nugget
    return covariance


def vecchia_loglikelihood(observations, coordinates, *, variance=1.0,
                          length_scale=1.0, nugget=0.0, n_neighbors=10,
                          order=None, jitter=1e-10):
    """Evaluate Vecchia's product of local Gaussian conditionals.

    At each ordered site, condition on its n_neighbors nearest predecessors.
    With all predecessors selected, the factorisation is the exact Gaussian
    likelihood (up to numerical jitter).
    """
    y = np.asarray(observations, dtype=float)
    x = np.asarray(coordinates, dtype=float)
    if y.ndim != 1 or x.ndim != 2 or x.shape[0] != y.size or y.size == 0:
        raise ValueError("observations must be 1-D and match nonempty coordinate rows")
    if not np.all(np.isfinite(y)) or not np.all(np.isfinite(x)):
        raise ValueError("observations and coordinates must be finite")
    if not isinstance(n_neighbors, int) or isinstance(n_neighbors, bool) or n_neighbors < 1:
        raise ValueError("n_neighbors must be a positive integer")
    if not np.isfinite(jitter) or jitter < 0:
        raise ValueError("jitter must be finite and nonnegative")
    if order is None:
        ordering = np.arange(y.size)
    else:
        ordering = np.asarray(order)
        if ordering.shape != (y.size,) or not np.issubdtype(ordering.dtype, np.integer) or not np.array_equal(np.sort(ordering), np.arange(y.size)):
            raise ValueError("order must be a permutation of observation indices")
    covariance = squared_exponential_covariance(
        x, variance=variance, length_scale=length_scale, nugget=nugget)
    means = np.zeros(y.size, dtype=float)
    conditional_variances = np.diag(covariance).copy()
    loglikelihood = 0.0
    for position, index in enumerate(ordering):
        previous = ordering[:position]
        if previous.size:
            distances2 = np.sum((x[previous] - x[index]) ** 2, axis=1)
            neighbours = previous[np.argsort(distances2, kind="stable")[:n_neighbors]]
            knn = covariance[np.ix_(neighbours, neighbours)].copy()
            knn.flat[::len(neighbours) + 1] += jitter
            kin = covariance[index, neighbours]
            try:
                weights = np.linalg.solve(knn, y[neighbours])
                solved_cov = np.linalg.solve(knn, kin)
            except np.linalg.LinAlgError as exc:
                raise ValueError("local covariance system is singular; increase nugget or jitter") from exc
            mean = float(kin @ weights)
            conditional_variance = float(covariance[index, index] - kin @ solved_cov)
        else:
            mean = 0.0
            conditional_variance = float(covariance[index, index])
        if not np.isfinite(conditional_variance) or conditional_variance <= 0:
            raise ValueError("non-positive conditional variance; increase nugget or jitter")
        means[index] = mean
        conditional_variances[index] = conditional_variance
        residual = y[index] - mean
        loglikelihood += -0.5 * (np.log(2*np.pi) + np.log(conditional_variance)
                                 + residual*residual/conditional_variance)
    return {"loglikelihood": float(loglikelihood), "conditional_means": means,
            "conditional_variances": conditional_variances,
            "order": ordering.copy()}


def vecchia_predict(observations, coordinates, prediction_coordinates, *,
                    variance=1.0, length_scale=1.0, nugget=0.0,
                    n_neighbors=10, jitter=1e-10):
    """Predict independently at new sites from their nearest observed neighbours.

    This is a local conditional predictor (NNGP-style sparse conditioning),
    not a joint predictive covariance for the entire prediction set.
    """
    y=np.asarray(observations,dtype=float)
    x=np.asarray(coordinates,dtype=float)
    xp=np.asarray(prediction_coordinates,dtype=float)
    if y.ndim!=1 or x.ndim!=2 or x.shape[0]!=y.size or y.size==0:
        raise ValueError("observations must be 1-D and match nonempty training coordinates")
    if xp.ndim!=2 or xp.shape[1]!=x.shape[1] or xp.shape[0]==0:
        raise ValueError("prediction coordinates must be a nonempty 2-D array with matching dimension")
    if not np.isfinite(y).all() or not np.isfinite(x).all() or not np.isfinite(xp).all():
        raise ValueError("observations and coordinates must be finite")
    if not isinstance(n_neighbors,int) or isinstance(n_neighbors,bool) or n_neighbors<1:
        raise ValueError("n_neighbors must be a positive integer")
    if not np.isfinite(jitter) or jitter<0:
        raise ValueError("jitter must be finite and nonnegative")
    # Reuse the covariance builder for parameter validation and training K.
    k_train=squared_exponential_covariance(x,variance=variance,length_scale=length_scale,nugget=nugget)
    delta=xp[:,None,:]-x[None,:,:]
    d2=np.sum(delta*delta,axis=2)
    cross=variance*np.exp(-0.5*d2/(length_scale*length_scale))
    prior_variance=float(variance+nugget)
    means=np.empty(len(xp)); variances=np.empty(len(xp)); selected=[]
    for i in range(len(xp)):
        neighbours=np.argsort(d2[i],kind="stable")[:min(n_neighbors,len(y))]
        knn=k_train[np.ix_(neighbours,neighbours)].copy()
        knn.flat[::len(neighbours)+1]+=jitter
        kin=cross[i,neighbours]
        try:
            alpha=np.linalg.solve(knn,y[neighbours])
            solved=np.linalg.solve(knn,kin)
        except np.linalg.LinAlgError as exc:
            raise ValueError("local covariance system is singular; increase nugget or jitter") from exc
        means[i]=float(kin@alpha)
        variances[i]=prior_variance-float(kin@solved)
        if not np.isfinite(variances[i]) or variances[i]<=0:
            raise ValueError("non-positive predictive variance; increase nugget or jitter")
        selected.append(neighbours.copy())
    return {"predictive_mean":means,"predictive_variance":variances,
            "neighbour_indices":selected}
