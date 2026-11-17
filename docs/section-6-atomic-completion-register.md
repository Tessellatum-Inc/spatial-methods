# Section 6 atomic completion register

**Source:** *Spatial Analysis Algorithms: Complete Compendium*, Section 6, pages 10–11.  
**Intake:** [preserved pages 6–10](../source-inventory/pages-06-10.md) and [pages 11–15](../source-inventory/pages-11-15.md).  
**Section index:** [Section 6 catalogue record](../catalog/sections/06-optimization-mobility-transport.md).

This register separates optimisation problems, exact algorithms, heuristics, behavioural models, metrics and software. Use the [verification protocol](../catalog/verification-protocol.md) and [completion standard](compendium-completion-standard.md).

| Status | Meaning |
|---|---|
| Open | No item-specific independent evidence recorded. |
| Partial | A bounded related implementation exists; variants or validation remain open. |
| Verify | Exact method, formulation or software version must be resolved. |
| Not applicable | A broad workflow or platform is not a standalone algorithm. |

## Atomic source register

### Location-allocation and spatial optimisation — page 10

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S06-LO-01 | p-median | Facility location optimisation | Partial | Define demand weights, candidate sites and assignment; test exact small instances. |
| S06-LO-02 | p-center | Facility location optimisation | Partial | Define min-max objective and service metric; test exact small instances. |
| S06-LO-03 | p-dispersion | Facility location optimisation | Open | Define separation objective and selected-site constraints; test ties and infeasibility. |
| S06-LO-04 | Set covering | Facility location optimisation | Partial | Define coverage radius and candidate set; compare greedy and exact solutions. |
| S06-LO-05 | Maximal Covering Location Problem (MCLP) | Facility location optimisation | Partial | Define budget and partial demand coverage; test exact binary model. |
| S06-LO-06 | MEXCLP | Probabilistic facility location | Partial | Existing `mexclp` package exactly enumerates small-instance unit placements under a common or candidate-specific independent busy-fraction assumption, including co-location and diminishing expected coverage. Tests cover hand calculations, heterogeneous busy fractions, zero units, deterministic ties and validation. It is not the adjusted/dependent MEXCLP correction or a hypercube queueing model; large-instance optimisation and dependence calibration remain open. |
| S06-LO-07 | MALP | Probabilistic facility location | Verify | Resolve exact maximal availability location problem variant and source. |
| S06-LO-08 | BACOP | Facility location model | Verify | Resolve acronym and exact formulation; do not infer from shorthand. |
| S06-LO-09 | Hypercube queuing model | Queueing/location model | Verify | Verify dispatch/availability assumptions and approximation; compare simulation. |
| S06-LO-10 | Capacitated facility location | Facility location optimisation | Partial | Define capacities, fixed costs and assignment; test infeasible cases. |
| S06-LO-11 | Hub location | Network location optimisation | Partial | Split p-hub median/centre and uncapacitated/capacitated variants. |
| S06-LO-12 | p-hub median | Hub location optimisation | Verify | Verify flow routing and hub cost structure; test exact small instances. |
| S06-LO-13 | Hierarchical facility location | Facility location family | Open | Define facility tiers and assignment hierarchy; test capacity and service constraints. |
| S06-LO-14 | Stochastic facility location | Stochastic optimisation | Open | Define scenarios, recourse and probability; test sample-average convergence. |
| S06-LO-15 | Robust facility location | Robust optimisation | Open | Define uncertainty set and robustness criterion; quantify price of robustness. |
| S06-LO-16 | Redistricting | Spatial partition optimisation | Open | Define population/election constraints and legal context; distinguish algorithms from metrics. |
| S06-LO-17 | ReCom | Redistricting Markov-chain method | Verify | Verify recombination proposal, spanning-tree cut and reversibility; test chain diagnostics. |
| S06-LO-18 | MCMC redistricting | Sampling method | Open | Define state space, proposal, target distribution and constraints; test mixing. |
| S06-LO-19 | Flip redistricting | Local Markov-chain proposal | Verify | Verify boundary-unit flip rules and connectivity preservation. |
| S06-LO-20 | Polsby–Popper compactness | District compactness metric | Partial | Define perimeter/area and geometry units; document sensitivity to boundary detail. |
| S06-LO-21 | Reock compactness | District compactness metric | Partial | Define minimum enclosing circle and area ratio; test elongated/concave shapes. |
| S06-LO-22 | Schwartzberg compactness | District compactness metric | Partial | Existing `districting-compactness` package computes the perimeter/equal-area-circle circumference ratio from a planar simple exterior ring and tests analytic square/circle-like fixtures, orientation and ring-closure invariance. Holes, multipart/geodesic geometry, legal constraints and source-specific convention checks remain open. |
| S06-LO-23 | Territory design | Spatial partitioning family | Open | Define contiguity, balance, workload and compactness objectives. |
| S06-LO-24 | Set partitioning | Combinatorial optimisation | Partial | Define exact-cover constraints and column generation interface; test infeasibility. |
| S06-LO-25 | Land-use allocation | Spatial allocation workflow | Open | Define demand, suitability, transition and competing uses; test conservation and constraints. |
| S06-LO-26 | Marxan reserve design | Conservation optimisation software | Verify | Pin version and objective/penalty settings; document input feature/cost semantics. |
| S06-LO-27 | Art gallery problem | Visibility optimisation problem | Open | Define polygon domain, guard type and coverage; distinguish exact/approximation results. |
| S06-LO-28 | Sensor placement | Sensor network optimisation | Partial | Define coverage, information and cost objectives; test network observability. |
| S06-LO-29 | Camera placement | Visibility/facility optimisation | Open | Define field of view, occlusion and privacy constraints; test coverage. |
| S06-LO-30 | Cell tower siting | Telecommunications facility location | Open | Define propagation, capacity and interference; validate against RF models. |
| S06-LO-31 | Genetic algorithms | Metaheuristic | Partial | Define encoding, operators and selection; benchmark convergence and reproducibility. |
| S06-LO-32 | Simulated annealing | Metaheuristic | Partial | Define neighbourhood, cooling and acceptance; test schedule sensitivity. |
| S06-LO-33 | NSGA-II | Multiobjective evolutionary algorithm | Verify | Verify nondominated sorting/crowding and constraints; test benchmark fronts. |
| S06-LO-34 | Particle swarm optimisation | Metaheuristic | Partial | Define topology, inertia and boundary handling; test convergence and seed variance. |
| S06-LO-35 | Ant colony optimisation | Metaheuristic | Partial | Define pheromone update and heuristic; test stagnation and parameter sensitivity. |
| S06-LO-36 | Tabu search | Metaheuristic | Partial | Define tabu tenure, aspiration and neighbourhood; benchmark reproducibly. |
| S06-LO-37 | GRASP | Metaheuristic | Verify | Verify construction/local-search phases and restricted candidate list; test stability. |
| S06-LO-38 | Variable neighbourhood search | Metaheuristic | Partial | Define neighbourhood sequence and shaking; test stopping and local optimality. |
| S06-LO-39 | Matheuristics | Hybrid optimisation family | Open | Specify mathematical programming/heuristic coupling; report bounds and gaps. |
| S06-LO-40 | Branch-and-bound | Exact optimisation framework | Partial | Define relaxations, branching and bounds; test optimality certificates. |
| S06-LO-41 | Lagrangian relaxation | Mathematical optimisation method | Partial | Define relaxed constraints and dual bounds; test primal recovery. |
| S06-LO-42 | Benders decomposition | Mathematical optimisation method | Verify | Verify master/subproblem cuts and convergence; test feasibility cuts. |
| S06-LO-43 | Min-cost flow | Network optimisation | Partial | Define capacities, supplies/demands and costs; compare with LP oracle. |
| S06-LO-44 | Transportation problem | Linear optimisation problem | Partial | Define balanced/unbalanced supplies and demands; test duality. |
| S06-LO-45 | Assignment problem | Combinatorial optimisation | Partial | Define square/rectangular and forbidden assignments; compare with brute force. |
| S06-LO-46 | Hungarian algorithm | Exact assignment algorithm | Partial | Verify potential/augmenting path formulation and complexity; test rectangular cases. |
| S06-LO-47 | Quantum annealing | Emerging optimisation platform | Verify | Distinguish hardware/software and QUBO formulation; document embedding and solution quality. |
| S06-LO-48 | Quantum Approximate Optimization Algorithm (QAOA) | Quantum optimisation algorithm | Verify | Verify circuit/ansatz and approximation objective; treat practical geospatial utility as experimental. |

