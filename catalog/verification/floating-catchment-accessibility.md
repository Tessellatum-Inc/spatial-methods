# Verification record: 2SFCA and E2SFCA

- Hand calculation checks a one-facility ratio and the resulting demand accessibility.
- Catchment boundary test confirms the 2SFCA radius is inclusive.
- E2SFCA fixture independently calculates zone membership, supply-demand ratios and final accessibility.
- Unreachable facilities and zero denominators are handled without division by zero.
- Invalid dimensions, negative/non-finite data, invalid radius and malformed decay zones are rejected.

Run `python -m pytest -q` in implementations/python/floating-catchment. CI must pass before release verification is complete.
