# Table 10: Sector Difference-in-Differences Estimations

Difference-in-Differences (DiD) specifications evaluating energy transmission across Downstream Consumers, Upstream Producers, and Clean Defensives. Standard errors are clustered by trading session date. Significance: * p < 0.10, ** p < 0.05, *** p < 0.01.

| Specification | DiD Parameter | DiD Coefficient | Day-Clustered SE | t-Statistic | p-value | Resolved Trades (N) | Trading Days |
|:---|:---|---:|---:|---:|:---:|---:|---:|
| Spec 1A: Downstream Consumers vs. Defensives (Acute Mar 2026) | β₃ (PostShock × Downstream) | -8.09%*** | 2.76% | -2.93 | 0.0034 | 101,349 | 1,009 |
| Spec 1B: Downstream Consumers vs. Defensives (Extended Mar–Jul 2026) | β₃ (PostShock × Downstream) | -2.74%* | 1.65% | -1.66 | 0.0976 | 108,119 | 1,077 |
| Spec 1C: Upstream Producers vs. Defensives (Acute Mar 2026) | β₃ (PostShock × Upstream) | 0.48% | 4.37% | 0.11 | 0.9118 | 75,451 | 1,009 |
| Spec 2: Naive Binary DiD (Pooled Upstream + Downstream vs. Others) | β₃ (PostShock × EnergySector) | 0.06% | 0.98% | 0.06 | 0.9498 | 404,437 | 1,077 |
| Spec 2A: Pre-Shock Brent Beta Quartile Dummy (All 480 Stocks) | β₃ (PostShock × HighBrentBeta) | -1.57%** | 0.65% | -2.42 | 0.0157 | 404,437 | 1,077 |
| Spec 3A: Continuous Brent Volatility × Downstream Consumers | β₃ (σ_Brent × Downstream) | -0.8251** | 0.3809 | -2.17 | 0.0303 | 105,493 | 1,050 |