### Logistics — page 10

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S06-LOG-01 | Multi-depot VRP | Vehicle routing problem | Partial | Define depot assignment, fleet and capacities; test exact small instances. |
| S06-LOG-02 | Periodic routing | Routing problem family | Open | Define service days, frequency and periodicity; test multi-day feasibility. |
| S06-LOG-03 | Inventory-routing | Integrated optimisation problem | Open | Define inventory dynamics, replenishment and route decisions; test conservation. |
| S06-LOG-04 | Drone-truck routing | Synchronised routing problem | Open | Define rendezvous, payload, endurance and launch/recovery; test schedule feasibility. |
| S06-LOG-05 | School bus routing | Routing optimisation | Open | Define students, stops, capacity, ride time and school windows; test feasibility. |
| S06-LOG-06 | Snow-plow arc routing | Arc routing problem | Open | Define required road segments, depots and service direction; test route coverage. |
| S06-LOG-07 | Waste collection arc routing | Arc routing problem | Partial | Define required edges, capacities and disposal trips; test route feasibility. |
| S06-LOG-08 | Ride-hailing dispatch | Dynamic assignment/dispatch | Open | Define requests, drivers, pooling and fairness; evaluate wait and deadhead distance. |
| S06-LOG-09 | Bike rebalancing | Inventory-routing problem | Open | Define station inventory, vehicle capacity and demand uncertainty; test stockouts. |
| S06-LOG-10 | ETA prediction with WDR | Travel-time prediction model | Verify | Resolve exact WDR model/source and inputs; test temporal/geographic generalisation. |
| S06-LOG-11 | DeepTTE | Travel-time prediction architecture | Verify | Verify paper/model and route representation; test calibration and route-length bias. |
| S06-LOG-12 | GNN travel-time prediction | Graph ML model family | Open | Split architectures and graph construction; test unseen routes and temporal drift. |
| S06-LOG-13 | OR-Tools | Optimisation software library | Verify | Pin version and routing solver semantics; document licence and search limits. |

