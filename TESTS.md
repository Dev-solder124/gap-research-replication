# Test Specifications

This document describes every econometric test included in the manuscript. It is a **specification only** — no results, no computed numbers, no expected outputs of any kind appear here. An independent researcher reads this document, writes their own code, runs it on the raw data in `data/`, and produces all manuscript tables and figures from scratch.

**Global sample-cleaning rule (apply to every test below):**

Purge the following three Muhurat Diwali trading sessions before any calculation:
- 2022-10-24
- 2023-11-12
- 2024-11-01

After purging, the master sample is **1,116 regular trading sessions** spanning January 2022 through May 2026.

**Regime boundary definitions (used in multiple tests):**

| Regime | Date range |
|--------|------------|
| Pre-stable | Before 2022-03-01 |
| Stable | 2022-03-01 to 2026-02-28 inclusive |
| Post-shock | 2026-03-01 onward |

---

## Test 1: Sample Partition and Descriptive Statistics

**Manuscript reference:** Table 3, Section 3.3

**Input files:**
- `data/trades/1:1-480gap_strategy_all_trades.csv`
- `data/daily/daily_series_clean.csv`

**Cleaning steps:**
1. Apply the three-date Muhurat purge (see global rule above).
2. Partition all rows by the `regime` column (or by date against the regime boundary dates if computing from the trade panel directly).

**What to compute (by regime partition):**

For each of Pre-stable, Stable, Post-shock, and Full Sample:

- Total trade count (all statuses)
- Resolved trade count (`status IN ('TARGET', 'STOP_LOSS')`)
- Number of unique trading days
- Number of unique symbols traded
- Resolved win rate: n_targets / n_resolved
- Mean daily resolved win rate: mean of `resolved_wr` from `daily_series_clean.csv` for days in that regime
- Standard deviation of daily resolved win rate

**What to report:** The partition table (Table 3) showing the four regime panels with the statistics above.

**No test statistic is required for Table 3 itself** — it is descriptive. The win-rate difference between regimes is tested formally in Test 4 (LPM).

---

## Test 2: 16-Quarter Walk-Forward OOS Threshold Convergence

**Manuscript reference:** Table 4, Figure 2, Section 3.5

**Input files:**
- `data/trades/1:1-480gap_strategy_all_trades.csv`

**Cleaning steps:**
1. Apply Muhurat purge.
2. Load all trades, tracking both Nominal Win Rate (`status == 'TARGET'` over all trades) and Resolved Win Rate (`status == 'TARGET'` over resolved trades).

**Algorithm — expanding-window walk-forward with quarterly OOS:**

The sample is partitioned into 16 out-of-sample (OOS) quarters, each of approximately 60–65 trading days (Q3 2022 through Q2 2026). The walk-forward proceeds as follows:

For OOS quarter k (k = 1 to 16):
1. **Training window**: all trades from the start of the full sample through the last day before OOS quarter k begins.
2. **Threshold estimation on training window (First-Crossing Breakeven Cutoff)**:
   - Per methodology, the threshold estimator c*(k) is defined as the non-parametric first-crossing cutoff of the 50.0% directional breakeven barrier, not an unconstrained tail argmax.
   - Partition training window trades with 0.0 ≤ gap_size_pct ≤ 5.0 into 20 equal-width bins over [0.0, 5.0] using 21 bin edges (`np.linspace(0.0, 5.0, 21)`, width = 0.25%, midpoints m_j = 0.125%, 0.375%, ..., 4.875%).
   - For each bin j, compute the bin win rate wr_j and trade count n_j. Retain only valid bins with n_j ≥ 30.
   - Scan left-to-right from the smallest bin midpoint (j = 0, 1, ...). Identify the first adjacent pair of valid bins (j, j+1) where wr_j < 0.50 and wr_{j+1} ≥ 0.50.
   - Compute threshold c*(k) via linear interpolation between (m_j, wr_j) and (m_{j+1}, wr_{j+1}) at wr = 0.50:

$$
c^*(k) = m_j + \frac{0.50 - wr_j}{wr_{j+1} - wr_j} \cdot (m_{j+1} - m_j)
$$

   - If the first valid bin already has wr_0 ≥ 0.50, set c*(k) = m_0. If no bin crosses 0.50, record c*(k) as missing (NaN).
