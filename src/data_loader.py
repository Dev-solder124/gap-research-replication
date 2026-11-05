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