### Accessibility and spatial interaction — page 10

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S06-AC-01 | Gravity model | Spatial interaction model | Partial | Define mass/impedance and constraints; compare with observed flows. |
| S06-AC-02 | Huff model | Probabilistic destination choice model | Partial | Define attractiveness/impedance and calibration; test market-share normalisation. |
| S06-AC-03 | Hansen accessibility | Accessibility metric | Partial | Define opportunities and impedance; test units and thresholds. |
| S06-AC-04 | Reilly's law | Retail gravitation model | Verify | Verify break-point formula and assumptions; compare with Huff model. |
| S06-AC-05 | 2SFCA | Two-Step Floating Catchment Area | Partial | Define catchment and supply/demand ratio; test zero supply and overlapping catchments. |
| S06-AC-06 | E2SFCA | Enhanced 2SFCA | Partial | Existing `floating-catchment` package implements two-step FCA and E2SFCA with caller-supplied increasing distance-zone upper bounds and non-negative zone weights, plus explicit Gaussian, power-law and Epanechnikov decay kernels. Tests cover hand calculations, inclusive zone boundaries, zero-safe denominators, monotone kernels and compact support. Network impedance, competition choice, capacity, uncertainty and exact published variant verification remain open. |
| S06-AC-07 | 3SFCA | Three-Step Floating Catchment Area | Verify | Resolve exact variant and step sequence; verify supply/demand competition. |
| S06-AC-08 | M2SFCA | Modified 2SFCA | Verify | Identify exact modification and source; do not infer from acronym. |
| S06-AC-09 | G2SFCA | Gaussian 2SFCA variant | Verify | Verify Gaussian decay and parameterisation. |
| S06-AC-10 | KD2SFCA | Kernel-density 2SFCA variant | Verify | Verify kernel and catchment semantics; test normalization. |
| S06-AC-11 | Cumulative opportunities accessibility | Accessibility metric | Partial | Define threshold and opportunity count; test multimodal travel times. |
| S06-AC-12 | Impedance decay functions | Accessibility model family | Partial | Split exponential, power, Gaussian and empirically calibrated forms. |
| S06-AC-13 | Radiation model | Spatial interaction model | Verify | Verify intervening-opportunities derivation and parameter-free assumptions; test flows. |
| S06-AC-14 | Intervening opportunities model | Spatial interaction model | Partial | Resolve Stouffer/Schneider variants; define opportunities and distance. |
| S06-AC-15 | Origin-destination flow models | Interaction model family | Open | Split gravity, radiation, entropy and econometric models; specify constraints. |
| S06-AC-16 | Accessibility Gini | Equity metric | Partial | Define population weighting and accessibility distribution; test decomposition. |
| S06-AC-17 | Accessibility Lorenz curve | Equity visualisation/metric | Partial | Define cumulative population/opportunity weighting; test ordering and area. |
| S06-AC-18 | Drive-time trade area | Retail catchment workflow | Open | Define network travel time, competition and time of day; validate with customers. |
| S06-AC-19 | Huff trade area | Retail catchment model | Partial | Cross-link Huff model; define store attractiveness and calibration. |
| S06-AC-20 | Analog trade area | Retail catchment workflow | Open | Define comparable store/market and similarity; validate transferability. |
| S06-AC-21 | Cannibalisation analysis | Retail spatial analysis | Open | Define store overlap and incremental sales; distinguish correlation from causal effect. |
| S06-AC-22 | Retail gravity | Spatial interaction family | Open | Identify exact formulation and market assumptions; test against observed visits. |
| S06-AC-23 | 15-minute city metrics | Accessibility metric family | Open | Define destination categories, network mode and threshold; audit distributional equity. |

