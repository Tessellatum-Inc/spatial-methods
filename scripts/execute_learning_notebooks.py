"""Execute the curated learning notebooks from the repository root."""
import argparse
from pathlib import Path
from notebook_sharding import select_notebooks
import json
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

NOTEBOOKS = [["global-morans-i-lab.ipynb",120],["bivariate-morans-i-lab.ipynb",180],["lees-l-lab.ipynb",180],["linear-algebra-computational-companion-lab.ipynb",180],["mantel-tests-lab.ipynb",180],["gearys-c-lab.ipynb",120],["local-morans-i-lab.ipynb",180],["local-geary-lab.ipynb",180],["getis-ord-gi-star-lab.ipynb",180],["global-getis-ord-g-lab.ipynb",180],["spatial-econometrics-lab.ipynb",180],["str-packed-rtree-lab.ipynb",180],["filter-refine-spatial-join-lab.ipynb",180],["spatial-weights-lab.ipynb",180],["geometry-foundations-lab.ipynb",180],["quadtree-lab.ipynb",180],["polygon-overlay-lab.ipynb",180],["cascaded-union-lab.ipynb",180],["convex-hull-lab.ipynb",180],["graham-scan-lab.ipynb",180],["voronoi-delaunay-lab.ipynb",180],["core-gis-algorithms-lab.ipynb",180],["dijkstra-lab.ipynb",180],["coverage-simplification-routing-lab.ipynb",180],["geostatistics-interpolation-lab.ipynb",180],["empirical-semivariogram-lab.ipynb",180],["ordinary-kriging-lab.ipynb",180],["inverse-distance-weighting-lab.ipynb",180],["raster-distance-transform-lab.ipynb",180],["ndvi-lab.ipynb",180],["p-median-facility-location-lab.ipynb",180],["capacitated-p-median-lab.ipynb",180],["accessibility-equity-lab.ipynb",180],["equity-constrained-covering-lab.ipynb",180],["p-center-lab.ipynb",180],["set-covering-lab.ipynb",180],["maximal-covering-lab.ipynb",180],["backup-coverage-lab.ipynb",180],["mmc-queue-lab.ipynb",180],["mexclp-lab.ipynb",180],["dbscan-clustering-lab.ipynb",180],["two-step-fca-accessibility-lab.ipynb",180],["d8-flow-direction-lab.ipynb",180],["d8-flow-accumulation-lab.ipynb",180],["watershed-delineation-lab.ipynb",180],["stream-order-lab.ipynb",180],["priority-flood-lab.ipynb",180],["focal-raster-statistics-lab.ipynb",180],["point-pattern-kde-lab.ipynb",180],["clark-evans-lab.ipynb",180],["ripley-k-lab.ipynb",180],["slope-aspect-lab.ipynb",180],["cost-distance-lab.ipynb",180],["raster-resampling-lab.ipynb",180],["zonal-statistics-lab.ipynb",180],["raster-connected-components-lab.ipynb",180],["contrastive-info-nce-lab.ipynb",180],["crs-transformation-lab.ipynb",180],["point-location-lab.ipynb",180],["weighted-linear-combination-lab.ipynb",180],["triple-collocation-lab.ipynb",180],["marine-heatwave-detection-lab.ipynb",180],["exact-orientation-lab.ipynb",180],["covariance-functions-lab.ipynb",180],["spherical-covariance-lab.ipynb",180],["graph-spectral-covariance-lab.ipynb",180],["nonseparable-space-time-covariance-lab.ipynb",180],["weights-of-evidence-lab.ipynb",180],["electre-i-outranking-lab.ipynb",180],["snap-rounding-noder-lab.ipynb",180],["ear-clipping-lab.ipynb",180],["minkowski-convex-lab.ipynb",180],["convex-decomposition-lab.ipynb",180],["proximity-graphs-delaunay-lab.ipynb",180],["electre-i-kernel-lab.ipynb",180],["geometry-metrics-lab.ipynb",180],["pareto-multi-criteria-routing-lab.ipynb",180],["spatial-scan-statistic-lab.ipynb",180],["mean-radiant-temperature-lab.ipynb",180],["mfd-flow-routing-lab.ipynb",180],["ecef-enu-lab.ipynb",180],["rasterization-lab.ipynb",180],["line-clipping-lab.ipynb",180],["hmm-viterbi-lab.ipynb",180],["curves-smoothing-lab.ipynb",180],["forecast-verification-lab.ipynb",180],["forecast-fractions-skill-score-lab.ipynb",180],["line-simplification-lab.ipynb",180],["change-point-detection-lab.ipynb",180],["bspline-nurbs-lab.ipynb",180],["schneider-bezier-fitting-lab.ipynb",180],["population-diversity-segregation-lab.ipynb",180],["kalman-rts-smoothing-lab.ipynb",180],["bayesian-online-change-point-lab.ipynb",180],["potential-field-derivatives-lab.ipynb",180],["ensemble-forecast-verification-lab.ipynb",180],["geophysical-gridding-lab.ipynb",180],["lucas-kanade-optical-flow-lab.ipynb",180],["spatial-distribution-shift-lab.ipynb",180],["spatial-cross-validation-splitters-lab.ipynb",180],["adaptive-cluster-sampling-lab.ipynb",180],["gp-ucb-spatial-survey-lab.ipynb",180],["ucb1-survey-bandit-lab.ipynb",180],["spatial-active-learning-lab.ipynb",180],["ais-gap-detection-lab.ipynb",180],["area-of-applicability-baseline-lab.ipynb",180],["arima-forecasting-lab.ipynb",180],["crps-decomposition-lab.ipynb",180],["dasymetric-allocation-lab.ipynb",180],["dense-optical-flow-farneback-dis-lab.ipynb",180],["discrete-biharmonic-gridding-lab.ipynb",180],["domain-classifier-shift-lab.ipynb",180],["euler-deconvolution-lab.ipynb",180],["gaussian-plume-inversion-lab.ipynb",180],["knndm-spatial-validation-lab.ipynb",180],["methane-plume-detection-and-flux-lab.ipynb",180],["mode-inspired-object-verification-lab.ipynb",180],["nndm-spatial-validation-lab.ipynb",180],["potential-field-downward-continuation-lab.ipynb",180],["potential-field-matched-filtering-lab.ipynb",180],["potential-field-radial-spectrum-lab.ipynb",180],["potential-field-upward-continuation-lab.ipynb",180],["sal-precipitation-verification-lab.ipynb",180],["spatial-block-permutation-mmd-lab.ipynb",180],["spatial-differential-privacy-lab.ipynb",180],["spatial-k-anonymity-lab.ipynb",180],["spatial-microdata-ipf-lab.ipynb",180],["spatial-privacy-composition-lab.ipynb",180],["spatiotemporal-llto-lab.ipynb",180],["stl-decomposition-lab.ipynb",180],["theil-sen-trend-lab.ipynb",180],["werner-deconvolution-lab.ipynb",180],["louvain-community-detection-lab.ipynb",180],["transit-routing-lab.ipynb",180],["adaptive-spatial-sampling-lab.ipynb",180],["baarda-data-snooping-lab.ipynb",180],["bootstrap-particle-filter-lab.ipynb",180],["compositional-logratio-lab.ipynb",180],["cp-parafac-tensor-decomposition-lab.ipynb",180],["discrete-centroidal-voronoi-lloyd-lab.ipynb",180],["empirical-bayes-rate-smoothing-lab.ipynb",180],["ensemble-transform-kalman-filter-lab.ipynb",180],["gnss-dual-frequency-combinations-lab.ipynb",180],["gnss-geometry-free-cycle-slip-lab.ipynb",180],["gnss-integer-ambiguity-search-lab.ipynb",180],["gnss-lambda-integer-ambiguity-lab.ipynb",180],["gnss-melbourne-wubbena-cycle-slip-lab.ipynb",180],["gnss-residual-raim-fde-lab.ipynb",180],["graph-fused-spatial-regression-lab.ipynb",180],["harris-market-potential-lab.ipynb",180],["kalman-temporal-filtering-lab.ipynb",180],["least-squares-collocation-lab.ipynb",180],["median-polish-lab.ipynb",180],["mesh-geodesics-lab.ipynb",180],["moran-eigenvector-filtering-lab.ipynb",180],["multi-criteria-shortest-paths-lab.ipynb",180],["multiple-testing-corrections-lab.ipynb",180],["network-cascading-overload-lab.ipynb",180],["network-edge-failure-and-reliability-lab.ipynb",180],["network-percolation-resilience-lab.ipynb",180],["nonlinear-kalman-ekf-ukf-lab.ipynb",180],["nonnegative-matrix-factorization-lab.ipynb",180],["point-pattern-second-order-statistics-lab.ipynb",180],["rasterization-algorithms-lab.ipynb",180],["regional-beta-convergence-lab.ipynb",180],["regional-distribution-dynamics-lab.ipynb",180],["regional-gravity-ppml-lab.ipynb",180],["gravity-flow-models-lab.ipynb",180],["terrain-travel-time-lab.ipynb",180],["spatial-and-spacetime-kde-lab.ipynb",180],["spatial-distribution-summaries-lab.ipynb",180],["spatial-inequality-lab.ipynb",180],["spatial-thin-plate-spline-lab.ipynb",180],["stl-seasonal-trend-decomposition-lab.ipynb",180],["temporal-models-lab.ipynb",180],["tensor-train-decomposition-and-completion-lab.ipynb",180],["third-order-tensor-svd-lab.ipynb",180],["tucker-hosvd-tensor-decomposition-lab.ipynb",180],["voronoi-point-intensity-lab.ipynb",180],["weighted-head-banging-lab.ipynb",180],["k-medoids-clara-lab.ipynb",180],["hansen-hurwitz-lab.ipynb",180]]

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--shard-count", type=int, default=1)
    parser.add_argument("--shard-index", type=int, default=0)
    args = parser.parse_args(argv)
    selected = select_notebooks(NOTEBOOKS, args.shard_count, args.shard_index)
    print(f"Executing notebook shard {args.shard_index}/{args.shard_count}: {len(selected)} notebooks")
    root = Path.cwd().resolve()
    output = Path("/tmp/notebook-output")
    output.mkdir(parents=True, exist_ok=True)
    for filename, timeout in selected:
        source = root / "notebooks" / filename
        if not source.is_file():
            raise FileNotFoundError(source)
        notebook = nbformat.read(source, as_version=4)
        # Notebook cells historically use both repository-root-relative and
        # notebook-directory-relative package paths. Make every first-party
        # Python implementation package available to the kernel so either
        # convention resolves consistently without changing notebook semantics.
        package_root = root / "implementations" / "python"
        package_paths = sorted(
            path for path in package_root.iterdir() if path.is_dir()
        ) if package_root.is_dir() else []
        bootstrap = nbformat.v4.new_code_cell(
            "import sys\n"
            + "from pathlib import Path\n"
            + "for package_path in " + repr([str(p.resolve()) for p in package_paths]) + ":\n"
            + "    sys.path.insert(0, package_path)\n"
        )
        notebook.cells.insert(0, bootstrap)
        executor = ExecutePreprocessor(timeout=timeout)
        try:
            executor.preprocess(notebook, {"metadata": {"path": str(root / "notebooks")}})
        finally:
            nbformat.write(notebook, output / filename)

if __name__ == "__main__":
    main()
