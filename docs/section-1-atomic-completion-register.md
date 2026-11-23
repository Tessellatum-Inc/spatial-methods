# Section 1 atomic completion register

**Source:** *Spatial Analysis Algorithms: Complete Compendium*, Section 1, pages 1–2.  
**Intake:** [preserved pages 1–5 transcription](../source-inventory/pages-01-05.md).  
**Section index:** [Section 1 catalogue record](../catalog/sections/01-core-gis.md).

This register separates source groupings into child records. It is not a claim that every variant has a canonical lesson, implementation, independent test or verified reference. Follow the [source-entry verification protocol](../catalog/verification-protocol.md) and [compendium completion standard](compendium-completion-standard.md).

## Status vocabulary

| Status | Meaning |
|---|---|
| Open | No item-specific independent evidence recorded in this register. |
| Partial | A bounded related implementation exists; variants or validation remain open. |
| Verify | Exact method, variant, standard or software identity must be resolved. |
| Not applicable | A model family, data format or workflow needs a different record type. |

## Atomic source register

### Vector and computational geometry — page 1

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S01-GE-01 | Buffer | Geometry operation | Partial | Define planar/geodesic, cap/join and negative-buffer semantics; test topology and CRS. |
| S01-GE-02 | Clip | Overlay operation | Partial | Test mixed geometry, boundaries, empty results and precision model. |
| S01-GE-03 | Intersection | Overlay operation | Partial | Test polygon/line/point dimensions, invalid inputs and robustness. |
| S01-GE-04 | Union | Overlay operation | Partial | Verify cascaded and unary variants, precision and geometry collections. |
| S01-GE-05 | Difference | Overlay operation | Partial | Test holes, shared boundaries and precision robustness. |
| S01-GE-06 | Dissolve | Aggregation/overlay operation | Partial | Define grouping and topology semantics; test multipart and invalid inputs. |
| S01-GE-07 | Centroid | Geometric metric | Partial | Distinguish centroid by dimension and centroid-of-mass; test degenerate geometries. |
| S01-GE-08 | Minimum bounding geometry | Geometry operation family | Partial | Tested planar baselines cover convex hull, minimum-area oriented rectangle (including a rotating-calipers sweep) and smallest enclosing circle; the broader family still needs distinct envelope/output contracts, robust degeneracy handling and source-level verification. |
| S01-GE-09 | Graham scan convex hull | Hull algorithm | Partial | Test collinear points, duplicates, orientation and complexity. |
| S01-GE-10 | Jarvis march convex hull | Hull algorithm | Partial | Test collinear/extreme-point ties and output orientation. |
| S01-GE-11 | Quickhull | Hull algorithm | Partial | Verify 2D/3D variants, degeneracies and worst-case behaviour. |
| S01-GE-12 | Alpha shapes / concave hull | Shape reconstruction | Partial | Define alpha parameter and singular simplices; test disconnected/degenerate cases. |
| S01-GE-13 | Fortune sweep Voronoi | Voronoi algorithm | Partial | Verify event queue/beach line and degeneracy handling; compare with Delaunay dual. |
| S01-GE-14 | Bowyer–Watson Delaunay | Triangulation algorithm | Partial | A dependency-free incremental 2D teaching baseline now uses exact rational orientation/in-circle predicates, a temporary super-triangle and cavity-boundary retriangulation; tests cover orientation, Euler triangle counts, empty circumcircles, seeded clouds, cocircular insertion, duplicate/invalid/collinear inputs and removal of super-triangle faces: [package](../implementations/python/bowyer-watson/README.md), [verification](../catalog/verification/bowyer-watson.md). Efficient point location/adjacency, constrained segments, holes, refinement, full degeneracy handling and independent source-variant review remain open. |
| S01-GE-15 | Incremental Delaunay triangulation | Triangulation family | Partial | Define insertion order and point location; test exact empty-circle property. |
| S01-GE-16 | Divide-and-conquer Delaunay | Triangulation algorithm | Open | Verify merge procedure and robust predicates; compare with independent oracle. |
| S01-GE-17 | Constrained Delaunay triangulation | Triangulation algorithm | Partial | A dependency-free exact-rational Lawson-flip baseline triangulates one simple polygon ring, preserves boundary constraints, and accepts non-crossing interior diagonals between existing vertices; tests cover area preservation, local weak-Delaunay legality, boundary/diagonal incidence, concavity, clockwise closure, collinear normalization and invalid/crossing constraints: [package](../implementations/python/constrained-delaunay/README.md). Holes, Steiner points, general PSLG segment recovery, refinement and production-scale adjacency remain unsupported. |
| S01-GE-18 | Ruppert refinement | Mesh refinement algorithm | Partial | Verify termination/quality assumptions and encroachment rules; test minimum angles. |
| S01-GE-19 | Ray-casting point-in-polygon | Point location predicate | Partial | Tested O(n) even–odd ray crossing reports inside/outside/boundary separately; an exact-rational variant now uses division-free orientation signs for decimal inputs, with tests for near-boundary values, large integer coordinates, concavity, horizontal edges and vertex ties: [package](../implementations/python/point-in-polygon/README.md). Single simple planar rings only; holes, multipolygons, self-intersections and topology validation remain open. |
| S01-GE-20 | Winding-number point-in-polygon | Point location predicate | Partial | Floating and exact-rational signed winding-number functions and nonzero-fill classifiers report boundary separately; exact variants use rational orientation predicates and are cross-checked against even–odd classification on seeded simple rings: [package and tests](../implementations/python/point-in-polygon/README.md). Self-intersecting compound paths, holes and topology validation remain outside the current contract. |
| S01-GE-21 | Slab-method point location | Point location data structure/algorithm | Partial | Static x-slab locator for valid pairwise interior-disjoint polygon faces, explicit boundary/outside results and seeded differential tests; worst-case quadratic storage/construction and event-line fallback remain documented limitations. |
| S01-GE-22 | Trapezoidal map point location | Point location structure | Partial | Bounded randomized prototype for pairwise-disjoint non-vertical segments in general position, with corridor replacement, persistent history-DAG queries and differential slab-oracle tests; it does not claim Seidel's expected construction bound or fully local neighbour maintenance. |
| S01-GE-23 | Bentley–Ottmann segment intersection | Sweep-line algorithm | Partial | Test vertical/overlapping/collinear segments and event tie ordering. |
| S01-GE-24 | Sutherland–Hodgman clipping | Polygon clipping algorithm | Partial | State convex clip-window assumption; test concavity and boundary cases. |
| S01-GE-25 | Weiler–Atherton clipping | Polygon clipping algorithm | Verify | Verify entry/exit traversal and holes; test concave/multipart cases. |
| S01-GE-26 | Vatti clipping | Polygon clipping algorithm | Verify | Verify scanbeam implementation, fill rules and self-intersections. |
| S01-GE-27 | Greiner–Hormann clipping | Polygon clipping algorithm | Verify | Verify intersection-node traversal and degeneracy limits. |
| S01-GE-28 | Clipper offsetting | Polygon offset algorithm/software | Verify | Pin Clipper version, join/end types, fill rules and licence; test self-intersection cleanup. |
| S01-GE-29 | Cascaded union | Overlay optimisation | Partial | Verify STR-tree batching and topology equivalence with unary union. |
| S01-GE-30 | Self-intersection repair | Geometry repair workflow | Partial | Separate make-valid algorithms and heuristics; document dimensional collapse. |
| S01-GE-31 | Geometry validity checking | Predicate/standard | Partial | Verify OGC validity rules by geometry type and version; test invalid rings/collections. |
| S01-GE-32 | Douglas–Peucker simplification | Line simplification algorithm | Partial | Test Hausdorff deviation, endpoints and topology failure. |
| S01-GE-33 | Visvalingam simplification | Line simplification algorithm | Partial | Verify effective-area weighting and threshold semantics. |
| S01-GE-34 | Topology-preserving simplification | Simplification algorithm family | Partial | Identify exact algorithm and topology guarantees; test shared boundaries. |
| S01-GE-35 | Snap rounding | Robust precision algorithm | Partial | Verify hot-pixel model and precision grid; test intersection preservation. |
| S01-GE-36 | Ear clipping | Polygon triangulation algorithm | Partial | Test orientation, holes (bridging separately), collinear vertices and degeneracy. |
| S01-GE-37 | Trapezoidal polygon decomposition | Polygon decomposition | Open | Define decomposition objective and sweep algorithm; test monotone pieces. |
| S01-GE-38 | Convex decomposition | Polygon decomposition family | Partial | Separate approximate/exact methods and objective; test partition coverage. |
| S01-GE-39 | Medial axis | Geometric skeleton | Partial | Define exact/approximate skeleton and boundary sampling; test stability. |
| S01-GE-40 | Straight skeleton | Geometric skeleton algorithm | Verify | Verify wavefront definition, weighted/unweighted variants and degeneracies. |
| S01-GE-41 | Minkowski sum | Configuration-space geometry operation | Partial | Define polygon/segment/circle operands and approximation; test convex/nonconvex cases. |
| S01-GE-42 | Hausdorff distance | Geometry metric | Partial | Define directed/symmetric and continuous/discrete variants; test outliers. |
| S01-GE-43 | Fréchet distance | Curve similarity metric | Partial | Separate continuous/discrete variants; test parameterisation and monotonicity. |
| S01-GE-44 | Rotating calipers | Computational geometry technique | Partial | Identify supported outputs (diameter, width, rectangle); test convexity assumptions. |
| S01-GE-45 | Welzl smallest enclosing circle | Enclosing-circle algorithm | Partial | Verify randomized incremental algorithm, degeneracies and deterministic seeding. |
| S01-GE-46 | Largest empty circle | Geometric optimisation problem | Partial | Tested additive-tolerance branch-and-bound baseline maximises nearest-site clearance with centre constrained to the sites' convex hull; exact Voronoi candidates, arbitrary domains, obstacles and geodesic/weighted variants remain open. |
| S01-GE-47 | Pole of inaccessibility (polylabel) | Geometric optimisation algorithm | Partial | Verify priority queue bounds and tolerance; test holes and concavity. |
| S01-GE-48 | Oriented minimum bounding rectangle | Geometry metric/algorithm | Partial | Define minimum-area rectangle and tie handling; test degenerate hulls. |
| S01-GE-49 | Gabriel graph | Proximity graph | Partial | Test diameter-circle emptiness and duplicates; compare with Delaunay subgraph. |
| S01-GE-50 | Relative neighborhood graph | Proximity graph | Partial | Verify lune definition and tie handling; compare with MST inclusion. |
| S01-GE-51 | Beta-skeleton | Proximity graph family | Partial | Tested open-lune beta-skeleton for beta in [1,2], explicitly linking beta=1 to the Gabriel graph and beta=2 to the relative-neighbourhood graph under the package's convention; circle-based variants and broader beta conventions remain open. |
| S01-GE-52 | Yao graph | Proximity graph | Partial | Tested planar equal-angle cone partition, nearest selection, deterministic tie-breaking and undirected union; cone orientation variants and scalable/robust constructions remain open. |
| S01-GE-53 | Euclidean minimum spanning tree | Graph optimisation | Partial | Verify exact edge selection and degeneracy handling; test connectivity and cycle absence. |
| S01-GE-54 | Visibility polygon | Visibility algorithm | Partial | Define simple polygon/obstacle assumptions; test vertex degeneracies and holes. |
| S01-GE-55 | Funnel algorithm | Shortest path in simple polygonal domain | Partial | Define corridor/portal input; test shortest path against visibility graph oracle. |
| S01-GE-56 | Constructive solid geometry (CSG) | 3D modelling representation/workflow | Verify | Separate set operations, representation and evaluation; document robustness. |
| S01-GE-57 | BSP Boolean operations | 3D Boolean algorithm | Partial | Document convex planar polygon-soup limits; test coplanar and nonmanifold cases. |
| S01-GE-58 | DCEL overlay | Planar subdivision data structure/algorithm | Partial | Verify half-edge invariants and overlay construction; test face/edge consistency. |
| S01-GE-59 | Arrangements | Computational geometry structure | Open | Define curve family and arrangement construction; test intersections and face enumeration. |
| S01-GE-60 | Planarization | Graph geometry operation | Partial | Define crossing insertion and edge splitting; test multiway intersections and topology. |