### Transport planning — pages 10–11

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S06-TP-01 | Four-step trip generation | Transport demand model | Partial | Define trip purpose, rates and calibration; validate against counts/surveys. |
| S06-TP-02 | Gravity trip distribution | Transport demand model | Partial | Cross-link gravity models; document balancing and impedance. |
| S06-TP-03 | Multinomial logit mode choice | Discrete choice model | Partial | Define utility, IIA and estimation; test probabilities and elasticities. |
| S06-TP-04 | Nested logit mode choice | Discrete choice model | Verify | Define nest structure and inclusive value; test consistency conditions. |
| S06-TP-05 | Traffic assignment | Network equilibrium workflow | Partial | Define user/system optimum and capacity functions; test conservation. |
| S06-TP-06 | User equilibrium | Traffic assignment equilibrium | Verify | Define Wardrop conditions and convergence; test Beckmann formulation where applicable. |
| S06-TP-07 | Frank–Wolfe traffic assignment | Convex optimisation algorithm | Verify | Verify line search and all-or-nothing assignment; test convergence gap. |
| S06-TP-08 | Wardrop equilibrium | Equilibrium principle | Not applicable | State first/second principles; distinguish behavioural condition from solver. |
| S06-TP-09 | Dynamic traffic assignment | Traffic model family | Open | Split within-day and day-to-day; define time-dependent network loading. |
| S06-TP-10 | Cell Transmission Model (CTM) | Traffic flow simulation | Verify | Verify discretisation, CFL condition and sending/receiving flows; test shockwaves. |