3. **OOS evaluation**:
   - Apply filter `gap_size_pct ≥ c*(k)` to trades in OOS quarter k.
   - Report unfiltered OOS win rate, filtered OOS win rate, filtered trade count, and whether the filtered OOS win rate exceeds 50.0% separately for both Resolved and Nominal win rates.

**Gap size in percent**: Compute `gap_size_pct = gap_size / entry_price × 100`.

**What to report (Table 4):** For each of the 16 OOS quarters — the OOS quarter label (e.g., Q3 2022, Q4 2022 … Q2 2026), the estimated threshold c*(k), unfiltered and filtered trade counts, unfiltered and filtered win rates (both Nominal and Resolved), and the two separate fade-dominant breakeven indicators (`Fade-Dominant Resolved (>50%)` and `Fade-Dominant Nominal (>50%)`).

**What to report (Figure 2):** A 2-panel stacked figure (`figsize=(11, 7.5)`, `sharex=True`):
- **Panel A (Top)**: Grouped bar chart showing OOS Filtered Resolved Win Rate (%) and OOS Filtered Nominal Win Rate (%) for each of the 16 OOS quarters against the 50.0% directional breakeven barrier.
- **Panel B (Bottom)**: Line plot with markers showing the expanding-window First-Crossing Cutoff c*(k) (%) estimated strictly on training data prior to each quarter k, demonstrating threshold stability and convergence.

---

## Test 3: Structural Break Tests — Quandt-Andrews and Bai-Perron

**Manuscript reference:** Table 5, Figure 1, Section 4.1

**Input files:**
- `data/daily/daily_series_clean.csv`

**Cleaning steps:**
1. Apply Muhurat purge.
2. Use the `resolved_wr` column as the dependent time series.

**Specification A — Quandt-Andrews single break (Sup-F, Exp-F, Ave-F):**

- Regress `resolved_wr` on a constant plus a step-shift dummy for a hypothesized break at date τ.
- Trim 5% of observations from each end of the sample (do not test for breaks in the first or last 5% of trading days).
- Compute the F-statistic for a structural change in the constant at each candidate break date τ in the trimmed interior.
- Report: Sup-F = max F(τ) over all interior τ; Exp-F = log(mean exp(F(τ)/2)); Ave-F = mean F(τ).
- Use HAC-robust standard errors (Newey-West) with automatic lag selection.
- Null hypothesis: no structural break anywhere in the interior.
- Reference: Andrews (1993) for Sup-F; Andrews and Ploberger (1994) for Exp-F and Ave-F.

**Specification B — Bai-Perron multiple breaks:**

- Allow up to M = 5 structural breaks in the `resolved_wr` time series.
- Use the Bai-Perron (1998, 2003) dynamic programming algorithm with 5% trimming.
- Apply HAC-robust residuals.
- Report: the number of breaks selected by the BIC, the estimated break dates, and the 95% confidence intervals around each break date.
- Reference: Bai and Perron (1998, 2003). Implementation in R package `strucchange` or Python via rolling Chow tests.

**Quandt–Andrews HAC F-Statistic Sequence for Figure 1:**
- Plot the full-sample Quandt–Andrews HAC F-statistic sequence across all 5%-trimmed interior candidate break dates against calendar time.
- Superimpose horizontal reference lines for the Andrews (1993) / Hansen (1997) asymptotic critical values at 5% (F = 8.85) and 1% (F = 12.35).
- Plot a vertical line at the peak Sup-F date and dynamically annotate the peak Sup-F value and date.
- Shade the 95% Bai–Perron HAC confidence interval around the final break date (`axvspan` with alpha = 0.20).

**What to report (Table 5):** Test statistics and p-values for Sup-F, Exp-F, Ave-F; number of breaks and break dates from Bai-Perron; confidence intervals on break dates.

---

## Test 4: Two-Way Clustered Linear Probability Model

**Manuscript reference:** Table 6, Section 4.2

**Input files:**
- `data/trades/1:1-480gap_strategy_all_trades.csv`