### Spatial indexing and query processing — pages 1–2

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S01-ID-01 | R-tree | Spatial index | Partial | Verify insertion/split/search invariants and overlap metrics; test adversarial distributions. |
| S01-ID-02 | R*-tree | Spatial index variant | Verify | Verify forced reinsertion, split and choose-subtree; benchmark workload. |
| S01-ID-03 | R+-tree | Spatial index variant | Verify | Verify non-overlap decomposition and object duplication; test range/kNN queries. |
| S01-ID-04 | Hilbert R-tree | Spatial index variant | Verify | Verify Hilbert ordering and dynamic/static variant; test locality and update cost. |
| S01-ID-05 | STR bulk loading | Spatial index construction | Partial | Verify sort-tile-recursive packing and occupancy; compare query performance. |
| S01-ID-06 | Quadtree | Spatial index | Partial | Define point/region/PR variants and termination; test boundary assignment. |
| S01-ID-07 | Octree | 3D spatial index | Partial | Define cell split and sparse representation; test depth/precision. |
| S01-ID-08 | k-d tree | Spatial index | Partial | Verify construction, tie-breaking and nearest-neighbour pruning; test duplicates. |
| S01-ID-09 | Ball tree | Metric index | Partial | Verify node bounds and metric assumptions; test non-Euclidean distance. |
| S01-ID-10 | VP-tree | Metric index | Partial | Verify pivot/radius partition and pruning; test ties and metric validity. |
| S01-ID-11 | BSP tree | Spatial partition structure | Partial | Define splitting hyperplanes and polygon clipping; test depth and degeneracy. |
| S01-ID-12 | KD-B-tree | Spatial index | Verify | Resolve exact historical structure and source; do not conflate with kd-tree/B-tree. |
| S01-ID-13 | Grid File | Multidimensional index | Verify | Verify directory/linear scales and split strategy; test skew and update behaviour. |
| S01-ID-14 | Z-order / Morton code | Space-filling ordering | Partial | Define bit interleaving and coordinate quantisation; test locality limits. |
| S01-ID-15 | Hilbert curve indexing | Space-filling ordering | Partial | Verify orientation/rotation convention and dimensional variant; test encode/decode. |
| S01-ID-16 | Geohash | Spatial encoding | Partial | Verify alphabet, precision and neighbour handling; document rectangular cell distortion. |
| S01-ID-17 | H3 | Hierarchical global grid/index | Verify | Pin official version and API; test pentagons, hierarchy and area/edge semantics. |
| S01-ID-18 | S2 | Spherical cell hierarchy/index | Verify | Pin official version and projection/cell semantics; test face boundaries and hierarchy. |
| S01-ID-19 | Quadkeys | Tile addressing scheme | Partial | Define zoom/x/y encoding and coordinate convention; test boundary cases. |
| S01-ID-20 | HEALPix | Equal-area spherical pixelisation | Verify | Verify official scheme and indexing; test equal-area and neighbour properties. |
| S01-ID-21 | Range query | Spatial query operation | Partial | Define exact predicates and inclusive boundaries; test index-vs-scan equivalence. |
| S01-ID-22 | k-nearest-neighbour query | Spatial query algorithm | Partial | Define metric/ties and exactness; compare with brute-force oracle. |
| S01-ID-23 | Reverse kNN query | Spatial query algorithm | Partial | Exact planar 2D Euclidean baseline with inclusive kth-distance ties, one static k-d tree, strict closer-point counting and seeded differential tests against a quadratic oracle; geographic/network metrics, dynamic updates and a specialised subquadratic index remain open. |
| S01-ID-24 | Closest-pair query | Computational geometry query | Partial | Define duplicates and metric; compare with quadratic oracle. |
| S01-ID-25 | Spatial skyline | Spatial preference query | Partial | Exact block-nested-loop baseline combines squared planar Euclidean distance with explicitly minimised/maximised numeric attributes; identical criterion vectors are retained as ties and seeded tests compare with an independent exhaustive oracle. Indexed/large-scale, network-distance and textual variants remain open. |
| S01-ID-26 | Top-k spatial keyword query | Spatial/text query | Open | Define text relevance, distance aggregation and pruning; compare with exhaustive ranking. |
| S01-ID-27 | Geofencing | Spatial event/query workflow | Partial | Define geometry, boundary, temporal sampling and event debounce; test entry/exit transitions. |
| S01-ID-28 | Filter-and-refine spatial join | Spatial join algorithm | Partial | Verify candidate filter and exact refinement; compare with nested-loop oracle. |
| S01-ID-29 | Plane-sweep spatial join | Spatial join algorithm | Partial | Define sweep ordering and active structure; test touching/overlap semantics. |
| S01-ID-30 | PBSM spatial join | Partition-based join algorithm | Verify | Verify Partition-Based Spatial-Merge partitioning and duplicate suppression. |
| S01-ID-31 | TOUCH spatial join | Spatial join algorithm | Verify | Resolve exact TOUCH method and paper; verify partition and replication semantics. |
| S01-ID-32 | Partition-based spatial join | Spatial join family | Partial | Split grid/recursive partition variants; define skew and boundary replication. |
| S01-ID-33 | kNN join | Spatial join algorithm | Partial | Define all-pairs vs per-record kNN join and tie semantics; test brute force. |
| S01-ID-34 | Locality-sensitive hashing (LSH) | Approximate similarity search | Partial | Existing random-hyperplane cosine LSH is one family only; add Euclidean/p-stable and benchmark recall. |
| S01-ID-35 | HNSW | Approximate nearest-neighbour index | Open | Verify hierarchy/search construction; test recall, memory and updates. |
| S01-ID-36 | IVF-PQ | Approximate nearest-neighbour index | Open | Define coarse quantiser and product quantisation; test recall/latency/storage. |
| S01-ID-37 | ScaNN | Approximate nearest-neighbour system | Verify | Verify current algorithm/library and anisotropic quantisation; document integration/licence. |
| S01-ID-38 | ZM index | Learned spatial index | Verify | Resolve exact method/source and key model; test range query correctness. |
| S01-ID-39 | RSMI | Learned spatial index | Verify | Resolve acronym, architecture and exact paper; document data distribution assumptions. |
| S01-ID-40 | LISA | Learned spatial index | Verify | Verify exact method/version and spatial partition; test skew/generalisation. |
| S01-ID-41 | Selectivity estimation | Query optimisation statistic | Open | Define estimator and workload; measure cardinality error and plan impact. |
| S01-ID-42 | Spatial histograms | Query optimisation summary | Partial | Split histogram structures and estimators; test skew, correlation and resolution. |

