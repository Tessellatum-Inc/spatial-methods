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

## SAFE metadata preflight audit

After the downloader's ZIP/SAFE structure check passes, run the separate metadata
preflight against the immutable archive:

```bash
python explorations/radar/audit_sentinel1_safe_metadata.py \
  data/copernicus/nairobi/sentinel1_8ffa5641-c404-4189-b0fb-ed805b077d71.SAFE.zip \
  --expected-product-name S1C_IW_GRDH_1SDV_20261102T031112_20261102T031137_010152_01443B_5D46.SAFE \
  --output data/copernicus/nairobi/sentinel1_8ffa5641-c404-4189-b0fb-ed805b077d71.preflight.json
```

This second gate checks ZIP CRCs, a parseable `manifest.safe`, safe member
paths, and the presence of VV and VH measurement, annotation, calibration and
noise-annotation file sets based on SAFE member names. It also verifies that
the SAFE root name identifies a Sentinel-1 IW GRD product and that the manifest
declares IW mode. When an expected catalogue product name is supplied, the
audit checks that exact identity too. It records the archive SHA-256 and
metadata values exposed by the manifest. It does not extract or modify the
source archive.

The readiness reconciler requires all seven base audit checks to be present
and pass: the four VV/VH file-set checks, well-formed manifest XML, IW GRD SAFE
root identity, and IW mode in the manifest. Missing checks are treated as
incomplete evidence, not silently accepted. The optional expected-name
comparison is an additional identity check when included in the audit.

A failed dual-polarisation gate blocks processing. A passing gate is still
only a structural preflight: it does not inspect raster pixels, validate
calibration LUT values, verify geolocation, or prove full datatake coverage.
The actual downloaded product must be inspected before selecting SNAP
operators or parameter values.

Offline tests:

```bash
python -m unittest discover -s scripts -p "test_audit_sentinel1_safe_metadata.py"
```


## Reconcile evidence into a processing-readiness record

Once the candidate manifest, downloader sidecar and SAFE audit JSON exist, reconcile them by product UUID and archive identity:

```bash
python explorations/radar/build_sentinel1_processing_readiness.py \
  --stack-manifest explorations/radar/nairobi-sentinel-1-stack-manifest.json \
  --download-sidecar data/copernicus/nairobi/sentinel1_8ffa5641-c404-4189-b0fb-ed805b077d71.SAFE.zip.metadata.json \
  --safe-audit data/copernicus/nairobi/sentinel1_8ffa5641-c404-4189-b0fb-ed805b077d71.preflight.json \
  --output data/copernicus/nairobi/sentinel1_8ffa5641-c404-4189-b0fb-ed805b077d71.readiness.json
```

The reconciler requires exactly one matching catalogue candidate, a successful
download validation, matching archive filenames and SHA-256 checksums, a
passing dual-polarisation structural gate, all reported audit checks passing,
and a SAFE root name matching the catalogue product name. Any mismatch blocks
the structural preflight record and is named explicitly.

**A passed structural preflight does not authorize scientific processing.**
The record keeps `processing_authorized: false` and lists the remaining gates:
required datatake/slice coverage, locked software and parameters, radiometric
and geometric QA, and independent review. This is deliberate; no SNAP graph
or scientific result should be inferred from file-presence checks alone.

Offline tests:

```bash
python -m unittest discover -s scripts -p "test_build_sentinel1_processing_readiness.py"
```


## Optional GitHub Actions download and preflight

A manually triggered workflow is available at **Actions → Sentinel-1 Nairobi download and structural preflight → Run workflow**. It is pinned to the 2 November 2026 candidate UUID above; it does not accept arbitrary product IDs and does not run on pushes. Before using it, add these two repository secrets under **Settings → Secrets and variables → Actions → Repository secrets**:

- `CDSE_USERNAME`: your Copernicus Data Space account email.
- `CDSE_PASSWORD`: your Copernicus Data Space password.

Do not put either value in workflow inputs, source files, commits, or chat. The workflow passes them only to the downloader process as environment variables. It builds the candidate manifest from the committed inventory, downloads the selected ZIP, runs the SAFE metadata audit, and reconciles the evidence. The workflow artifact contains JSON metadata and provenance only; the SAFE archive is removed from the runner workspace and is not uploaded to GitHub.

**Runner capacity is a real constraint.** The standard hosted runner has finite temporary storage, and the product's actual archive size must fit alongside the operating environment and working files. The workflow prints available disk capacity before download, but this is not a guarantee that the archive will fit. If the download fails for space, timeout, account entitlement, or provider availability, use the documented local download procedure on a machine with sufficient disk instead. A successful workflow run establishes only the structural preflight recorded in the artifact; it does not authorize SNAP processing or establish scientific validity.

### Copernicus authentication troubleshooting

The workflow first verifies that both repository secrets are present, but that
check cannot verify that the account credentials are valid or that the account
has completed any required authentication steps. If token generation fails,
inspect the failed **Download the selected Sentinel-1 SAFE archive** step for
the HTTP status and the provider's safe error description. The downloader
reports only the OAuth error code/description; it never prints the username,
password, request body or response headers.

The official [token-generation guide](https://documentation.dataspace.copernicus.eu/APIs/Token.html)
documents the password grant and an additional `totp` parameter for accounts
using two-factor authentication. If the provider reports an invalid grant,
check that the secret contains the Copernicus Data Space login email and the
current account password (not a Sentinel Hub OAuth client secret), and confirm
whether the account requires TOTP. Do not disable account security or paste
one-time codes into repository files, workflow inputs, logs or chat. The
workflow currently supports username/password authentication only; TOTP
support must be added safely if the account requires it.