**Cleaning steps:**
1. Apply Muhurat purge.
2. Use resolved trades only (`status IN ('TARGET', 'STOP_LOSS')`).
3. Create binary outcome: `win_i = 1` if `status == 'TARGET'`, else 0.

**Econometric specification:**

$$
win_{i,t} = \alpha + \beta_1 \cdot \text{PostShock}_t + \beta_2 \cdot \text{PreStable}_t + \varepsilon_{i,t}
$$

where:
- `PostShock_t = 1` if the trade date is on or after 2026-03-01, else 0
- `PreStable_t = 1` if the trade date is before 2022-03-01, else 0
- The Stable regime (2022-03-01 to 2026-02-28) is the omitted baseline

**Clustering:** Two-way clustering by trading day and by stock symbol, following Cameron, Gelbach, and Miller (2011). The two-way clustered variance-covariance matrix is:

$$
\hat{V}_{2\text{-way}} = \hat{V}_{\text{day}} + \hat{V}_{\text{stock}} - \hat{V}_{\text{White}}
$$

where V_day clusters by date, V_stock clusters by symbol, and V_White is the heteroskedasticity-robust (White) variance.

**Sub-samples to estimate separately:**
Run the LPM above on each of the following sub-samples:
1. Full sample (all 1,116 days)
2. January 2026 alone (post-shock month 1)
3. February 2026 alone (post-shock month 2)
4. March 2026 alone (post-shock month 3)
5. April 2026 alone (post-shock month 4)
6. May 2026 alone (post-shock month 5)
7. Full post-shock window (all post-2026-03-01 days)

**What to report (Table 6):** For each sub-sample — the β₁ coefficient (PostShock), two-way clustered SE, t-statistic, p-value, number of resolved trades, and number of trading days.

---

## Test 5: Daily WLS with Newey-West HAC

**Manuscript reference:** Table 7, Section 4.3

**Input files:**
- `data/daily/daily_series_clean.csv`

**Cleaning steps:**
1. Apply Muhurat purge.
2. Use all 1,116 days.

**Econometric specification:**

$$
WR_t = \alpha + \beta_1 \cdot \text{PostShock}_t + \varepsilon_t
$$

where:
- `WR_t = resolved_wr` from `daily_series_clean.csv` on day t
- `PostShock_t = 1` if date ≥ 2026-03-01, else 0
- **Weights**: use `n_resolved` (daily count of resolved trades) as WLS weights — days with more trades get more weight
- **Standard errors**: Newey-West HAC with lags = 5, 10, and 20 (report all three in separate columns or rows)

**What to report (Table 7):** The β₁ estimate and SE under each of the three HAC lag choices; the implied t-statistic and p-value; the weighted R².

---

## Test 6: Gap-Size Bin Win-Rate Analysis

**Manuscript reference:** Table 8, Figure 3, Section 4.4

**Input files:**
- `data/trades/1:1-480gap_strategy_all_trades.csv`

**Cleaning steps:**
1. Apply Muhurat purge.
2. Load all trades, retaining status indicators for `TARGET`, `STOP_LOSS`, and `TIME_EXIT`.
3. Compute gap size as a percentage: `gap_size_pct = gap_size / entry_price × 100`.

**Bin definitions (10 fixed bins):**

| Bin label | Range (%) |
|-----------|-----------|
| 0.00–0.25 | [0.00, 0.25) |
| 0.25–0.50 | [0.25, 0.50) |
| 0.50–0.75 | [0.50, 0.75) |
| 0.75–1.00 | [0.75, 1.00) |
| 1.00–1.25 | [1.00, 1.25) |
| 1.25–1.50 | [1.25, 1.50) |
| 1.50–2.00 | [1.50, 2.00) |
| 2.00–2.50 | [2.00, 2.50) |
| 2.50–3.00 | [2.50, 3.00) |
| 3.00+ | [3.00, ∞) |

Use `pandas.cut` or equivalent with these exact boundaries and right=False (left-closed, right-open) except the final bin which is open on the right.

**Within each bin, separately for Stable and Post-Shock regimes:**
- Compute **Resolved Win Rate**: TARGET / (TARGET + STOP_LOSS)
- Compute **Nominal Win Rate**: TARGET / (TARGET + STOP_LOSS + TIME_EXIT)
- Track trade counts for resolved trades and all trades.