### Proximity, topology and relations — page 2

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S01-PR-01 | Nearest neighbour | Proximity query | Partial | State metric/geometry semantics; test ties, invalid coordinates and index equivalence. |
| S01-PR-02 | Euclidean distance matrix | Distance computation | Partial | Define units/CRS and numerical precision; test symmetry and zero diagonal. |
| S01-PR-03 | Geodesic distance matrix | Geodesic computation | Partial | Define ellipsoid and algorithm; test antimeridian/near-antipodal cases. |
| S01-PR-04 | Spatial joins | Spatial query family | Partial | Split predicates and join strategies; test exact predicate semantics. |
| S01-PR-05 | DE-9IM | Topological relation model | Partial | Verify matrix semantics and dimension labels; test canonical geometry pairs. |
| S01-PR-06 | RCC-8 | Qualitative spatial relation calculus | Verify | Verify eight relations and domain assumptions; test composition constraints. |
| S01-PR-07 | Cardinal direction relations | Qualitative spatial relation model | Partial | Tested bounded 9-region cardinal-direction baseline using axis-aligned minimum bounding rectangles, with inverse-direction fixtures; this is not a full projection-based/centroid calculus, and composition, 3D and geographic semantics remain open. |
| S01-PR-08 | Contiguity spatial weights | Spatial weights construction | Partial | Separate rook/queen and order-k; define islands and row standardisation. |
| S01-PR-09 | Distance-band spatial weights | Spatial weights construction | Partial | Define threshold, units, CRS and symmetry; test disconnected units. |
| S01-PR-10 | kNN spatial weights | Spatial weights construction | Partial | Define ties, directed/symmetrised graph and standardisation; test islands/duplicates. |

