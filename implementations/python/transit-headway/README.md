# Transit headway and expected waiting time

Dependency-free timetable-derived service-frequency and passenger waiting-time metrics.

## Run
```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

## Contract
- Times use one numeric unit; seconds are recommended. GTFS extended service-day times above 24:00 are supported.
- Departures are sorted, unique and inside the closed service window.
- Headway statistics describe consecutive departures and exclude boundary gaps.
- Expected wait includes initial and terminal partial intervals.
- Optional arrival_weights provide one non-negative relative arrival rate per positive wait interval. The weighted expectation is sum(rate * gap^2 / 2) / sum(rate * gap).
- Omitting rates assumes uniform passenger arrivals and recovers sum(gap^2)/(2 * service duration).
- If no departures exist or all arrival rates are zero, expected_wait is None.
- This is not a GTFS parser, network accessibility model, capacity model or stochastic reliability model.

See the algorithm note and verification record linked in the repository.