**Statistical inference per bin (Day-Clustered Linear Probability Model):**
To account for cross-sectional dependence across stocks executing trades on the same calendar trading day, replace unclustered tests with a day-clustered Linear Probability Model (LPM) within each bin across the Stable and Post-Shock regimes:

$$
win_{i,t} = \alpha + \beta_1 \cdot \text{PostShock}_t + \varepsilon_{i,t}
$$

Estimate via OLS with standard errors clustered on trading day `date` (`cov_type='cluster', cov_kwds={'groups': date}`).
Estimate this model separately for:
1. **Resolved trades**: `win = 1` if `TARGET`, `0` if `STOP_LOSS`.
2. **All trades (Nominal)**: `win = 1` if `TARGET`, `0` if `STOP_LOSS` or `TIME_EXIT`.

**What to report (Table 8):** For each of the 10 bins — Stable and Post-Shock sample sizes, Stable and Post-Shock win rates for both Resolved and Nominal definitions, day-clustered differences (Δ), day-clustered standard errors, t-statistics, and two-sided p-values.

**What to report (Figure 3):** 2-panel stacked bar chart (`figsize=(12, 8.5)`, `sharex=True`) showing Stable vs. Post-Shock win rates across the 10 gap-size bins with day-clustered 95% confidence interval error bars (`yerr = 1.96 * se`, `capsize=3`) and a horizontal dashed line at 50.0% (Panel A: Resolved Win Rate; Panel B: Nominal Win Rate).

---

## Test 7: Event Study — Cumulative Abnormal Win Rate (CAWR)

**Manuscript reference:** Table 9, Figure 4, Section 4.5

**Input files:**
- `data/daily/daily_series_clean.csv`

**Cleaning steps:**
1. Apply Muhurat purge.
2. Use `resolved_wr` as the daily win-rate series.

**Event date:** 2026-03-04 (the first post-shock trading session exhibiting an observable shock; confirm this date from the `daily_series_clean.csv` date column — it should be the first date in the post-shock regime with a large negative WR deviation).

**Estimation window:** 2022-03-15 to 2025-07-31 (the Stable regime sub-window used to estimate the benchmark win rate μ and standard deviation σ of daily win rates).

**Benchmark parameters (computed from estimation window only):**
- μ = mean of `resolved_wr` over estimation window
- σ = standard deviation of `resolved_wr` over estimation window

**Abnormal Win Rate for each post-event day t:**

$$
AWR_t = WR_t - \mu
$$

**Cumulative Abnormal Win Rate over window [+a, +b] (event-relative days):**

$$
CAWR_{[a,b]} = \sum_{t=a}^{b} AWR_t
$$

**Standard error of CAWR over a window of length L:**

$$
SE(CAWR) = \sigma \times \sqrt{L}
$$

where L = b − a + 1 and σ is from the estimation window.

**t-statistic:**

$$
t_{[a,b]} = \frac{CAWR_{[a,b]}}{SE(CAWR_{[a,b]})}
$$

**Windows to evaluate:**

| Window label | Event-relative days |
|--------------|---------------------|
| Pre-event | [−10, −1] |
| Short post | [+1, +5] |
| Medium post | [+1, +10] |
| Long post | [+1, +20] |
| Extended post | [+1, +40] |

**What to report (Table 9):** For each window — CAWR in percentage points, SE, t-statistic, and p-value. Report the pre-event window as a placebo/validation check.

**What to report (Figure 4):** Line chart of Cumulative Abnormal Win Rate (CAWR, in percentage points) from day −10 to day +40 around the event date using Day 0 as the 0.0 reference origin (cumulated outward from Day 0 over [d, −1] for pre-event days and [1, d] for post-event days), with 95% confidence bands (±1.96 × σ × √|k| where k is the number of cumulated days), matching Table 9 exactly at Days −10, +5, +10, +20, and +40.

---

## Test 8: Sector Difference-in-Differences — Energy Exposure Specifications

**Manuscript reference:** Table 10, Figure 5, Section 4.6