### Network analysis — pages 1–2

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S01-NT-01 | Dijkstra shortest path | Graph algorithm | Partial | Verify nonnegative-weight contract and stale-queue handling; compare all-pairs oracle. |
| S01-NT-02 | A* shortest path | Heuristic search | Partial | Define admissible/consistent heuristic and units; test against Dijkstra. |
| S01-NT-03 | Bellman–Ford | Shortest-path algorithm | Partial | Test negative edges, negative cycles and unreachable vertices. |
| S01-NT-04 | Floyd–Warshall | All-pairs shortest path | Partial | Test negative cycles, infinity and path reconstruction. |
| S01-NT-05 | Bidirectional Dijkstra | Shortest-path speedup | Partial | Verify stopping condition and directed reverse graph; compare exact distances. |
| S01-NT-06 | ALT (A*, Landmarks, Triangle inequality) | Shortest-path speedup | Verify | Verify landmark preprocessing and admissible bounds; test directed graphs. |
| S01-NT-07 | Contraction Hierarchies | Shortest-path speedup | Verify | Verify contraction order, shortcuts and witness searches; compare exact routes. |
| S01-NT-08 | Hub labeling | Shortest-path index | Verify | Verify labels and canonical shortest-path cover; test preprocessing/query complexity. |
| S01-NT-09 | Customizable Route Planning | Shortest-path speedup | Verify | Verify customization/query phases and metric assumptions; test metric updates. |
| S01-NT-10 | Service areas and isochrones | Network accessibility workflow | Partial | Define edge interpolation and cutoff; test directed/time-dependent reachability. |
| S01-NT-11 | Many-to-many routing | Routing workload/algorithm family | Partial | Split one-to-many batching and specialised algorithms; benchmark exactness. |
| S01-NT-12 | Yen k-shortest loopless paths | k-shortest path algorithm | Partial | Verify candidate management and tie semantics; test against exhaustive paths. |
| S01-NT-13 | Alternative routes | Route-set generation family | Open | Define acceptable detour/diversity and overlap; distinguish from k-shortest paths. |
| S01-NT-14 | Betweenness centrality | Graph metric | Partial | Define normalisation, directed/weighted and approximation variants; test known graphs. |
| S01-NT-15 | Closeness centrality | Graph metric | Partial | Define disconnected graph correction and direction; test known graphs. |
| S01-NT-16 | PageRank | Link analysis algorithm | Partial | Define damping, dangling nodes and weighted/directed semantics; test convergence. |
| S01-NT-17 | Axial space syntax | Urban network representation/analysis | Verify | Define axial map construction and graph semantics; verify integration/choice. |
| S01-NT-18 | Space syntax integration | Network metric | Verify | Identify global/local integration definitions and normalisation. |
| S01-NT-19 | Street orientation | Network morphology metric | Partial | Define segment bearings and axial/directional treatment; test aggregation. |
| S01-NT-20 | Street circuity | Network morphology metric | Partial | Define network/Euclidean ratio and sampling; handle disconnected pairs. |
| S01-NT-21 | Intersection density | Network morphology metric | Partial | Define intersection degree and study area edge correction. |
| S01-NT-22 | Louvain community detection | Graph clustering algorithm | Partial | Verify modularity optimisation and resolution; test stability and disconnected graphs. |
| S01-NT-23 | Leiden community detection | Graph clustering algorithm | Partial | Verify refinement guarantees and objective; compare partitions on known graphs. |
| S01-NT-24 | Infomap | Flow-based community detection | Verify | Verify map equation and directed/weighted handling; test synthetic benchmarks. |
| S01-NT-25 | Label propagation | Graph clustering algorithm | Partial | Define asynchronous/synchronous updates and tie-breaking; test stochastic stability. |
| S01-NT-26 | Kernighan–Lin partitioning | Graph partition algorithm | Verify | Verify swap passes and objective; test balanced partitions. |
| S01-NT-27 | Spectral graph partitioning | Graph partition family | Partial | Define Laplacian and rounding; test disconnected and weighted graphs. |
| S01-NT-28 | METIS partitioning | Graph partition software/algorithm | Verify | Verify version, objective and licence; document integration and constraints. |
| S01-NT-29 | Maximum flow | Network optimisation | Partial | Define capacity and residual graph; compare with min-cut oracle. |
| S01-NT-30 | Minimum cut | Network optimisation | Partial | Define s-t/global cut and capacity semantics; test exhaustive small graphs. |
| S01-NT-31 | Minimum spanning tree | Graph optimisation | Partial | Verify Kruskal/Prim variants, ties and disconnected input. |
| S01-NT-32 | Steiner tree | Network optimisation problem | Partial | Exact Dreyfus–Wagner subset dynamic program with shortest-path closure for undirected weighted graphs and small terminal sets (default cap 12); exponential terminal dependence, directed/approximation variants and geometric Steiner trees remain open. |
| S01-NT-33 | k-core decomposition | Graph structure algorithm | Partial | Define core number and directed variants; test iterative peeling. |
| S01-NT-34 | HMM map matching | Probabilistic map matching | Partial | Define emission/transition models and candidate generation; test sparse/noisy traces. |
| S01-NT-35 | ST-Matching | Map matching algorithm | Verify | Verify exact algorithm and temporal constraints; compare with HMM baseline. |
| S01-NT-36 | IVMM | Map matching algorithm | Verify | Resolve exact name/version and route inference; test sparse sampling. |
| S01-NT-37 | Fast Map Matching | Map matching algorithm | Verify | Identify exact method/paper; benchmark runtime and matching quality. |
| S01-NT-38 | Neural map matching | Learned map matching family | Open | Split architectures/objectives and map inputs; test geographic transfer and calibration. |
| S01-NT-39 | RAPTOR | Public transit routing algorithm | Verify | Verify rounds, transfer semantics and timetable assumptions; compare with timetable oracle. |
| S01-NT-40 | Connection Scan Algorithm | Public transit routing algorithm | Verify | Verify connection ordering and transfer rules; test Pareto arrival/departure queries. |
| S01-NT-41 | Time-dependent routing | Routing problem family | Partial | Define FIFO/non-FIFO and time-dependent edge functions; test departure-time profiles. |
| S01-NT-42 | Stochastic routing | Routing problem family | Open | Define random travel-time model and risk objective; test expected/quantile path cost. |
| S01-NT-43 | Multimodal routing | Routing problem family | Partial | Define transfer graph, mode constraints and fares; test itinerary feasibility. |
| S01-NT-44 | Turn-restricted routing | Routing model | Partial | Define edge-based state and restriction encoding; test prohibited/penalised turns. |
| S01-NT-45 | Road network generalisation | Cartographic/network workflow | Partial | Define scale, connectivity and topology constraints; evaluate network preservation. |
| S01-NT-46 | Stroke generation | Network grouping algorithm | Partial | Define Gestalt criteria and thresholds; test intersections, loops and ambiguity. |

