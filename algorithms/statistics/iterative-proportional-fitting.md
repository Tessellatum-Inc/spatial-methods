# Iterative proportional fitting

Iterative proportional fitting (IPF), also called raking, adjusts a
nonnegative contingency table to match supplied marginal totals. The
algorithm alternately scales rows and columns, repeating until the margins
match within a chosen tolerance.

A zero in the seed table remains zero. This structural-zero preservation is
useful when some combinations are impossible, but it can also make target
margins infeasible. Positive target margins with no seed support are
rejected. The linked implementation reports convergence and the final
maximum absolute marginal error.

IPF is a component used in spatial microsimulation and survey calibration;
it is not, by itself, a complete population synthesis workflow.
