# Time-aligned and multi-ping hydrographic sensor-chain geometry

## Time alignment

The sounding coordinate depends on the navigation pose at the acoustic
observation epoch. Given \(t_0<t_1\), evaluate at
\(t_e=t_{\rm ping}+\Delta t\), requiring \(t_e\in[t_0,t_1]\).
Antenna position is linearly interpolated and attitude follows the shortest
SO(3) geodesic:
\[
\mathbf r_{n,g}(\alpha)=(1-\alpha)\mathbf r_{n,g,0}+\alpha\mathbf r_{n,g,1},
\quad \alpha=\frac{t_e-t_0}{t_1-t_0},
\]
\[
\mathbf R_{n\leftarrow i}(\alpha)=
\mathbf R_{n\leftarrow i,0}\exp\left(\alpha\log(
\mathbf R_{n\leftarrow i,0}^{T}\mathbf R_{n\leftarrow i,1})\right).
\]
This assumes constant translational velocity and body angular rate over the
bracket. The timing derivative includes translation and attitude-induced
displacement:
\[
\frac{\partial\mathbf p_n}{\partial\Delta t}
=\frac{\mathbf r_{n,g,1}-\mathbf r_{n,g,0}}{t_1-t_0}
+\mathbf R_{n\leftarrow i}
\left[\frac{\boldsymbol\phi}{t_1-t_0}\right]_\times\mathbf v_i,
\]
where \(\boldsymbol\phi=\log(\mathbf R_{n\leftarrow i,0}^{T}
\mathbf R_{n\leftarrow i,1})\) and
\(\mathbf v_i=-\mathbf l_{i,g}+\mathbf l_{i,t}+
\mathbf R_{i\leftarrow t}\mathbf s_t\).

## Shared multi-ping uncertainty

For ping \(i\), let \(\mathbf x_i\) be ping-local parameters and
\(\mathbf c\) parameters shared across the survey, such as installation
lever arms, mounting angles, common clock offset and drift. The joint input
order is all local blocks followed by one shared block. With local Jacobians
\(\mathbf J_i\) and shared Jacobians \(\mathbf K_i\):
\[
\mathbf J_{\rm all}=
\begin{bmatrix}
\mathbf J_1&0&\cdots&0&\mathbf K_1\\
0&\mathbf J_2&\cdots&0&\mathbf K_2\\
\vdots&&\ddots&&\vdots\\
0&0&\cdots&\mathbf J_N&\mathbf K_N
\end{bmatrix},
\qquad
\mathbf C_p=\mathbf J_{\rm all}\mathbf C_x\mathbf J_{\rm all}^{T}.
\]
The result is a \(3N\times3N\) covariance. Off-diagonal blocks represent
cross-ping correlation induced by common uncertain parameters. In particular,
a shared clock offset contributes
\[
\mathbf C_{p_i p_j}^{(t)}
=\sigma_{\delta t}^2\mathbf j_{t,i}\mathbf j_{t,j}^{T}.
\]
Independent ping jitter belongs in each local block and does not itself
create cross-ping covariance.

For
\[
\Delta t_i=\delta t_0+\dot{\delta t}(t_i-t_{\rm ref})+\epsilon_i,
\]
the shared clock columns are
\[
\frac{\partial\mathbf p_i}{\partial\delta t_0}=\mathbf j_{t,i},
\qquad
\frac{\partial\mathbf p_i}{\partial\dot{\delta t}}
=(t_i-t_{\rm ref})\mathbf j_{t,i}.
\]
Choose \(t_{\rm ref}\) near the survey midpoint. Preserve known correlations
between local navigation states and shared clock or calibration parameters.
The implementation validates shape, finiteness and covariance symmetry;
positive-semidefinite validation remains the responsibility of the covariance
provider.

## Implementation and limits

The [Python implementation and tests](../../implementations/python/hydrographic-sensor-chain/README.md)
provide two-state pose interpolation, timing sensitivity, block-Jacobian
assembly, offset/drift sensitivity construction and full cross-ping covariance
propagation. This is a first-order uncertainty model, not a clock or
calibration estimator. It does not yet model clock random walks, high-dynamic
trajectory splines, asynchronous filtering, vessel flexure, acoustic ray
tracing or bottom detection. Operational work must preserve raw time tags,
clock definitions, calibration records and navigation provenance.
