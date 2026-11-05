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