**Input files:**
- `data/trades/1:1-480gap_strategy_all_trades.csv`
- `data/universe/SECTOR_MAP.py`
- `data/macro/XBR_USD Historical Data.csv`

**Cleaning steps:**
1. Apply Muhurat purge.
2. Use resolved trades only (`status IN ('TARGET', 'STOP_LOSS')`).
3. Merge sector labels from `SECTOR_MAP.py` onto the trade panel using the ticker root (strip the `_1M` suffix from `symbol`).
4. Define three mutually exclusive industry groups from `SECTOR_MAP.py`:
   - **Downstream Consumers** (energy/petrochemical input cost sensitive): `{'Auto', 'Automobile', 'Cement', 'Cement & Cement Products', 'Chemicals', 'Power', 'Fertilisers', 'Fertilisers & Pesticides'}`
   - **Upstream Producers** (crude/commodity revenue beneficiaries): `{'Oil & Gas', 'Metals'}`
   - **Clean Defensives** (energy price insensitive): `{'FMCG', 'Consumer Goods', 'Healthcare', 'Healthcare Services', 'Pharma', 'IT'}`

**Specification 1A — Downstream Consumers vs. Clean Defensives (Acute March 2026):**

$$
win_{i,t} = \alpha + \beta_1 \cdot \text{PostShock}_t + \beta_2 \cdot \text{Downstream}_i + \beta_3 \cdot (\text{PostShock}_t \times \text{Downstream}_i) + \varepsilon_{i,t}
$$

Sample restriction: Downstream Consumers and Clean Defensives only. Post-Shock window: Acute March 2026 only (2026-03-01 to 2026-03-31). Pre-period baseline: Stable regime (2022-03-01 to 2026-02-28). Standard errors: clustered by trading day.

**Specification 1B — Downstream Consumers vs. Clean Defensives (Full Post-Shock Mar–Jul 2026):**

Same equation and sample as Spec 1A, but Post-Shock window extended to the full post-shock period (2026-03-01 through 2026-07-31). Standard errors: clustered by trading day.

**Specification 1C — Upstream Producers vs. Clean Defensives (Acute March 2026):**

$$
win_{i,t} = \alpha + \beta_1 \cdot \text{PostShock}_t + \beta_2 \cdot \text{Upstream}_i + \beta_3 \cdot (\text{PostShock}_t \times \text{Upstream}_i) + \varepsilon_{i,t}
$$

Sample restriction: Upstream Producers and Clean Defensives only. Post-Shock window: Acute March 2026 only (2026-03-01 to 2026-03-31). Pre-period baseline: Stable regime (2022-03-01 to 2026-02-28). Standard errors: clustered by trading day.

**Specification 2 — Naive Binary DiD (Pooled Upstream + Downstream vs. All Other Sectors):**

$$
win_{i,t} = \alpha + \beta_1 \cdot \text{PostShock}_t + \beta_2 \cdot \text{Treated}_i + \beta_3 \cdot (\text{PostShock}_t \times \text{Treated}_i) + \varepsilon_{i,t}
$$

Full 480-stock universe, where `Treated_i = 1` for pooled Upstream Producers + Downstream Consumers, and `0` for all other sectors. Acute March 2026 vs. Stable baseline. Standard errors: clustered by trading day.

**Specification 2A — Pre-Shock Brent Beta Quartile Dummy:**

For each stock, compute its pre-shock Brent beta from regressing stock daily returns on Brent crude daily log-returns during the pre-shock Stable period (2022-03-01 to 2026-02-28). Rank all 480 stocks into quartiles; define `HighBrentBeta_i = 1` for the top quartile (highest sensitivity). Acute March 2026 vs. Stable baseline across all 480 stocks. Standard errors: clustered by trading day:

$$
win_{i,t} = \alpha + \beta_1 \cdot \text{PostShock}_t + \beta_2 \cdot \text{HighBrentBeta}_i + \beta_3 \cdot (\text{PostShock}_t \times \text{HighBrentBeta}_i) + \varepsilon_{i,t}
$$

**Specification 3A — Continuous 20-day Brent Realized Volatility × Downstream Interaction:**

Compute 20-day rolling realized volatility of Brent crude log-returns: σ_Brent,20d. Downstream Consumers vs. Clean Defensives across the full 2022–2026 sample. Standard errors: clustered by trading day:

$$
win_{i,t} = \alpha + \beta_1 \cdot \sigma_{\text{Brent},t}^{20d} + \beta_2 \cdot \text{Downstream}_i + \beta_3 \cdot (\sigma_{\text{Brent},t}^{20d} \times \text{Downstream}_i) + \varepsilon_{i,t}
$$

**What to report (Table 10):** For each specification — the treatment/interaction coefficient (β₃ in 1A, 1B, 1C, 2, 2A, 3A), day-clustered SE, t-statistic, p-value, resolved trade count N, and number of unique trading days.

**What to report (Figure 5):** 2-panel figure (`figsize=(12, 8)`): Panel A shows focused 20-day moving averages of daily resolved win rates for Downstream Consumers, Upstream Producers, and Clean Defensives over 2025-06-01 through 2026-07-10 with the March 4, 2026 structural break line; Panel B shows a sorted horizontal bar chart of the cross-sectional win rate contraction (Acute March 2026 minus Stable baseline, in percentage points) across sectors with N ≥ 1,000 resolved trades, color-coded by industry group.

---

## Test 9: Survivorship and Liquidity Strata

**Manuscript reference:** Table 11, Figure 7, Section 4.7

**Input files:**
- `data/trades/1:1-480gap_strategy_all_trades.csv`
- `data/daily/daily_win_rate_full_480.csv`
- `data/daily/daily_win_rate_nifty50.csv`
- `data/daily/daily_win_rate_midcap50.csv`
- `data/daily/daily_win_rate_smcap50.csv`
- `data/universe/nifty50_symbols.txt`
- `data/universe/midcap50_symbols.txt`
- `data/universe/smcap50_symbols.txt`
- `data/universe/delisted_2022.txt`

**Cleaning steps:**
1. Apply Muhurat purge (all three dates).
2. Use resolved trades only.

**8 strata to analyze:**

| Stratum | Definition |
|---------|------------|
| Full 480 Universe | All 480 strategy stocks |
| Nifty 50 Sub-universe | Stocks in `nifty50_symbols.txt` |
| Midcap 50 Sub-universe | Stocks in `midcap50_symbols.txt` |
| Smallcap 50 Sub-universe | Stocks in `smcap50_symbols.txt` |
| Liquidity Q1 (highest) | Top quartile of ex-ante 2022 turnover |
| Liquidity Q2 | Second quartile |
| Liquidity Q3 | Third quartile |
| Liquidity Q4 (lowest) | Bottom quartile |

**Liquidity quartile assignment**: Compute mean daily turnover per stock during the first 60 trading days of the sample (January–March 2022). Rank all 480 stocks and assign to Q1–Q4 based on this pre-sample liquidity measure. This is an ex-ante assignment — do not use post-shock data to form quartiles.

**Turnover proxy**: Use `n_trades` per symbol per day as a volume proxy if actual rupee turnover is not available in the trade panel. Alternatively, derive from the opening bar pickle if volume data is present there.

**Per-stratum model**: Run the same two-way clustered LPM as Test 4 (PostShock dummy, pre-stable dummy, two-way clustering by day and symbol) but restricted to only the stocks in that stratum.

Report for each stratum: β₁ (PostShock), two-way clustered SE, t-statistic, p-value, N_resolved (stable regime), N_resolved (post-shock regime), number of symbols.

**What to report (Table 11):** 8-row table, one row per stratum.

**What to report (Figure 7):** Coefficient plot (forest plot) showing β₁ and 95% confidence interval for each stratum.

---

## Test 10: Macro Horse Race — Sequential WLS Models

**Manuscript reference:** Table 12, Figure 8, Section 4.8

**Input files:**
- `data/daily/daily_series_clean.csv`
- `data/macro/XBR_USD Historical Data.csv`
- `data/macro/India VIX Historical Data.csv`
- `data/macro/Nifty 500 Historical Data.csv`
- `data/macro/INR_USD Historical Data.csv`
- `data/macro/NSE_Volume_Jan2022_to_May2026.csv`
- `data/macro/fii_dii_cash_2025_to_present.csv`
- `data/microstructure/opening_bar_ranges.pkl`