### Activity-based simulation and traffic forecasting — page 11

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S06-AS-01 | MATSim | Agent-based transport simulation software | Verify | Pin release and modules; document demand, replanning and scoring. |
| S06-AS-02 | SUMO | Traffic simulation software | Verify | Pin release and network/route semantics; document calibration. |
| S06-AS-03 | ActivitySim | Activity-based travel model software | Verify | Pin version and model components; document synthetic population and validation. |
| S06-AS-04 | UrbanSim | Urban simulation platform | Verify | Identify current project/version and model architecture; document dependencies/licence. |
| S06-AS-05 | Intelligent Driver Model (IDM) | Car-following model | Verify | Verify acceleration/deceleration/headway parameters; test equilibrium and stability. |
| S06-AS-06 | Gipps car-following model | Car-following model | Verify | Verify safe-speed equation and parameter constraints; test collision avoidance. |
| S06-AS-07 | OD estimation from counts | Inverse transport model | Open | Define link counts, priors and regularisation; test identifiability. |
| S06-AS-08 | GTFS processing | Transit data workflow | Partial | Define static feed version and validation; test calendar, transfers and stop times. |
| S06-AS-09 | Transit accessibility | Accessibility workflow | Partial | Cross-link Section 18; define timetable/frequency and population weighting. |
| S06-AS-10 | Crash hotspot analysis | Road safety spatial analysis | Partial | Define exposure denominator and spatial dependence; avoid raw count ranking. |
| S06-AS-11 | Empirical Bayes crash screening | Road safety estimation | Verify | Verify safety performance function and prior; test regression-to-mean correction. |
| S06-AS-12 | DCRNN | Traffic forecasting architecture | Verify | Verify diffusion convolution and recurrent unit; test temporal/spatial splits. |
| S06-AS-13 | STGCN | Traffic forecasting architecture | Verify | Verify temporal gated convolution and graph convolution; reproduce baseline. |
| S06-AS-14 | Graph WaveNet | Traffic forecasting architecture | Verify | Verify adaptive adjacency and dilated convolutions; test graph generalisation. |
| S06-AS-15 | ASTGCN | Traffic forecasting architecture | Verify | Verify attention components and temporal windows; document variants. |
| S06-AS-16 | GMAN | Traffic forecasting architecture | Verify | Verify transform attention and spatiotemporal embeddings; reproduce. |
| S06-AS-17 | PDFormer | Traffic forecasting architecture | Verify | Verify propagation-delay-aware attention; document input graph. |
| S06-AS-18 | STID | Traffic forecasting architecture | Verify | Verify spatial-temporal identity embeddings and exact version; compare baselines. |

### Supplementary descriptive inequality diagnostics\n\nThe existing Section 6 entries S06-AC-16 (Accessibility Gini) and S06-AC-17 (Accessibility Lorenz curve) remain **Partial**: adding more indices does not complete their source-specific verification or decomposition requirements. The shared [accessibility-equity implementation](../implementations/python/accessibility-equity/README.md) now also includes population-weighted Atkinson and Theil T diagnostics as complementary measures. Their parameter/zero-value conventions are documented and tested; these additions do not change the source-entry status.\n\n## Completion gates

1. Every optimisation formulation must define decision variables, objective, constraints, units and feasibility conditions.
2. Exact methods require optimality certificates or small-instance exhaustive oracles; heuristics require seeds, stopping rules, gaps and sensitivity.
3. Accessibility and choice models require explicit impedance, opportunity, population, mode and equity assumptions.
4. Simulation/forecasting must use temporally and geographically blocked validation, calibration and transparent baselines.
5. Operational software integrations must pin versions, licences and data requirements; package availability is not method verification.
6. Reconcile canonical records, implementations, tests, notebooks and coverage dashboards only after evidence is recorded.

**Current conclusion:** Section 6 is atomised into auditable child records. It remains open; this register is not proof of complete optimisation, simulation or transport-model coverage.
