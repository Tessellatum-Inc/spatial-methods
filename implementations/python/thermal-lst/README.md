# Thermal land-surface temperature baselines

This package implements three deliberately scoped thermal-infrared methods:

- Planck radiance-to-brightness-temperature conversion using supplied band constants.
- Single-channel land-surface temperature retrieval by inverting a supplied
  atmospheric radiative-transfer equation.
- A generalized two-channel split-window correction using caller-supplied
  coefficients.

## Units and calibration

Brightness and surface temperatures are kelvin. Spectral radiance, Planck
constants, atmospheric radiances, water-vapour units and split-window
coefficients must be mutually consistent with the selected sensor and
calibration. Emissivity and transmittance are dimensionless fractions.

The single-channel method requires emissivity, atmospheric transmittance,
upwelling radiance and downwelling radiance. These are inputs, not retrieved
quantities. The split-window method requires coefficients calibrated for the
sensor, band pair, atmospheric profile and water-vapour units. No universal
coefficient set is bundled.

## Run tests

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

## Limitations

These are retrieval kernels, not complete satellite processing systems.
They do not perform radiometric calibration from digital numbers, atmospheric
profile retrieval, cloud screening, emissivity estimation, adjacency
correction, view-angle correction, uncertainty propagation or validation
against in-situ radiometric measurements. Incorrect or mismatched constants
can produce plausible but physically meaningless temperatures.
