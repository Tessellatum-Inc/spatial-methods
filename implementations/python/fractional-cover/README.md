# Fractional-cover regression tree

A small CART regression-tree implementation for estimating field-labelled
fractional cover from spectral or other predictor features.

## Contract

- X is a finite matrix of predictor samples by features (for example reflectance bands).
- y is a finite vector of field/reference fractions in [0, 1].
- predict(X) returns leaf-mean predictions clipped to [0, 1].
- Splits maximise squared-error reduction; ties are deterministic.
- Maximum depth and minimum leaf size constrain model complexity.

## Run

Install dependencies with python -m pip install -r requirements.txt, then run
python -m pytest -q.

## Scientific scope

This is a transparent single CART tree baseline. It is not a Random Forest,
gradient-boosted model, fractional-cover product, or vegetation continuous
fields dataset. It does not perform atmospheric correction, spectral
unmixing, spatial cross-validation, uncertainty calibration, sensor
harmonisation or field-data quality control. Evaluate with spatially separated
field samples and report bias, RMSE, sample design and domain transfer before
using outputs operationally.
