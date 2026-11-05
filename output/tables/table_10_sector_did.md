# Table 10: Sector Difference-in-Differences Estimations

Difference-in-Differences (DiD) specifications evaluating sector vulnerabilities across Downstream and Defensive industries. Standard errors are clustered by trading day. Significance: * p < 0.10, ** p < 0.05, *** p < 0.01.

| Specification | DiD Parameter | DiD Coefficient | Day-Clustered SE | t-Statistic | p-value | Resolved Trades (N) | Trading Days |
|:---|:---|---:|---:|---:|:---:|---:|---:|
| Spec 1A: Downstream vs Defensives (Acute Mar 2026) | β₃ (PostShock × Downstream) | -3.49% | 3.38% | -1.03 | 0.3015 | 87,065 | 1,009 |
| Spec 1B: Downstream vs Defensives (Extended Mar–Jul 2026) | β₃ (PostShock × Downstream) | -1.50% | 1.71% | -0.88 | 0.3776 | 92,852 | 1,077 |
| Spec 2: Naive Binary DiD (Pooled All Sectors) | β₁ (PostShock) | -8.15%*** | 1.32% | -6.18 | < 0.0001 | 404,437 | 1,077 |
| Spec 2A: Pre-Shock Brent Beta Quartile Dummy | β₃ (PostShock × HighBrentBeta) | -1.57%** | 0.65% | -2.42 | 0.0157 | 404,437 | 1,077 |
| Spec 3A: Continuous Brent Volatility × Downstream | β₃ (σ_Brent × Downstream) | -0.4984 | 0.3816 | -1.31 | 0.1915 | 90,595 | 1,050 |
