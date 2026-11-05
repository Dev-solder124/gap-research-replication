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

