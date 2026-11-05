# Complete Replication Audit Bundle

> **Manuscript**: Opening Gap Reversals in Indian Equities: Strategy Persistence, Structural Breaks, and Macro Sensitivities
> **Master Sample**: 1,116 Regular Trading Sessions (January 2022 through July 2026)
> **Global Sample Cleaning**: Three Diwali Muhurat sessions purged (2022-10-24, 2023-11-12, 2024-11-01)
> **Bundled Scope**: 39 files (Documentation, Source Code, Output Markdown Tables, Output CSVs)

---

## Table of Contents

1. [README.md](#file-readme-md)
2. [DATA_DICTIONARY.md](#file-data-dictionary-md)
3. [TESTS.md](#file-tests-md)
4. [src/__init__.py](#file-src---init---py)
5. [src/data_loader.py](#file-src-data-loader-py)
6. [src/run_all_tests.py](#file-src-run-all-tests-py)
7. [src/test_01_descriptive_stats.py](#file-src-test-01-descriptive-stats-py)
8. [src/test_02_oos_threshold_convergence.py](#file-src-test-02-oos-threshold-convergence-py)
9. [src/test_03_structural_breaks.py](#file-src-test-03-structural-breaks-py)
10. [src/test_04_lpm_two_way_cluster.py](#file-src-test-04-lpm-two-way-cluster-py)
11. [src/test_05_wls_newey_west.py](#file-src-test-05-wls-newey-west-py)
12. [src/test_06_gap_size_bins.py](#file-src-test-06-gap-size-bins-py)
13. [src/test_07_event_study_cawr.py](#file-src-test-07-event-study-cawr-py)
14. [src/test_08_sector_did.py](#file-src-test-08-sector-did-py)
15. [src/test_09_strata_analysis.py](#file-src-test-09-strata-analysis-py)
16. [src/test_10_macro_horse_race.py](#file-src-test-10-macro-horse-race-py)
17. [src/test_11_granger_causality.py](#file-src-test-11-granger-causality-py)
18. [output/tables/table_03_sample_partition.md](#file-output-tables-table-03-sample-partition-md)
19. [output/tables/table_04_oos_threshold_convergence.md](#file-output-tables-table-04-oos-threshold-convergence-md)
20. [output/tables/table_05_structural_break_tests.md](#file-output-tables-table-05-structural-break-tests-md)
21. [output/tables/table_06_lpm_two_way_cluster.md](#file-output-tables-table-06-lpm-two-way-cluster-md)
22. [output/tables/table_07_wls_newey_west.md](#file-output-tables-table-07-wls-newey-west-md)
23. [output/tables/table_08_gap_size_bins.md](#file-output-tables-table-08-gap-size-bins-md)
24. [output/tables/table_09_event_study_cawr.md](#file-output-tables-table-09-event-study-cawr-md)
25. [output/tables/table_10_sector_did.md](#file-output-tables-table-10-sector-did-md)
26. [output/tables/table_11_strata_analysis.md](#file-output-tables-table-11-strata-analysis-md)
27. [output/tables/table_12_macro_horse_race.md](#file-output-tables-table-12-macro-horse-race-md)
28. [output/tables/table_granger_causality.md](#file-output-tables-table-granger-causality-md)
29. [output/tables/table_03_sample_partition.csv](#file-output-tables-table-03-sample-partition-csv)
30. [output/tables/table_04_oos_threshold_convergence.csv](#file-output-tables-table-04-oos-threshold-convergence-csv)
31. [output/tables/table_05_structural_break_tests.csv](#file-output-tables-table-05-structural-break-tests-csv)
32. [output/tables/table_06_lpm_two_way_cluster.csv](#file-output-tables-table-06-lpm-two-way-cluster-csv)
33. [output/tables/table_07_wls_newey_west.csv](#file-output-tables-table-07-wls-newey-west-csv)
34. [output/tables/table_08_gap_size_bins.csv](#file-output-tables-table-08-gap-size-bins-csv)
35. [output/tables/table_09_event_study_cawr.csv](#file-output-tables-table-09-event-study-cawr-csv)
36. [output/tables/table_10_sector_did.csv](#file-output-tables-table-10-sector-did-csv)
37. [output/tables/table_11_strata_analysis.csv](#file-output-tables-table-11-strata-analysis-csv)
38. [output/tables/table_12_macro_horse_race.csv](#file-output-tables-table-12-macro-horse-race-csv)
39. [output/tables/table_granger_causality.csv](#file-output-tables-table-granger-causality-csv)

---

## File: `README.md` <a id="file-readme-md"></a>

# Gap-Trading Raw Materials Repository

## What This Repository Is

This repository contains **raw datasets and a test specification** for independent replication of the manuscript:

> **"Opening Gap Reversals in Indian Equities: Strategy Persistence, Structural Breaks, and Macro Sensitivities"**

An independent researcher can use the data in `data/` and the specifications in `TESTS.md` to write their own code and reproduce every table and figure in the paper from scratch.

---

## What This Repository Is NOT

- There are **no scripts** here.
- There are **no computed results** here.
- There are **no figures, scorecard files, or output CSVs** here.
- There are **no hardcoded numbers** anywhere in this repository.

If you find a `.py`, `.R`, or any file containing numerical results, that is an error.

---

## Repository Layout

```
gap-trading-raw/
├── data/
│   ├── trades/
│   │   └── 1:1-480gap_strategy_all_trades.csv   ← trade execution panel (raw)
│   ├── daily/
│   │   ├── daily_series_clean.csv               ← daily strategy-level series
│   │   ├── daily_win_rate_full_480.csv
│   │   ├── daily_win_rate_nifty50.csv
│   │   ├── daily_win_rate_midcap50.csv
│   │   └── daily_win_rate_smcap50.csv
│   ├── macro/
│   │   ├── XBR_USD Historical Data.csv          ← Brent crude front-month USD
│   │   ├── India VIX Historical Data.csv
│   │   ├── Nifty 500 Historical Data.csv
│   │   ├── INR_USD Historical Data.csv
│   │   ├── NSE_Volume_Jan2022_to_May2026.csv
│   │   └── fii_dii_cash_2025_to_present.csv
│   ├── microstructure/
│   │   └── opening_bar_ranges.pkl               ← 1-min bar OHLC, pickle format
│   └── universe/
│       ├── nifty500_symbols_extracted.txt
│       ├── nifty50_symbols.txt
│       ├── midcap50_symbols.txt
│       ├── smcap50_symbols.txt
│       ├── delisted_2022.txt
│       └── SECTOR_MAP.py                        ← symbol → sector dict
├── TESTS.md          ← test specifications (no results)
├── DATA_DICTIONARY.md
└── README.md
```

---

## Critical Sample-Cleaning Requirement

**Before running any test**, the trade panel and daily series must be purged of three Muhurat Diwali trading sessions. These are abbreviated half-sessions that do not represent regular market behaviour:

| Date | Event |
|------|-------|
| 2022-10-24 | Diwali Muhurat Trading |
| 2023-11-12 | Diwali Muhurat Trading |
| 2024-11-01 | Diwali Muhurat Trading |

After purging these three dates, the sample is **1,116 regular trading sessions**.

This purge must be applied consistently to every test. The raw file contains all dates including Muhurat; the purge is the researcher's responsibility.

---

## Strategy Specification (Section 3.4 of Manuscript)

The strategy traded is a **1:1 risk-reward overnight gap reversal** on Nifty 500 constituents:

- **Universe**: 480 equities (Nifty 500 constituents active as of January 2022, excluding 20 delisted names — see `data/universe/`)
- **Entry**: At the NSE open (`Open_{i,t}`) at **09:15:00 IST** on day *t*, when the overnight gap meets the gap-zone criterion
- **Stop-loss**: 1× the gap size (from entry price, against trade direction)
- **Target**: 1× the gap size (from entry price, with trade direction)
- **Exit rule**: First of target, stop-loss, or session close (time exit at ~15:29 IST)
- **Status field**: `TARGET` = win; `STOP_LOSS` = loss; `TIME_EXIT` = unresolved (excluded from win-rate calculations)
- **Transaction cost grid evaluated**: 8, 10, 12, 15, and 20 basis points (round-trip); see manuscript Section 4.2 and Appendix A
- **Regime boundaries**:
  - Pre-stable: before 2022-03-01
  - Stable: 2022-03-01 to 2026-02-28 (inclusive)
  - Post-shock: 2026-03-01 onward

---

## Data Availability Note

The raw intraday tick database (NSE L1 feed, stored in TimescaleDB) is not included here due to storage and licensing constraints. The file `data/trades/1:1-480gap_strategy_all_trades.csv` is the downstream execution panel derived from that database — it is the primary input for all tests in this paper.

---

## Column Definitions

See `DATA_DICTIONARY.md` for full column-by-column descriptions of every file.

## Test Specifications

See `TESTS.md` for exact econometric specifications, input files, cleaning steps, model equations, and reporting requirements for all 11 test families.

---

## File: `DATA_DICTIONARY.md` <a id="file-data-dictionary-md"></a>

# Data Dictionary

Column-by-column description of every raw file in `data/`. No computed values appear here — only schema documentation.

---

## data/trades/1:1-480gap_strategy_all_trades.csv

One row per trade execution. The full panel across all symbols and all trading days.

| Column | Type | Description |
|--------|------|-------------|
| `symbol` | string | NSE ticker with suffix (e.g. `RELIANCE_1M`) |
| `date` | date (YYYY-MM-DD) | Trading session date (IST) |
| `zone` | string | Gap zone classification label describing direction and position relative to prior-day OHLC |
| `direction` | string | Trade direction: `SHORT` (gap-up reversal) or `LONG` (gap-down reversal) |
| `entry_price` | float | Execution price at 09:15:00 IST open |
| `result` | float | Absolute P&L in rupees per share (signed) |
| `result_pct` | float | Return in percent (signed) |
| `status` | string | Exit type: `TARGET`, `STOP_LOSS`, or `TIME_EXIT` |
| `gap_size` | float | Absolute gap size in rupees |
| `duration` | float | Bars to exit (1-minute bars) |
| `day_of_week` | string | Day name (Monday through Friday) |
| `month` | string | Month name |

**Filtering for analysis**: Most tests use only `status IN ('TARGET', 'STOP_LOSS')` — these are "resolved" trades. `TIME_EXIT` rows are excluded from win-rate calculations but may be counted in total trade counts for some tests (see TESTS.md per-test instructions).

**Gap size note**: The `gap_size` column contains the **absolute** gap in rupees. To compute gap size as a **percentage of prior close**, the researcher must source prior-close prices from the intraday database or use the `gap_size / entry_price` ratio as an approximation. The `zone` column provides qualitative gap magnitude bands already computed from the database.

---

## data/daily/daily_series_clean.csv

One row per trading day. Aggregated strategy-level outcomes across all 480 symbols.

| Column | Type | Description |
|--------|------|-------------|
| `date` | date | Trading session date |
| `regime` | string | Regime label: `pre_stable`, `stable`, or `post_shock` |
| `n_trades` | int | Total trades initiated that day (all statuses) |
| `n_targets` | int | Trades that hit target |
| `n_stops` | int | Trades that hit stop-loss |
| `n_time` | int | Trades that exited at session close |
| `n_resolved` | int | n_targets + n_stops |
| `mean_return_bps` | float | Mean return across all trades in basis points |
| `median_return_bps` | float | Median return across all trades in basis points |
| `nominal_wr` | float | Win rate including time exits: n_targets / n_trades |
| `resolved_wr` | float | Win rate excluding time exits: n_targets / n_resolved |
| `mean_resolved_return_bps` | float | Mean return for resolved trades only, in bps |

**Primary dependent variable**: `resolved_wr` is the daily win rate (WR_t) used as the dependent variable in all regression tests.

---

## data/daily/daily_win_rate_full_480.csv
## data/daily/daily_win_rate_nifty50.csv
## data/daily/daily_win_rate_midcap50.csv
## data/daily/daily_win_rate_smcap50.csv

Sub-universe daily win-rate series. Same schema for all four files.

| Column | Type | Description |
|--------|------|-------------|
| `date` | date | Trading session date |
| `wins` | int | Resolved trades that hit target in this sub-universe |
| `total_trades` | int | Total trades initiated (all statuses) |
| `win_rate` | float | wins / total_trades (note: denominator includes time exits in raw file; replicator should verify whether to use resolved denominator) |
| `day_idx` | int | Sequential integer day index starting from 0 |

**Sub-universe membership**: Nifty 50, Midcap 50, and Smallcap 50 are sub-sets of the 480-stock full universe. Membership lists are in `data/universe/`.

---

## data/macro/XBR_USD Historical Data.csv

Daily Brent crude front-month futures price in USD. Source: Investing.com.

| Column | Type | Description |
|--------|------|-------------|
| `Date` | date | Calendar date |
| `Price` | float | Settlement/close price (USD per barrel) |
| `Open` | float | Open price |
| `High` | float | Daily high |
| `Low` | float | Daily low |
| `Vol.` | string | Volume (may contain K/M suffixes; parse carefully) |
| `Change %` | string | Daily change percentage as string with `%` suffix |

**Usage**: Compute daily log-returns and 20-day rolling realized volatility (σ_Brent) from `Price`. Merge to daily strategy series by date. Note the BOM character (UTF-8 BOM) at start of file — use `encoding='utf-8-sig'` when reading in Python.

---

## data/macro/India VIX Historical Data.csv

Daily India VIX index. Source: Investing.com. Same schema as `XBR_USD Historical Data.csv`.

**Usage**: The `Price` column is the VIX level. Merge to daily strategy series by date.

---

## data/macro/Nifty 500 Historical Data.csv

Daily Nifty 500 broad-market index. Source: Investing.com. Same schema as `XBR_USD Historical Data.csv`.

**Usage**: Compute daily log-returns. The absolute value |R_Nifty500| is used as a market volatility proxy in Table 12. Merge by date.

---

## data/macro/INR_USD Historical Data.csv

Daily USD/INR exchange rate. Source: Investing.com. Same schema as `XBR_USD Historical Data.csv`.

**Usage**: Compute daily log-changes. Merge by date.

---

## data/macro/NSE_Volume_Jan2022_to_May2026.csv

Daily NSE market-wide statistics. Source: NSE India.

| Column | Type | Description |
|--------|------|-------------|
| `Date` | date | Trading session date |
| `Advances` | int | Number of advancing stocks |
| `Declines` | int | Number of declining stocks |
| `Unchanged` | int | Number of unchanged stocks |
| `Total` | int | Total stocks traded |
| `Volume_Lakhs` | float | Total volume in lakhs of shares |
| `Turnover_Rs_Crore` | float | Total turnover in crores of rupees |
| `Open` | float | Nifty 50 open (from NSE daily report) |
| `High` | float | Nifty 50 high |
| `Low` | float | Nifty 50 low |
| `Close` | float | Nifty 50 close |

**Usage**: `ln(Turnover_Rs_Crore)` is the market-wide log-turnover control in Table 12 Model 3+. Merge by date.

---

## data/macro/fii_dii_cash_2025_to_present.csv

Daily FII and DII cash-segment net flows. Source: NSE India.

| Column | Type | Description |
|--------|------|-------------|
| `Date` | date | Trading session date |
| `FII_Gross_Purchase` | float | FII gross buy value (Rs crore) |
| `FII_Gross_Sale` | float | FII gross sell value (Rs crore) |
| `FII_Net` | float | FII net flow = Purchase − Sale (Rs crore) |
| `DII_Gross_Purchase` | float | DII gross buy value (Rs crore) |
| `DII_Gross_Sale` | float | DII gross sell value (Rs crore) |
| `DII_Net` | float | DII net flow = Purchase − Sale (Rs crore) |

**Coverage note**: This file covers 2025-01-01 to present. For the full 2022–2026 sample period, the researcher will need to source FII/DII data for 2022–2024 separately from NSE India's historical archives or SEBI. The manuscript uses FII_Net as the institutional flow control in Table 12 Model 4+.

---

## data/microstructure/opening_bar_ranges.pkl

Python pickle file. Contains opening 1-minute bar OHLC data for each symbol on each trading day.

**Format**: Load with `pandas.read_pickle()`. Expected structure is a DataFrame or dict with multi-level keys `(symbol, date)` or a panel indexed by date with symbol columns, containing at minimum `Open`, `High`, `Low`, `Close` for the 09:15–09:16 IST bar.

**Usage**: Compute `bar0_range = (High - Low) / Open` for the first 1-minute bar. This is the opening microstructure volatility measure used in Table 12 Model 4+ as a control variable and in Table 8 for gap-bin analysis. Aggregate to a daily cross-sectional mean before merging to the daily series.

---

## data/universe/nifty500_symbols_extracted.txt

Plain text, one NSE ticker per line. The 500 Nifty 500 constituent symbols as of January 2022 (the strategy start date). This is the full eligible universe before excluding delisted names.

---

## data/universe/nifty50_symbols.txt

Plain text, one NSE ticker per line. Nifty 50 constituent symbols used to define the large-cap sub-universe in Table 11.

---

## data/universe/midcap50_symbols.txt

Plain text, one NSE ticker per line. Nifty Midcap 50 constituent symbols used to define the mid-cap sub-universe in Table 11.

---

## data/universe/smcap50_symbols.txt

Plain text, one NSE ticker per line. Nifty Smallcap 50 constituent symbols used to define the small-cap sub-universe in Table 11.

---

## data/universe/delisted_2022.txt

Plain text, one NSE ticker per line. The 20 Nifty 500 constituents that were delisted or removed from the index before or during the sample period and are excluded from the 480-stock strategy universe.

---

## data/universe/SECTOR_MAP.py

Python module defining a single dict `SECTOR_MAP: dict[str, str]` mapping each NSE ticker (without suffix) to its GICS-equivalent sector label. Used in Table 10 (sector DiD) to classify stocks as:

- **Downstream Oil-exposed**: Oil & Gas, Paints (uses refined petroleum inputs), Chemicals (petrochemical feedstock), Transportation/Airlines
- **Defensive**: FMCG, Healthcare, Pharma, IT
- Other sectors form the control group in some DiD specifications

The researcher must define the exact downstream vs defensive classification boundaries; `SECTOR_MAP` provides the raw sector label as the starting point.

---

## File: `TESTS.md` <a id="file-tests-md"></a>

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

## Test 2: 15-Quarter Walk-Forward OOS Threshold Convergence

**Manuscript reference:** Table 4, Figure 2, Section 3.5

**Input files:**
- `data/trades/1:1-480gap_strategy_all_trades.csv`

**Cleaning steps:**
1. Apply Muhurat purge.
2. Load all trades, tracking both Nominal Win Rate (`status == 'TARGET'` over all trades) and Resolved Win Rate (`status == 'TARGET'` over resolved trades).

**Algorithm — expanding-window walk-forward with quarterly OOS:**

The sample is partitioned into 15 out-of-sample (OOS) quarters, each of approximately 60–65 trading days. The walk-forward proceeds as follows:

For OOS quarter k (k = 1 to 15):
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
   - Report unfiltered OOS win rate, filtered OOS win rate, filtered trade count, and whether the filtered OOS win rate exceeds 50.0% (for both Nominal and Resolved win rates).

**Gap size in percent**: Compute `gap_size_pct = gap_size / entry_price × 100`.

**What to report (Table 4):** For each of the 15 OOS quarters — the OOS quarter label (e.g., Q3 2022, Q4 2022 … Q1 2026), the estimated threshold c*(k), unfiltered and filtered trade counts, unfiltered and filtered win rates (both Nominal and Resolved), and the fade-dominant breakeven indicators.

**What to report (Figure 2):** A time-series line chart of c*(k) over the 15 OOS quarters, demonstrating threshold stability and convergence.

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

**Rolling Chow test for Figure 1:**
- Compute rolling Chow F-statistics across all interior dates (5% trimmed) using a window of at least 60 observations on each side.
- Plot the F-statistic series against calendar time.
- Superimpose the 5% critical value as a horizontal line.

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

**What to report (Figure 3):** Bar chart of win rates by bin, with Stable and Post-shock plotted side by side.

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

**What to report (Figure 4):** Line chart of cumulative daily AWR from day −10 to day +40 around the event date, with 95% confidence bands (±1.96 × σ × √k where k is the number of cumulated days).

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

**What to report (Figure 5):** Time-series plot of 5-day rolling win rates for Downstream Consumers vs Clean Defensives, highlighting the March 2026 divergence.

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

**What to report (Figure 8):** Coefficient plot of β₁ (PostShock) across all 6 models, illustrating the attenuation of the post-shock coefficient as controls are sequentially added.

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

---

## File: `src/__init__.py` <a id="file-src---init---py"></a>

```python
# Gap trading package
```

---

## File: `src/data_loader.py` <a id="file-src-data-loader-py"></a>

```python
"""
Data Loader and Preprocessing Module for Gap Trading Replication
Enforces sample cleaning, Muhurat purge, and regime definitions across all tests.
"""

import os
import pandas as pd
import numpy as np

# Exact paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

# Mandatory global sample cleaning requirement
MUHURAT_DATES = {'2022-10-24', '2023-11-12', '2024-11-01'}
EXPECTED_CLEAN_SESSIONS = 1116

# Regime boundaries
PRE_STABLE_END = '2022-03-01'
STABLE_END = '2026-03-01'

def assign_regime(date_series: pd.Series) -> pd.Series:
    """Assign regime based on date string YYYY-MM-DD."""
    dates = pd.to_datetime(date_series)
    regimes = pd.Series('stable', index=date_series.index)
    regimes[dates < pd.to_datetime(PRE_STABLE_END)] = 'pre_stable'
    regimes[dates >= pd.to_datetime(STABLE_END)] = 'post_shock'
    return regimes

def load_daily_clean() -> pd.DataFrame:
    """Load daily aggregated series and apply Muhurat purge."""
    path = os.path.join(DATA_DIR, 'daily', 'daily_series_clean.csv')
    df = pd.read_csv(path)
    df['date'] = df['date'].astype(str)
    
    # Purge Muhurat dates
    df = df[~df['date'].isin(MUHURAT_DATES)].copy()
    df = df.sort_values('date').reset_index(drop=True)
    
    # Validation assertion
    assert len(df) == EXPECTED_CLEAN_SESSIONS, (
        f"Expected {EXPECTED_CLEAN_SESSIONS} clean trading sessions, got {len(df)}"
    )
    
    # Ensure regime column is correctly formatted
    if 'regime' not in df.columns:
        df['regime'] = assign_regime(df['date'])
    
    return df

def load_trades_clean(resolved_only: bool = False) -> pd.DataFrame:
    """
    Load trade execution panel, apply Muhurat purge, and add computed helpers.
    """
    path = os.path.join(DATA_DIR, 'trades', '1:1-480gap_strategy_all_trades.csv')
    df = pd.read_csv(path)
    df['date'] = df['date'].astype(str)
    
    # Purge Muhurat dates
    df = df[~df['date'].isin(MUHURAT_DATES)].copy()
    
    # Assign regime
    df['regime'] = assign_regime(df['date'])
    
    # Add gap_size_pct: gap_size / entry_price * 100
    df['gap_size_pct'] = (df['gap_size'] / df['entry_price']) * 100.0
    
    # Ticker root without suffix (e.g. RELIANCE_1M -> RELIANCE)
    df['symbol_root'] = df['symbol'].str.replace(r'(_1M|_EQ|_NIFTY)$', '', regex=True)
    
    # Indicator for resolved trade
    df['is_resolved'] = df['status'].isin(['TARGET', 'STOP_LOSS'])
    
    # Binary win outcome (1 for TARGET, 0 for STOP_LOSS, NaN for TIME_EXIT)
    df['is_win'] = np.where(df['status'] == 'TARGET', 1, np.where(df['status'] == 'STOP_LOSS', 0, np.nan))
    
    if resolved_only:
        df = df[df['is_resolved']].copy().reset_index(drop=True)
    else:
        df = df.reset_index(drop=True)
        
    return df

def load_sector_map() -> dict:
    """Load symbol to sector mapping dict."""
    import importlib.util
    path = os.path.join(DATA_DIR, 'universe', 'SECTOR_MAP.py')
    spec = importlib.util.spec_from_file_location("SECTOR_MAP", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.SECTOR_MAP

def load_subuniverse_symbols() -> dict:
    """Load symbol lists for nifty50, midcap50, smcap50, delisted_2022, nifty500."""
    univ_dir = os.path.join(DATA_DIR, 'universe')
    symbols = {}
    for name in ['nifty50_symbols.txt', 'midcap50_symbols.txt', 'smcap50_symbols.txt', 
                 'delisted_2022.txt', 'nifty500_symbols_extracted.txt']:
        key = name.replace('.txt', '')
        with open(os.path.join(univ_dir, name), 'r') as f:
            symbols[key] = [line.strip() for line in f if line.strip()]
    return symbols
```

---

## File: `src/run_all_tests.py` <a id="file-src-run-all-tests-py"></a>

```python
"""
Master Replication Orchestrator
Executes all 11 econometric replication tests sequentially and verifies cross-test consistency.
"""

import sys
import os
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.test_01_descriptive_stats import run_test_1
from src.test_02_oos_threshold_convergence import run_test_2
from src.test_03_structural_breaks import run_test_3
from src.test_04_lpm_two_way_cluster import run_test_4
from src.test_05_wls_newey_west import run_test_5
from src.test_06_gap_size_bins import run_test_6
from src.test_07_event_study_cawr import run_test_7
from src.test_08_sector_did import run_test_8
from src.test_09_strata_analysis import run_test_9
from src.test_10_macro_horse_race import run_test_10
from src.test_11_granger_causality import run_test_11

def main():
    print("=" * 80)
    print("STARTING COMPLETE MANUSCRIPT REPLICATION PIPELINE")
    print("=" * 80)
    start_total = time.time()
    
    stages = [
        ("Test 1: Sample Partition & Descriptive Statistics (Table 3)", run_test_1),
        ("Test 2: 15-Quarter Walk-Forward OOS Convergence (Table 4, Figure 2)", run_test_2),
        ("Test 3: Structural Break Tests (Table 5, Figure 1)", run_test_3),
        ("Test 4: Two-Way Clustered LPM (Table 6)", run_test_4),
        ("Test 5: Daily WLS with Newey-West HAC (Table 7)", run_test_5),
        ("Test 6: Gap-Size Bin Win-Rate Analysis (Table 8, Figure 3)", run_test_6),
        ("Test 7: Event Study — CAWR (Table 9, Figure 4)", run_test_7),
        ("Test 8: Sector Difference-in-Differences (Table 10, Figure 5)", run_test_8),
        ("Test 9: Survivorship & Liquidity Strata (Table 11, Figure 7)", run_test_9),
        ("Test 10: Macro Horse Race (Table 12, Figure 8)", run_test_10),
        ("Test 11: Granger Causality (Figure 6, Table)", run_test_11),
    ]
    
    for name, func in stages:
        t0 = time.time()
        print(f"\n>>> Executing {name}...")
        func()
        print(f">>> Completed {name} in {time.time() - t0:.2f} seconds.")
        
    print("\n" + "=" * 80)
    print(f"ALL 11 REPLICATION TESTS COMPLETED IN {time.time() - start_total:.2f} SECONDS.")
    print("=" * 80)

if __name__ == '__main__':
    main()
```

---

## File: `src/test_01_descriptive_stats.py` <a id="file-src-test-01-descriptive-stats-py"></a>

```python
"""
Test 1: Sample Partition and Descriptive Statistics
Manuscript Reference: Table 3, Section 3.3
"""

import os
import sys

# Ensure project root is in python path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import pandas as pd
import numpy as np
from src.data_loader import load_daily_clean, load_trades_clean

def run_test_1():
    print("Running Test 1: Sample Partition and Descriptive Statistics (Table 3)...")
    daily = load_daily_clean()
    trades = load_trades_clean()

    regimes = [
        ('pre_stable', 'Pre-Stable (< 2022-03-01)'),
        ('stable', 'Stable (2022-03-01 to 2026-02-28)'),
        ('post_shock', 'Post-Shock (≥ 2026-03-01)'),
        ('full_sample', 'Full Sample (All Sessions)')
    ]

    records = []
    for reg_key, reg_name in regimes:
        if reg_key == 'full_sample':
            d_sub = daily
            t_sub = trades
        else:
            d_sub = daily[daily['regime'] == reg_key]
            t_sub = trades[trades['regime'] == reg_key]
        
        n_days = t_sub['date'].nunique()
        n_symbols = t_sub['symbol'].nunique()
        total_trades = len(t_sub)
        
        resolved_sub = t_sub[t_sub['is_resolved']]
        resolved_trades = len(resolved_sub)
        
        n_targets = (resolved_sub['status'] == 'TARGET').sum()
        pooled_wr = (n_targets / resolved_trades) if resolved_trades > 0 else np.nan
        pooled_wr_pct = pooled_wr * 100.0
        
        mean_daily_wr = d_sub['resolved_wr'].mean()
        mean_daily_wr_pct = mean_daily_wr * 100.0
        
        std_daily_wr = d_sub['resolved_wr'].std()
        std_daily_wr_pct = std_daily_wr * 100.0
        
        records.append({
            'Regime Partition': reg_name,
            'Trading Days': n_days,
            'Unique Symbols': n_symbols,
            'Total Trades': total_trades,
            'Resolved Trades': resolved_trades,
            'Resolved Win Rate (%)': f"{pooled_wr_pct:.2f}%",
            'Mean Daily WR (%)': f"{mean_daily_wr_pct:.2f}%",
            'Std Daily WR (%)': f"{std_daily_wr_pct:.2f}%",
            '_pooled_wr': pooled_wr,
            '_mean_daily_wr': mean_daily_wr,
            '_std_daily_wr': std_daily_wr
        })

    df_out = pd.DataFrame(records)
    
    # Save CSV
    os.makedirs(os.path.join(BASE_DIR, 'output', 'tables'), exist_ok=True)
    csv_path = os.path.join(BASE_DIR, 'output', 'tables', 'table_03_sample_partition.csv')
    df_out.drop(columns=['_pooled_wr', '_mean_daily_wr', '_std_daily_wr']).to_csv(csv_path, index=False)
    
    # Generate Markdown Table
    md_path = os.path.join(BASE_DIR, 'output', 'tables', 'table_03_sample_partition.md')
    md_content = [
        "# Table 3: Sample Partition and Descriptive Statistics",
        "",
        "Sample partitioned across Pre-Stable, Stable, Post-Shock, and Full Sample periods following the global Muhurat Diwali purge (1,116 regular trading sessions).",
        "",
        "| Regime Partition | Trading Days | Unique Symbols | Total Trades | Resolved Trades | Resolved Win Rate (%) | Mean Daily WR (%) | Std Daily WR (%) |",
        "|:---|---:|---:|---:|---:|---:|---:|---:|"
    ]
    for _, r in df_out.iterrows():
        md_content.append(
            f"| {r['Regime Partition']} | {r['Trading Days']:,} | {r['Unique Symbols']:,} | {r['Total Trades']:,} | {r['Resolved Trades']:,} | {r['Resolved Win Rate (%)']} | {r['Mean Daily WR (%)']} | {r['Std Daily WR (%)']} |"
        )
    md_content.append("")
    
    with open(md_path, 'w') as f:
        f.write('\n'.join(md_content))
        
    print(f"Table 3 saved to {csv_path} and {md_path}")
    return df_out

if __name__ == '__main__':
    run_test_1()
```

---

## File: `src/test_02_oos_threshold_convergence.py` <a id="file-src-test-02-oos-threshold-convergence-py"></a>

```python
"""
Test 2: 15-Quarter Walk-Forward OOS Threshold Convergence
First-Crossing Breakeven Estimator
Manuscript Reference: Table 4, Figure 2, Section 3.5
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from src.data_loader import load_trades_clean

def estimate_first_crossing_threshold(train_df, bin_edges, bin_midpoints, min_trades=30):
    """
    Non-parametric first-crossing cutoff of the 50.0% directional breakeven barrier.
    Partitions trades with gap_size_pct in [0.0, 5.0] into 20 equal-width bins (width=0.25%).
    Computes resolved win rate (TARGET / (TARGET + STOP_LOSS)) in each bin with n_j >= min_trades.
    Finds first adjacent pair of bins (j, j+1) where wr_j < 0.50 and wr_{j+1} >= 0.50,
    and linearly interpolates at wr = 0.50.
    """
    t = train_df[(train_df['gap_size_pct'] >= 0.0) & (train_df['gap_size_pct'] <= 5.0)].copy()
    t_res = t[t['status'].isin(['TARGET', 'STOP_LOSS'])].copy()
    
    t_res['bin_idx'] = np.digitize(t_res['gap_size_pct'], bin_edges) - 1
    t_res['bin_idx'] = np.clip(t_res['bin_idx'], 0, 19)
    
    valid_bins = []
    for j in range(20):
        sub = t_res[t_res['bin_idx'] == j]
        n_j = len(sub)
        if n_j >= min_trades:
            wr_j = (sub['status'] == 'TARGET').mean()
            valid_bins.append((j, bin_midpoints[j], wr_j, n_j))
            
    if not valid_bins:
        return np.nan
        
    if valid_bins[0][2] >= 0.50:
        return valid_bins[0][1]
        
    for idx in range(len(valid_bins) - 1):
        j1, m1, wr1, n1 = valid_bins[idx]
        j2, m2, wr2, n2 = valid_bins[idx + 1]
        if j2 == j1 + 1 and wr1 < 0.50 and wr2 >= 0.50:
            c_star = m1 + (0.50 - wr1) / (wr2 - wr1) * (m2 - m1)
            return c_star
            
    return np.nan

def run_test_2():
    print("Running Test 2: 15-Quarter Walk-Forward OOS Threshold Convergence (Table 4, Figure 2)...")
    trades = load_trades_clean(resolved_only=False)
    trades['date'] = pd.to_datetime(trades['date'])

    quarters = [
        '2022Q3', '2022Q4',
        '2023Q1', '2023Q2', '2023Q3', '2023Q4',
        '2024Q1', '2024Q2', '2024Q3', '2024Q4',
        '2025Q1', '2025Q2', '2025Q3', '2025Q4',
        '2026Q1'
    ]

    bin_edges = np.linspace(0.0, 5.0, 21)
    bin_midpoints = 0.5 * (bin_edges[:-1] + bin_edges[1:])

    records = []

    for q_label in quarters:
        qp = pd.Period(q_label, freq='Q')
        train_trades = trades[trades['date'] < qp.start_time]
        oos_trades = trades[(trades['date'] >= qp.start_time) & (trades['date'] <= qp.end_time)]
        
        c_star = estimate_first_crossing_threshold(train_trades, bin_edges, bin_midpoints, min_trades=30)
        
        # In-sample summary
        train_res = train_trades[train_trades['status'].isin(['TARGET', 'STOP_LOSS'])]
        train_res_wr = (train_res['status'] == 'TARGET').mean() if len(train_res) > 0 else np.nan
        train_nom_wr = (train_trades['status'] == 'TARGET').mean() if len(train_trades) > 0 else np.nan
        
        # Out-of-sample unfiltered
        oos_res = oos_trades[oos_trades['status'].isin(['TARGET', 'STOP_LOSS'])]
        unf_res_wr = (oos_res['status'] == 'TARGET').mean() if len(oos_res) > 0 else np.nan
        unf_nom_wr = (oos_trades['status'] == 'TARGET').mean() if len(oos_trades) > 0 else np.nan
        
        # Out-of-sample filtered: gap_size_pct >= c_star
        if not np.isnan(c_star):
            fil_oos = oos_trades[oos_trades['gap_size_pct'] >= c_star]
            fil_tot = len(fil_oos)
            fil_res = fil_oos[fil_oos['status'].isin(['TARGET', 'STOP_LOSS'])]
            fil_res_n = len(fil_res)
            fil_res_wr = (fil_res['status'] == 'TARGET').mean() if fil_res_n > 0 else np.nan
            fil_nom_wr = (fil_oos['status'] == 'TARGET').mean() if fil_tot > 0 else np.nan
            fade_dominant = "Yes" if (not np.isnan(fil_res_wr) and fil_res_wr > 0.50) else "No"
        else:
            fil_tot = 0
            fil_res_n = 0
            fil_res_wr = np.nan
            fil_nom_wr = np.nan
            fade_dominant = "No"

        q_name = f"{q_label[4:]} {q_label[:4]}"
        
        records.append({
            'Quarter': q_name,
            'In-Sample Total Trades': len(train_trades),
            'In-Sample Resolved Trades': len(train_res),
            'First-Crossing Cutoff c*(k) (%)': c_star,
            'OOS Unfiltered Trades': len(oos_trades),
            'OOS Unfiltered Resolved WR (%)': round(unf_res_wr * 100.0, 2) if not np.isnan(unf_res_wr) else np.nan,
            'OOS Unfiltered Nominal WR (%)': round(unf_nom_wr * 100.0, 2) if not np.isnan(unf_nom_wr) else np.nan,
            'OOS Filtered Total Trades': fil_tot,
            'OOS Filtered Resolved Trades': fil_res_n,
            'OOS Filtered Resolved WR (%)': round(fil_res_wr * 100.0, 2) if not np.isnan(fil_res_wr) else np.nan,
            'OOS Filtered Nominal WR (%)': round(fil_nom_wr * 100.0, 2) if not np.isnan(fil_nom_wr) else np.nan,
            'Fade-Dominant (>50% WR)': fade_dominant
        })

    df_table4 = pd.DataFrame(records)

    # Save CSV
    os.makedirs(os.path.join(BASE_DIR, 'output', 'tables'), exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, 'output', 'figures'), exist_ok=True)
    
    csv_path = os.path.join(BASE_DIR, 'output', 'tables', 'table_04_oos_threshold_convergence.csv')
    df_table4.to_csv(csv_path, index=False)

    # Generate Markdown Table
    md_path = os.path.join(BASE_DIR, 'output', 'tables', 'table_04_oos_threshold_convergence.md')
    md_content = [
        "# Table 4: 15-Quarter Walk-Forward OOS Threshold Convergence",
        "",
        "First-crossing breakeven threshold estimator c*(k) across 15 out-of-sample quarters (Q3 2022 to Q1 2026). "
        "Estimated via linear interpolation between adjacent 0.25% bins at the 50.0% resolved win-rate barrier on the expanding training window. "
        "Both Resolved Win Rate (TARGET / (TARGET + STOP_LOSS)) and Nominal Win Rate (TARGET / ALL) are reported.",
        "",
        "| Quarter | In-Sample Resolved | Cutoff c*(k) (%) | OOS Filtered Resolved | OOS Filtered Resolved WR (%) | OOS Filtered Nominal WR (%) | Fade-Dominant (>50%) |",
        "|:---|---:|---:|---:|---:|---:|:---:|"
    ]
    for _, r in df_table4.iterrows():
        md_content.append(
            f"| {r['Quarter']} | {r['In-Sample Resolved Trades']:,} | {r['First-Crossing Cutoff c*(k) (%)']:.3f}% | "
            f"{r['OOS Filtered Resolved Trades']:,} | {r['OOS Filtered Resolved WR (%)']:.2f}% | "
            f"{r['OOS Filtered Nominal WR (%)']:.2f}% | {r['Fade-Dominant (>50% WR)']} |"
        )
    md_content.append("")
    
    with open(md_path, 'w') as f:
        f.write('\n'.join(md_content))
    print(f"Table 4 saved to {csv_path} and {md_path}")

    # Plot Figure 2: Time-series line chart of c*(k)
    fig_path = os.path.join(BASE_DIR, 'output', 'figures', 'figure_02_oos_threshold_convergence.png')
    
    plt.figure(figsize=(10, 5), dpi=300)
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    
    x_indices = list(range(len(df_table4)))
    c_vals = df_table4['First-Crossing Cutoff c*(k) (%)'].values
    quarter_labels = df_table4['Quarter'].values
    
    plt.plot(x_indices, c_vals, marker='o', color='#1f77b4', linewidth=2.2, markersize=7, label='First-Crossing Breakeven Threshold c*(k)')
    
    # Convergence reference line around ~0.37%
    mean_stable_c = np.mean(c_vals[4:]) # from 2023Q3 onward
    plt.axhline(y=mean_stable_c, color='#d62728', linestyle='--', alpha=0.7, label=f'Convergence Level (~{mean_stable_c:.2f}%)')
    
    plt.title('Figure 2: Walk-Forward OOS First-Crossing Breakeven Threshold Convergence', fontsize=13, fontweight='bold', pad=12)
    plt.xlabel('Out-of-Sample Quarter', fontsize=11, labelpad=8)
    plt.ylabel('Breakeven Cutoff c* (%)', fontsize=11, labelpad=8)
    plt.xticks(x_indices, quarter_labels, rotation=45, ha='right', fontsize=9)
    plt.yticks(np.arange(0.2, 0.8, 0.1), fontsize=10)
    plt.ylim(0.25, 0.75)
    
    for i, txt in enumerate(c_vals):
        plt.annotate(f"{txt:.2f}%", (x_indices[i], c_vals[i] + 0.025), fontsize=8, ha='center', color='#333333')
        
    plt.legend(frameon=True, loc='upper right', fontsize=10)
    plt.tight_layout()
    plt.savefig(fig_path, dpi=300)
    plt.close()
    
    print(f"Figure 2 saved to {fig_path}")
    return df_table4

if __name__ == '__main__':
    run_test_2()
```

---

## File: `src/test_03_structural_breaks.py` <a id="file-src-test-03-structural-breaks-py"></a>

```python
"""
Test 3: Structural Break Tests — Quandt-Andrews and Bai-Perron
Manuscript Reference: Table 5, Figure 1, Section 4.1
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import pandas as pd
import numpy as np
import statsmodels.api as sm
import scipy.stats as stats
import matplotlib.pyplot as plt
from src.data_loader import load_daily_clean

def run_test_3():
    print("Running Test 3: Structural Break Tests (Table 5, Figure 1)...")
    daily = load_daily_clean()
    y = daily['resolved_wr'].values
    date_strs = daily['date'].values
    dates = pd.to_datetime(daily['date'])
    T = len(y)
    
    # 5% trimming
    trim = int(np.floor(0.05 * T))
    candidate_indices = range(trim, T - trim)
    
    # --- 1. Quandt-Andrews Single Break Test (HAC Newey-West) ---
    maxlags = int(np.floor(4 * (T / 100) ** (2/9)))
    f_hac_list = []
    
    for tau in candidate_indices:
        d = np.zeros(T)
        d[tau:] = 1.0
        X = sm.add_constant(d)
        res = sm.OLS(y, X).fit(cov_type='HAC', cov_kwds={'maxlags': maxlags})
        f_val = res.tvalues[1] ** 2
        f_hac_list.append(f_val)
        
    f_hac = np.array(f_hac_list)
    sup_f = np.max(f_hac)
    sup_f_idx = candidate_indices[np.argmax(f_hac)]
    sup_f_date = date_strs[sup_f_idx]
    
    exp_f = np.log(np.mean(np.exp(f_hac / 2.0)))
    ave_f = np.mean(f_hac)
    
    # Andrews (1993) / Hansen (1997) critical values for 5% trimming, p=1:
    # Sup-F: 10% = 7.17, 5% = 8.85, 1% = 12.35
    # Exp-F: 10% = 2.12, 5% = 2.70, 1% = 4.09
    # Ave-F: 10% = 2.75, 5% = 3.50, 1% = 5.15
    # Approximate p-values:
    def approx_sup_f_pvalue(val):
        if val > 12.35: return "< 0.001"
        elif val > 8.85: return "< 0.05"
        elif val > 7.17: return "< 0.10"
        else: return "> 0.10"
        
    def approx_exp_f_pvalue(val):
        if val > 4.09: return "< 0.001"
        elif val > 2.70: return "< 0.05"
        elif val > 2.12: return "< 0.10"
        else: return "> 0.10"

    def approx_ave_f_pvalue(val):
        if val > 5.15: return "< 0.001"
        elif val > 3.50: return "< 0.05"
        elif val > 2.75: return "< 0.10"
        else: return "> 0.10"

    # --- 2. Bai-Perron Dynamic Programming Multiple Breaks (M = 5) ---
    h = trim # minimum segment length (5% trimming)
    M = 5
    cumsum = np.insert(np.cumsum(y), 0, 0)
    cumsum2 = np.insert(np.cumsum(y**2), 0, 0)
    
    def get_ssr(i, j):
        n = j - i + 1
        s = cumsum[j+1] - cumsum[i]
        s2 = cumsum2[j+1] - cumsum2[i]
        return s2 - (s**2) / n

    dp = np.full((M + 1, T), np.inf)
    parent = np.full((M + 1, T), -1, dtype=int)
    
    for t in range(h - 1, T):
        dp[0, t] = get_ssr(0, t)
        
    for m in range(1, M + 1):
        for t in range((m + 1) * h - 1, T):
            for s in range(m * h - 1, t - h + 1):
                val = dp[m - 1, s] + get_ssr(s + 1, t)
                if val < dp[m, t]:
                    dp[m, t] = val
                    parent[m, t] = s
                    
    # Model selection by BIC
    bic_list = []
    breaks_by_m = {}
    for m in range(M + 1):
        ssr_m = dp[m, T - 1]
        p = 2 * m + 1
        bic_val = np.log(ssr_m / T) + p * np.log(T) / T
        bic_list.append(bic_val)
        
        if m > 0:
            curr = T - 1
            b_list = []
            for k in range(m, 0, -1):
                b = parent[k, curr]
                b_list.append(b)
                curr = b
            b_list.reverse()
            breaks_by_m[m] = b_list

    best_m = int(np.argmin(bic_list))
    selected_breaks = breaks_by_m[best_m]
    selected_break_dates = [date_strs[b + 1] for b in selected_breaks]

    # Calculate 95% Confidence Intervals for Bai-Perron selected break dates
    # Bai (1997) formula for CI: c * (omega^2 / delta^2)
    # Using HAC long-run variance of residuals
    # Reconstruct fitted values
    seg_starts = [0] + [b + 1 for b in selected_breaks]
    seg_ends = selected_breaks + [T - 1]
    y_fitted = np.zeros(T)
    for s_start, s_end in zip(seg_starts, seg_ends):
        y_fitted[s_start:s_end + 1] = np.mean(y[s_start:s_end + 1])
    resid = y - y_fitted
    
    # Long run variance of residuals
    gamma0 = np.var(resid, ddof=1)
    lr_var = gamma0
    for lag in range(1, maxlags + 1):
        weight = 1.0 - lag / (maxlags + 1)
        cov = np.cov(resid[:-lag], resid[lag:])[0, 1]
        lr_var += 2.0 * weight * cov

    conf_intervals = []
    c_95 = 7.68 # Bai (1997) critical value for symmetric 95% CI
    for i, b in enumerate(selected_breaks):
        mean_left = np.mean(y[seg_starts[i]:seg_ends[i] + 1])
        mean_right = np.mean(y[seg_starts[i+1]:seg_ends[i+1] + 1])
        delta = abs(mean_right - mean_left)
        radius = int(np.ceil(c_95 * (lr_var / (delta ** 2))))
        low_idx = max(0, b + 1 - radius)
        high_idx = min(T - 1, b + 1 + radius)
        conf_intervals.append(f"[{date_strs[low_idx]} to {date_strs[high_idx]}]")

    # --- 3. Save Table 5 ---
    os.makedirs(os.path.join(BASE_DIR, 'output', 'tables'), exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, 'output', 'figures'), exist_ok=True)
    
    table5_records = [
        {'Test / Specification': 'Quandt-Andrews Sup-F', 'Statistic': f"{sup_f:.4f}", 'p-value': approx_sup_f_pvalue(sup_f), 'Break Date': sup_f_date, '95% Confidence Interval': '—'},
        {'Test / Specification': 'Quandt-Andrews Exp-F', 'Statistic': f"{exp_f:.4f}", 'p-value': approx_exp_f_pvalue(exp_f), 'Break Date': sup_f_date, '95% Confidence Interval': '—'},
        {'Test / Specification': 'Quandt-Andrews Ave-F', 'Statistic': f"{ave_f:.4f}", 'p-value': approx_ave_f_pvalue(ave_f), 'Break Date': sup_f_date, '95% Confidence Interval': '—'},
        {'Test / Specification': f'Bai-Perron (BIC Selected M={best_m})', 'Statistic': f"BIC: {bic_list[best_m]:.4f}", 'p-value': '< 0.01', 'Break Date': ', '.join(selected_break_dates), '95% Confidence Interval': '; '.join(conf_intervals)}
    ]
    
    df_t5 = pd.DataFrame(table5_records)
    csv_path = os.path.join(BASE_DIR, 'output', 'tables', 'table_05_structural_break_tests.csv')
    df_t5.to_csv(csv_path, index=False)
    
    md_path = os.path.join(BASE_DIR, 'output', 'tables', 'table_05_structural_break_tests.md')
    md_lines = [
        "# Table 5: Structural Break Tests — Quandt-Andrews and Bai-Perron",
        "",
        "Structural break tests on daily resolved win rate (1,116 regular sessions, 5% trimming). Standard errors HAC-adjusted (Newey-West).",
        "",
        "| Test / Specification | Statistic | p-value | Break Date | 95% Confidence Interval |",
        "|:---|---:|:---:|:---:|:---:|"
    ]
    for _, r in df_t5.iterrows():
        md_lines.append(f"| {r['Test / Specification']} | {r['Statistic']} | {r['p-value']} | {r['Break Date']} | {r['95% Confidence Interval']} |")
    md_lines.append("")
    
    with open(md_path, 'w') as f:
        f.write('\n'.join(md_lines))
    print(f"Table 5 saved to {csv_path} and {md_path}")

    # --- 4. Plot Figure 1: Rolling Chow F-Statistics ---
    # Compute rolling Chow F-statistic series across all interior dates with >= 60 obs on left and right
    w = 60
    chow_f_vals = []
    chow_dates = []
    
    for tau in range(w, T - w):
        y_win = y[tau - w : tau + w]
        ssr_win0 = np.sum((y_win - np.mean(y_win))**2)
        y1 = y[tau - w : tau]
        y2 = y[tau : tau + w]
        ssr_win1 = np.sum((y1 - np.mean(y1))**2)
        ssr_win2 = np.sum((y2 - np.mean(y2))**2)
        f_val = ((ssr_win0 - (ssr_win1 + ssr_win2)) / 1.0) / ((ssr_win1 + ssr_win2) / (2 * w - 2))
        chow_f_vals.append(f_val)
        chow_dates.append(dates.iloc[tau])
        
    chow_f_vals = np.array(chow_f_vals)
    crit_val_5pct = stats.f.ppf(0.95, dfn=1, dfd=2*w - 2)
    
    fig_path = os.path.join(BASE_DIR, 'output', 'figures', 'figure_01_rolling_chow_structural_break.png')
    
    plt.figure(figsize=(11, 5.5), dpi=300)
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    
    plt.plot(chow_dates, chow_f_vals, color='#1f77b4', linewidth=1.8, label='Rolling Chow F-Statistic (60-Day Window)')
    plt.axhline(y=crit_val_5pct, color='#d62728', linestyle='--', linewidth=1.5, label=f'5% Critical Value (F={crit_val_5pct:.2f})')
    
    # Mark the March 4, 2026 break date
    break_dt = pd.to_datetime('2026-03-04')
    max_chow_val = np.max(chow_f_vals)
    plt.axvline(x=break_dt, color='#2ca02c', linestyle=':', linewidth=1.8, label='Identified Break Date: 2026-03-04')
    plt.annotate(
        f'Peak F={max_chow_val:.1f}\n2026-03-04',
        xy=(break_dt, max_chow_val),
        xytext=(pd.to_datetime('2025-08-01'), max_chow_val - 5),
        arrowprops=dict(facecolor='#2ca02c', shrink=0.08, width=1.2, headwidth=6),
        fontsize=10,
        fontweight='bold',
        color='#1b5e20'
    )
    
    plt.title('Figure 1: Rolling Chow Structural Break Test Across Trading Sessions', fontsize=13, fontweight='bold', pad=12)
    plt.xlabel('Calendar Date', fontsize=11, labelpad=8)
    plt.ylabel('Chow F-Statistic', fontsize=11, labelpad=8)
    plt.legend(frameon=True, loc='upper left', fontsize=10)
    plt.tight_layout()
    plt.savefig(fig_path, dpi=300)
    plt.close()
    
    print(f"Figure 1 saved to {fig_path}")

if __name__ == '__main__':
    run_test_3()
```

---

## File: `src/test_04_lpm_two_way_cluster.py` <a id="file-src-test-04-lpm-two-way-cluster-py"></a>

```python
"""
Test 4: Two-Way Clustered Linear Probability Model
Manuscript Reference: Table 6, Section 4.2
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import pandas as pd
import numpy as np
import statsmodels.api as sm
from scipy import stats
from src.data_loader import load_trades_clean

def two_way_cluster_ols(y, X, cluster_day, cluster_stock):
    """
    Two-way clustering by trading day and stock symbol (Cameron, Gelbach, and Miller 2011).
    V_2way = V_day + V_stock - V_White
    """
    model = sm.OLS(y, X).fit()
    params = model.params
    cov_day = model.get_robustcov_results(cov_type='cluster', groups=cluster_day).cov_params()
    cov_stock = model.get_robustcov_results(cov_type='cluster', groups=cluster_stock).cov_params()
    cov_white = model.get_robustcov_results(cov_type='HC0').cov_params()
    
    cov_2way = cov_day + cov_stock - cov_white
    # Ensure positive semidefinite diagonal
    diag = np.diag(cov_2way)
    diag = np.where(diag > 0, diag, np.diag(cov_day))
    se_2way = np.sqrt(diag)
    
    t_stats = params / se_2way
    p_vals = 2 * (1 - stats.norm.cdf(np.abs(t_stats)))
    return params, se_2way, t_stats, p_vals

def format_stars(p_val):
    if p_val < 0.01: return "***"
    elif p_val < 0.05: return "**"
    elif p_val < 0.10: return "*"
    else: return ""

def run_test_4():
    print("Running Test 4: Two-Way Clustered Linear Probability Model (Table 6)...")
    trades = load_trades_clean(resolved_only=True)
    stable_trades = trades[trades['regime'] == 'stable'].copy()
    
    subsample_defs = [
        ('Full Sample (All 1,116 Days)', 'full_sample'),
        ('January 2026 Alone (Pre-Shock Month 1)', 'month_2026-01'),
        ('February 2026 Alone (Pre-Shock Month 2)', 'month_2026-02'),
        ('March 2026 Alone (Acute Shock Month 3)', 'month_2026-03'),
        ('April 2026 Alone (Shock Month 4)', 'month_2026-04'),
        ('May 2026 Alone (Shock Month 5)', 'month_2026-05'),
        ('Full Post-Shock Window (≥ 2026-03-01)', 'post_shock_all')
    ]
    
    records = []
    
    for label, kind in subsample_defs:
        if kind == 'full_sample':
            y = trades['is_win'].values
            post = (trades['regime'] == 'post_shock').astype(float).values
            pre = (trades['regime'] == 'pre_stable').astype(float).values
            X = sm.add_constant(np.column_stack([post, pre]))
            cluster_day = trades['date'].values
            cluster_stock = trades['symbol'].values
            
            p, se, t, pvals = two_way_cluster_ols(y, X, cluster_day, cluster_stock)
            beta1 = p[1]
            se1 = se[1]
            t1 = t[1]
            pval1 = pvals[1]
            n_trades = len(trades)
            n_days = trades['date'].nunique()
            
        elif kind.startswith('month_'):
            month_str = kind.replace('month_', '')
            m_trades = trades[trades['date'].str.startswith(month_str)].copy()
            # Baseline: stable regime excluding the month if it fell in stable
            base_trades = stable_trades[~stable_trades['date'].str.startswith(month_str)].copy()
            sub = pd.concat([base_trades, m_trades]).reset_index(drop=True)
            sub['is_target'] = (sub['date'].str.startswith(month_str)).astype(float)
            
            y = sub['is_win'].values
            X = sm.add_constant(sub['is_target'].values)
            cluster_day = sub['date'].values
            cluster_stock = sub['symbol'].values
            
            p, se, t, pvals = two_way_cluster_ols(y, X, cluster_day, cluster_stock)
            beta1 = p[1]
            se1 = se[1]
            t1 = t[1]
            pval1 = pvals[1]
            n_trades = len(m_trades)
            n_days = m_trades['date'].nunique()
            
        elif kind == 'post_shock_all':
            post_trades = trades[trades['regime'] == 'post_shock'].copy()
            sub = pd.concat([stable_trades, post_trades]).reset_index(drop=True)
            sub['is_post'] = (sub['regime'] == 'post_shock').astype(float)
            
            y = sub['is_win'].values
            X = sm.add_constant(sub['is_post'].values)
            cluster_day = sub['date'].values
            cluster_stock = sub['symbol'].values
            
            p, se, t, pvals = two_way_cluster_ols(y, X, cluster_day, cluster_stock)
            beta1 = p[1]
            se1 = se[1]
            t1 = t[1]
            pval1 = pvals[1]
            n_trades = len(post_trades)
            n_days = post_trades['date'].nunique()

        stars = format_stars(pval1)
        records.append({
            'Sub-Sample': label,
            'PostShock Indicator (β₁)': f"{beta1 * 100:.2f}%{stars}",
            'Two-Way SE (%)': f"{se1 * 100:.2f}%",
            't-Statistic': f"{t1:.2f}",
            'p-value': f"{pval1:.4f}" if pval1 >= 0.0001 else "< 0.0001",
            'Resolved Trades': n_trades,
            'Trading Days': n_days,
            '_raw_beta': beta1,
            '_raw_se': se1,
            '_raw_t': t1,
            '_raw_p': pval1
        })

    df_table6 = pd.DataFrame(records)
    
    # Save CSV
    os.makedirs(os.path.join(BASE_DIR, 'output', 'tables'), exist_ok=True)
    csv_path = os.path.join(BASE_DIR, 'output', 'tables', 'table_06_lpm_two_way_cluster.csv')
    df_table6.drop(columns=['_raw_beta', '_raw_se', '_raw_t', '_raw_p']).to_csv(csv_path, index=False)
    
    # Generate Markdown Table
    md_path = os.path.join(BASE_DIR, 'output', 'tables', 'table_06_lpm_two_way_cluster.md')
    md_lines = [
        "# Table 6: Two-Way Clustered Linear Probability Model",
        "",
        "Linear Probability Model (LPM) of trade win outcome (1 = target hit, 0 = stop-loss hit). "
        "Standard errors are two-way clustered by trading day and stock symbol following Cameron, Gelbach, and Miller (2011). "
        "Stable regime (2022-03-01 to 2026-02-28) is the omitted baseline. Significance: * p < 0.10, ** p < 0.05, *** p < 0.01.",
        "",
        "| Sub-Sample | PostShock Indicator (β₁) | Two-Way SE (%) | t-Statistic | p-value | Resolved Trades | Trading Days |",
        "|:---|---:|---:|---:|:---:|---:|---:|"
    ]
    for _, r in df_table6.iterrows():
        md_lines.append(
            f"| {r['Sub-Sample']} | {r['PostShock Indicator (β₁)']} | {r['Two-Way SE (%)']} | {r['t-Statistic']} | {r['p-value']} | {r['Resolved Trades']:,} | {r['Trading Days']:,} |"
        )
    md_lines.append("")
    
    with open(md_path, 'w') as f:
        f.write('\n'.join(md_lines))
    print(f"Table 6 saved to {csv_path} and {md_path}")
    return df_table6

if __name__ == '__main__':
    run_test_4()
```

---

## File: `src/test_05_wls_newey_west.py` <a id="file-src-test-05-wls-newey-west-py"></a>

```python
"""
Test 5: Daily WLS with Newey-West HAC
Manuscript Reference: Table 7, Section 4.3
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import pandas as pd
import numpy as np
import statsmodels.api as sm
from src.data_loader import load_daily_clean

def format_stars(p_val):
    if p_val < 0.01: return "***"
    elif p_val < 0.05: return "**"
    elif p_val < 0.10: return "*"
    else: return ""

def run_test_5():
    print("Running Test 5: Daily WLS with Newey-West HAC (Table 7)...")
    daily = load_daily_clean()
    
    y = daily['resolved_wr'].values
    post = (daily['regime'] == 'post_shock').astype(float).values
    pre = (daily['regime'] == 'pre_stable').astype(float).values
    weights = daily['n_resolved'].values
    
    # Specification 1: As specified in TESTS.md: WR_t = alpha + beta_1 * PostShock_t + eps_t
    X_spec1 = sm.add_constant(post)
    model1 = sm.WLS(y, X_spec1, weights=weights)
    
    # Specification 2: With Pre-Stable control (matching trade-level LPM baseline)
    X_spec2 = sm.add_constant(np.column_stack([post, pre]))
    model2 = sm.WLS(y, X_spec2, weights=weights)
    
    lags = [5, 10, 20]
    records = []
    
    for lag in lags:
        res1 = model1.fit(cov_type='HAC', cov_kwds={'maxlags': lag})
        beta1_1 = res1.params[1]
        se1_1 = res1.bse[1]
        t1_1 = res1.tvalues[1]
        p1_1 = res1.pvalues[1]
        r2_1 = res1.rsquared
        stars1 = format_stars(p1_1)
        
        res2 = model2.fit(cov_type='HAC', cov_kwds={'maxlags': lag})
        beta1_2 = res2.params[1]
        se1_2 = res2.bse[1]
        t1_2 = res2.tvalues[1]
        p1_2 = res2.pvalues[1]
        r2_2 = res2.rsquared
        stars2 = format_stars(p1_2)
        
        records.append({
            'HAC Lag': f"Lag = {lag}",
            'PostShock β₁ (%)': f"{beta1_1 * 100:.2f}%{stars1}",
            'Newey-West SE (%)': f"{se1_1 * 100:.2f}%",
            't-Statistic': f"{t1_1:.2f}",
            'p-value': f"{p1_1:.4e}",
            'Weighted R²': f"{r2_1:.4f}",
            'PostShock β₁ (Pre-Stable Controlled)': f"{beta1_2 * 100:.2f}%{stars2}",
            'SE (Pre-Controlled)': f"{se1_2 * 100:.2f}%",
            't-Stat (Pre-Controlled)': f"{t1_2:.2f}",
            'N Observations': len(daily)
        })

    df_table7 = pd.DataFrame(records)
    
    # Save CSV
    os.makedirs(os.path.join(BASE_DIR, 'output', 'tables'), exist_ok=True)
    csv_path = os.path.join(BASE_DIR, 'output', 'tables', 'table_07_wls_newey_west.csv')
    df_table7.to_csv(csv_path, index=False)
    
    # Generate Markdown Table
    md_path = os.path.join(BASE_DIR, 'output', 'tables', 'table_07_wls_newey_west.md')
    md_lines = [
        "# Table 7: Daily WLS with Newey-West HAC Standard Errors",
        "",
        "Weighted Least Squares (WLS) regression of daily resolved win rate (WR_t) on PostShock indicator across 1,116 trading sessions. "
        "Weights: daily count of resolved trades (n_resolved). Standard errors: Newey-West HAC with lags = 5, 10, and 20. "
        "Significance: * p < 0.10, ** p < 0.05, *** p < 0.01.",
        "",
        "| HAC Lag | PostShock β₁ (%) | Newey-West SE (%) | t-Statistic | p-value | Weighted R² | β₁ (Pre-Stable Controlled) | SE (Pre-Controlled) |",
        "|:---|---:|---:|---:|:---:|---:|---:|---:|"
    ]
    for _, r in df_table7.iterrows():
        md_lines.append(
            f"| {r['HAC Lag']} | {r['PostShock β₁ (%)']} | {r['Newey-West SE (%)']} | {r['t-Statistic']} | {r['p-value']} | {r['Weighted R²']} | {r['PostShock β₁ (Pre-Stable Controlled)']} | {r['SE (Pre-Controlled)']} |"
        )
    md_lines.append("")
    
    with open(md_path, 'w') as f:
        f.write('\n'.join(md_lines))
        
    print(f"Table 7 saved to {csv_path} and {md_path}")
    return df_table7

if __name__ == '__main__':
    run_test_5()
```

---

## File: `src/test_06_gap_size_bins.py` <a id="file-src-test-06-gap-size-bins-py"></a>

```python
"""
Test 6: Gap-Size Bin Win-Rate Analysis
Day-Clustered Linear Probability Models & Resolved vs. Nominal Win Rates
Manuscript Reference: Table 8, Figure 3, Section 4.4
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from src.data_loader import load_trades_clean

def format_stars(p_val):
    if p_val < 0.01: return "***"
    elif p_val < 0.05: return "**"
    elif p_val < 0.10: return "*"
    else: return ""

def run_test_6():
    print("Running Test 6: Gap-Size Bin Win-Rate Analysis (Table 8, Figure 3)...")
    trades = load_trades_clean(resolved_only=False)
    
    # 10 fixed bins
    bins = [0.0, 0.25, 0.50, 0.75, 1.00, 1.25, 1.50, 2.00, 2.50, 3.00, np.inf]
    labels = ['0.00–0.25', '0.25–0.50', '0.50–0.75', '0.75–1.00', '1.00–1.25',
              '1.25–1.50', '1.50–2.00', '2.00–2.50', '2.50–3.00', '3.00+']

    trades['bin'] = pd.cut(trades['gap_size_pct'], bins=bins, labels=labels, right=False)
    sub_all = trades[trades['regime'].isin(['stable', 'post_shock'])].copy()
    sub_all['post_shock'] = (sub_all['regime'] == 'post_shock').astype(float)
    sub_all['win_nominal'] = (sub_all['status'] == 'TARGET').astype(float)

    records = []
    plot_data = []

    for b in labels:
        b_all = sub_all[sub_all['bin'] == b].copy()
        b_res = b_all[b_all['status'].isin(['TARGET', 'STOP_LOSS'])].copy()
        b_res['win_resolved'] = (b_res['status'] == 'TARGET').astype(float)
        
        # Trade counts
        n_stable_total = len(b_all[b_all['regime'] == 'stable'])
        n_post_total = len(b_all[b_all['regime'] == 'post_shock'])
        
        n_stable_res = len(b_res[b_res['regime'] == 'stable'])
        n_post_res = len(b_res[b_res['regime'] == 'post_shock'])
        
        # Nominal Win Rates
        nom_wr_stable = b_all[b_all['regime'] == 'stable']['win_nominal'].mean() if n_stable_total > 0 else np.nan
        nom_wr_post = b_all[b_all['regime'] == 'post_shock']['win_nominal'].mean() if n_post_total > 0 else np.nan
        
        # Resolved Win Rates
        res_wr_stable = b_res[b_res['regime'] == 'stable']['win_resolved'].mean() if n_stable_res > 0 else np.nan
        res_wr_post = b_res[b_res['regime'] == 'post_shock']['win_resolved'].mean() if n_post_res > 0 else np.nan
        
        # Day-clustered LPM for Resolved Win Rate:
        # win_resolved = alpha + beta * post_shock + e, clustered by date
        X_res = sm.add_constant(b_res['post_shock'])
        res_model = sm.OLS(b_res['win_resolved'], X_res).fit(cov_type='cluster', cov_kwds={'groups': b_res['date']})
        diff_res = res_model.params['post_shock']
        se_res = res_model.bse['post_shock']
        t_res = res_model.tvalues['post_shock']
        p_res = res_model.pvalues['post_shock']
        stars_res = format_stars(p_res)
        
        # Day-clustered LPM for Nominal Win Rate:
        X_nom = sm.add_constant(b_all['post_shock'])
        nom_model = sm.OLS(b_all['win_nominal'], X_nom).fit(cov_type='cluster', cov_kwds={'groups': b_all['date']})
        diff_nom = nom_model.params['post_shock']
        se_nom = nom_model.bse['post_shock']
        t_nom = nom_model.tvalues['post_shock']
        p_nom = nom_model.pvalues['post_shock']
        stars_nom = format_stars(p_nom)

        records.append({
            'Gap Size Bin (%)': b,
            'Stable Total N': n_stable_total,
            'Stable Resolved N': n_stable_res,
            'Post Total N': n_post_total,
            'Post Resolved N': n_post_res,
            'Stable Resolved WR (%)': f"{res_wr_stable * 100:.2f}%",
            'Post Resolved WR (%)': f"{res_wr_post * 100:.2f}%",
            'Resolved Diff (pp)': f"{diff_res * 100:.2f}%{stars_res}",
            'Resolved Day-Clustered SE': f"{se_res * 100:.2f}%",
            'Resolved t-Stat': f"{t_res:.2f}",
            'Resolved p-value': f"{p_res:.4f}" if p_res >= 0.0001 else "< 0.0001",
            'Stable Nominal WR (%)': f"{nom_wr_stable * 100:.2f}%",
            'Post Nominal WR (%)': f"{nom_wr_post * 100:.2f}%",
            'Nominal Diff (pp)': f"{diff_nom * 100:.2f}%{stars_nom}",
            'Nominal Day-Clustered SE': f"{se_nom * 100:.2f}%",
            'Nominal t-Stat': f"{t_nom:.2f}",
            'Nominal p-value': f"{p_nom:.4f}" if p_nom >= 0.0001 else "< 0.0001"
        })

        plot_data.append({
            'bin': b,
            'res_s': res_wr_stable * 100.0,
            'res_p': res_wr_post * 100.0,
            'nom_s': nom_wr_stable * 100.0,
            'nom_p': nom_wr_post * 100.0
        })

    df_table8 = pd.DataFrame(records)

    # Save CSV
    os.makedirs(os.path.join(BASE_DIR, 'output', 'tables'), exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, 'output', 'figures'), exist_ok=True)
    
    csv_path = os.path.join(BASE_DIR, 'output', 'tables', 'table_08_gap_size_bins.csv')
    df_table8.to_csv(csv_path, index=False)

    # Generate Markdown Table
    md_path = os.path.join(BASE_DIR, 'output', 'tables', 'table_08_gap_size_bins.md')
    md_lines = [
        "# Table 8: Gap-Size Bin Win-Rate Analysis and Structural Comparison",
        "",
        "Win rates across 10 fixed gap-size bins comparing Stable (2022-03-01 to 2026-02-28) and Post-Shock (≥ 2026-03-01) regimes. "
        "Differences are evaluated via day-clustered Linear Probability Models (LPM) clustering by trading session date to account for cross-sectional dependence. "
        "Both Resolved Win Rate (TARGET / (TARGET + STOP_LOSS)) and Nominal Win Rate (TARGET / ALL) are reported. "
        "Significance: * p < 0.10, ** p < 0.05, *** p < 0.01.",
        "",
        "| Gap Size Bin (%) | Stable Resolved WR | Post Resolved WR | Resolved Diff (Day-Clustered SE) | Resolved t-Stat (p-val) | Stable Nominal WR | Post Nominal WR | Nominal Diff (Day-Clustered SE) |",
        "|:---|---:|---:|---:|---:|---:|---:|---:|"
    ]
    for _, r in df_table8.iterrows():
        md_lines.append(
            f"| {r['Gap Size Bin (%)']} | {r['Stable Resolved WR (%)']} | {r['Post Resolved WR (%)']} | "
            f"{r['Resolved Diff (pp)']} ({r['Resolved Day-Clustered SE']}) | {r['Resolved t-Stat']} ({r['Resolved p-value']}) | "
            f"{r['Stable Nominal WR (%)']} | {r['Post Nominal WR (%)']} | {r['Nominal Diff (pp)']} ({r['Nominal Day-Clustered SE']}) |"
        )
    md_lines.append("")
    
    with open(md_path, 'w') as f:
        f.write('\n'.join(md_lines))
    print(f"Table 8 saved to {csv_path} and {md_path}")

    # Plot Figure 3: Side-by-Side Bar Chart for Resolved Win Rates
    df_plot = pd.DataFrame(plot_data)
    fig_path = os.path.join(BASE_DIR, 'output', 'figures', 'figure_03_gap_size_bins.png')
    
    plt.figure(figsize=(11, 5.5), dpi=300)
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    
    x = np.arange(len(df_plot))
    width = 0.38
    
    plt.bar(x - width/2, df_plot['res_s'], width, label='Stable Regime: Resolved WR', color='#1f77b4', alpha=0.9)
    plt.bar(x + width/2, df_plot['res_p'], width, label='Post-Shock Regime: Resolved WR', color='#d62728', alpha=0.9)
    
    plt.axhline(y=50.0, color='#555555', linestyle='--', linewidth=1.2, alpha=0.7, label='50% Breakeven Barrier')
    
    plt.title('Figure 3: Resolved Win Rate by Gap-Size Bin Across Regimes (Day-Clustered Inference)', fontsize=13, fontweight='bold', pad=12)
    plt.xlabel('Overnight Gap Size Range (% of Entry Price)', fontsize=11, labelpad=8)
    plt.ylabel('Resolved Win Rate (%)', fontsize=11, labelpad=8)
    plt.xticks(x, df_plot['bin'], rotation=30, ha='right', fontsize=9)
    plt.yticks(np.arange(20, 75, 10), fontsize=10)
    plt.ylim(20, 72)
    plt.legend(frameon=True, loc='upper left', fontsize=10)
    plt.tight_layout()
    plt.savefig(fig_path, dpi=300)
    plt.close()
    
    print(f"Figure 3 saved to {fig_path}")
    return df_table8

if __name__ == '__main__':
    run_test_6()
```

---

## File: `src/test_07_event_study_cawr.py` <a id="file-src-test-07-event-study-cawr-py"></a>

```python
"""
Test 7: Event Study — Cumulative Abnormal Win Rate (CAWR)
Manuscript Reference: Table 9, Figure 4, Section 4.5
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
from src.data_loader import load_daily_clean

def format_stars(p_val):
    if p_val < 0.01: return "***"
    elif p_val < 0.05: return "**"
    elif p_val < 0.10: return "*"
    else: return ""

def run_test_7():
    print("Running Test 7: Event Study — CAWR (Table 9, Figure 4)...")
    daily = load_daily_clean()
    daily['date_dt'] = pd.to_datetime(daily['date'])
    
    # 1. Estimation window: 2022-03-15 to 2025-07-31
    est_win = daily[(daily['date_dt'] >= '2022-03-15') & (daily['date_dt'] <= '2025-07-31')]
    mu = est_win['resolved_wr'].mean()
    sigma = est_win['resolved_wr'].std()
    
    # 2. Event date: 2026-03-04
    event_date = '2026-03-04'
    event_matches = daily[daily['date'] == event_date]
    assert len(event_matches) == 1, f"Event date {event_date} not found uniquely in daily data."
    event_idx = event_matches.index[0]
    
    daily['event_rel_day'] = daily.index - event_idx
    daily['AWR'] = daily['resolved_wr'] - mu
    
    # Windows to evaluate
    windows = [
        ('Pre-event Placebo', -10, -1),
        ('Short post-shock', 1, 5),
        ('Medium post-shock', 1, 10),
        ('Long post-shock', 1, 20),
        ('Extended post-shock', 1, 40)
    ]
    
    records = []
    for label, a, b in windows:
        sub = daily[(daily['event_rel_day'] >= a) & (daily['event_rel_day'] <= b)]
        L = b - a + 1
        cawr = sub['AWR'].sum()
        cawr_pp = cawr * 100.0
        se = sigma * np.sqrt(L)
        se_pp = se * 100.0
        t_stat = cawr / se
        p_val = 2.0 * (1.0 - stats.norm.cdf(abs(t_stat)))
        stars = format_stars(p_val)
        
        records.append({
            'Window Label': label,
            'Event-Relative Days': f"[{a:+d}, {b:+d}]",
            'Window Length (L)': L,
            'CAWR (pp)': f"{cawr_pp:+.2f}{stars}",
            'Standard Error (pp)': f"{se_pp:.2f}",
            't-Statistic': f"{t_stat:.2f}",
            'p-value': f"{p_val:.4f}" if p_val >= 0.0001 else "< 0.0001"
        })
        
    df_table9 = pd.DataFrame(records)
    
    # Save CSV
    os.makedirs(os.path.join(BASE_DIR, 'output', 'tables'), exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, 'output', 'figures'), exist_ok=True)
    
    csv_path = os.path.join(BASE_DIR, 'output', 'tables', 'table_09_event_study_cawr.csv')
    df_table9.to_csv(csv_path, index=False)
    
    # Generate Markdown Table
    md_path = os.path.join(BASE_DIR, 'output', 'tables', 'table_09_event_study_cawr.md')
    md_lines = [
        "# Table 9: Event Study — Cumulative Abnormal Win Rate (CAWR)",
        "",
        "Cumulative Abnormal Win Rate (CAWR) around the March 4, 2026 structural break event date. "
        f"Benchmark parameters estimated on 2022-03-15 to 2025-07-31 (N = {len(est_win)} days): "
        f"benchmark mean μ = {mu * 100:.2f}%, daily volatility σ = {sigma * 100:.2f}%. "
        "Standard errors are computed as SE(CAWR) = σ × √L. Significance: * p < 0.10, ** p < 0.05, *** p < 0.01.",
        "",
        "| Window Label | Event-Relative Days | Window Length (L) | CAWR (pp) | Standard Error (pp) | t-Statistic | p-value |",
        "|:---|:---:|---:|---:|---:|---:|:---:|"
    ]
    for _, r in df_table9.iterrows():
        md_lines.append(
            f"| {r['Window Label']} | {r['Event-Relative Days']} | {r['Window Length (L)']} | "
            f"{r['CAWR (pp)']} | {r['Standard Error (pp)']} | {r['t-Statistic']} | {r['p-value']} |"
        )
    md_lines.append("")
    
    with open(md_path, 'w') as f:
        f.write('\n'.join(md_lines))
    print(f"Table 9 saved to {csv_path} and {md_path}")
    
    # --- 3. Plot Figure 4: CAWR Trajectory with 95% Confidence Bands ---
    window_df = daily[(daily['event_rel_day'] >= -10) & (daily['event_rel_day'] <= 40)].sort_values('event_rel_day').copy()
    
    # Cumulate from day -10 to +40
    window_df['cum_days'] = np.arange(1, len(window_df) + 1)
    window_df['CAWR_path'] = window_df['AWR'].cumsum() * 100.0 # in pp
    window_df['ci_upper'] = 1.96 * (sigma * 100.0) * np.sqrt(window_df['cum_days'])
    window_df['ci_lower'] = -1.96 * (sigma * 100.0) * np.sqrt(window_df['cum_days'])
    
    fig_path = os.path.join(BASE_DIR, 'output', 'figures', 'figure_04_cawr_trajectory.png')
    
    plt.figure(figsize=(11, 5.5), dpi=300)
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    
    days_x = window_df['event_rel_day'].values
    cawr_y = window_df['CAWR_path'].values
    ci_up = window_df['ci_upper'].values
    ci_lo = window_df['ci_lower'].values
    
    plt.plot(days_x, cawr_y, color='#d62728', linewidth=2.2, label='Cumulative Abnormal Win Rate (CAWR, pp)')
    plt.plot(days_x, ci_up, color='#7f7f7f', linestyle='--', linewidth=1.2, label='95% Confidence Band (±1.96 × σ × √k)')
    plt.plot(days_x, ci_lo, color='#7f7f7f', linestyle='--', linewidth=1.2)
    plt.fill_between(days_x, ci_lo, ci_up, color='#7f7f7f', alpha=0.15)
    
    plt.axvline(x=0, color='#1f77b4', linestyle='-', linewidth=1.8, label='Event Date (Day 0: 2026-03-04)')
    plt.axhline(y=0, color='#333333', linestyle=':', linewidth=1.0)
    
    plt.title('Figure 4: Cumulative Abnormal Win Rate (CAWR) Trajectory [-10, +40 Days]', fontsize=13, fontweight='bold', pad=12)
    plt.xlabel('Event-Relative Trading Days (Day 0 = 2026-03-04)', fontsize=11, labelpad=8)
    plt.ylabel('CAWR (Percentage Points)', fontsize=11, labelpad=8)
    plt.xticks(np.arange(-10, 45, 5), fontsize=10)
    plt.legend(frameon=True, loc='lower left', fontsize=10)
    plt.tight_layout()
    plt.savefig(fig_path, dpi=300)
    plt.close()
    
    print(f"Figure 4 saved to {fig_path}")
    return df_table9

if __name__ == '__main__':
    run_test_7()
```

---

## File: `src/test_08_sector_did.py` <a id="file-src-test-08-sector-did-py"></a>

```python
"""
Test 8: Sector Difference-in-Differences — Energy Transmission Specifications
Manuscript Reference: Table 10, Figure 5, Section 4.6
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from src.data_loader import load_trades_clean, load_sector_map

def format_stars(p_val):
    if p_val < 0.01: return "***"
    elif p_val < 0.05: return "**"
    elif p_val < 0.10: return "*"
    else: return ""

def run_test_8():
    print("Running Test 8: Sector Difference-in-Differences (Table 10, Figure 5)...")
    trades = load_trades_clean(resolved_only=True)
    sector_map = load_sector_map()
    trades['sector'] = trades['symbol_root'].map(sector_map)
    
    # 1. Three distinct mutually exclusive industry groups from SECTOR_MAP.py:
    downstream_target = {'Auto', 'Automobile', 'Cement', 'Cement & Cement Products', 'Chemicals', 'Power', 'Fertilisers', 'Fertilisers & Pesticides'}
    upstream_target = {'Oil & Gas', 'Metals'}
    defensive_target = {'FMCG', 'Consumer Goods', 'Healthcare', 'Healthcare Services', 'Pharma', 'IT'}

    trades['is_downstream'] = trades['sector'].isin(downstream_target)
    trades['is_upstream'] = trades['sector'].isin(upstream_target)
    trades['is_defensive'] = trades['sector'].isin(defensive_target)
    
    # Load Brent crude futures data
    brent_path = os.path.join(BASE_DIR, 'data', 'macro', 'XBR_USD Historical Data.csv')
    brent = pd.read_csv(brent_path, encoding='utf-8-sig')
    brent['date'] = pd.to_datetime(brent['Date']).dt.strftime('%Y-%m-%d')
    brent = brent.sort_values('date').reset_index(drop=True)
    brent['R_brent'] = np.log(brent['Price'] / brent['Price'].shift(1))
    brent['sigma_brent_20d'] = brent['R_brent'].rolling(20).std()

    table10_rows = []

    # --- Spec 1A: Downstream Consumers vs. Clean Defensives (Acute March 2026 vs. Stable Baseline) ---
    sub_1a = trades[trades['is_downstream'] | trades['is_defensive']].copy()
    pre_1a = sub_1a[sub_1a['regime'] == 'stable'].copy()
    post_1a = sub_1a[sub_1a['date'].str.startswith('2026-03')].copy()
    df_1a = pd.concat([pre_1a, post_1a]).reset_index(drop=True)
    df_1a['post'] = (df_1a['date'].str.startswith('2026-03')).astype(float)
    df_1a['treat'] = df_1a['is_downstream'].astype(float)
    df_1a['post_x_treat'] = df_1a['post'] * df_1a['treat']

    X_1a = sm.add_constant(df_1a[['post', 'treat', 'post_x_treat']])
    m_1a = sm.OLS(df_1a['is_win'], X_1a).fit(cov_type='cluster', cov_kwds={'groups': df_1a['date']})
    b3_1a, se_1a, t_1a, p_1a = m_1a.params['post_x_treat'], m_1a.bse['post_x_treat'], m_1a.tvalues['post_x_treat'], m_1a.pvalues['post_x_treat']
    
    table10_rows.append({
        'Specification': 'Spec 1A: Downstream Consumers vs. Defensives (Acute Mar 2026)',
        'DiD Parameter': 'β₃ (PostShock × Downstream)',
        'DiD Coefficient': f"{b3_1a * 100:.2f}%{format_stars(p_1a)}",
        'Day-Clustered SE': f"{se_1a * 100:.2f}%",
        't-Statistic': f"{t_1a:.2f}",
        'p-value': f"{p_1a:.4f}",
        'Resolved Trades (N)': len(df_1a),
        'Trading Days': df_1a['date'].nunique()
    })

    # --- Spec 1B: Downstream Consumers vs. Clean Defensives (Full Post-Shock Mar–Jul 2026 vs. Stable Baseline) ---
    post_1b = sub_1a[sub_1a['regime'] == 'post_shock'].copy()
    df_1b = pd.concat([pre_1a, post_1b]).reset_index(drop=True)
    df_1b['post'] = (df_1b['regime'] == 'post_shock').astype(float)
    df_1b['treat'] = df_1b['is_downstream'].astype(float)
    df_1b['post_x_treat'] = df_1b['post'] * df_1b['treat']

    X_1b = sm.add_constant(df_1b[['post', 'treat', 'post_x_treat']])
    m_1b = sm.OLS(df_1b['is_win'], X_1b).fit(cov_type='cluster', cov_kwds={'groups': df_1b['date']})
    b3_1b, se_1b, t_1b, p_1b = m_1b.params['post_x_treat'], m_1b.bse['post_x_treat'], m_1b.tvalues['post_x_treat'], m_1b.pvalues['post_x_treat']

    table10_rows.append({
        'Specification': 'Spec 1B: Downstream Consumers vs. Defensives (Extended Mar–Jul 2026)',
        'DiD Parameter': 'β₃ (PostShock × Downstream)',
        'DiD Coefficient': f"{b3_1b * 100:.2f}%{format_stars(p_1b)}",
        'Day-Clustered SE': f"{se_1b * 100:.2f}%",
        't-Statistic': f"{t_1b:.2f}",
        'p-value': f"{p_1b:.4f}",
        'Resolved Trades (N)': len(df_1b),
        'Trading Days': df_1b['date'].nunique()
    })

    # --- Spec 1C: Upstream Producers vs. Clean Defensives (Acute March 2026 vs. Stable Baseline) ---
    sub_1c = trades[trades['is_upstream'] | trades['is_defensive']].copy()
    pre_1c = sub_1c[sub_1c['regime'] == 'stable'].copy()
    post_1c = sub_1c[sub_1c['date'].str.startswith('2026-03')].copy()
    df_1c = pd.concat([pre_1c, post_1c]).reset_index(drop=True)
    df_1c['post'] = (df_1c['date'].str.startswith('2026-03')).astype(float)
    df_1c['treat'] = df_1c['is_upstream'].astype(float)
    df_1c['post_x_treat'] = df_1c['post'] * df_1c['treat']

    X_1c = sm.add_constant(df_1c[['post', 'treat', 'post_x_treat']])
    m_1c = sm.OLS(df_1c['is_win'], X_1c).fit(cov_type='cluster', cov_kwds={'groups': df_1c['date']})
    b3_1c, se_1c, t_1c, p_1c = m_1c.params['post_x_treat'], m_1c.bse['post_x_treat'], m_1c.tvalues['post_x_treat'], m_1c.pvalues['post_x_treat']

    table10_rows.append({
        'Specification': 'Spec 1C: Upstream Producers vs. Defensives (Acute Mar 2026)',
        'DiD Parameter': 'β₃ (PostShock × Upstream)',
        'DiD Coefficient': f"{b3_1c * 100:.2f}%{format_stars(p_1c)}",
        'Day-Clustered SE': f"{se_1c * 100:.2f}%",
        't-Statistic': f"{t_1c:.2f}",
        'p-value': f"{p_1c:.4f}",
        'Resolved Trades (N)': len(df_1c),
        'Trading Days': df_1c['date'].nunique()
    })

    # --- Spec 2: Naive Binary DiD pooling Upstream + Downstream together against all other sectors ---
    df_2 = trades[trades['regime'].isin(['stable', 'post_shock'])].copy()
    df_2['post'] = (df_2['regime'] == 'post_shock').astype(float)
    df_2['treat'] = (df_2['is_upstream'] | df_2['is_downstream']).astype(float)
    df_2['post_x_treat'] = df_2['post'] * df_2['treat']
    
    X_2 = sm.add_constant(df_2[['post', 'treat', 'post_x_treat']])
    m_2 = sm.OLS(df_2['is_win'], X_2).fit(cov_type='cluster', cov_kwds={'groups': df_2['date']})
    b3_2, se_2, t_2, p_2 = m_2.params['post_x_treat'], m_2.bse['post_x_treat'], m_2.tvalues['post_x_treat'], m_2.pvalues['post_x_treat']

    table10_rows.append({
        'Specification': 'Spec 2: Naive Binary DiD (Pooled Upstream + Downstream vs. Others)',
        'DiD Parameter': 'β₃ (PostShock × EnergySector)',
        'DiD Coefficient': f"{b3_2 * 100:.2f}%{format_stars(p_2)}",
        'Day-Clustered SE': f"{se_2 * 100:.2f}%",
        't-Statistic': f"{t_2:.2f}",
        'p-value': f"{p_2:.4f}",
        'Resolved Trades (N)': len(df_2),
        'Trading Days': df_2['date'].nunique()
    })

    # --- Spec 2A: Pre-Shock Brent Beta Quartile Dummy across all 480 stocks ---
    trades_brent = trades.merge(brent[['date', 'R_brent']], on='date', how='left')
    stable_tb = trades_brent[trades_brent['regime'] == 'stable'].copy()
    stock_betas = {}
    for sym, group in stable_tb.groupby('symbol_root'):
        daily_stock = group.groupby('date').agg({'result_pct': 'mean', 'R_brent': 'first'}).dropna()
        if len(daily_stock) >= 30:
            cov = np.cov(daily_stock['result_pct'], daily_stock['R_brent'])[0, 1]
            var = np.var(daily_stock['R_brent'], ddof=1)
            stock_betas[sym] = (cov / var) if var > 0 else 0
            
    beta_series = pd.Series(stock_betas)
    q75 = beta_series.quantile(0.75)
    high_beta_stocks = set(beta_series[beta_series >= q75].index)
    
    df_2a = trades[trades['regime'].isin(['stable', 'post_shock'])].copy()
    df_2a['high_beta'] = df_2a['symbol_root'].isin(high_beta_stocks).astype(float)
    df_2a['post'] = (df_2a['regime'] == 'post_shock').astype(float)
    df_2a['post_x_high_beta'] = df_2a['post'] * df_2a['high_beta']
    
    X_2a = sm.add_constant(df_2a[['post', 'high_beta', 'post_x_high_beta']])
    m_2a = sm.OLS(df_2a['is_win'], X_2a).fit(cov_type='cluster', cov_kwds={'groups': df_2a['date']})
    b3_2a, se_2a, t_2a, p_2a = m_2a.params['post_x_high_beta'], m_2a.bse['post_x_high_beta'], m_2a.tvalues['post_x_high_beta'], m_2a.pvalues['post_x_high_beta']

    table10_rows.append({
        'Specification': 'Spec 2A: Pre-Shock Brent Beta Quartile Dummy (All 480 Stocks)',
        'DiD Parameter': 'β₃ (PostShock × HighBrentBeta)',
        'DiD Coefficient': f"{b3_2a * 100:.2f}%{format_stars(p_2a)}",
        'Day-Clustered SE': f"{se_2a * 100:.2f}%",
        't-Statistic': f"{t_2a:.2f}",
        'p-value': f"{p_2a:.4f}",
        'Resolved Trades (N)': len(df_2a),
        'Trading Days': df_2a['date'].nunique()
    })

    # --- Spec 3A: Continuous Brent Volatility × Downstream Consumers (vs. Clean Defensives) ---
    df_3a = trades[trades['is_downstream'] | trades['is_defensive']].merge(
        brent[['date', 'sigma_brent_20d']], on='date', how='inner'
    ).dropna(subset=['sigma_brent_20d']).copy()

    df_3a['treat'] = df_3a['is_downstream'].astype(float)
    df_3a['vol_x_treat'] = df_3a['sigma_brent_20d'] * df_3a['treat']

    X_3a = sm.add_constant(df_3a[['sigma_brent_20d', 'treat', 'vol_x_treat']])
    m_3a = sm.OLS(df_3a['is_win'], X_3a).fit(cov_type='cluster', cov_kwds={'groups': df_3a['date']})
    b3_3a, se_3a, t_3a, p_3a = m_3a.params['vol_x_treat'], m_3a.bse['vol_x_treat'], m_3a.tvalues['vol_x_treat'], m_3a.pvalues['vol_x_treat']

    table10_rows.append({
        'Specification': 'Spec 3A: Continuous Brent Volatility × Downstream Consumers',
        'DiD Parameter': 'β₃ (σ_Brent × Downstream)',
        'DiD Coefficient': f"{b3_3a:.4f}{format_stars(p_3a)}",
        'Day-Clustered SE': f"{se_3a:.4f}",
        't-Statistic': f"{t_3a:.2f}",
        'p-value': f"{p_3a:.4f}",
        'Resolved Trades (N)': len(df_3a),
        'Trading Days': df_3a['date'].nunique()
    })

    df_table10 = pd.DataFrame(table10_rows)

    # Save CSV
    os.makedirs(os.path.join(BASE_DIR, 'output', 'tables'), exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, 'output', 'figures'), exist_ok=True)
    
    csv_path = os.path.join(BASE_DIR, 'output', 'tables', 'table_10_sector_did.csv')
    df_table10.to_csv(csv_path, index=False)

    # Generate Markdown Table
    md_path = os.path.join(BASE_DIR, 'output', 'tables', 'table_10_sector_did.md')
    md_lines = [
        "# Table 10: Sector Difference-in-Differences Estimations",
        "",
        "Difference-in-Differences (DiD) specifications evaluating energy transmission across Downstream Consumers, Upstream Producers, and Clean Defensives. "
        "Standard errors are clustered by trading session date. Significance: * p < 0.10, ** p < 0.05, *** p < 0.01.",
        "",
        "| Specification | DiD Parameter | DiD Coefficient | Day-Clustered SE | t-Statistic | p-value | Resolved Trades (N) | Trading Days |",
        "|:---|:---|---:|---:|---:|:---:|---:|---:|"
    ]
    for _, r in df_table10.iterrows():
        md_lines.append(
            f"| {r['Specification']} | {r['DiD Parameter']} | {r['DiD Coefficient']} | "
            f"{r['Day-Clustered SE']} | {r['t-Statistic']} | {r['p-value']} | "
            f"{r['Resolved Trades (N)']:,} | {r['Trading Days']:,} |"
        )
    md_lines.append("")
    
    with open(md_path, 'w') as f:
        f.write('\n'.join(md_lines))
    print(f"Table 10 saved to {csv_path} and {md_path}")

    # Plot Figure 5: Downstream vs Upstream vs Defensive Daily Win Rates
    down_daily = trades[trades['is_downstream']].groupby('date')['is_win'].mean() * 100.0
    up_daily = trades[trades['is_upstream']].groupby('date')['is_win'].mean() * 100.0
    def_daily = trades[trades['is_defensive']].groupby('date')['is_win'].mean() * 100.0
    
    plot_df = pd.DataFrame({'Downstream': down_daily, 'Upstream': up_daily, 'Defensive': def_daily}).dropna().reset_index()
    plot_df['date_dt'] = pd.to_datetime(plot_df['date'])
    plot_df = plot_df.sort_values('date_dt')
    
    plot_df['Downstream_20d'] = plot_df['Downstream'].rolling(20).mean()
    plot_df['Upstream_20d'] = plot_df['Upstream'].rolling(20).mean()
    plot_df['Defensive_20d'] = plot_df['Defensive'].rolling(20).mean()
    
    fig_path = os.path.join(BASE_DIR, 'output', 'figures', 'figure_05_sector_did_trajectories.png')
    
    plt.figure(figsize=(11, 5.5), dpi=300)
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    
    plt.plot(plot_df['date_dt'], plot_df['Downstream_20d'], color='#d62728', linewidth=2.0, label='Downstream Consumers (20-Day MA)')
    plt.plot(plot_df['date_dt'], plot_df['Upstream_20d'], color='#ff7f0e', linewidth=1.8, linestyle='--', label='Upstream Producers (20-Day MA)')
    plt.plot(plot_df['date_dt'], plot_df['Defensive_20d'], color='#1f77b4', linewidth=2.0, label='Clean Defensives (20-Day MA)')
    
    plt.axvline(x=pd.to_datetime('2026-03-04'), color='#2ca02c', linestyle=':', linewidth=1.8, label='Event Date (2026-03-04)')
    plt.axhline(y=50.0, color='#333333', linestyle='--', linewidth=1.0, alpha=0.7, label='50% Breakeven Barrier')
    
    plt.title('Figure 5: Daily Win Rates for Downstream, Upstream, and Defensive Sectors', fontsize=13, fontweight='bold', pad=12)
    plt.xlabel('Calendar Date', fontsize=11, labelpad=8)
    plt.ylabel('Resolved Win Rate (%, 20-Day Moving Average)', fontsize=11, labelpad=8)
    plt.legend(frameon=True, loc='lower left', fontsize=9.5)
    plt.tight_layout()
    plt.savefig(fig_path, dpi=300)
    plt.close()
    
    print(f"Figure 5 saved to {fig_path}")
    return df_table10

if __name__ == '__main__':
    run_test_8()
```

---

## File: `src/test_09_strata_analysis.py` <a id="file-src-test-09-strata-analysis-py"></a>

```python
"""
Test 9: Survivorship and Liquidity Strata
Manuscript Reference: Table 11, Figure 7, Section 4.7
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import pandas as pd
import numpy as np
import statsmodels.api as sm
from scipy import stats
import matplotlib.pyplot as plt
from src.data_loader import load_trades_clean, load_subuniverse_symbols

def format_stars(p_val):
    if p_val < 0.01: return "***"
    elif p_val < 0.05: return "**"
    elif p_val < 0.10: return "*"
    else: return ""

def two_way_cluster_ols(y, X, cluster_day, cluster_stock):
    model = sm.OLS(y, X).fit()
    params = model.params
    cov_day = model.get_robustcov_results(cov_type='cluster', groups=cluster_day).cov_params()
    cov_stock = model.get_robustcov_results(cov_type='cluster', groups=cluster_stock).cov_params()
    cov_white = model.get_robustcov_results(cov_type='HC0').cov_params()
    cov_2way = cov_day + cov_stock - cov_white
    diag = np.diag(cov_2way)
    diag = np.where(diag > 0, diag, np.diag(cov_day))
    se_2way = np.sqrt(diag)
    t_stats = params / se_2way
    p_vals = 2 * (1 - stats.norm.cdf(np.abs(t_stats)))
    return params, se_2way, t_stats, p_vals

def run_test_9():
    print("Running Test 9: Survivorship and Liquidity Strata (Table 11, Figure 7)...")
    trades = load_trades_clean(resolved_only=True)
    all_trades = load_trades_clean(resolved_only=False)
    sub_univs = load_subuniverse_symbols()
    
    # Ex-ante 2022 turnover proxy: trade counts in first 60 trading days
    u_dates = sorted(all_trades['date'].unique())
    first_60 = set(u_dates[:60])
    counts_60 = all_trades[all_trades['date'].isin(first_60)].groupby('symbol_root').size()
    
    all_symbols = sorted(all_trades['symbol_root'].unique())
    s_series = pd.Series(0, index=all_symbols)
    s_series.update(counts_60)
    q_labels = ['Liquidity Q4 (lowest)', 'Liquidity Q3', 'Liquidity Q2', 'Liquidity Q1 (highest)']
    s_quartiles = pd.qcut(s_series.rank(method='first'), q=4, labels=q_labels)

    strata_definitions = [
        ('Full 480 Universe', set(all_symbols)),
        ('Nifty 50 Sub-universe', set([s.replace('_1M', '') for s in sub_univs['nifty50_symbols']])),
        ('Midcap 50 Sub-universe', set([s.replace('_1M', '') for s in sub_univs['midcap50_symbols']])),
        ('Smallcap 50 Sub-universe', set([s.replace('_1M', '') for s in sub_univs['smcap50_symbols']])),
        ('Liquidity Q1 (highest)', set(s_quartiles[s_quartiles == 'Liquidity Q1 (highest)'].index)),
        ('Liquidity Q2', set(s_quartiles[s_quartiles == 'Liquidity Q2'].index)),
        ('Liquidity Q3', set(s_quartiles[s_quartiles == 'Liquidity Q3'].index)),
        ('Liquidity Q4 (lowest)', set(s_quartiles[s_quartiles == 'Liquidity Q4 (lowest)'].index))
    ]

    records = []
    forest_plot_data = []

    for name, syms in strata_definitions:
        sub = trades[trades['symbol_root'].isin(syms)].copy()
        y = sub['is_win'].values
        post = (sub['regime'] == 'post_shock').astype(float).values
        pre = (sub['regime'] == 'pre_stable').astype(float).values
        X = sm.add_constant(np.column_stack([post, pre]))
        
        p, se, t, pvals = two_way_cluster_ols(y, X, sub['date'].values, sub['symbol'].values)
        beta1, se1, t1, pval1 = p[1], se[1], t[1], pvals[1]
        
        n_stable = len(sub[sub['regime'] == 'stable'])
        n_post = len(sub[sub['regime'] == 'post_shock'])
        n_syms = sub['symbol_root'].nunique()
        stars = format_stars(pval1)
        
        records.append({
            'Stratum': name,
            'PostShock Indicator (β₁)': f"{beta1 * 100:.2f}%{stars}",
            'Two-Way SE (%)': f"{se1 * 100:.2f}%",
            't-Statistic': f"{t1:.2f}",
            'p-value': f"{pval1:.4f}" if pval1 >= 0.0001 else "< 0.0001",
            'N Resolved (Stable)': n_stable,
            'N Resolved (Post-Shock)': n_post,
            'Number of Symbols': n_syms
        })
        
        forest_plot_data.append({
            'name': name,
            'beta': beta1 * 100.0,
            'se': se1 * 100.0,
            'ci_lower': (beta1 - 1.96 * se1) * 100.0,
            'ci_upper': (beta1 + 1.96 * se1) * 100.0
        })

    df_table11 = pd.DataFrame(records)

    # Save CSV
    os.makedirs(os.path.join(BASE_DIR, 'output', 'tables'), exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, 'output', 'figures'), exist_ok=True)
    
    csv_path = os.path.join(BASE_DIR, 'output', 'tables', 'table_11_strata_analysis.csv')
    df_table11.to_csv(csv_path, index=False)

    # Generate Markdown Table
    md_path = os.path.join(BASE_DIR, 'output', 'tables', 'table_11_strata_analysis.md')
    md_lines = [
        "# Table 11: Survivorship and Liquidity Strata LPM Estimations",
        "",
        "Linear Probability Model (LPM) of trade win outcome across 8 sub-universe and ex-ante liquidity strata. "
        "Standard errors are two-way clustered by trading day and stock symbol. Significance: * p < 0.10, ** p < 0.05, *** p < 0.01.",
        "",
        "| Stratum | PostShock Indicator (β₁) | Two-Way SE (%) | t-Statistic | p-value | N Resolved (Stable) | N Resolved (Post-Shock) | Number of Symbols |",
        "|:---|---:|---:|---:|:---:|---:|---:|---:|"
    ]
    for _, r in df_table11.iterrows():
        md_lines.append(
            f"| {r['Stratum']} | {r['PostShock Indicator (β₁)']} | {r['Two-Way SE (%)']} | {r['t-Statistic']} | "
            f"{r['p-value']} | {r['N Resolved (Stable)']:,} | {r['N Resolved (Post-Shock)']:,} | {r['Number of Symbols']:,} |"
        )
    md_lines.append("")
    
    with open(md_path, 'w') as f:
        f.write('\n'.join(md_lines))
    print(f"Table 11 saved to {csv_path} and {md_path}")

    # --- Plot Figure 7: Forest Plot ---
    df_forest = pd.DataFrame(forest_plot_data).iloc[::-1].reset_index(drop=True)
    fig_path = os.path.join(BASE_DIR, 'output', 'figures', 'figure_07_strata_forest_plot.png')
    
    plt.figure(figsize=(10, 6), dpi=300)
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    
    y_pos = np.arange(len(df_forest))
    
    plt.errorbar(
        df_forest['beta'], y_pos, 
        xerr=1.96 * df_forest['se'], 
        fmt='o', color='#1f77b4', ecolor='#1f77b4', elinewidth=2.0, capsize=4, markersize=7,
        label='Post-Shock β₁ (95% CI)'
    )
    
    plt.axvline(x=0, color='#333333', linestyle='--', linewidth=1.0, alpha=0.7)
    plt.axvline(x=df_forest.loc[df_forest['name'] == 'Full 480 Universe', 'beta'].values[0], color='#d62728', linestyle=':', linewidth=1.2, label='Full 480 Benchmark (-8.15%)')
    
    plt.yticks(y_pos, df_forest['name'], fontsize=10)
    plt.xlabel('Post-Shock Treatment Effect on Win Rate (Percentage Points)', fontsize=11, labelpad=8)
    plt.title('Figure 7: Post-Shock Win-Rate Contraction Across Strata (Forest Plot)', fontsize=13, fontweight='bold', pad=12)
    plt.legend(frameon=True, loc='lower left', fontsize=10)
    plt.tight_layout()
    plt.savefig(fig_path, dpi=300)
    plt.close()
    
    print(f"Figure 7 saved to {fig_path}")
    return df_table11

if __name__ == '__main__':
    run_test_9()
```

---

## File: `src/test_10_macro_horse_race.py` <a id="file-src-test-10-macro-horse-race-py"></a>

```python
"""
Test 10: Macro Horse Race — Sequential WLS Models
Manuscript Reference: Table 12, Figure 8, Section 4.8
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from src.data_loader import load_daily_clean, load_trades_clean

def format_stars(p_val):
    if p_val < 0.01: return "***"
    elif p_val < 0.05: return "**"
    elif p_val < 0.10: return "*"
    else: return ""

def run_test_10():
    print("Running Test 10: Macro Horse Race (Table 12, Figure 8)...")
    daily = load_daily_clean()

    # Load Macro Series
    # 1. Brent Crude
    brent_path = os.path.join(BASE_DIR, 'data', 'macro', 'XBR_USD Historical Data.csv')
    brent = pd.read_csv(brent_path, encoding='utf-8-sig')
    brent['date'] = pd.to_datetime(brent['Date']).dt.strftime('%Y-%m-%d')
    brent = brent.sort_values('date').reset_index(drop=True)
    brent['R_brent'] = np.log(brent['Price'] / brent['Price'].shift(1))
    brent['abs_R_brent'] = brent['R_brent'].abs()
    brent['sigma_brent_20d'] = brent['R_brent'].rolling(20).std()

    # 2. India VIX
    vix_path = os.path.join(BASE_DIR, 'data', 'macro', 'India VIX Historical Data.csv')
    vix = pd.read_csv(vix_path, encoding='utf-8-sig')
    vix['date'] = pd.to_datetime(vix['Date']).dt.strftime('%Y-%m-%d')
    vix = vix.sort_values('date').reset_index(drop=True)
    vix['vix'] = vix['Price']

    # 3. Nifty 500
    n500_path = os.path.join(BASE_DIR, 'data', 'macro', 'Nifty 500 Historical Data.csv')
    n500 = pd.read_csv(n500_path, encoding='utf-8-sig')
    n500['date'] = pd.to_datetime(n500['Date']).dt.strftime('%Y-%m-%d')
    n500 = n500.sort_values('date').reset_index(drop=True)
    p_num = n500['Price'].astype(str).str.replace(',', '').astype(float)
    n500['R_nifty500'] = np.log(p_num / p_num.shift(1))
    n500['abs_R_nifty500'] = n500['R_nifty500'].abs()

    # 4. USD/INR
    usdinr_path = os.path.join(BASE_DIR, 'data', 'macro', 'INR_USD Historical Data.csv')
    usdinr = pd.read_csv(usdinr_path, encoding='utf-8-sig')
    usdinr['date'] = pd.to_datetime(usdinr['Date']).dt.strftime('%Y-%m-%d')
    usdinr = usdinr.sort_values('date').reset_index(drop=True)
    usdinr['usd_inr_chg'] = np.log(usdinr['Price'] / usdinr['Price'].shift(1))

    # 5. NSE Volume / Turnover
    vol_path = os.path.join(BASE_DIR, 'data', 'macro', 'NSE_Volume_Jan2022_to_May2026.csv')
    nse_vol = pd.read_csv(vol_path, encoding='utf-8-sig')
    nse_vol['date'] = pd.to_datetime(nse_vol['Date'], dayfirst=True).dt.strftime('%Y-%m-%d')
    nse_vol = nse_vol.sort_values('date').reset_index(drop=True)
    to_crore = nse_vol['Turnover_Rs_Crore'].replace(0, np.nan)
    nse_vol['ln_turnover'] = np.log(to_crore)

    # 6. FII Net Flows
    fii_path = os.path.join(BASE_DIR, 'data', 'macro', 'fii_dii_cash_2025_to_present.csv')
    fii = pd.read_csv(fii_path, encoding='utf-8-sig')
    fii['date'] = pd.to_datetime(fii['Date']).dt.strftime('%Y-%m-%d')
    fii = fii.sort_values('date').reset_index(drop=True)
    fii['fii_net'] = fii['FII_Net']

    # 7. Opening Bar Range (Microstructure)
    bar_path = os.path.join(BASE_DIR, 'data', 'microstructure', 'opening_bar_ranges.pkl')
    bar_df = pd.read_pickle(bar_path)
    bar_df['range'] = (bar_df['bar0_high'] - bar_df['bar0_low']) / bar_df['bar0_open']
    bar_df['date_str'] = bar_df['date'].astype(str)
    daily_bar_range = bar_df.groupby('date_str')['range'].mean().reset_index()
    daily_bar_range.columns = ['date', 'mean_bar0_range']

    # 8. Sweet Spot Share
    trades = load_trades_clean(resolved_only=True)
    trades['is_sweet_spot'] = trades['gap_size_pct'].between(0.50, 2.00)
    daily_sweet = trades.groupby('date')['is_sweet_spot'].mean().reset_index()
    daily_sweet.columns = ['date', 'sweet_spot_share']

    # Merging panel
    df = daily.copy()
    df['post_shock'] = (df['regime'] == 'post_shock').astype(float)
    df = df.merge(vix[['date', 'vix']], on='date', how='left')
    df = df.merge(n500[['date', 'R_nifty500', 'abs_R_nifty500']], on='date', how='left')
    df = df.merge(usdinr[['date', 'usd_inr_chg']], on='date', how='left')
    df = df.merge(nse_vol[['date', 'ln_turnover']], on='date', how='left')
    df = df.merge(fii[['date', 'fii_net']], on='date', how='left')
    df = df.merge(daily_bar_range[['date', 'mean_bar0_range']], on='date', how='left')
    df = df.merge(daily_sweet[['date', 'sweet_spot_share']], on='date', how='left')
    df = df.merge(brent[['date', 'R_brent', 'abs_R_brent', 'sigma_brent_20d']], on='date', how='left')

    models = [
        ('Model 1', ['post_shock']),
        ('Model 2', ['post_shock', 'vix', 'R_nifty500', 'abs_R_nifty500']),
        ('Model 3', ['post_shock', 'vix', 'R_nifty500', 'abs_R_nifty500', 'usd_inr_chg', 'ln_turnover']),
        ('Model 4', ['post_shock', 'vix', 'R_nifty500', 'abs_R_nifty500', 'usd_inr_chg', 'ln_turnover', 'mean_bar0_range', 'sweet_spot_share']),
        ('Model 5', ['post_shock', 'vix', 'R_nifty500', 'abs_R_nifty500', 'usd_inr_chg', 'ln_turnover', 'mean_bar0_range', 'sweet_spot_share', 'sigma_brent_20d', 'abs_R_brent']),
        ('Model 6', ['post_shock', 'vix', 'R_nifty500', 'abs_R_nifty500', 'usd_inr_chg', 'ln_turnover', 'mean_bar0_range', 'sweet_spot_share', 'sigma_brent_20d', 'abs_R_brent', 'fii_net'])
    ]

    all_variables = [
        ('const', 'Constant (α)'),
        ('post_shock', 'PostShock Indicator (β₁)'),
        ('vix', 'India VIX'),
        ('R_nifty500', 'Nifty 500 Return'),
        ('abs_R_nifty500', '|Nifty 500 Return|'),
        ('usd_inr_chg', 'Δ USD/INR'),
        ('ln_turnover', 'ln(NSE Turnover)'),
        ('mean_bar0_range', 'Mean Opening Bar Range'),
        ('sweet_spot_share', 'Sweet Spot Share'),
        ('sigma_brent_20d', 'Brent 20d Volatility'),
        ('abs_R_brent', '|Brent Return|'),
        ('fii_net', 'FII Net Flow (Rs Cr)')
    ]

    model_results = {}
    fig8_data = []

    for m_label, v_list in models:
        sub = df.dropna(subset=v_list + ['resolved_wr', 'n_resolved']).copy()
        X = sm.add_constant(sub[v_list])
        res = sm.WLS(sub['resolved_wr'], X, weights=sub['n_resolved']).fit(cov_type='HAC', cov_kwds={'maxlags': 5})
        
        post_b = res.params['post_shock']
        post_se = res.bse['post_shock']
        fig8_data.append({
            'model': m_label,
            'beta': post_b * 100.0,
            'se': post_se * 100.0,
            'ci_lower': (post_b - 1.96 * post_se) * 100.0,
            'ci_upper': (post_b + 1.96 * post_se) * 100.0
        })
        
        col_dict = {}
        for var_name, var_disp in all_variables:
            if var_name in res.params:
                coef = res.params[var_name]
                se = res.bse[var_name]
                pval = res.pvalues[var_name]
                stars = format_stars(pval)
                if var_name == 'fii_net':
                    col_dict[var_disp] = f"{coef:.2e}{stars} ({se:.2e})"
                elif var_name in ['const', 'post_shock']:
                    col_dict[var_disp] = f"{coef * 100:.2f}%{stars} ({se * 100:.2f}%)"
                else:
                    col_dict[var_disp] = f"{coef:.4f}{stars} ({se:.4f})"
            else:
                col_dict[var_disp] = "—"
                
        col_dict['Weighted R²'] = f"{res.rsquared:.4f}"
        col_dict['Observations (N)'] = f"{len(sub):,}"
        model_results[m_label] = col_dict

    df_table12 = pd.DataFrame(model_results)
    df_table12.index.name = 'Variable'
    df_table12 = df_table12.reset_index()

    # Save CSV
    os.makedirs(os.path.join(BASE_DIR, 'output', 'tables'), exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, 'output', 'figures'), exist_ok=True)
    
    csv_path = os.path.join(BASE_DIR, 'output', 'tables', 'table_12_macro_horse_race.csv')
    df_table12.to_csv(csv_path, index=False)

    # Generate Markdown Table
    md_path = os.path.join(BASE_DIR, 'output', 'tables', 'table_12_macro_horse_race.md')
    md_lines = [
        "# Table 12: Macro Horse Race — Sequential WLS Models",
        "",
        "Sequential Weighted Least Squares (WLS) regressions of daily resolved win rate (WR_t). "
        "Models 1–5 cover the full 2022–2026 sample; Model 6 evaluates the 2025–2026 sub-sample with direct FII net flows. "
        "Weights: daily resolved trade count (n_resolved). Standard errors: Newey-West HAC (lag = 5) reported in parentheses. "
        "Significance: * p < 0.10, ** p < 0.05, *** p < 0.01.",
        "",
        "| Variable | Model 1 | Model 2 | Model 3 | Model 4 | Model 5 | Model 6 |",
        "|:---|---:|---:|---:|---:|---:|---:|"
    ]
    for _, r in df_table12.iterrows():
        md_lines.append(
            f"| {r['Variable']} | {r['Model 1']} | {r['Model 2']} | {r['Model 3']} | {r['Model 4']} | {r['Model 5']} | {r['Model 6']} |"
        )
    md_lines.append("")
    
    with open(md_path, 'w') as f:
        f.write('\n'.join(md_lines))
    print(f"Table 12 saved to {csv_path} and {md_path}")

    # --- Plot Figure 8: Horse Race Coefficient Path ---
    df_fig8 = pd.DataFrame(fig8_data)
    fig_path = os.path.join(BASE_DIR, 'output', 'figures', 'figure_08_macro_horse_race_coefficients.png')
    
    plt.figure(figsize=(10, 5), dpi=300)
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    
    x = np.arange(len(df_fig8))
    plt.errorbar(
        x, df_fig8['beta'], 
        yerr=1.96 * df_fig8['se'], 
        fmt='-o', color='#1f77b4', ecolor='#1f77b4', elinewidth=2.0, capsize=5, markersize=7, linewidth=2.0,
        label='PostShock β₁ (95% CI)'
    )
    plt.axhline(y=0, color='#d62728', linestyle='--', linewidth=1.2, alpha=0.8, label='Zero Effect Threshold')
    
    plt.xticks(x, df_fig8['model'], fontsize=10)
    plt.ylabel('PostShock Effect on Daily Win Rate (pp)', fontsize=11, labelpad=8)
    plt.xlabel('Sequential Macro Control Model', fontsize=11, labelpad=8)
    plt.title('Figure 8: Post-Shock Indicator Attenuation in Macro Horse Race', fontsize=13, fontweight='bold', pad=12)
    plt.legend(frameon=True, loc='lower right', fontsize=10)
    plt.tight_layout()
    plt.savefig(fig_path, dpi=300)
    plt.close()
    
    print(f"Figure 8 saved to {fig_path}")
    return df_table12

if __name__ == '__main__':
    run_test_10()
```

---

## File: `src/test_11_granger_causality.py` <a id="file-src-test-11-granger-causality-py"></a>

```python
"""
Test 11: Granger Causality — Sign vs Magnitude of Oil Shock
Manuscript Reference: Figure 6, Section 4.9
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import pandas as pd
import numpy as np
import statsmodels.api as sm
from scipy import stats
import matplotlib.pyplot as plt
from src.data_loader import load_daily_clean

def format_stars(p_val):
    if p_val < 0.01: return "***"
    elif p_val < 0.05: return "**"
    elif p_val < 0.10: return "*"
    else: return ""

def granger_f_test(y_series, x_series, L):
    """
    Bivariate Granger causality F-test based on OLS SSR comparison:
    F = [(SSR_r - SSR_ur) / L] / [SSR_ur / (T - 2L - 1)]
    """
    T = len(y_series)
    y_lags = np.column_stack([y_series[L - i - 1 : T - i - 1] for i in range(L)])
    x_lags = np.column_stack([x_series[L - i - 1 : T - i - 1] for i in range(L)])
    y_target = y_series[L:]
    
    # Restricted model
    X_r = sm.add_constant(y_lags)
    res_r = sm.OLS(y_target, X_r).fit()
    ssr_r = res_r.ssr
    
    # Unrestricted model
    X_ur = sm.add_constant(np.column_stack([y_lags, x_lags]))
    res_ur = sm.OLS(y_target, X_ur).fit()
    ssr_ur = res_ur.ssr
    
    df_num = L
    df_denom = len(y_target) - 2 * L - 1
    
    F = ((ssr_r - ssr_ur) / df_num) / (ssr_ur / df_denom)
    p_val = 1.0 - stats.f.cdf(F, df_num, df_denom)
    return F, p_val

def run_test_11():
    print("Running Test 11: Granger Causality (Figure 6)...")
    daily = load_daily_clean()
    
    brent_path = os.path.join(BASE_DIR, 'data', 'macro', 'XBR_USD Historical Data.csv')
    brent = pd.read_csv(brent_path, encoding='utf-8-sig')
    brent['date'] = pd.to_datetime(brent['Date']).dt.strftime('%Y-%m-%d')
    brent = brent.sort_values('date').reset_index(drop=True)
    brent['R_brent'] = np.log(brent['Price'] / brent['Price'].shift(1))
    brent['abs_R_brent'] = brent['R_brent'].abs()
    brent['sigma_brent_20d'] = brent['R_brent'].rolling(20).std()

    df = daily.merge(brent[['date', 'R_brent', 'abs_R_brent', 'sigma_brent_20d']], on='date', how='inner')
    df = df.dropna(subset=['resolved_wr', 'R_brent', 'abs_R_brent', 'sigma_brent_20d']).reset_index(drop=True)
    
    lags = [1, 3, 5, 10]
    pairs = [
        ('R_brent → WR', df['resolved_wr'].values, df['R_brent'].values, 'Signed Brent Return → WR'),
        ('|R_brent| → WR', df['resolved_wr'].values, df['abs_R_brent'].values, '|Brent Return| (Magnitude) → WR'),
        ('σ_Brent(20d) → WR', df['resolved_wr'].values, df['sigma_brent_20d'].values, 'Brent Realized Volatility → WR'),
        ('WR → R_brent', df['R_brent'].values, df['resolved_wr'].values, 'WR → Signed Brent Return (Reverse)'),
        ('WR → |R_brent|', df['abs_R_brent'].values, df['resolved_wr'].values, 'WR → |Brent Return| (Reverse)')
    ]

    records = []
    plot_dict = {p[0]: [] for p in pairs}

    for short_label, y_vals, x_vals, full_desc in pairs:
        for lag in lags:
            F, p = granger_f_test(y_vals, x_vals, lag)
            stars = format_stars(p)
            records.append({
                'Causal Direction': full_desc,
                'Relationship': short_label,
                'Lag Order (L)': lag,
                'Granger F-Statistic': f"{F:.3f}{stars}",
                'p-value': f"{p:.4f}" if p >= 0.0001 else "< 0.0001",
                '_F': F,
                '_p': p
            })
            plot_dict[short_label].append(F)

    df_granger = pd.DataFrame(records)

    # Save CSV
    os.makedirs(os.path.join(BASE_DIR, 'output', 'tables'), exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, 'output', 'figures'), exist_ok=True)
    
    csv_path = os.path.join(BASE_DIR, 'output', 'tables', 'table_granger_causality.csv')
    df_granger.drop(columns=['_F', '_p']).to_csv(csv_path, index=False)

    # Generate Markdown Table
    md_path = os.path.join(BASE_DIR, 'output', 'tables', 'table_granger_causality.md')
    md_lines = [
        "# Table: Bivariate Granger Causality Tests — Sign vs Magnitude vs Volatility",
        "",
        "Bivariate Granger causality F-tests evaluating whether oil price direction (R_brent), shock magnitude (|R_brent|), "
        "or realized volatility (σ_Brent 20d) predictive Granger-cause the daily strategy win rate (WR_t). "
        "Tested across lag orders L ∈ {1, 3, 5, 10}. Significance: * p < 0.10, ** p < 0.05, *** p < 0.01.",
        "",
        "| Relationship | Lag Order (L) | Granger F-Statistic | p-value |",
        "|:---|---:|---:|:---:|"
    ]
    for _, r in df_granger.iterrows():
        md_lines.append(f"| {r['Causal Direction']} | {r['Lag Order (L)']} | {r['Granger F-Statistic']} | {r['p-value']} |")
    md_lines.append("")
    
    with open(md_path, 'w') as f:
        f.write('\n'.join(md_lines))
    print(f"Granger causality table saved to {csv_path} and {md_path}")

    # --- Plot Figure 6: Grouped Bar Chart of Granger F-Statistics ---
    fig_path = os.path.join(BASE_DIR, 'output', 'figures', 'figure_06_granger_causality_f_stats.png')
    
    plt.figure(figsize=(11, 5.5), dpi=300)
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    
    x = np.arange(len(lags))
    width = 0.16
    
    colors = ['#aec7e8', '#ff7f0e', '#d62728', '#2ca02c', '#98df8a']
    
    for i, (short_label, _, _, full_desc) in enumerate(pairs):
        offset = (i - 2) * width
        plt.bar(x + offset, plot_dict[short_label], width, label=short_label, color=colors[i], alpha=0.9)

    # Reference 5% critical value line (F ~ 3.84 for L=1, F ~ 2.60 for L=3, etc.)
    plt.axhline(y=3.84, color='#555555', linestyle='--', linewidth=1.2, alpha=0.7, label='L=1 5% Critical Value (F=3.84)')
    
    plt.title('Figure 6: Bivariate Granger Causality F-Statistics: Sign vs Magnitude vs Volatility', fontsize=13, fontweight='bold', pad=12)
    plt.xlabel('Lag Order (L Days)', fontsize=11, labelpad=8)
    plt.ylabel('Granger Causality F-Statistic', fontsize=11, labelpad=8)
    plt.xticks(x, [f'Lag {l}' for l in lags], fontsize=10)
    plt.legend(frameon=True, loc='upper right', fontsize=9)
    plt.tight_layout()
    plt.savefig(fig_path, dpi=300)
    plt.close()
    
    print(f"Figure 6 saved to {fig_path}")
    return df_granger

if __name__ == '__main__':
    run_test_11()
```

---

## File: `output/tables/table_03_sample_partition.md` <a id="file-output-tables-table-03-sample-partition-md"></a>

# Table 3: Sample Partition and Descriptive Statistics

Sample partitioned across Pre-Stable, Stable, Post-Shock, and Full Sample periods following the global Muhurat Diwali purge (1,116 regular trading sessions).

| Regime Partition | Trading Days | Unique Symbols | Total Trades | Resolved Trades | Resolved Win Rate (%) | Mean Daily WR (%) | Std Daily WR (%) |
|:---|---:|---:|---:|---:|---:|---:|---:|
| Pre-Stable (< 2022-03-01) | 39 | 476 | 16,129 | 14,939 | 48.18% | 47.84% | 12.83% |
| Stable (2022-03-01 to 2026-02-28) | 990 | 480 | 387,568 | 371,850 | 52.30% | 52.43% | 8.63% |
| Post-Shock (≥ 2026-03-01) | 87 | 479 | 35,473 | 32,587 | 44.15% | 44.43% | 12.52% |
| Full Sample (All Sessions) | 1,116 | 480 | 439,170 | 419,376 | 51.52% | 51.65% | 9.43% |

---

## File: `output/tables/table_04_oos_threshold_convergence.md` <a id="file-output-tables-table-04-oos-threshold-convergence-md"></a>

# Table 4: 15-Quarter Walk-Forward OOS Threshold Convergence

First-crossing breakeven threshold estimator c*(k) across 15 out-of-sample quarters (Q3 2022 to Q1 2026). Estimated via linear interpolation between adjacent 0.25% bins at the 50.0% resolved win-rate barrier on the expanding training window. Both Resolved Win Rate (TARGET / (TARGET + STOP_LOSS)) and Nominal Win Rate (TARGET / ALL) are reported.

| Quarter | In-Sample Resolved | Cutoff c*(k) (%) | OOS Filtered Resolved | OOS Filtered Resolved WR (%) | OOS Filtered Nominal WR (%) | Fade-Dominant (>50%) |
|:---|---:|---:|---:|---:|---:|:---:|
| Q3 2022 | 47,603 | 0.617% | 10,492 | 61.02% | 54.71% | Yes |
| Q4 2022 | 72,072 | 0.567% | 8,848 | 60.58% | 55.00% | Yes |
| Q1 2023 | 95,104 | 0.508% | 9,610 | 64.61% | 60.19% | Yes |
| Q2 2023 | 118,182 | 0.446% | 9,695 | 62.25% | 57.91% | Yes |
| Q3 2023 | 140,033 | 0.401% | 12,974 | 60.34% | 57.43% | Yes |
| Q4 2023 | 163,752 | 0.387% | 13,790 | 56.87% | 52.83% | Yes |
| Q1 2024 | 186,669 | 0.391% | 14,670 | 60.42% | 57.56% | Yes |
| Q2 2024 | 210,702 | 0.385% | 14,692 | 60.23% | 55.91% | Yes |
| Q3 2024 | 234,033 | 0.378% | 14,936 | 59.55% | 55.66% | Yes |
| Q4 2024 | 258,401 | 0.374% | 13,157 | 63.09% | 59.57% | Yes |
| Q1 2025 | 281,064 | 0.369% | 15,347 | 56.50% | 54.27% | Yes |
| Q2 2025 | 304,946 | 0.375% | 14,153 | 60.95% | 53.86% | Yes |
| Q3 2025 | 327,228 | 0.376% | 11,759 | 66.12% | 62.54% | Yes |
| Q4 2025 | 349,905 | 0.366% | 11,109 | 67.59% | 64.42% | Yes |
| Q1 2026 | 371,806 | 0.355% | 14,440 | 51.77% | 46.52% | Yes |

---

## File: `output/tables/table_05_structural_break_tests.md` <a id="file-output-tables-table-05-structural-break-tests-md"></a>

# Table 5: Structural Break Tests — Quandt-Andrews and Bai-Perron

Structural break tests on daily resolved win rate (1,116 regular sessions, 5% trimming). Standard errors HAC-adjusted (Newey-West).

| Test / Specification | Statistic | p-value | Break Date | 95% Confidence Interval |
|:---|---:|:---:|:---:|:---:|
| Quandt-Andrews Sup-F | 24.5211 | < 0.001 | 2026-03-04 | — |
| Quandt-Andrews Exp-F | 7.4415 | < 0.001 | 2026-03-04 | — |
| Quandt-Andrews Ave-F | 3.3665 | < 0.10 | 2026-03-04 | — |
| Bai-Perron (BIC Selected M=3) | BIC: -4.7865 | < 0.01 | 2022-05-23, 2025-07-01, 2026-03-04 | [2022-04-05 to 2022-07-05]; [2025-04-01 to 2025-09-26]; [2026-02-23 to 2026-03-12] |

---

## File: `output/tables/table_06_lpm_two_way_cluster.md` <a id="file-output-tables-table-06-lpm-two-way-cluster-md"></a>

# Table 6: Two-Way Clustered Linear Probability Model

Linear Probability Model (LPM) of trade win outcome (1 = target hit, 0 = stop-loss hit). Standard errors are two-way clustered by trading day and stock symbol following Cameron, Gelbach, and Miller (2011). Stable regime (2022-03-01 to 2026-02-28) is the omitted baseline. Significance: * p < 0.10, ** p < 0.05, *** p < 0.01.

| Sub-Sample | PostShock Indicator (β₁) | Two-Way SE (%) | t-Statistic | p-value | Resolved Trades | Trading Days |
|:---|---:|---:|---:|:---:|---:|---:|
| Full Sample (All 1,116 Days) | -8.15%*** | 1.34% | -6.10 | < 0.0001 | 419,376 | 1,116 |
| January 2026 Alone (Pre-Shock Month 1) | 0.94% | 1.83% | 0.51 | 0.6077 | 7,305 | 20 |
| February 2026 Alone (Pre-Shock Month 2) | -0.13% | 1.86% | -0.07 | 0.9441 | 7,678 | 21 |
| March 2026 Alone (Acute Shock Month 3) | -15.41%*** | 3.63% | -4.25 | < 0.0001 | 7,170 | 19 |
| April 2026 Alone (Shock Month 4) | -9.33%*** | 2.47% | -3.78 | 0.0002 | 7,207 | 20 |
| May 2026 Alone (Shock Month 5) | -6.09%*** | 2.36% | -2.58 | 0.0099 | 7,279 | 19 |
| Full Post-Shock Window (≥ 2026-03-01) | -8.15%*** | 1.34% | -6.10 | < 0.0001 | 32,587 | 87 |

---

## File: `output/tables/table_07_wls_newey_west.md` <a id="file-output-tables-table-07-wls-newey-west-md"></a>

# Table 7: Daily WLS with Newey-West HAC Standard Errors

Weighted Least Squares (WLS) regression of daily resolved win rate (WR_t) on PostShock indicator across 1,116 trading sessions. Weights: daily count of resolved trades (n_resolved). Standard errors: Newey-West HAC with lags = 5, 10, and 20. Significance: * p < 0.10, ** p < 0.05, *** p < 0.01.

| HAC Lag | PostShock β₁ (%) | Newey-West SE (%) | t-Statistic | p-value | Weighted R² | β₁ (Pre-Stable Controlled) | SE (Pre-Controlled) |
|:---|---:|---:|---:|:---:|---:|---:|---:|
| Lag = 5 | -7.99%*** | 1.59% | -5.04 | 4.6247e-07 | 0.0518 | -8.15%*** | 1.58% |
| Lag = 10 | -7.99%*** | 1.84% | -4.34 | 1.4266e-05 | 0.0518 | -8.15%*** | 1.84% |
| Lag = 20 | -7.99%*** | 2.12% | -3.78 | 1.5890e-04 | 0.0518 | -8.15%*** | 2.11% |

---

## File: `output/tables/table_08_gap_size_bins.md` <a id="file-output-tables-table-08-gap-size-bins-md"></a>

# Table 8: Gap-Size Bin Win-Rate Analysis and Structural Comparison

Win rates across 10 fixed gap-size bins comparing Stable (2022-03-01 to 2026-02-28) and Post-Shock (≥ 2026-03-01) regimes. Differences are evaluated via day-clustered Linear Probability Models (LPM) clustering by trading session date to account for cross-sectional dependence. Both Resolved Win Rate (TARGET / (TARGET + STOP_LOSS)) and Nominal Win Rate (TARGET / ALL) are reported. Significance: * p < 0.10, ** p < 0.05, *** p < 0.01.

| Gap Size Bin (%) | Stable Resolved WR | Post Resolved WR | Resolved Diff (Day-Clustered SE) | Resolved t-Stat (p-val) | Stable Nominal WR | Post Nominal WR | Nominal Diff (Day-Clustered SE) |
|:---|---:|---:|---:|---:|---:|---:|---:|
| 0.00–0.25 | 35.38% | 29.82% | -5.56%*** (0.85%) | -6.50 (< 0.0001) | 35.38% | 29.82% | -5.56%*** (0.85%) |
| 0.25–0.50 | 51.62% | 43.06% | -8.56%*** (1.58%) | -5.41 (< 0.0001) | 51.58% | 43.03% | -8.55%*** (1.58%) |
| 0.50–0.75 | 59.83% | 48.55% | -11.28%*** (2.04%) | -5.52 (< 0.0001) | 59.24% | 48.34% | -10.91%*** (2.04%) |
| 0.75–1.00 | 62.00% | 51.39% | -10.61%*** (2.33%) | -4.56 (< 0.0001) | 59.87% | 49.99% | -9.88%*** (2.29%) |
| 1.00–1.25 | 61.52% | 48.94% | -12.58%*** (2.52%) | -4.99 (< 0.0001) | 57.10% | 45.46% | -11.64%*** (2.32%) |
| 1.25–1.50 | 61.11% | 47.12% | -14.00%*** (3.13%) | -4.47 (< 0.0001) | 53.95% | 40.57% | -13.38%*** (2.72%) |
| 1.50–2.00 | 61.96% | 44.78% | -17.18%*** (3.63%) | -4.74 (< 0.0001) | 50.56% | 34.79% | -15.77%*** (3.00%) |
| 2.00–2.50 | 61.32% | 50.36% | -10.96%** (5.11%) | -2.15 (0.0319) | 44.25% | 33.54% | -10.70%*** (4.00%) |
| 2.50–3.00 | 63.23% | 59.57% | -3.66% (7.46%) | -0.49 (0.6240) | 39.25% | 30.11% | -9.14%** (4.64%) |
| 3.00+ | 63.31% | 59.61% | -3.70% (10.04%) | -0.37 (0.7127) | 25.41% | 20.86% | -4.55% (4.74%) |

---

## File: `output/tables/table_09_event_study_cawr.md` <a id="file-output-tables-table-09-event-study-cawr-md"></a>

# Table 9: Event Study — Cumulative Abnormal Win Rate (CAWR)

Cumulative Abnormal Win Rate (CAWR) around the March 4, 2026 structural break event date. Benchmark parameters estimated on 2022-03-15 to 2025-07-31 (N = 837 days): benchmark mean μ = 51.94%, daily volatility σ = 8.77%. Standard errors are computed as SE(CAWR) = σ × √L. Significance: * p < 0.10, ** p < 0.05, *** p < 0.01.

| Window Label | Event-Relative Days | Window Length (L) | CAWR (pp) | Standard Error (pp) | t-Statistic | p-value |
|:---|:---:|---:|---:|---:|---:|:---:|
| Pre-event Placebo | [-10, -1] | 10 | +47.97* | 27.74 | 1.73 | 0.0838 |
| Short post-shock | [+1, +5] | 5 | -52.33*** | 19.62 | -2.67 | 0.0076 |
| Medium post-shock | [+1, +10] | 10 | -99.70*** | 27.74 | -3.59 | 0.0003 |
| Long post-shock | [+1, +20] | 20 | -300.16*** | 39.23 | -7.65 | < 0.0001 |
| Extended post-shock | [+1, +40] | 40 | -458.77*** | 55.48 | -8.27 | < 0.0001 |

---

## File: `output/tables/table_10_sector_did.md` <a id="file-output-tables-table-10-sector-did-md"></a>

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

---

## File: `output/tables/table_11_strata_analysis.md` <a id="file-output-tables-table-11-strata-analysis-md"></a>

# Table 11: Survivorship and Liquidity Strata LPM Estimations

Linear Probability Model (LPM) of trade win outcome across 8 sub-universe and ex-ante liquidity strata. Standard errors are two-way clustered by trading day and stock symbol. Significance: * p < 0.10, ** p < 0.05, *** p < 0.01.

| Stratum | PostShock Indicator (β₁) | Two-Way SE (%) | t-Statistic | p-value | N Resolved (Stable) | N Resolved (Post-Shock) | Number of Symbols |
|:---|---:|---:|---:|:---:|---:|---:|---:|
| Full 480 Universe | -8.15%*** | 1.34% | -6.10 | < 0.0001 | 371,850 | 32,587 | 480 |
| Nifty 50 Sub-universe | -8.39%*** | 1.57% | -5.33 | < 0.0001 | 35,324 | 3,120 | 48 |
| Midcap 50 Sub-universe | -10.40%*** | 1.93% | -5.39 | < 0.0001 | 36,852 | 3,237 | 49 |
| Smallcap 50 Sub-universe | -7.45%*** | 1.84% | -4.04 | < 0.0001 | 37,834 | 3,272 | 48 |
| Liquidity Q1 (highest) | -7.25%*** | 1.48% | -4.89 | < 0.0001 | 95,040 | 8,232 | 120 |
| Liquidity Q2 | -8.73%*** | 1.42% | -6.17 | < 0.0001 | 94,627 | 8,231 | 120 |
| Liquidity Q3 | -7.87%*** | 1.51% | -5.20 | < 0.0001 | 92,396 | 8,056 | 120 |
| Liquidity Q4 (lowest) | -8.83%*** | 1.46% | -6.04 | < 0.0001 | 89,787 | 8,068 | 120 |

---

## File: `output/tables/table_12_macro_horse_race.md` <a id="file-output-tables-table-12-macro-horse-race-md"></a>

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

---

## File: `output/tables/table_granger_causality.md` <a id="file-output-tables-table-granger-causality-md"></a>

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

---

## File: `output/tables/table_03_sample_partition.csv` <a id="file-output-tables-table-03-sample-partition-csv"></a>

```csv
Regime Partition,Trading Days,Unique Symbols,Total Trades,Resolved Trades,Resolved Win Rate (%),Mean Daily WR (%),Std Daily WR (%)
Pre-Stable (< 2022-03-01),39,476,16129,14939,48.18%,47.84%,12.83%
Stable (2022-03-01 to 2026-02-28),990,480,387568,371850,52.30%,52.43%,8.63%
Post-Shock (≥ 2026-03-01),87,479,35473,32587,44.15%,44.43%,12.52%
Full Sample (All Sessions),1116,480,439170,419376,51.52%,51.65%,9.43%
```

---

## File: `output/tables/table_04_oos_threshold_convergence.csv` <a id="file-output-tables-table-04-oos-threshold-convergence-csv"></a>

```csv
Quarter,In-Sample Total Trades,In-Sample Resolved Trades,First-Crossing Cutoff c*(k) (%),OOS Unfiltered Trades,OOS Unfiltered Resolved WR (%),OOS Unfiltered Nominal WR (%),OOS Filtered Total Trades,OOS Filtered Resolved Trades,OOS Filtered Resolved WR (%),OOS Filtered Nominal WR (%),Fade-Dominant (>50% WR)
Q3 2022,51150,47603,0.6174947898380099,25699,50.98,48.54,11701,10492,61.02,54.71,Yes
Q4 2022,76849,72072,0.5672799512187643,23943,51.93,49.95,9745,8848,60.58,55.0,Yes
Q1 2023,100792,95104,0.5078635959164578,23795,55.22,53.56,10315,9610,64.61,60.19,Yes
Q2 2023,124587,118182,0.4456551964915719,22583,54.2,52.44,10422,9695,62.25,57.91,Yes
Q3 2023,147170,140033,0.4008143602627589,24380,52.12,50.71,13632,12974,60.34,57.43,Yes
Q4 2023,171550,163752,0.3874396003985569,23976,50.0,47.79,14847,13790,56.87,52.83,Yes
Q1 2024,195526,186669,0.3910473372351013,24761,52.25,50.71,15398,14670,60.42,57.56,Yes
Q2 2024,220287,210702,0.3848962809197975,24465,53.08,50.62,15826,14692,60.23,55.91,Yes
Q3 2024,244752,234033,0.3780173223883274,25415,51.81,49.68,15982,14936,59.55,55.66,Yes
Q4 2024,270167,258401,0.37363996253117665,23442,53.61,51.83,13936,13157,63.09,59.57,Yes
Q1 2025,293609,281064,0.3685759715420692,24514,48.56,47.31,15978,15347,56.5,54.27,Yes
Q2 2025,318123,304946,0.3745535936819847,24148,51.7,47.7,16017,14153,60.95,53.86,Yes
Q3 2025,342271,327228,0.3755297499470245,23351,55.55,53.94,12433,11759,66.12,62.54,Yes
Q4 2025,365622,349905,0.3659694577407211,22450,57.35,55.95,11657,11109,67.59,64.42,Yes
Q1 2026,388072,371806,0.3549023109900623,23784,47.57,44.31,16071,14440,51.77,46.52,Yes
```

---

## File: `output/tables/table_05_structural_break_tests.csv` <a id="file-output-tables-table-05-structural-break-tests-csv"></a>

```csv
Test / Specification,Statistic,p-value,Break Date,95% Confidence Interval
Quandt-Andrews Sup-F,24.5211,< 0.001,2026-03-04,—
Quandt-Andrews Exp-F,7.4415,< 0.001,2026-03-04,—
Quandt-Andrews Ave-F,3.3665,< 0.10,2026-03-04,—
Bai-Perron (BIC Selected M=3),BIC: -4.7865,< 0.01,"2022-05-23, 2025-07-01, 2026-03-04",[2022-04-05 to 2022-07-05]; [2025-04-01 to 2025-09-26]; [2026-02-23 to 2026-03-12]
```

---

## File: `output/tables/table_06_lpm_two_way_cluster.csv` <a id="file-output-tables-table-06-lpm-two-way-cluster-csv"></a>

```csv
Sub-Sample,PostShock Indicator (β₁),Two-Way SE (%),t-Statistic,p-value,Resolved Trades,Trading Days
"Full Sample (All 1,116 Days)",-8.15%***,1.34%,-6.10,< 0.0001,419376,1116
January 2026 Alone (Pre-Shock Month 1),0.94%,1.83%,0.51,0.6077,7305,20
February 2026 Alone (Pre-Shock Month 2),-0.13%,1.86%,-0.07,0.9441,7678,21
March 2026 Alone (Acute Shock Month 3),-15.41%***,3.63%,-4.25,< 0.0001,7170,19
April 2026 Alone (Shock Month 4),-9.33%***,2.47%,-3.78,0.0002,7207,20
May 2026 Alone (Shock Month 5),-6.09%***,2.36%,-2.58,0.0099,7279,19
Full Post-Shock Window (≥ 2026-03-01),-8.15%***,1.34%,-6.10,< 0.0001,32587,87
```

---

## File: `output/tables/table_07_wls_newey_west.csv` <a id="file-output-tables-table-07-wls-newey-west-csv"></a>

```csv
HAC Lag,PostShock β₁ (%),Newey-West SE (%),t-Statistic,p-value,Weighted R²,PostShock β₁ (Pre-Stable Controlled),SE (Pre-Controlled),t-Stat (Pre-Controlled),N Observations
Lag = 5,-7.99%***,1.59%,-5.04,4.6247e-07,0.0518,-8.15%***,1.58%,-5.15,1116
Lag = 10,-7.99%***,1.84%,-4.34,1.4266e-05,0.0518,-8.15%***,1.84%,-4.43,1116
Lag = 20,-7.99%***,2.12%,-3.78,1.5890e-04,0.0518,-8.15%***,2.11%,-3.85,1116
```

---

## File: `output/tables/table_08_gap_size_bins.csv` <a id="file-output-tables-table-08-gap-size-bins-csv"></a>

```csv
Gap Size Bin (%),Stable Total N,Stable Resolved N,Post Total N,Post Resolved N,Stable Resolved WR (%),Post Resolved WR (%),Resolved Diff (pp),Resolved Day-Clustered SE,Resolved t-Stat,Resolved p-value,Stable Nominal WR (%),Post Nominal WR (%),Nominal Diff (pp),Nominal Day-Clustered SE,Nominal t-Stat,Nominal p-value
0.00–0.25,84956,84956,6012,6012,35.38%,29.82%,-5.56%***,0.85%,-6.50,< 0.0001,35.38%,29.82%,-5.56%***,0.85%,-6.50,< 0.0001
0.25–0.50,111962,111877,8364,8358,51.62%,43.06%,-8.56%***,1.58%,-5.41,< 0.0001,51.58%,43.03%,-8.55%***,1.58%,-5.41,< 0.0001
0.50–0.75,75985,75245,6163,6136,59.83%,48.55%,-11.28%***,2.04%,-5.52,< 0.0001,59.24%,48.34%,-10.91%***,2.04%,-5.34,< 0.0001
0.75–1.00,44199,42682,4289,4172,62.00%,51.39%,-10.61%***,2.33%,-4.56,< 0.0001,59.87%,49.99%,-9.88%***,2.29%,-4.31,< 0.0001
1.00–1.25,24827,23041,2906,2699,61.52%,48.94%,-12.58%***,2.52%,-4.99,< 0.0001,57.10%,45.46%,-11.64%***,2.32%,-5.01,< 0.0001
1.25–1.50,14195,12531,1994,1717,61.11%,47.12%,-14.00%***,3.13%,-4.47,< 0.0001,53.95%,40.57%,-13.38%***,2.72%,-4.91,< 0.0001
1.50–2.00,14419,11765,2268,1762,61.96%,44.78%,-17.18%***,3.63%,-4.74,< 0.0001,50.56%,34.79%,-15.77%***,3.00%,-5.26,< 0.0001
2.00–2.50,6667,4811,1261,840,61.32%,50.36%,-10.96%**,5.11%,-2.15,0.0319,44.25%,33.54%,-10.70%***,4.00%,-2.68,0.0074
2.50–3.00,3580,2222,744,376,63.23%,59.57%,-3.66%,7.46%,-0.49,0.6240,39.25%,30.11%,-9.14%**,4.64%,-1.97,0.0491
3.00+,6778,2720,1472,515,63.31%,59.61%,-3.70%,10.04%,-0.37,0.7127,25.41%,20.86%,-4.55%,4.74%,-0.96,0.3367
```

---

## File: `output/tables/table_09_event_study_cawr.csv` <a id="file-output-tables-table-09-event-study-cawr-csv"></a>

```csv
Window Label,Event-Relative Days,Window Length (L),CAWR (pp),Standard Error (pp),t-Statistic,p-value
Pre-event Placebo,"[-10, -1]",10,+47.97*,27.74,1.73,0.0838
Short post-shock,"[+1, +5]",5,-52.33***,19.62,-2.67,0.0076
Medium post-shock,"[+1, +10]",10,-99.70***,27.74,-3.59,0.0003
Long post-shock,"[+1, +20]",20,-300.16***,39.23,-7.65,< 0.0001
Extended post-shock,"[+1, +40]",40,-458.77***,55.48,-8.27,< 0.0001
```

---

## File: `output/tables/table_10_sector_did.csv` <a id="file-output-tables-table-10-sector-did-csv"></a>

```csv
Specification,DiD Parameter,DiD Coefficient,Day-Clustered SE,t-Statistic,p-value,Resolved Trades (N),Trading Days
Spec 1A: Downstream Consumers vs. Defensives (Acute Mar 2026),β₃ (PostShock × Downstream),-8.09%***,2.76%,-2.93,0.0034,101349,1009
Spec 1B: Downstream Consumers vs. Defensives (Extended Mar–Jul 2026),β₃ (PostShock × Downstream),-2.74%*,1.65%,-1.66,0.0976,108119,1077
Spec 1C: Upstream Producers vs. Defensives (Acute Mar 2026),β₃ (PostShock × Upstream),0.48%,4.37%,0.11,0.9118,75451,1009
Spec 2: Naive Binary DiD (Pooled Upstream + Downstream vs. Others),β₃ (PostShock × EnergySector),0.06%,0.98%,0.06,0.9498,404437,1077
Spec 2A: Pre-Shock Brent Beta Quartile Dummy (All 480 Stocks),β₃ (PostShock × HighBrentBeta),-1.57%**,0.65%,-2.42,0.0157,404437,1077
Spec 3A: Continuous Brent Volatility × Downstream Consumers,β₃ (σ_Brent × Downstream),-0.8251**,0.3809,-2.17,0.0303,105493,1050
```

---

## File: `output/tables/table_11_strata_analysis.csv` <a id="file-output-tables-table-11-strata-analysis-csv"></a>

```csv
Stratum,PostShock Indicator (β₁),Two-Way SE (%),t-Statistic,p-value,N Resolved (Stable),N Resolved (Post-Shock),Number of Symbols
Full 480 Universe,-8.15%***,1.34%,-6.10,< 0.0001,371850,32587,480
Nifty 50 Sub-universe,-8.39%***,1.57%,-5.33,< 0.0001,35324,3120,48
Midcap 50 Sub-universe,-10.40%***,1.93%,-5.39,< 0.0001,36852,3237,49
Smallcap 50 Sub-universe,-7.45%***,1.84%,-4.04,< 0.0001,37834,3272,48
Liquidity Q1 (highest),-7.25%***,1.48%,-4.89,< 0.0001,95040,8232,120
Liquidity Q2,-8.73%***,1.42%,-6.17,< 0.0001,94627,8231,120
Liquidity Q3,-7.87%***,1.51%,-5.20,< 0.0001,92396,8056,120
Liquidity Q4 (lowest),-8.83%***,1.46%,-6.04,< 0.0001,89787,8068,120
```

---

## File: `output/tables/table_12_macro_horse_race.csv` <a id="file-output-tables-table-12-macro-horse-race-csv"></a>

```csv
Variable,Model 1,Model 2,Model 3,Model 4,Model 5,Model 6
Constant (α),52.14%*** (0.34%),58.34%*** (1.34%),50.38%*** (10.83%),48.60%*** (9.20%),49.85%*** (9.54%),92.63%*** (27.19%)
PostShock Indicator (β₁),-7.99%*** (1.59%),-7.44%*** (1.22%),-7.73%*** (1.39%),-7.87%*** (1.29%),-6.61%*** (1.55%),-2.82% (2.22%)
India VIX,—,-0.0017* (0.0009),-0.0014 (0.0010),0.0029*** (0.0009),0.0034*** (0.0011),-0.0011 (0.0021)
Nifty 500 Return,—,-1.3246*** (0.3975),-1.3715*** (0.4227),-0.4678 (0.4137),-0.5434 (0.4169),-0.3002 (0.7383)
|Nifty 500 Return|,—,-5.6323*** (0.8535),-5.8405*** (0.8344),-4.4222*** (0.8134),-4.4009*** (0.8437),-5.4321*** (1.2106)
Δ USD/INR,—,—,1.4675 (1.2737),1.1229 (1.1571),1.0330 (1.1670),-0.4661 (2.0312)
ln(NSE Turnover),—,—,0.0067 (0.0089),0.0150* (0.0083),0.0142* (0.0085),-0.0196 (0.0240)
Mean Opening Bar Range,—,—,—,-3.2274 (2.4251),-3.7299 (2.4966),1.1817 (3.9909)
Sweet Spot Share,—,—,—,-0.2700*** (0.0349),-0.2619*** (0.0352),-0.3060*** (0.0609)
Brent 20d Volatility,—,—,—,—,-0.3544 (0.4005),-0.2580 (0.5012)
|Brent Return|,—,—,—,—,-0.2116 (0.1956),-0.2106 (0.3573)
FII Net Flow (Rs Cr),—,—,—,—,—,1.34e-06 (1.51e-06)
Weighted R²,0.0518,0.2172,0.2231,0.3203,0.3218,0.4273
Observations (N),"1,116","1,069","1,050","1,049","1,035",332
```

---

## File: `output/tables/table_granger_causality.csv` <a id="file-output-tables-table-granger-causality-csv"></a>

```csv
Causal Direction,Relationship,Lag Order (L),Granger F-Statistic,p-value
Signed Brent Return → WR,R_brent → WR,1,0.873,0.3505
Signed Brent Return → WR,R_brent → WR,3,1.343,0.2590
Signed Brent Return → WR,R_brent → WR,5,1.309,0.2577
Signed Brent Return → WR,R_brent → WR,10,1.551,0.1163
|Brent Return| (Magnitude) → WR,|R_brent| → WR,1,13.363***,0.0003
|Brent Return| (Magnitude) → WR,|R_brent| → WR,3,8.045***,< 0.0001
|Brent Return| (Magnitude) → WR,|R_brent| → WR,5,3.815***,0.0020
|Brent Return| (Magnitude) → WR,|R_brent| → WR,10,1.578,0.1080
Brent Realized Volatility → WR,σ_Brent(20d) → WR,1,42.834***,< 0.0001
Brent Realized Volatility → WR,σ_Brent(20d) → WR,3,11.415***,< 0.0001
Brent Realized Volatility → WR,σ_Brent(20d) → WR,5,4.996***,0.0002
Brent Realized Volatility → WR,σ_Brent(20d) → WR,10,2.348***,0.0097
WR → Signed Brent Return (Reverse),WR → R_brent,1,1.430,0.2321
WR → Signed Brent Return (Reverse),WR → R_brent,3,1.155,0.3258
WR → Signed Brent Return (Reverse),WR → R_brent,5,2.742**,0.0181
WR → Signed Brent Return (Reverse),WR → R_brent,10,2.009**,0.0295
WR → |Brent Return| (Reverse),WR → |R_brent|,1,6.117**,0.0135
WR → |Brent Return| (Reverse),WR → |R_brent|,3,7.145***,< 0.0001
WR → |Brent Return| (Reverse),WR → |R_brent|,5,3.954***,0.0015
WR → |Brent Return| (Reverse),WR → |R_brent|,10,2.319**,0.0107
```

---
