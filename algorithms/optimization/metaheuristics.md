# Metaheuristics for spatial optimisation

Metaheuristics are broad search strategies for finding useful solutions to difficult optimisation problems when exact optimisation is too expensive, unavailable or impractical for the required instance. They are not a single algorithm, and they do not all provide the same guarantees.

Spatial applications include facility location, districting, routing, sensor placement, land-use allocation, network design and multi-objective planning. The problem model still matters more than the search label: a metaheuristic needs a clearly defined feasible-solution representation, objective(s), constraints, neighbourhood or variation operators, stopping rule and validation method.

## A taxonomy of the methods named in the source

| Method | Search pattern | What distinguishes it | Important cautions |
|---|---|---|---|
| Genetic algorithms (GA) | Population-based evolutionary search | Encodes candidate solutions and applies selection, recombination and mutation | Representation and operators must preserve or repair feasibility; convergence and solution quality are problem-dependent |
| Simulated annealing (SA) | Single-trajectory stochastic local search | Sometimes accepts worsening moves according to a temperature-controlled probability | Cooling schedule, neighbourhood and scale strongly affect behaviour; finite runs do not guarantee a global optimum |
| NSGA-II | Multi-objective evolutionary algorithm | Uses non-dominated sorting, elitist parent/offspring selection and crowding-distance diversity | It is one specific MOEA, not a synonym for all genetic algorithms; objective scaling and constraint handling matter |
| Particle swarm optimisation (PSO) | Population-based swarm search | Particles update position and velocity using individual and social information | Continuous-space variants do not directly solve discrete spatial problems without a defensible encoding and update rule |
| Ant colony optimisation (ACO) | Population-based constructive search | Artificial ants build solutions using pheromone trails and heuristic desirability | Pheromone updates, evaporation and construction constraints are problem-specific; the original Ant System is one ACO variant |
| Tabu search | Memory-guided local search | Uses short-, intermediate- or long-term memory to discourage cycling and guide intensification/diversification | Tabu tenure, aspiration and neighbourhood design are substantive algorithm choices |
| GRASP | Multi-start construction plus local search | Repeatedly constructs a randomized greedy feasible solution, then locally improves it | Construction and local-search definitions depend on the target problem; iteration count affects effort |
| Variable neighbourhood search (VNS) | Systematic neighbourhood-changing search | Changes neighbourhood structures to escape local optima in one neighbourhood | Neighbourhood ordering, shaking and local-search choices define the actual variant |
| Matheuristics | Hybridisation of mathematical programming and heuristic search | Uses exact optimisation models/solvers inside or alongside heuristic components | This is a design family, not one canonical algorithm; the exact subproblem, solver limits and hybrid interface must be reported |

These methods are alternatives or components, not interchangeable drop-in solvers. For a facility-location model, for example, an exact mixed-integer model may be the right choice for small and medium instances; a metaheuristic may be useful for larger or more complex variants, but it must be compared against a valid objective and feasibility baseline.

## A responsible spatial-optimisation workflow

1. Define the decision variables, objective(s), constraints and units before selecting a search method.
2. Define a feasible encoding for the spatial problem. State whether geometry, contiguity, network connectivity, capacity, service thresholds or equity constraints are enforced during construction, repaired afterwards or only measured.
3. Choose a search family that matches the problem structure. Do not select an algorithm solely because it is popular.
4. Specify all stochastic controls: seed, population/replica count, initialisation, operators, neighbourhoods, cooling or pheromone schedules, stopping criteria and restart policy.
5. Validate feasibility independently of the search code. A low objective value is meaningless if the solution violates the model.
6. Compare with exact solutions on small instances, simple constructive baselines and multiple seeded runs. Report distributions and feasibility rates, not only the best run.
7. Separate tuning data from evaluation instances and document computational budget, hardware, solver version and parameter-selection procedure.
8. Test robustness to demand weights, network costs, spatial constraints and modelling assumptions. A metaheuristic does not repair a misspecified spatial model.

## What this repository currently provides

This page is a researched taxonomy and bibliographic entry point. It is **not** a claim that all nine methods have been implemented or reproduced here. The repository has separate exact and heuristic implementations for selected location, covering, routing and districting problems; those implementations must be evaluated under their own contracts.

No general-purpose GA, SA, NSGA-II, PSO, ACO, tabu-search, GRASP or VNS engine is claimed by this page. No single "best metaheuristic" is recommended. A future implementation should begin with one explicitly named spatial optimisation problem and one method variant, not a generic framework with an untestable promise.

## Primary and authoritative references

1. Holland, J. H. (1975). *Adaptation in Natural and Artificial Systems: An Introductory Analysis with Applications to Biology, Control, and Artificial Intelligence*. University of Michigan Press. Reprinted by MIT Press (1992). [MIT Press edition and DOI](https://doi.org/10.7551/mitpress/1090.001.0001).
2. Kirkpatrick, S., Gelatt, C. D., & Vecchi, M. P. (1983). Optimization by simulated annealing. *Science*, 220(4598), 671–680. [https://doi.org/10.1126/science.220.4598.671](https://doi.org/10.1126/science.220.4598.671).
3. Deb, K., Pratap, A., Agarwal, S., & Meyarivan, T. (2002). A fast and elitist multiobjective genetic algorithm: NSGA-II. *IEEE Transactions on Evolutionary Computation*, 6(2), 182–197. [https://doi.org/10.1109/4235.996017](https://doi.org/10.1109/4235.996017).
4. Kennedy, J., & Eberhart, R. (1995). Particle swarm optimization. *Proceedings of ICNN'95 – International Conference on Neural Networks*, 4, 1942–1948. IEEE. [https://doi.org/10.1109/ICNN.1995.488968](https://doi.org/10.1109/ICNN.1995.488968).
5. Dorigo, M., Maniezzo, V., & Colorni, A. (1996). Ant system: Optimization by a colony of cooperating agents. *IEEE Transactions on Systems, Man, and Cybernetics, Part B (Cybernetics)*, 26(1), 29–41. [https://doi.org/10.1109/3477.484436](https://doi.org/10.1109/3477.484436).
6. Glover, F. (1989). Tabu search—Part I. *ORSA Journal on Computing*, 1(3), 190–206. [https://doi.org/10.1287/ijoc.1.3.190](https://doi.org/10.1287/ijoc.1.3.190).
7. Feo, T. A., & Resende, M. G. C. (1995). Greedy randomized adaptive search procedures. *Journal of Global Optimization*, 6, 109–133. [https://doi.org/10.1007/BF01096763](https://doi.org/10.1007/BF01096763).
8. Mladenović, N., & Hansen, P. (1997). Variable neighborhood search. *Computers & Operations Research*, 24(11), 1097–1100. [https://doi.org/10.1016/S0305-0548(97)00031-2](https://doi.org/10.1016/S0305-0548(97)00031-2).
9. Maniezzo, V., Stützle, T., & Voß, S. (Eds.). (2010). *Matheuristics: Hybridizing Metaheuristics and Mathematical Programming*. Annals of Information Systems, 10. Springer. [https://doi.org/10.1007/978-1-4419-1306-7](https://doi.org/10.1007/978-1-4419-1306-7).

The references establish the identity and bibliographic starting point for the named methods. They do not, by themselves, validate every modern variant or any particular spatial application. Use the [verification record](../../catalog/verification/metaheuristics.md) for the current evidence boundary.
