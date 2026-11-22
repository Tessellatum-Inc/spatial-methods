# Hydrographic multi-stage sensor-chain geometry

Dependency-free first-order geometry from a GNSS antenna reference point through
an IMU and mounted transducer to an acoustic detection point.

## Frames and model

Let (n), (i), and (t) be navigation, IMU, and transducer frames.
(mathbf l_{i,g}) and (mathbf l_{i,t}) are vectors from the IMU origin to
the GNSS antenna and transducer origins, both expressed in IMU axes.
(mathbf s_t) runs from transducer origin to acoustic detection in transducer
axes. (mathbf R_{nleftarrow i}) maps IMU to navigation and
(mathbf R_{ileftarrow t}) maps transducer to IMU.

[
mathbf p_n=mathbf r_{n,g}+
mathbf R_{nleftarrow i}(-mathbf l_{i,g}+mathbf l_{i,t}+
mathbf R_{ileftarrow t}mathbf s_t).
]

The negative antenna lever-arm term follows from solving for the IMU origin.
The supplied GNSS position must refer to the antenna. If the navigation
solution already reports the IMU origin, do not apply this correction again.

## Jacobian

For (mathbf q=mathbf R_{ileftarrow t}mathbf s_t) and
(mathbf v_n=mathbf R_{nleftarrow i}(-mathbf l_{i,g}+mathbf l_{i,t}+mathbf q)),
the input order is
([mathbf r_{n,g},deltaoldsymbol	heta_n,mathbf l_{i,g},
mathbf l_{i,t},deltaoldsymbolphi_i,mathbf s_t]), and

[
mathbf J=[mathbf I, -[mathbf v_n]_	imes,-mathbf R_{nleftarrow i}, mathbf R_{nleftarrow i},-mathbf R_{nleftarrow i}[mathbf q]_	imes,mathbf R_{nleftarrow i}mathbf R_{ileftarrow t}].
]

Both attitude perturbations are left-multiplicative: navigation attitude
error is expressed in navigation axes; transducer mounting error is in IMU
axes. Angular derivatives are per radian. Combine this 3 by 18 Jacobian with
a joint covariance in the same order to preserve shared calibration and
trajectory correlations.

## Run and test

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

Tests cover identity and composed rotations, lever-arm signs, all Jacobian
blocks by finite differences, invalid rotations, non-finite inputs and
invalid tolerance.

## Scope

Static rigid-body geometry only. No trajectory estimation, time alignment,
latency, heave/draft/squat, vessel flexure, acoustic ray tracing, beamforming,
bottom detection, geodetic projection, vertical datum reduction, calibration
estimation or full hydrographic TPU. Not a substitute for instrument-specific
calibration or field validation.