### Classic routing — page 2

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S01-CR-01 | 2-opt TSP improvement | Local-search heuristic | Partial | Verify symmetric/asymmetric delta and termination; compare with exact small instances. |
| S01-CR-02 | Lin–Kernighan TSP heuristic | TSP heuristic | Verify | Identify exact LK/LKH variant and move rules; benchmark known instances. |
| S01-CR-03 | Christofides algorithm | TSP approximation | Verify | Verify metric symmetric assumptions and 3/2 guarantee; test MST/matching construction. |
| S01-CR-04 | Clarke–Wright savings | Vehicle routing heuristic | Partial | Define parallel/sequential variants and capacity constraints; compare with exact CVRP. |
| S01-CR-05 | Sweep VRP heuristic | Vehicle routing heuristic | Partial | Define polar ordering and route split; test depot and capacity constraints. |
| S01-CR-06 | Chinese Postman Problem | Arc routing optimisation | Partial | Separate undirected/directed/mixed variants; test parity/connectivity and augmentation. |
| S01-CR-07 | Arc routing | Routing problem family | Open | Identify CARP and related formulations; define required/optional edges and service costs. |
| S01-CR-08 | Capacitated VRP (CVRP) | Vehicle routing optimisation | Partial | Define depot, demand, fleet and capacity; add exact small-instance oracle and feasibility tests. |
| S01-CR-09 | VRP with time windows (VRPTW) | Vehicle routing optimisation | Partial | Define hard/soft windows, service and waiting; test time feasibility and exact small cases. |
| S01-CR-10 | Pickup-and-delivery problem | Vehicle routing optimisation | Open | Define paired requests, precedence, capacity and time windows; test load feasibility. |
| S01-CR-11 | Dial-a-ride problem | Demand-responsive transport optimisation | Open | Define passenger time, ride-time and accessibility constraints; test feasibility. |
| S01-CR-12 | Adaptive Large Neighbourhood Search (ALNS) | Metaheuristic | Partial | Verify destroy/repair operator selection and acceptance; benchmark reproducibly. |
| S01-CR-13 | Column generation | Optimisation method | Partial | Define master/pricing problems and reduced costs; test LP bounds. |
| S01-CR-14 | Branch-and-price | Exact optimisation framework | Open | Define branching and pricing integration; test integrality and optimality certificates. |

