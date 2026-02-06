# Methodology: Bayesian Change Point Analysis

## 1. Data Preparation
- Convert prices to log returns: `log(P_t/P_{t-1})`
- Check stationarity with Augmented Dickey-Fuller test
- Handle missing values with forward fill

## 2. Bayesian Model
```python
with pm.Model() as model:
    tau = pm.DiscreteUniform("tau", lower=1, upper=n_days-1)
    mu1 = pm.Normal("mu1", mu=0, sigma=1)
    mu2 = pm.Normal("mu2", mu=0, sigma=1)
    mean = pm.math.switch(time_idx < tau, mu1, mu2)
    pm.Normal("returns", mu=mean, sigma=1, observed=log_returns)
3. MCMC Sampling
Chains: 4

Draws: 2000 per chain

Tune: 1000

Algorithm: NUTS

4. Diagnostics
R-hat < 1.01 for convergence

Effective Sample Size > 1000

Trace plots show good mixing
