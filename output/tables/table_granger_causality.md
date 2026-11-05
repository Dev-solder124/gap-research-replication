# Table: Bivariate Granger Causality Tests — Sign vs Magnitude vs Volatility

Bivariate Granger causality F-tests evaluating whether oil price direction (R_brent), shock magnitude (|R_brent|), or realized volatility (σ_Brent 20d) predictive Granger-cause the daily strategy win rate (WR_t). Tested across lag orders L ∈ {1, 3, 5, 10}. Significance: * p < 0.10, ** p < 0.05, *** p < 0.01.

| Relationship | Lag Order (L) | Granger F-Statistic | p-value |
|:---|---:|---:|:---:|
| Signed Brent Return → WR | 1 | 0.873 | 0.3505 |
| Signed Brent Return → WR | 3 | 1.343 | 0.2590 |
| Signed Brent Return → WR | 5 | 1.309 | 0.2577 |
| Signed Brent Return → WR | 10 | 1.551 | 0.1163 |
| |Brent Return| (Magnitude) → WR | 1 | 13.363*** | 0.0003 |
| |Brent Return| (Magnitude) → WR | 3 | 8.045*** | < 0.0001 |
| |Brent Return| (Magnitude) → WR | 5 | 3.815*** | 0.0020 |
| |Brent Return| (Magnitude) → WR | 10 | 1.578 | 0.1080 |
| Brent Realized Volatility → WR | 1 | 42.834*** | < 0.0001 |
| Brent Realized Volatility → WR | 3 | 11.415*** | < 0.0001 |
| Brent Realized Volatility → WR | 5 | 4.996*** | 0.0002 |
| Brent Realized Volatility → WR | 10 | 2.348*** | 0.0097 |
| WR → Signed Brent Return (Reverse) | 1 | 1.430 | 0.2321 |
| WR → Signed Brent Return (Reverse) | 3 | 1.155 | 0.3258 |
| WR → Signed Brent Return (Reverse) | 5 | 2.742** | 0.0181 |
| WR → Signed Brent Return (Reverse) | 10 | 2.009** | 0.0295 |
| WR → |Brent Return| (Reverse) | 1 | 6.117** | 0.0135 |
| WR → |Brent Return| (Reverse) | 3 | 7.145*** | < 0.0001 |
| WR → |Brent Return| (Reverse) | 5 | 3.954*** | 0.0015 |
| WR → |Brent Return| (Reverse) | 10 | 2.319** | 0.0107 |
