# Fay-Herriot area-level model

The Fay-Herriot model links direct area estimates to auxiliary covariates
while separating sampling error from between-area variation:

    y_i = x_i' beta + u_i + e_i
    u_i ~ N(0, A), e_i ~ N(0, D_i)

The sampling variances D_i are treated as known. Restricted maximum
likelihood estimates the between-area variance A; generalized least squares
estimates beta. The empirical best linear unbiased predictor is:

    theta_hat_i = x_i' beta_hat + A_hat/(A_hat + D_i) * (y_i - x_i' beta_hat)

The linked implementation returns predictions and a plug-in MSE
approximation. Its MSE omits variance-component estimation uncertainty.
This area-level model is distinct from unit-level mixed models, direct
Horvitz-Thompson estimation and multilevel regression with poststratification.


## Source
- Fay, R. E., & Herriot, R. A. (1979). Estimates of income for small places: An application of James-Stein procedures to census data. *Journal of the American Statistical Association*, 74(366a), 269–277. https://doi.org/10.1080/01621459.1979.10482505.
