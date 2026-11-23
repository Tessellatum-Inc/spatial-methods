"""Discrete Lloyd iteration for weighted centroidal Voronoi tessellations."""
from __future__ import annotations
import numpy as np

def lloyd_cvt(points, seeds, weights=None, max_iter=100, tolerance=1e-6):
    """Iterate nearest-seed assignment and weighted centroid updates.

    This computes a discrete approximation over supplied sample points, not
    exact continuous Voronoi cells clipped to a polygon or domain.
    """
    x=np.asarray(points,dtype=float)
    z=np.asarray(seeds,dtype=float)
    if x.ndim!=2 or z.ndim!=2 or x.shape[1]!=z.shape[1] or len(x)<1 or len(z)<1:
        raise ValueError("points and seeds must be nonempty 2D arrays with matching dimensions")
    if not np.all(np.isfinite(x)) or not np.all(np.isfinite(z)):
        raise ValueError("points and seeds must be finite")
    if weights is None:
        mass=np.ones(len(x),dtype=float)
    else:
        mass=np.asarray(weights,dtype=float)
        if mass.shape!=(len(x),) or not np.all(np.isfinite(mass)) or np.any(mass<0):
            raise ValueError("weights must be finite, nonnegative and match points")
    if mass.sum()<=0:
        raise ValueError("weights must have positive total mass")
    if not isinstance(max_iter,int) or isinstance(max_iter,bool) or max_iter<1:
        raise ValueError("max_iter must be a positive integer")
    if not np.isfinite(tolerance) or tolerance<0:
        raise ValueError("tolerance must be finite and nonnegative")
    centers=z.copy()
    history=[]
    assignments=np.zeros(len(x),dtype=int)
    for iteration in range(max_iter):
        d2=((x[:,None,:]-centers[None,:,:])**2).sum(axis=2)
        assignments=np.argmin(d2,axis=1)
        updated=centers.copy()
        for j in range(len(centers)):
            mask=assignments==j
            if np.any(mask):
                local_mass=mass[mask].sum()
                if local_mass>0:
                    updated[j]=(x[mask]*mass[mask,None]).sum(axis=0)/local_mass
        movement=np.linalg.norm(updated-centers,axis=1)
        centers=updated
        # Objective evaluated after moving centers, using the current assignment.
        objective=float(np.sum(mass*np.sum((x-centers[assignments])**2,axis=1)))
        history.append(objective)
        if float(movement.max(initial=0.0))<=tolerance:
            break
    final_d2=((x[:,None,:]-centers[None,:,:])**2).sum(axis=2)
    assignments=np.argmin(final_d2,axis=1)
    objective=float(np.sum(mass*np.min(final_d2,axis=1)))
    if not history or objective!=history[-1]:
        history.append(objective)
    return {"centers":centers,"assignments":assignments,"objective":objective,
            "objective_history":history,"iterations":iteration+1}
