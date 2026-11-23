undefined

## Independent Sentinel Hub access route

The repository also contains a separate OAuth2 client-credentials route for Sentinel Hub. It does not replace or modify the OData SAFE downloader.

- [Sentinel Hub Sentinel-1 Catalog client](query_sentinelhub_sentinel1.py) requests a short-lived token from the CDSE identity service, then searches the `sentinel-1-grd` collection for IW scenes intersecting the Nairobi study bounding box.
- The client reads `SENTINEL_HUB_CLIENT_ID` and `SENTINEL_HUB_CLIENT_SECRET` from environment variables. It never prints or writes the client secret or access token.
- The manual workflow is [sentinelhub-sentinel1-catalogue.yml](../../.github/workflows/sentinelhub-sentinel1-catalogue.yml). Configure two GitHub Actions repository secrets with those exact names before dispatching it.
- The workflow saves the STAC response and a metadata sidecar as a short-lived Actions artifact. It does not download a SAFE archive or imagery pixels; catalogue discovery is a first authentication and data-availability check, not a processing result.

Run locally from the repository root:

```bash
export SENTINEL_HUB_CLIENT_ID='your-client-id'
export SENTINEL_HUB_CLIENT_SECRET='your-client-secret'
python explorations/radar/query_sentinelhub_sentinel1.py
```

The OAuth client-credentials flow and Catalog API endpoint/collection are documented by [CDSE Sentinel Hub authentication](https://documentation.dataspace.copernicus.eu/APIs/SentinelHub/Overview/Authentication.html), [Catalog API](https://documentation.dataspace.copernicus.eu/APIs/SentinelHub/Catalog.html), and [Sentinel-1 GRD collection guidance](https://documentation.dataspace.copernicus.eu/APIs/SentinelHub/Data/S1GRD.html). Sentinel Hub catalogue results are not equivalent to original SAFE archive downloads; use the OData route when the study requires the original product package and its complete SAFE structure.
