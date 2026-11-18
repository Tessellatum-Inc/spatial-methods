# Verification record — Harris market potential

- **Primary source:** Harris (1954), The Market as a Factor in the Localization of Industry in the United States, DOI 10.1080/00045605409352140.
- **Method identity:** destination market mass weighted by a declining distance/transport-cost function.
- **Implementation:** [existing NumPy implementation](../../implementations/python/regional-dynamics/market_potential.py) provides inverse-power impedance decay with configurable exponent and explicit self-potential handling; see [tests](../../implementations/python/regional-dynamics/test_market_potential.py) and [lab notebook](../../notebooks/harris-market-potential-lab.ipynb).
- **Limitations:** descriptive index only; no estimated gravity coefficients, economic equilibrium, endogenous market-size correction or causal interpretation.
- **Status:** implementation and tests exist; CI for the current completion branch is pending. Method identity was checked against the primary bibliographic record and corroborating descriptions; this is not a reproduction of Harris's original regional dataset.