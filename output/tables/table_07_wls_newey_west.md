# Table 7: Daily WLS with Newey-West HAC Standard Errors

Weighted Least Squares (WLS) regression of daily resolved win rate (WR_t) on PostShock indicator across 1,116 trading sessions. Weights: daily count of resolved trades (n_resolved). Standard errors: Newey-West HAC with lags = 5, 10, and 20. Significance: * p < 0.10, ** p < 0.05, *** p < 0.01.

| HAC Lag | PostShock β₁ (%) | Newey-West SE (%) | t-Statistic | p-value | Weighted R² | β₁ (Pre-Stable Controlled) | SE (Pre-Controlled) |
|:---|---:|---:|---:|:---:|---:|---:|---:|
| Lag = 5 | -7.99%*** | 1.59% | -5.04 | 4.6247e-07 | 0.0518 | -8.15%*** | 1.58% |
| Lag = 10 | -7.99%*** | 1.84% | -4.34 | 1.4266e-05 | 0.0518 | -8.15%*** | 1.84% |
| Lag = 20 | -7.99%*** | 2.12% | -3.78 | 1.5890e-04 | 0.0518 | -8.15%*** | 2.11% |