## Completion gates

1. Resolve source wording to canonical names without losing the source label; keep variants as separate child records.
2. For geometry, test degeneracies, invalid inputs, precision and topology—not only ordinary fixtures.
3. For indexes and query processing, compare indexed answers with brute-force scans and measure update/query/storage trade-offs.
4. For graph and routing methods, use independent exact oracles on small graphs; state weight, direction, time, turn and feasibility assumptions.
5. For heuristics and approximate methods, report optimality gap/recall/error and reproducible seeds; do not imply exactness.
6. Verify external library versions, licences and standards; integrations are not original implementations.
7. Reconcile lessons, implementation contracts, tests, notebooks, verification records and catalogue only when evidence changes.

**Current conclusion:** Section 1 is atomised into child records. It remains open; the status labels are conservative triage, not a claim of completed verification.


## Implementation reconciliation — reverse k-nearest-neighbour query

The Section 1 reverse-kNN entry now links to an exact planar 2D Euclidean implementation. Its tie rule includes every data point for which the query has fewer than k strictly closer competitors. It builds a static k-d tree once, uses radius queries only to generate candidate competitors, and checks strict squared distances for membership. The package includes a separate quadratic oracle and seeded differential tests, including duplicates, ties, empty inputs and k greater than the data count. The source row moves from Open to Partial; geographic/network metrics, dynamic updates, a specialised subquadratic index and source/bibliography/rights verification remain outstanding.


## Implementation reconciliation — additional Section 1 methods

A cross-check of the Section 1 atomic register against its implementation-linked catalogue records identified nine existing, tested baselines that had remained incorrectly labelled Open at the atomic level. Their records now move to Partial, with explicit scope and limits:

- Minimum bounding geometry: convex hull, minimum-area oriented rectangle and smallest enclosing circle baselines.
- Slab point location: static locator for pairwise interior-disjoint polygon faces.
- Trapezoidal map: bounded general-position prototype with corridor replacement, persistent history-DAG queries and slab-oracle differential tests; no classic expected-bound claim.
- Largest empty circle: additive-tolerance branch-and-bound within the sites' convex hull.
- Beta-skeleton and Yao graph: specified lune-based beta convention and equal-angle cone baseline.
- Spatial skyline: exact block-nested-loop planar distance plus numeric-attribute Pareto frontier.
- Cardinal directions: bounded MBR 9-region relation.
- Steiner tree: exact Dreyfus–Wagner subset DP for small undirected terminal sets.

These are status reconciliations, not claims that the full grouped source families are complete. Source identity, primary bibliography, claim-by-claim review, broader variants and publication-rights checks remain outstanding.
