"""Harris-style regional market-potential indices."""
import numpy as np

def market_potential(mass, impedance, *, exponent=1.0, self_potential=True):
    """Return destination-mass-weighted inverse-impedance potential by origin.

    impedance[i,j] is the generalized travel cost from origin i to market j.
    Zero off-diagonal costs are invalid; diagonal zeros are allowed and are
    excluded when self_potential=False. This is an index, not a structural
    gravity estimate or an equilibrium market-access measure.
    """
    mass=np.asarray(mass,dtype=float); cost=np.asarray(impedance,dtype=float)
    if mass.ndim!=1 or cost.shape!=(mass.size,mass.size) or mass.size==0:
        raise ValueError("mass must be (n,) and impedance must be (n,n)")
    if not np.all(np.isfinite(mass)) or np.any(mass<0): raise ValueError("market mass must be finite and nonnegative")
    if not np.all(np.isfinite(cost)) or np.any(cost<0): raise ValueError("impedance must be finite and nonnegative")
    if not np.isfinite(exponent) or exponent<=0: raise ValueError("exponent must be positive")
    c=cost.copy(); diagonal=np.eye(mass.size,dtype=bool)
    if np.any((c==0)&(~diagonal)): raise ValueError("off-diagonal impedance must be positive")
    if not self_potential: c[diagonal]=np.inf
    else:
        if np.any(np.diag(c)==0): raise ValueError("self-potential requires positive diagonal impedance")
    return np.sum(mass[None,:] / np.power(c,exponent),axis=1)
