# Lee's L implementation walkthrough

## 1. Align the data

x and y must describe the same spatial units in exactly the same order. W rows and columns must use that same order. A valid-looking number calculated from misaligned arrays is still wrong.

## 2. Validate the weights

The implementation requires a square, finite, non-negative matrix with a zero diagonal and at least one neighbour in every row. It rejects islands rather than silently assigning a zero spatial lag. This keeps the row-standardized simplification explicit.

## 3. Row-standardize

Each row is divided by its sum. The resulting spatial lags are weighted neighbourhood averages: x_tilde = W x and y_tilde = W y.

## 4. Calculate the original-variable sums of squares

~~~text
SS_x = sum((x - mean(x)) ** 2)
SS_y = sum((y - mean(y)) ** 2)
~~~

Constant variables are rejected because the denominator would be zero.

## 5. Calculate Lee's L

Following Lee (2001), equations 13–14:

~~~text
L = sum((x_tilde - mean(x)) * (y_tilde - mean(y)))
    / sqrt(SS_x * SS_y)
~~~

The numerator uses both spatial lag vectors. The denominator uses variation in the original variables. This is not the bivariate Moran cross-product x'Wy.

## 6. Return diagnostic smoothing scalars

~~~text
SSS_x = sum((x_tilde - mean(x)) ** 2) / SS_x
SSS_y = sum((y_tilde - mean(y)) ** 2) / SS_y
~~~

These diagnostics describe the amount of variation remaining after neighbourhood smoothing. Lee's paper relates the statistic to the product of the square roots of these smoothing scalars and the correlation between the lagged variables.

## 7. Test the contract

Tests cover hand-checkable lags, symmetry under swapping x and y, positive and negative smoothed association, row standardization, finite output and invalid dimensions/weights/constant variables.

The tests establish this declared implementation contract. They do not establish inferential significance or validate a real study's neighbourhood design.
