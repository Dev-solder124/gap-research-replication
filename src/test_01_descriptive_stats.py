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
