# GNSS–IMU–transducer sounding-point geometry and Jacobian

## Frames and model

Let (n,i,t) denote navigation, IMU and transducer frames. The GNSS
position (mathbf r_{n,g}) refers to the antenna reference point.
The lever arms (mathbf l_{i,g}) and (mathbf l_{i,t}) both point outward
from the IMU origin and are expressed in IMU axes. The acoustic vector
(mathbf s_t) is expressed in transducer axes. Rotations map
(mathbf R_{nleftarrow i}) from IMU to navigation and
(mathbf R_{ileftarrow t}) from transducer to IMU.

[
mathbf r_{n,i}=mathbf r_{n,g}-
mathbf R_{nleftarrow i}mathbf l_{i,g}
]

[
oxed{mathbf p_n=mathbf r_{n,g}+
mathbf R_{nleftarrow i}(-mathbf l_{i,g}+mathbf l_{i,t}+
mathbf R_{ileftarrow t}mathbf s_t)}
]

The negative GNSS lever-arm term follows from solving for the IMU origin.
If the navigation solution already reports the IMU origin, do not apply the
antenna correction a second time.

## Jacobian and conventions

Define (mathbf q=mathbf R_{ileftarrow t}mathbf s_t) and
(mathbf v_n=mathbf R_{nleftarrow i}(-mathbf l_{i,g}+mathbf l_{i,t}+mathbf q)).
For input order
([mathbf r_{n,g},deltaoldsymbol	heta_n,mathbf l_{i,g},
mathbf l_{i,t},deltaoldsymbolphi_i,mathbf s_t]),

[
mathbf J=[mathbf I, -[mathbf v_n]_	imes,
-mathbf R_{nleftarrow i},mathbf R_{nleftarrow i},
-mathbf R_{nleftarrow i}[mathbf q]_	imes,
mathbf R_{nleftarrow i}mathbf R_{ileftarrow t}].
]

The navigation attitude perturbation is left-multiplicative in navigation
axes; the transducer mounting perturbation is left-multiplicative in IMU
axes. Both angular derivatives are per radian. First-order covariance is

[
mathbf C_p=mathbf Jmathbf C_xmathbf J^T.
]

Use a joint covariance to preserve correlations between trajectory,
installation and calibration parameters. Shared parameters across pings
also induce cross-ping covariance; treating every ping independently loses
that structure.

## Computational reference

The [Python implementation](../../implementations/python/hydrographic-sensor-chain/README.md)
returns the point and analytic 3 by 18 Jacobian. Tests compare every
sensitivity block against finite differences under the stated conventions.

## Limits

Static geometry only: no time-tag interpolation, latency, heave, draft, squat,
vessel flexure, water-column refraction, bottom detection, vertical datum
reduction or parameter estimation. This is not a complete TPU engine or
validated MBES processing chain. Confirm the GNSS position reference point
before using the antenna lever arm.
