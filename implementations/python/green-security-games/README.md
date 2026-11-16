# Green security-game patrol allocation

Install and test with `python -m pip install -r requirements.txt && python -m pytest -q`.

The package solves a single-period minimax Stackelberg coverage game. Site i has attacker value (v_i), detection effectiveness (e_i), and patrol coverage (x_i) between zero and one. The attacker's expected payoff is (v_i(1-e_ix_i)). A bisection water-filling solution allocates the available fractional patrol resource to minimize the maximum site payoff.

This model assumes the defender can distribute divisible coverage independently across sites. It does not model patrol routes, travel time, interdiction dynamics, attacker uncertainty, multiple attacker types, learned policies or real patrol data.
