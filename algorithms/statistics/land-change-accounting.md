# Land-change accounting and intensity analysis

Given categorical maps at two dates, transition matrix C_ij counts area changing from class i to class j. Row totals are initial class areas; column totals are final areas; diagonal values are persistence. Loss is row total minus persistence; gain is column total minus persistence; net change is gain minus loss; swap is twice the smaller of gain and loss.

Total disagreement is changed area divided by total mapped area. Quantity disagreement is half the sum of absolute row/column marginal differences divided by total area. Allocation disagreement is the residual total disagreement after quantity disagreement.

For an interval of T years, interval intensity is changed area divided by total area and T. Class gain intensity divides class gains by initial area of all other classes and T; class loss intensity divides losses by class initial area and T. These are annualized descriptive rates. The implementation is a two-date accounting baseline and does not include complete multi-interval significance tests or transition-specific uniformity tests.
