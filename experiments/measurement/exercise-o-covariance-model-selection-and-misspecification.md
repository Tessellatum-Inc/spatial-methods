# Exercise O — Covariance-model selection and stochastic-model misspecification

**Status:** Reproducible synthetic Monte Carlo experiment  
**Prerequisite:** [Exercise N — variance-component estimation from repeated networks](exercise-n-variance-component-estimation-from-repeated-networks.md)  
**Dataset basis:** [Exercise D synthetic vertical-control observations](../../data/measurement/exercise-d-stochastic-control-network.csv)  
**Implementation:** [analyze_exercise_o.py](../../scripts/measurement/analyze_exercise_o.py)

> All observations and trials are synthetic. Candidate models, component magnitudes and correlation form are deliberately controlled. This is an exploratory model-selection demonstration, not a validated field procedure.

## 1. Question

Exercise N estimated two variance components under a correctly specified covariance structure. Exercise O asks whether repeated observations can distinguish several plausible covariance structures, and how often model selection chooses the structure that generated the data.

This matters because an adjustment's coordinate estimates may look stable while its uncertainty estimates and statistical tests depend materially on the stochastic model. Geodetic VCE literature emphasises that a realistic observation covariance model is central to defensible precision and testing.

## 2. Candidate covariance structures

The same nine-observation vertical network is repeated in twelve independent sessions per trial. Four candidate structures are compared:

1. **Independent:** observation-specific diagonal variances only.
2. **Session:** diagonal variances plus one additive session-common random effect.
3. **AR(1):** diagonal variances plus a within-session first-order temporal correlation component.
4. **Both:** session-common and AR(1) components together.

The candidate covariance is:

```
Q = D + sigma_session^2 11' + sigma_AR^2 R(rho)
R(rho)[i,j] = rho^|i-j|
```

Terms absent from a candidate model are set to zero. The simulated truth uses either no extra component, a session-common standard deviation of 0.50 mm, an AR(1) component with marginal standard deviation 0.50 mm and rho=0.60, or both components. The observation-specific diagonal variances are taken from the Exercise D synthetic dataset.

## 3. Selection method

For each candidate, the script evaluates a restricted-likelihood-style profile criterion after eliminating the four unknown point elevations. The variance-component standard deviations are searched on a fixed grid from 0 to 1.5 mm in 0.15 mm increments. The AR(1) correlation coefficient is fixed at 0.60 for candidate fitting.

The selected structure is the candidate with the smallest criterion. This is a coarse-grid, controlled comparison; it is not a full continuous REML optimiser. Candidate ordering resolves exact ties. Because the correlation form and rho are supplied in advance, the exercise tests discrimination among these structures, not unrestricted discovery of an unknown covariance function.

## 4. Monte Carlo design

- 250 trials for each of four generating structures.
- Twelve independent repeated sessions per trial.
- Nine observations per session.
- Fixed seed 20261119.
- Independent observation noise follows the observation-specific diagonal variances.
- Session effects are independent between sessions.
- AR(1) components are generated within each session with stationary marginal standard deviation 0.50 mm and rho=0.60.

The primary result is the fraction of trials selecting each candidate model. For the correctly specified non-independent model, the script also reports mean grid-estimated component standard deviations.

## 5. Reproduction

From the repository root:

```bash
python scripts/measurement/analyze_exercise_o.py
```

The implementation uses only Python's standard library and reads the Exercise D CSV without modifying it.

## 6. Interpretation and limitations

Model-selection frequencies are empirical properties of this network, sample size, component magnitudes, candidate set, grid and tie rule. They are not universal detection probabilities. A weak component may be difficult to distinguish from noise; two covariance components may compete to explain similar residual patterns. The finite grid also introduces discretisation error.

The experiment does not include systematic biases, non-Gaussian errors, cross-session correlation, unknown correlation range, changing network geometry, missing observations, robust estimation, or uncertainty intervals for model-selection probabilities. It does not claim that the candidate set is exhaustive.

A practical workflow should:
- Define candidate error mechanisms from acquisition physics and metadata before fitting.
- Estimate covariance components and assess their identifiability.
- Compare competing structures using likelihood criteria and residual diagnostics, not a single score alone.
- Check sensitivity of coordinates, uncertainty and statistical tests to plausible alternatives.
- Use independent check observations and preserve raw data.
- Avoid selecting a complicated model merely because it improves an in-sample criterion.

## 7. Research basis

- Teunissen, P. J. G. & Amiri-Simkooei, A. R. (2008). “Least-squares variance component estimation.” *Journal of Geodesy*, 82, 65–82. https://doi.org/10.1007/s00190-007-0157-x. Presents LS-VCE and discusses estimability and precision of variance components.
- Amiri-Simkooei, A. R., Teunissen, P. J. G. & Tiberius, C. C. J. M. (2009). “Application of Least-Squares Variance Component Estimation to GPS Observables.” *Journal of Surveying Engineering*, 135(4), 149–160. https://doi.org/10.1061/(ASCE)0733-9453(2009)135:4(149). Demonstrates the practical importance of observation-type variance, elevation dependence, inter-observable correlation and temporal correlation.
- Fotopoulos, G. (2003). *An Overview of Variance Component Estimation in GPS Applications*. University of Calgary thesis. Reviews stochastic modelling and variance-component estimation in geodetic adjustment.

The exercise's REML-style criterion and simulation are a simplified teaching implementation, not a reproduction of any cited paper.