**Data preparation:**
1. Apply Muhurat purge to `daily_series_clean.csv`.
2. Merge macro series to daily series by date. All macro files must be date-aligned; drop days present in macro but not in strategy series.
3. Compute derived variables:
   - `R_brent`: daily log-return of Brent `Price` column
   - `abs_R_brent`: absolute value of `R_brent`
   - `sigma_brent_20d`: 20-day rolling standard deviation of `R_brent` (backward-looking)
   - `vix`: India VIX `Price` column level
   - `R_nifty500`: daily log-return of Nifty 500 `Price` column
   - `abs_R_nifty500`: absolute value of `R_nifty500`
   - `usd_inr_chg`: daily log-change of USD/INR `Price` column
   - `fii_net`: `FII_Net` column from fii_dii_cash file (Rs crore, may require sourcing 2022–2024 separately)
   - `ln_turnover`: natural log of `Turnover_Rs_Crore` from NSE volume file
   - `mean_bar0_range`: cross-sectional mean of `(High - Low) / Open` from first 1-minute bar in `opening_bar_ranges.pkl`
   - `sweet_spot_share`: fraction of resolved trades on that day with gap size in the "sweet spot" bin (researcher defines sweet spot based on Test 6 results)
4. Drop any day with missing values in any control variable used in the model being estimated.

**6 sequential WLS models:**

To prevent the partial 2025–2026 FII flows file (`fii_dii_cash_2025_to_present.csv`, ~337 trading days) from truncating the 2022–2024 sample (~1,010–1,050 trading days) in full-sample regressions, Models 1–5 are estimated on the full sample without `fii_net`. Model 6 evaluates the 2025–2026 sub-sample where direct FII flows are observed.

**WLS weighting:** `n_resolved` (daily count of resolved trades) as weights throughout.

**SE estimator:** Newey-West HAC with lag = 5 throughout.

**Dependent variable:** `resolved_wr` from `daily_series_clean.csv`.

---

**Model 1 — PostShock only (Full Sample):**

$$
WR_t = \alpha + \beta_1 \cdot \text{PostShock}_t + \varepsilon_t
$$

---

**Model 2 — Add VIX and market return (Full Sample):**

$$
WR_t = \alpha + \beta_1 \cdot \text{PostShock}_t + \beta_2 \cdot \text{VIX}_t + \beta_3 \cdot R_{\text{Nifty500},t} + \beta_4 \cdot |R_{\text{Nifty500},t}| + \varepsilon_t
$$

---

**Model 3 — Add USD/INR and log-turnover (Full Sample):**

$$
WR_t = \alpha + \beta_1 \cdot \text{PostShock}_t + \beta_2 \cdot \text{VIX}_t + \beta_3 \cdot R_{\text{Nifty500},t} + \beta_4 \cdot |R_{\text{Nifty500},t}| + \beta_5 \cdot \Delta \text{USD/INR}_t + \beta_6 \cdot \ln(\text{Turnover}_t) + \varepsilon_t
$$

---

**Model 4 — Microstructure and Gap Controls (Full Sample):**

$$
WR_t = \alpha + \beta_1 \cdot \text{PostShock}_t + \ldots + \beta_7 \cdot \overline{\text{Bar0Range}}_t + \beta_8 \cdot \text{SweetSpotShare}_t + \varepsilon_t
$$

(The `…` represents the same controls as Model 3. `fii_net` is excluded to preserve full 2022–2026 sample continuity.)

---

**Model 5 — Add Energy Volatility Controls (Full Sample):**

$$
WR_t = \alpha + \beta_1 \cdot \text{PostShock}_t + \ldots + \beta_9 \cdot \sigma_{\text{Brent},t}^{20d} + \beta_{10} \cdot |R_{\text{Brent},t}| + \varepsilon_t
$$

(The `…` represents all controls from Model 4.)

---

**Model 6 — Direct FII Net Flows (2025–2026 Sub-Sample):**

$$
WR_t = \alpha + \beta_1 \cdot \text{PostShock}_t + \ldots + \beta_{11} \cdot \text{FII\_Net}_t + \varepsilon_t
$$

