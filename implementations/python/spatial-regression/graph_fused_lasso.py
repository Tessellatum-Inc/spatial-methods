"""Graph-fused sparse regression with location-specific coefficients (ADMM)."""
from __future__ import annotations
import numpy as np

def graph_fused_lasso(X, y, locations, n_locations, edges,
                      lambda_l1=0.0, lambda_fused=1.0, rho=1.0,
                      max_iter=2000, absolute_tolerance=1e-5,
                      relative_tolerance=1e-4):
    """Fit location-specific coefficients with L1 and graph-TV penalties.

    Minimizes 0.5*sum_i ||y_i-X_i beta_location(i)||^2
      + lambda_l1*||B||_1 + lambda_fused*||D B||_1.

    D is an oriented node-edge incidence matrix. The graph orientation does
    not affect the L1 total-variation penalty. ADMM solves the dense normal
    equations each iteration; intended for small/medium teaching problems.
    """
    X=np.asarray(X,dtype=float); y=np.asarray(y,dtype=float)
    loc=np.asarray(locations)
    edge=np.asarray(edges,dtype=int)
    if X.ndim!=2 or X.shape[0]<1 or X.shape[1]<1 or not np.all(np.isfinite(X)):
        raise ValueError("X must be a finite nonempty 2D design matrix")
    if y.shape!=(X.shape[0],) or not np.all(np.isfinite(y)):
        raise ValueError("y must be a finite vector matching X rows")
    if loc.shape!=(X.shape[0],) or not np.issubdtype(loc.dtype,np.integer):
        raise ValueError("locations must be an integer index per observation")
    if isinstance(n_locations,bool) or int(n_locations)!=n_locations or n_locations<1:
        raise ValueError("n_locations must be a positive integer")
    n_locations=int(n_locations); p=X.shape[1]
    if np.any(loc<0) or np.any(loc>=n_locations):
        raise ValueError("location indices are outside [0, n_locations)")
    if edge.size==0: edge=np.empty((0,2),dtype=int)
    if edge.ndim!=2 or edge.shape[1]!=2:
        raise ValueError("edges must have shape (n_edges, 2)")
    if np.any(edge<0) or np.any(edge>=n_locations) or np.any(edge[:,0]==edge[:,1]):
        raise ValueError("edges contain invalid endpoints or self-loops")
    canonical=[tuple(sorted(map(int,e))) for e in edge]
    if len(set(canonical))!=len(canonical):
        raise ValueError("duplicate undirected edges are not supported")
    for name,value in [("lambda_l1",lambda_l1),("lambda_fused",lambda_fused)]:
        if not np.isfinite(value) or value<0: raise ValueError(f"{name} must be finite and nonnegative")
    if not np.isfinite(rho) or rho<=0: raise ValueError("rho must be finite and positive")
    if isinstance(max_iter,bool) or int(max_iter)!=max_iter or max_iter<1:
        raise ValueError("max_iter must be a positive integer")
    if not np.isfinite(absolute_tolerance) or absolute_tolerance<=0:
        raise ValueError("absolute_tolerance must be finite and positive")
    if not np.isfinite(relative_tolerance) or relative_tolerance<=0:
        raise ValueError("relative_tolerance must be finite and positive")
    m=len(edge)
    D=np.zeros((m,n_locations))
    for k,(u,v) in enumerate(edge):
        D[k,u]=-1.0; D[k,v]=1.0
    gram=np.zeros((n_locations*p,n_locations*p))
    rhs_data=np.zeros(n_locations*p)
    for j in range(n_locations):
        rows=(loc==j)
        if np.any(rows):
            block=X[rows].T@X[rows]
            sl=slice(j*p,(j+1)*p)
            gram[sl,sl]=block
            rhs_data[sl]=X[rows].T@y[rows]
    incidence=np.kron(D,np.eye(p))
    system=gram+rho*np.eye(n_locations*p)+rho*(incidence.T@incidence)
    beta=np.zeros((n_locations,p)); z=beta.copy(); u=beta.copy()
    w=np.zeros((m,p)); v=w.copy()
    history=[]
    for iteration in range(int(max_iter)):
        rhs=rhs_data+rho*(z-u).reshape(-1)+rho*incidence.T@(w-v).reshape(-1)
        beta=np.linalg.solve(system,rhs).reshape(n_locations,p)
        db=incidence@beta.reshape(-1)
        z_old=z.copy(); w_old=w.copy()
        a=beta+u
        z=np.sign(a)*np.maximum(np.abs(a)-lambda_l1/rho,0.0)
        b=db.reshape(m,p)+v
        w=np.sign(b)*np.maximum(np.abs(b)-lambda_fused/rho,0.0)
        u+=beta-z; v+=db.reshape(m,p)-w
        primal=float(np.sqrt(np.linalg.norm(beta-z)**2+np.linalg.norm(db.reshape(m,p)-w)**2))
        dual_vec=(z-z_old).reshape(-1)+incidence.T@(w-w_old).reshape(-1)
        dual=float(rho*np.linalg.norm(dual_vec))
        dim=n_locations*p+m*p
        eps_pri=np.sqrt(dim)*absolute_tolerance+relative_tolerance*max(
            np.linalg.norm(beta),np.linalg.norm(z),np.linalg.norm(db),np.linalg.norm(w))
        eps_dual=np.sqrt(n_locations*p)*absolute_tolerance+relative_tolerance*rho*np.linalg.norm(
            u.reshape(-1)+incidence.T@v.reshape(-1))
        history.append({"primal_residual":primal,"dual_residual":dual,
                        "primal_tolerance":float(eps_pri),"dual_tolerance":float(eps_dual)})
        if primal<=eps_pri and dual<=eps_dual: break
    return {"coefficients":beta,"iterations":iteration+1,"converged":bool(
        history[-1]["primal_residual"]<=history[-1]["primal_tolerance"] and
        history[-1]["dual_residual"]<=history[-1]["dual_tolerance"]),
        "history":history,"objective":float(
            0.5*sum(np.sum((y[loc==j]-X[loc==j]@beta[j])**2) for j in range(n_locations))
            +lambda_l1*np.sum(np.abs(beta))+lambda_fused*np.sum(np.abs(incidence@beta.reshape(-1))))}
