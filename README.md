# Gap-Trading Raw Materials & Replication Repository

## What This Repository Contains

This repository contains the **raw datasets, econometric test specifications, and complete replication codebase** for the manuscript:

> **"Opening Gap Reversals in Indian Equities: Strategy Persistence, Structural Breaks, and Macro Sensitivities"**

Visitors can inspect the raw data in `data/`, review the econometric specifications in `TESTS.md`, and execute the replication pipeline in `src/run_all_tests.py` to regenerate all tables and figures in `output/` from scratch.

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
├── src/                                         ← complete replication codebase
│   ├── data_loader.py                           ← sample cleaning & data loaders
│   ├── run_all_tests.py                         ← master replication orchestrator
│   ├── test_01_descriptive_stats.py             ← Table 3
│   ├── test_02_oos_threshold_convergence.py     ← Table 4, Figure 2
│   ├── test_03_structural_breaks.py             ← Table 5, Figure 1
│   ├── test_04_lpm_two_way_cluster.py           ← Table 6
│   ├── test_05_wls_newey_west.py                ← Table 7
│   ├── test_06_gap_size_bins.py                 ← Table 8, Figure 3
│   ├── test_07_event_study_cawr.py              ← Table 9, Figure 4
│   ├── test_08_sector_did.py                    ← Table 10, Figure 5
│   ├── test_09_strata_analysis.py               ← Table 11, Figure 7
│   ├── test_10_macro_horse_race.py              ← Table 12, Figure 8
│   └── test_11_granger_causality.py             ← Table Granger, Figure 6
├── output/                                      ← generated replication artifacts
│   ├── tables/                                  ← output tables (Markdown & CSV)
│   └── figures/                                 ← output figures (300 DPI PNG)
├── TESTS.md                                     ← econometric test specifications
├── DATA_DICTIONARY.md                           ← column-by-column descriptions
└── README.md
```

---

## Replication Execution

To execute the entire replication pipeline sequentially and regenerate all tables and figures from raw data:

```bash
python src/run_all_tests.py
```

All 11 replication tests execute end-to-end without hardcoded numbers, validating cross-test sample sizes, day-clustered and HAC standard errors, and exporting 300 DPI figures.

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

