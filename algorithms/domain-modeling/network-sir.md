# Discrete-time SIR simulation on a network

## Model

Each node is susceptible (S), infected (I) or recovered (R). An undirected adjacency matrix describes contacts. During one synchronous step, a susceptible node with (k) infected neighbors is infected with probability

\[
P(S\rightarrow I\mid k)=1-(1-\beta)^k,
\]

where (eta\) is the per-contact transmission probability. Each node infected at the start of the step independently recovers with probability (gamma\). Recovered nodes remain recovered in this SIR baseline.

The implementation evaluates all transitions from the same prior state. Newly infected nodes do not transmit until the next step. A seeded random generator makes runs reproducible.

## Inputs and outputs

- A one-dimensional integer state vector using 0=S, 1=I and 2=R.
- A square, symmetric, binary adjacency matrix with no self-loops.
- Per-contact infection probability (eta\in[0,1]), recovery probability (gamma\in[0,1]), a non-negative step count and an optional seed.
- The simulation returns final node states and S/I/R counts for the initial state and every subsequent step.

## Limits

This is a discrete-time network SIR teaching baseline. It assumes a static, undirected contact graph, homogeneous transmission and recovery probabilities, no latency period, no reinfection, no births/deaths, and no spatial movement. It does not reproduce a named epidemiological model, fit parameters, estimate uncertainty or forecast a real outbreak. Spatially explicit diffusion, metapopulation coupling, mobility-driven transmission and empirical calibration remain separate tasks.

## Tests

The independent tests cover synchronous transmission, one-step propagation, recovery, population conservation, seeded reproducibility, invalid states, invalid graph structure and probability bounds.
