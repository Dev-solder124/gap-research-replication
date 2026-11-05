# Table 12: Macro Horse Race — Sequential WLS Models

Sequential Weighted Least Squares (WLS) regressions of daily resolved win rate (WR_t). Models 1–5 cover the full 2022–2026 sample; Model 6 evaluates the 2025–2026 sub-sample with direct FII net flows. Weights: daily resolved trade count (n_resolved). Standard errors: Newey-West HAC (lag = 5) reported in parentheses. Significance: * p < 0.10, ** p < 0.05, *** p < 0.01.

| Variable | Model 1 | Model 2 | Model 3 | Model 4 | Model 5 | Model 6 |
|:---|---:|---:|---:|---:|---:|---:|
| Constant (α) | 52.14%*** (0.34%) | 58.34%*** (1.34%) | 50.38%*** (10.83%) | 48.60%*** (9.20%) | 49.85%*** (9.54%) | 92.63%*** (27.19%) |
| PostShock Indicator (β₁) | -7.99%*** (1.59%) | -7.44%*** (1.22%) | -7.73%*** (1.39%) | -7.87%*** (1.29%) | -6.61%*** (1.55%) | -2.82% (2.22%) |
| India VIX | — | -0.0017* (0.0009) | -0.0014 (0.0010) | 0.0029*** (0.0009) | 0.0034*** (0.0011) | -0.0011 (0.0021) |
| Nifty 500 Return | — | -1.3246*** (0.3975) | -1.3715*** (0.4227) | -0.4678 (0.4137) | -0.5434 (0.4169) | -0.3002 (0.7383) |
| |Nifty 500 Return| | — | -5.6323*** (0.8535) | -5.8405*** (0.8344) | -4.4222*** (0.8134) | -4.4009*** (0.8437) | -5.4321*** (1.2106) |
| Δ USD/INR | — | — | 1.4675 (1.2737) | 1.1229 (1.1571) | 1.0330 (1.1670) | -0.4661 (2.0312) |
| ln(NSE Turnover) | — | — | 0.0067 (0.0089) | 0.0150* (0.0083) | 0.0142* (0.0085) | -0.0196 (0.0240) |
| Mean Opening Bar Range | — | — | — | -3.2274 (2.4251) | -3.7299 (2.4966) | 1.1817 (3.9909) |
| Sweet Spot Share | — | — | — | -0.2700*** (0.0349) | -0.2619*** (0.0352) | -0.3060*** (0.0609) |
| Brent 20d Volatility | — | — | — | — | -0.3544 (0.4005) | -0.2580 (0.5012) |
| |Brent Return| | — | — | — | — | -0.2116 (0.1956) | -0.2106 (0.3573) |
| FII Net Flow (Rs Cr) | — | — | — | — | — | 1.34e-06 (1.51e-06) |
| Weighted R² | 0.0518 | 0.2172 | 0.2231 | 0.3203 | 0.3218 | 0.4273 |
| Observations (N) | 1,116 | 1,069 | 1,050 | 1,049 | 1,035 | 332 |
