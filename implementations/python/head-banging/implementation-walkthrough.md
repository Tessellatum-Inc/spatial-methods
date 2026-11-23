# Weighted head-banging — implementation walkthrough

1. Find each location's k nearest neighbours.
2. Form pairs whose angle at the target is within phi degrees of 180 degrees. Keep the most nearly collinear pairs up to the triple cap.
3. For each triple, identify lower and higher endpoint values. Compute weighted medians of the lower and higher endpoints using their corresponding endpoint weights.
4. Update the target with the weighted median of low screen, current value and high screen. Screen weights are the sums of selected endpoint weights; target weight is the number of triples times the target's weight.
5. Update all locations synchronously until the maximum absolute change is within tolerance or the iteration cap is reached.
6. Locations with no qualifying triples remain unchanged in this teaching implementation; the full software has additional corner-point rules.