(All controls from Model 5 plus `fii_net`, estimated on the 2025–2026 dates where FII net flows are observed.)

---

**What to report (Table 12):** For each of the 6 models — all coefficient estimates with Newey-West HAC (lag = 5) SEs in parentheses, t-statistics, significance stars (* p<0.10, ** p<0.05, *** p<0.01), weighted R², and number of observations N.

**What to report (Figure 8):** Coefficient plot of β₁ (PostShock) with 95% Newey-West HAC confidence intervals across all 6 models, where each x-axis label dynamically displays the model name and its exact sample size N (e.g., `Model 1\n(N=1,116)` vs. `Model 6\n(N=332)`), illustrating the attenuation of the post-shock coefficient as controls are sequentially added.

---

## Test 11: Granger Causality — Sign vs Magnitude of Oil Shock

**Manuscript reference:** Figure 6, Section 4.9

**Input files:**
- `data/daily/daily_series_clean.csv`
- `data/macro/XBR_USD Historical Data.csv`

**Cleaning steps:**
1. Apply Muhurat purge.
2. Merge Brent series to daily strategy series by date.
3. Compute:
   - `R_brent`: daily log-return of Brent `Price`
   - `abs_R_brent`: |R_brent|
   - `sigma_brent_20d`: 20-day rolling SD of R_brent (backward-looking)
   - `WR_t`: `resolved_wr` from daily series

**Purpose:** Test whether the *signed direction* of the Brent return, the *absolute magnitude*, or the *realized volatility* best Granger-causes the daily strategy win rate. This distinguishes a directional channel (long oil price moves hurt gap reversal returns) from a volatility/uncertainty channel.

**Bivariate Granger tests to run (all pairs below):**

For each lag order L ∈ {1, 3, 5, 10}:

1. `R_brent` → `WR_t`: Does lagged signed Brent return Granger-cause WR?
2. `abs_R_brent` → `WR_t`: Does lagged |Brent return| Granger-cause WR?
3. `sigma_brent_20d` → `WR_t`: Does lagged Brent realized vol Granger-cause WR?
4. `WR_t` → `R_brent`: Reverse causation check (WR should not cause Brent).
5. `WR_t` → `abs_R_brent`: Reverse causation check.

**Test statistic:** Standard Granger causality F-test based on SSR comparison between restricted model (WR regressed on its own lags only) and unrestricted model (WR regressed on its own lags and lags of the candidate causal variable). Use OLS throughout.

$$
F = \frac{(SSR_{\text{restricted}} - SSR_{\text{unrestricted}}) / L}{SSR_{\text{unrestricted}} / (T - 2L - 1)}
$$

**What to report (Figure 6):** Heatmap or grouped bar chart of F-statistics (or p-values) for each causal direction and each lag order. The chart should make visually clear which Brent variable (signed vs absolute vs volatility) has the strongest predictive relationship with WR_t.

If formal tabular results are included, report the F-statistic and p-value for each test cell (causal variable × lag order).

---

## Cross-Test Consistency Requirements

The following must be numerically consistent across all tests:

1. **Sample size**: After Muhurat purge, all tests drawing from the full sample must share the same set of 1,116 trading days.

2. **Resolved trade count**: The count of resolved trades in the Stable regime (from Test 4 LPM or Test 9 stratum for Full 480) must equal the count in Test 7's estimation window.

3. **Win-rate baseline**: The mean of `resolved_wr` in the Stable regime (computed in Test 1) should approximately equal μ used in the estimation window of Test 7 (the event study) — small differences are acceptable if the estimation window is a strict sub-window of the Stable regime.

4. **β₁ (PostShock) sign and direction**: The PostShock coefficient in Test 4 (trade-level LPM), Test 5 (daily WLS), and Table 12 Model 1 (macro horse race Model 1) are the same regression with different SE estimators and potentially different samples. Their point estimates should be numerically very close (within rounding). Large discrepancies indicate a data-cleaning inconsistency.

5. **Sector SECTOR_MAP**: Use the same `SECTOR_MAP.py` classification in both Test 8 (gap bin analysis, if sector-stratified) and Test 9 (sector DiD). Do not reclassify sectors between tests.

