# Multispectral numerical primitives

The module `multispectral_metrics.py` implements deterministic calculations used by the Fiji pilot:

- NDVI, McFeeters NDWI, MNDWI, NDBI and NDRE;
- explicit NaN handling for nodata and unstable denominators;
- SCL-based validity mask;
- masked point/neighbourhood summaries;
- index-stack calculation when required co-registered bands are supplied.

## Important input contract

All arrays passed to index functions must be on the same grid, with matching shape, pixel alignment and compatible reflectance scaling. The module does not fetch STAC items, open raster assets, reproject bands or choose observations. Those are separate workflow stages and must record their own provenance. Do not pass 10 m B08 directly against 20 m B11 without explicitly harmonizing the grids; any 20 m index using B11 must be computed on a declared 20 m grid.

SCL classes excluded are 0, 1, 3, 7, 8, 9, 10 and 11. Classes 2, 4, 5 and 6 are retained. This is an analysis mask, not a guarantee that retained pixels are free of contamination.

## Run tests

From this directory:

```bash
python -m pip install numpy
python -m unittest -v test_multispectral_metrics.py
```

The tests use synthetic arrays and validate arithmetic/masking only. They do not validate live STAC discovery, remote raster access, spatial alignment, sensor calibration or land-cover classification.
