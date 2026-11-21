# Sentinel-1 product download and structural validation

This procedure downloads one selected Copernicus Data Space Sentinel-1 product
and checks the archive before any scientific processing. It deliberately does
not perform calibration, terrain correction, resampling, or interpretation.

## Prerequisites

- A Copernicus Data Space account with product-download access.
- Python 3.10 or later; the downloader uses only the Python standard library.
- Sufficient local disk space for the full extracted SAFE product and a ZIP
  archive. Do not run this on a low-capacity runner or commit the product to Git.
- Network access to the Copernicus identity and download endpoints.

Copernicus requires an access token for product downloads. The documented
password-grant token endpoint and product download endpoint are described in
the [official OData documentation](https://documentation.dataspace.copernicus.eu/APIs/OData.html).

## Download the first full-AOI candidate

The 2 November 2026 product is one of four same-orbit full-AOI candidates. It
also had both compressed and extracted product forms in the captured catalogue.
The script requests the extracted form using the product UUID:

```text
8ffa5641-c404-4189-b0fb-ed805b077d71
```

Set credentials in the shell environment without putting them in the command
history, source code, workflow YAML, or repository:

```bash
export CDSE_USERNAME="your-copernicus-account-email"
read -rsp "Copernicus password: " CDSE_PASSWORD
export CDSE_PASSWORD
printf '\n'
```

Run the download and validation:

```bash
python explorations/radar/download_copernicus_sentinel1.py \
  --product-id 8ffa5641-c404-4189-b0fb-ed805b077d71 \
  --output-dir data/copernicus/nairobi
```

After the run, clear the shell variables:

```bash
unset CDSE_PASSWORD CDSE_USERNAME
```

The script writes a ZIP archive and a JSON provenance sidecar. It checks ZIP
CRC integrity, exactly one `manifest.safe`, at least one measurement GeoTIFF
under `measurement/`, and at least one annotation XML under `annotation/`.
It records archive size, SHA-256, product ID, retrieval time and the structural
validation outcome. A failed download or validation must not be used downstream.

## Interpretation boundary

Passing the archive checks establishes only that the downloaded file is a
readable ZIP with a minimal expected SAFE structure. It does not establish
that the scene is radiometrically correct, that both VV and VH measurement
files are present, or that the scene is scientifically suitable.

Before processing, inspect the manifest and annotation metadata for:
- actual measurement polarisation and swath membership;
- acquisition start/stop and slice identity;
- processing baseline and product generation metadata;
- calibration and noise annotation references;
- orbit and incidence-angle information;
- missing adjacent slices or coverage outside the selected slice.

Keep the original archive immutable. Perform processing into a separate
derived-data directory and record software versions, parameters, CRS, pixel
spacing, resampling method, masks and output checksums. Do not commit product
archives or credentials to the repository.

## Offline tests

```bash
python -m unittest scripts/test_download_copernicus_sentinel1.py
```
