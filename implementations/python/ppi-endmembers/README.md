# Pixel Purity Index (PPI)

A NumPy reference implementation of hyperspectral Pixel Purity Index. Random unit directions are projected through mean-centred pixel spectra; each projection votes for its minimum and maximum. Pixels are ranked by accumulated votes.

## Run

    python -m pip install -r requirements.txt
    pytest -q

    from ppi import pixel_purity_index
    result = pixel_purity_index(cube, n_projections=2000, top_k=50, seed=7)
    scores = result["scores"]
    candidate_spectra = result["candidate_spectra"]

The cube is finite (rows, columns, bands) data. A boolean valid_mask excludes invalid pixels. Scores are row-major aligned; excluded cells are -1. A fixed seed gives reproducible projections.

PPI is a candidate-screening heuristic. Projection count, atmospheric correction, scaling, noise, and scene composition affect rankings. Validate candidates with spectral inspection and a separate unmixing or field-validation workflow; do not interpret the score as a probability or purity estimate.
