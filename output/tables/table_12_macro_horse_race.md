# Table 12: Macro Horse Race — Sequential WLS Models

Sequential Weighted Least Squares (WLS) regressions of daily resolved win rate (WR_t). Weights: daily resolved trade count (n_resolved). Standard errors: Newey-West HAC (lag = 5) reported in parentheses. Significance: * p < 0.10, ** p < 0.05, *** p < 0.01.

| Variable | Model 1 | Model 2 | Model 3 | Model 4 | Model 5 |
|:---|---:|---:|---:|---:|---:|
| Constant (α) | 52.14%*** (0.34%) | 58.34%*** (1.34%) | 50.38%*** (10.83%) | 93.18%*** (26.27%) | 92.63%*** (27.19%) |
| PostShock Indicator (β₁) | -7.99%*** (1.59%) | -7.44%*** (1.22%) | -7.73%*** (1.39%) | -3.65%** (1.84%) | -2.82% (2.22%) |
| India VIX | — | -0.0017* (0.0009) | -0.0014 (0.0010) | -0.0014 (0.0021) | -0.0011 (0.0021) |
| Nifty 500 Return | — | -1.3246*** (0.3975) | -1.3715*** (0.4227) | -0.2080 (0.7315) | -0.3002 (0.7383) |
| |Nifty 500 Return| | — | -5.6323*** (0.8535) | -5.8405*** (0.8344) | -5.5584*** (1.1727) | -5.4321*** (1.2106) |
| Δ USD/INR | — | — | 1.4675 (1.2737) | -0.3762 (2.0036) | -0.4661 (2.0312) |
| ln(NSE Turnover) | — | — | 0.0067 (0.0089) | -0.0200 (0.0232) | -0.0196 (0.0240) |
| FII Net Flow (Rs Cr) | — | — | — | 1.39e-06 (1.50e-06) | 1.34e-06 (1.51e-06) |
| Mean Opening Bar Range | — | — | — | 1.1876 (3.9593) | 1.1817 (3.9909) |
| Sweet Spot Share | — | — | — | -0.3144*** (0.0581) | -0.3060*** (0.0609) |
| Brent 20d Volatility | — | — | — | — | -0.2580 (0.5012) |
| |Brent Return| | — | — | — | — | -0.2106 (0.3573) |
| Weighted R² | 0.0518 | 0.2172 | 0.2231 | 0.4342 | 0.4273 |
| Observations (N) | 1,116 | 1,069 | 1,050 | 337 | 332 |
